"""Обработка событий с наземкой (дамаг, киллы), расчёт уничтожения целей (артпозиций, складов и т.п.)"""
import logging
import re

import configs
import log_objects
import atypes
import geometry
import rcon

from model.campaign_mission import CampaignMission


DIVISION_RE = re.compile(
    '^REXPERT_(?P<side>[BR])(?P<type>[TAI])D(?P<number>\d)_(?P<durability>\d+).*$'
)

WAREHOUSE_RE = re.compile(
    '^REXPERT_(?P<side>[BR])WH(?P<number>\d)_(?P<durability>\d+).*$'
)


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


class GroundTargetUnit(geometry.Point):
    """Часть кластерной цели (секция склада или подразделение дивизии)"""

    def __init__(
            self,
            name: str,
            pos: dict,
            side: str,
            parent_name: str,
            durability: int,
            radius: float,
            tvd_name: str
    ):
        super().__init__(pos['x'], pos['z'])
        self.pos = pos
        self.name = name  # имя цели
        self.tvd_name = tvd_name  # имя твд, на котором расположен объект
        self._side = side  # сторона цели в виде буквы B или R
        self._radius = radius  # радиус цели, в котором она засчитывает килы
        self._durability = durability  # количество килов цели до её уничтожения
        self.parent_name = parent_name  # имя дивизии или склада

        self._kills = list()

    @property
    def country(self) -> int:
        """Сторона, к которой принадлежит цель"""
        if self._side == 'R':
            return 101
        if self._side == 'B':
            return 201

    @property
    def killed(self) -> bool:
        """Убита ли цель"""
        return len(self._kills) >= self._durability

    def try_add_kill(self, point: geometry.Point) -> bool:
        """Проверить и добавить килл"""
        if self.distance_to(x=point.x, z=point.z) < self._radius:
            self._kills.append(point)
            return True
        return False


def _to_unit(unit) -> GroundTargetUnit:
    return unit


class DivisionUnit(GroundTargetUnit):
    """Наземная цель в составе дивизии, отслеживание её состояния"""

    def __init__(self, name: str, pos: dict, radius: float, tvd_name: str):
        data = DIVISION_RE.match(name).groupdict()
        self.type = data['type']  # тип цели в виде буквы
        self.division_name = f'{data["side"]}{data["type"]}D{data["number"]}'  # имя дивизии, к которой принадлежит цель
        super().__init__(name, pos, data['side'], self.division_name, int(data['durability']), radius, tvd_name)


class WarehouseUnit(GroundTargetUnit):
    """Наземная цель в составе склада, отслеживание её состояния"""

    def __init__(self, name: str, pos: dict, radius: float, tvd_name: str):
        data = WAREHOUSE_RE.match(name).groupdict()
        self.warehouse_name = f'{data["side"]}WH{data["number"]}'
        super().__init__(name, pos, data["side"], self.warehouse_name, int(data['durability']), radius, tvd_name)

    @property
    def killed(self):
        """Убита ли цель"""
        return len(self._kills) >= int(self._durability * 0.80)


class GroundController:
    """Контроллер обработки событий с наземными целями"""

    def __init__(self, ioc):
        self.ground_kills = list()
        self.targets = list()
        self._server_inputs = set()
        self._killed_units = set()
        self._ioc = ioc

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def rcon(self) -> rcon.DServerRcon:
        """Консоль сервера"""
        return self._ioc.rcon

    # TODO подумать над тем, чтобы дёргать этот обработчик на атайп15, а не на каждый кил
    def _check_targets(self, tik: int):
        """Проверить состояние целей и отправить инпуты в консоль при необходимости"""
        for target in self.targets:
            unit = _to_unit(target)
            if unit.killed and unit not in self._killed_units:
                self._killed_units.add(unit)
                if isinstance(unit, DivisionUnit):
                    self._ioc.divisions_controller.damage_division(tik, unit.tvd_name, unit.name)
                if isinstance(unit, WarehouseUnit):
                    self._ioc.warehouses_controller.damage_warehouse(tik, unit)

    def _send_input(self, server_input: str):
        """Отправить инпут на сервер, если он не был отправлен"""
        if server_input not in self._server_inputs:
            if not self.config.main.offline_mode:
                if not self.rcon.connected:
                    self.rcon.connect()
                    self.rcon.auth(self.config.main.rcon_login, self.config.main.rcon_password)
                self._server_inputs.add(server_input)
                self.rcon.server_input(server_input)

    def _get_unit_radius(self, tvd_name: str) -> int:
        """Получить радиус юнита дивизии из конфига"""
        return self.config.mgen.cfg[tvd_name]['division_unit_radius']

    def start_mission(self):
        """Обработать начало миссии"""
        self._killed_units.clear()
        self.ground_kills.clear()
        self.targets.clear()
        mission = _to_campaign_mission(self._ioc.campaign_controller.mission)

        for unit in mission.units:
            if WAREHOUSE_RE.match(unit['name']):
                self.targets.append(WarehouseUnit(
                    unit['name'],
                    unit['pos'],
                    self.config.gameplay.warehouse_unit_radius[mission.tvd_name],
                    mission.tvd_name
                ))
                continue
            if DIVISION_RE.match(unit['name']):
                self.targets.append(DivisionUnit(
                    unit['name'],
                    unit['pos'],
                    self.config.gameplay.division_unit_radius[mission.tvd_name],
                    mission.tvd_name
                ))
                continue

    def kill(self, atype: atypes.Atype3) -> None:
        """Обработать уничтожение наземного объекта"""
        target = self._ioc.objects_controller.get_object(atype.target_id)
        if isinstance(target, log_objects.Ground):
            kill = geometry.Point(x=atype.pos['x'], z=atype.pos['z'])
            self.ground_kills.append(kill)
            target.kill(atype.pos)
            changed = False
            for unit in self.targets:
                if unit.try_add_kill(atype.point):
                    changed = True
                    logging.debug(f'ground kill in unit: {unit.name} at {unit.pos}')
                    break
            if changed:
                self._check_targets(atype.tik)

    def mission_result(self, atype: atypes.Atype8) -> None:
        """Обработать mission objective в логах"""
        pass
