"""Управление дивизиями"""
from __future__ import annotations
from typing import List, Dict, Set
import logging
import re

from core import EventsEmitter, DivisionDamage, PointsGain
from configs import Config
from storage import Storage
from model import Division, \
    DIVISIONS, \
    DivisionKill, \
    CampaignMission, \
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

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.campaign_mission.subscribe_(
                self.start_mission),
            self.emitter.gameplay_division_damage.subscribe_(
                self.damage_division),
        ])

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
        for server_input in self._campaign_mission.server_inputs:
            if DIVISION_INPUT_RE.match(server_input['name']):
                division = self._storage.divisions.load_by_name(
                    self._campaign_mission.tvd_name, server_input['name'])
                division.pos = server_input['pos']
                self._storage.divisions.update(division)
        divisions = self.parse_divisions(self._campaign_mission.units, self._campaign_mission.tvd_name)
        for division in divisions:
            self._current_divisions[_to_division(division).name] = division
            self._check_division(0, division)

    def parse_divisions(self, units: List[Dict], tvd_name: str) -> List[Division]:
        "Считать дивизии из обнаруженных юнитов в исходнике миссии"
        data: Dict[str, Dict] = dict()
        for unit in units:
            groupdict = DIVISION_UNIT_RE.match(unit['name']).groupdict()
            if groupdict['division_name'] not in data:
                data[groupdict['division_name']] = {
                    'units': list()
                }
            data[groupdict['division_name']]['units'].append({**groupdict, **unit})

        return [Division(tvd_name, x, len(data[x]['units']), data[x]['units'][0]['pos']) for x in data]

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
        division.units -= 1
        if division.units < 0:
            division.units = 0
        self._check_division(damage.tik, division)
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
                division.country,
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
