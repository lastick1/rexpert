"""Управление дивизиями"""
from __future__ import annotations
from typing import List, Dict, Set
import logging
import re

from rx import interval

from constants import INVERT, COUNTRY_NAMES
from core import EventsEmitter, DivisionDamage, PointsGain
from configs import Config
from storage import Storage
from model import Division, \
    WarehouseDisable, \
    DIVISIONS, \
    DivisionKill, \
    CampaignMission, \
    MessageAll, \
    ServerInput

from .base_event_service import BaseEventService

DIVISION_INPUT_RE = re.compile(
    r'^(?P<side>[BR])(?P<type>[TAI])D(?P<number>\d)$'
)

DIVISION_UNIT_RE = re.compile(
    r'^REXPERT_(?P<division_name>[BR][TAI]D\d)_(?P<durability>\d+)$'
)


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


def _to_division(division) -> Division:
    return division


def _make_notify_message(division: Division) -> str:
    "Сделать информационное сообщение о статусе укрепрайона"
    return f'{COUNTRY_NAMES[division.country]} fortified area ({division.type_of_army}) has ' + \
        f'{division.units}/{DIVISIONS[division.name]} sections'


def _make_damage_message(division: Division) -> str:
    "Сообщение повреждении дивизии"
    return f'{COUNTRY_NAMES[division.country]} fortified area ({division.type_of_army}) section destroyed. ' + \
        f'{division.units} sections left'


class DivisionsService(BaseEventService):
    """Управление созданием, уроном, состоянием дивизий"""

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config,
            storage: Storage
    ):
        super().__init__(emitter)
        self._config: Config = config
        self._storage: Storage = storage
        self._campaign_mission: CampaignMission = None
        self._current_divisions: Dict[str, Division] = dict()
        self._sent_inputs: Set[str] = set()
        self._round_ended: bool = False
        self._warehouses_disables: Dict[Set[WarehouseDisable]] = None
        self.event_notify = interval(self._config.main.chat.division_notification_interval)

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.campaign_mission.subscribe_(self.start_mission),
            self.emitter.gameplay_division_damage.subscribe_(self.damage_division),
            self.emitter.mission_victory.subscribe_(self._mission_victory),
            self.emitter.gameplay_points_gain.subscribe_(self._points_gain),
            self.event_notify.subscribe_(self.notify)
        ])

    def notify(self, *args) -> None:
        "Отправить состояние укрепрайонов в чат"
        for division_name in self._current_divisions:
            self.emitter.commands_rcon.on_next(MessageAll(_make_notify_message(self._current_divisions[division_name])))

    def filter_airfields(self, tvd_name: str, airfields: list) -> list:
        """Отбросить аэродромы, расположенные близко к дивизиям"""
        result = list()
        divisions = self._storage.divisions.load_by_tvd(tvd_name)
        for airfield in airfields:
            close = False
            for division in divisions:
                if division.point.distance_to(airfield.x, airfield.z) < self._config.gameplay.division_margin:
                    close = True
                    break
            if not close:
                result.append(airfield)
        return result

    def initialize_divisions(self, tvd_name: str):
        """Инициализировать дивизии в кампании для указанного ТВД"""
        for name in DIVISIONS:
            self._storage.divisions.update(
                Division(
                    tvd_name=tvd_name,
                    name=name,
                    units=DIVISIONS[name],
                    # {'x': 0.0, 'z': 0.0}
                    pos=self._config.mgen.cfg[tvd_name]['division_start_locations'][name]
                )
            )
        logging.debug(f'{tvd_name} divisions initialized')

    def start_mission(self, campaign_mission: CampaignMission):
        """Обработать начало миссии - обновить положение дивизий из исходников"""
        self._campaign_mission = campaign_mission
        self._round_ended = False
        self._current_divisions.clear()
        self._sent_inputs.clear()
        self._warehouses_disables = {101: set(), 201: set()}
        for server_input in self._campaign_mission.server_inputs:
            if DIVISION_INPUT_RE.match(server_input['name']):
                division = self._storage.divisions.load_by_name(
                    self._campaign_mission.tvd_name, server_input['name'])
                division.pos = server_input['pos']
                self._storage.divisions.update(division)
        divisions = self.parse_divisions(
            self._campaign_mission.tvd_name, self._campaign_mission.units, self._campaign_mission.server_inputs)
        for division in divisions:
            self._current_divisions[_to_division(division).name] = division
            self._check_division(0, division)

    def parse_divisions(self, tvd_name: str, units: List[Dict], server_inputs: List[Dict]) -> List[Division]:
        "Считать дивизии из обнаруженных юнитов в исходнике миссии"
        data: Dict[str, Dict] = dict()
        for unit in units:
            match = DIVISION_UNIT_RE.match(unit['name'])
            if match:
                groupdict = match.groupdict()
                if groupdict['division_name'] not in data:
                    data[groupdict['division_name']] = {
                        'units': list()
                    }
                data[groupdict['division_name']]['units'].append(
                    {**groupdict, **unit})

        return [Division(tvd_name, x, len(data[x]['units']), self._get_division_pos(server_inputs, x)) for x in data]

    def _get_division_pos(self, server_inputs: List[Dict], division_name: str) -> Dict[str, float]:
        "Получить позицию дивизии по координатам её Translator: ServerInput"
        for server_input in server_inputs:
            if server_input['name'] == division_name:
                return server_input['pos']

    def end_round(self):
        """Обработать завершение раунда"""
        self._round_ended = True
        for division_name in self._current_divisions:
            self.repair_division(
                self._current_divisions[division_name].tvd_name, division_name, 0)

    def damage_division(self, damage: DivisionDamage):
        """Зачесть уничтожение подразделения дивизии"""
        division_name = damage.unit_name.split(sep='_')[1]
        division = self._storage.divisions.load_by_name(
            damage.tvd_name, division_name)
        if self._round_ended:
            logging.warning(
                f'{division.name} unit {damage.unit_name} destroyed after round end')
            return
        if division.units > 0:
            division.units -= 1
        self._check_division(damage.tik, division)
        self.emitter.commands_rcon.on_next(MessageAll(_make_damage_message(division)))
        logging.info(
            f'{division.tvd_name} division {division.name} lost unit:{damage.unit_name}')
        self._storage.divisions.update(division)

    def _check_division_health(self, division: Division) -> bool:
        "Проверить порог уничтожения дивизии"
        return division.units <= self._config.gameplay.division_death

    def _check_division(self, tik: int, division: Division) -> None:
        "Проверить дивизию и отправить отреагировать на уничтожение при необходимости"
        if self._check_division_health(division) and division.name not in self._sent_inputs:
            self.emitter.gameplay_points_gain.on_next(PointsGain(
                INVERT[division.country],
                3,
                DivisionKill(tik, division.country, division.name)))
            self._sent_inputs.add(division.name)
            self.emitter.commands_rcon.on_next(ServerInput(division.name))

    def repair_rate(self, penalties: int):
        """Получить множитель восстановления с учётом уничтоженных складов"""
        result = 1 + (self._config.gameplay.division_repair -
                      penalties * 5) / 100
        return result if result > 1 else 1

    def repair_division(self, tvd_name: str, division_name: str, penalties: int):
        """Восполнить дивизию"""
        division = self._storage.divisions.load_by_name(
            tvd_name, division_name)
        division.units *= self.repair_rate(penalties)
        if division.units > DIVISIONS[division_name]:
            division.units = DIVISIONS[division_name]
        self._storage.divisions.update(division)

    def get_division(self, division_name: str) -> Division:
        """Получить дивизию по имени для текущего ТВД"""
        return self._current_divisions[division_name]

    def _points_gain(self, gain: PointsGain) -> None:
        """Обработать получение очков захвата за склад"""
        if isinstance(gain.reason, WarehouseDisable):
            disable: WarehouseDisable = gain.reason
            self._warehouses_disables[INVERT[gain.country]].add(disable.warehouse_name)

    def _mission_victory(self, country: int) -> None:
        """Обработать победу страны в миссии"""
        for division_name in self._current_divisions:
            division: Division = self._current_divisions[division_name]
            self.repair_division(division.tvd_name, division.name, len(self._warehouses_disables[division.country]))
