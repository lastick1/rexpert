"""Управление дивизиями"""
from __future__ import annotations
import logging
import re

from core import EventsEmitter
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
        self._current_divisions = dict()
        self._sent_inputs = set()
        self._round_ended: bool = False

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.campaign_mission.subscribe_(
                self._update_campaign_mission),
            self.emitter.gameplay_division_damage.subscribe_(
                self.damage_division),
        ])

    def _update_campaign_mission(self, campaign_mission: CampaignMission) -> None:
        self._campaign_mission = campaign_mission

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

    def start_mission(self):
        """Обработать начало миссии - обновить положение дивизий из исходников"""
        self._round_ended = False
        self._current_divisions.clear()
        self._sent_inputs.clear()
        for server_input in self._campaign_mission.server_inputs:
            if DIVISION_INPUT_RE.match(server_input['name']):
                division = self._storage.divisions.load_by_name(
                    self._campaign_mission.tvd_name, server_input['name'])
                division.pos = server_input['pos']
                self._storage.divisions.update(division)
        divisions = self._storage.divisions.load_by_tvd(
            self._campaign_mission.tvd_name)
        for division in divisions:
            self._current_divisions[_to_division(division).name] = division

    def end_round(self):
        """Обработать завершение раунда"""
        self._round_ended = True
        for division_name in self._current_divisions:
            self.repair_division(
                self._current_divisions[division_name].tvd_name, division_name, 0)

    def damage_division(self, tik: int, tvd_name: str, unit_name: str):
        """Зачесть уничтожение подразделения дивизии"""
        division_name = unit_name.split(sep='_')[1]
        division = self._storage.divisions.load_by_name(
            tvd_name, division_name)
        if self._round_ended:
            logging.warning(
                f'{division.name} unit {unit_name} destroyed after round end')
            return
        division.units -= 1
        if division.units < 0:
            division.units = 0
        if division.units <= self._config.gameplay.division_death and division.name not in self._sent_inputs:
            self.emitter.gameplay_division_kill.on_next(
                DivisionKill(tik, division.country, division.name))
            self._sent_inputs.add(division.name)
            self.emitter.commands_rcon.on_next(ServerInput(division.name))
        logging.info(
            f'{division.tvd_name} division {division.name} lost unit:{unit_name}')
        self._storage.divisions.update(division)

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
