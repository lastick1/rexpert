"""Обработка событий с наземкой (дамаг, киллы), расчёт уничтожения целей (артпозиций, складов и т.п.)"""
import re

import log_objects
import atypes
import geometry

from model.campaign_mission import CampaignMission


DIVISION_RE = re.compile(
    '^REXPERT_(?P<side>[BR])(?P<type>[TAI])D(?P<number>\d)_(?P<durability>\d+).*$'
)


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


class GroundTargetUnit:
    """Наземная цель в составе дивизии, отслеживание её состояния"""

    def __init__(self, name: str, pos: geometry.Point, radius: float):
        self.name = name  # имя цели
        self._pos = pos  # центр цели
        self._radius = radius  # радиус цели, в котором она засчитывает килы
        self._kills = 0

        data = DIVISION_RE.match(name).groupdict()
        self._durability = int(data['durability'])  # количество килов цели до её уничтожения
        self._side = data['side']  # сторона цели в виде буквы B или R
        self._number = data['number']
        self.type = data['type']  # тип цели в виде буквы
        self.division_name = f'{self._side}{self.type}D{self._number}'  # имя дивизии, к которой принадледит цель

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
        return self._kills >= self._durability

    def check_kill(self, pos: geometry.Point):
        """Проверить отношение кила к цели и учесть его"""
        if self._pos.distance_to(x=pos.x, z=pos.z) < self._radius:
            self._kills += 1


class GroundController:
    """Контроллер обработки событий с наземными целями"""

    def __init__(self, ioc):
        self.ground_kills = list()
        self.targets = list()
        self._server_inputs = set()
        self._ioc = ioc

    # TODO подумать над тем, чтобы дёргать этот обработчик на атайп15, а не на каждый кил
    def _check_targets(self, kill: geometry.Point):
        """Проверить состояние целей и отправить инпуты в консоль при необходимости"""
        for target in self.targets:
            target.check_kill(kill)
            if target.killed:
                self._send_input(target.division_name)

    def _send_input(self, server_input: str):
        """Отправить инпут на сервер, если он не был отправлен"""
        if server_input not in self._server_inputs:
            if not self._ioc.config.main.offline_mode:
                if not self._ioc.rcon.connected:
                    self._ioc.rcon.connect()
                    self._ioc.rcon.auth(self._ioc.config.main.rcon_login, self._ioc.config.main.rcon_password)
                self._server_inputs.add(server_input)
                self._ioc.rcon.server_input(server_input)

    def _get_tvd_name(self, mission) -> str:
        """Получить имя ТВД из данных о миссии"""
        for tvd_name in self._ioc.config.mgen.maps:
            if tvd_name in mission.guimap:
                return tvd_name
        raise NameError(f'невозможно определить имя ТВД из guimap {mission.guimap}')

    def _get_unit_radius(self, tvd_name: str) -> int:
        """Получить радиус юнита дивизии из конфига"""
        return self._ioc.config.mgen.cfg[tvd_name]['division_unit_radius']

    def start_mission(self):
        """Обработать начало миссии"""
        self.ground_kills.clear()
        self.targets.clear()
        mission = _to_campaign_mission(self._ioc.campaign_controller.mission)

        for unit in mission.division_units:
            self.targets.append(GroundTargetUnit(
                unit['name'],
                geometry.Point(x=unit['pos']['x'], z=unit['pos']['z']),
                self._get_unit_radius(self._get_tvd_name(mission))))

    def kill(self, atype: atypes.Atype3) -> None:
        """Обработать уничтожение наземного объекта"""
        target = self._ioc.objects_controller.get_object(atype.target_id)
        if isinstance(target, log_objects.Ground):
            kill = geometry.Point(x=atype.pos['x'], z=atype.pos['z'])
            self.ground_kills.append(kill)
            target.kill(atype.pos)
            self._check_targets(kill)
