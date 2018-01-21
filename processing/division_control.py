"""Управление дивизиями"""
import re

from .division import Division, DIVISIONS
from .campaign_mission import CampaignMission


DIVISION_INPUT_RE = re.compile(
    '^(?P<side>[BR])(?P<type>[TAI])D(?P<number>\d)$'
)


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


class DivisionsController:
    """Управляение созданием, уроном, состоянием дивизий"""
    def __init__(self, ioc):
        self._ioc = ioc

    def initialize_divisions(self, tvd_name: str):
        """Инициализировать дивизии в кампании для указанного ТВД"""
        for name in DIVISIONS:
            self._ioc.storage.divisions.update(
                Division(
                    tvd_name=tvd_name,
                    name=name,
                    units=DIVISIONS[name],
                    pos={'x': 0.0, 'z': 0.0}
                )
            )

    def start_mission(self):
        """Обработать начало миссии - обновить положение дивизий из исходников"""
        campaign_mission = _to_campaign_mission(self._ioc.campaign_controller.mission)
        for server_input in campaign_mission.server_inputs:
            if DIVISION_INPUT_RE.match(server_input['name']):
                division = self._ioc.storage.divisions.load_by_name(campaign_mission.guimap, server_input['name'])
                division.pos = server_input['pos']
                self._ioc.storage.divisions.update(division)

    def damage_division(self, tvd_name: str, unit_name: str):
        """Зачесть уничтожение подразделения дивизии"""
        division_name = unit_name.split(sep='_')[1]
        division = self._ioc.storage.divisions.load_by_name(tvd_name, division_name)
        division.units -= 1
        if division.units < 0:
            division.units = 0
        self._ioc.storage.divisions.update(division)

    def repair_rate(self, penalties: int):
        """Получить множитель восстановления с учётом уничтоженных складов"""
        result = 1 + (self._ioc.config.gameplay.division_repair - penalties * 5) / 100
        return result if result > 1 else 1

    def repair_division(self, tvd_name: str, division_name: str, penalties: int):
        """Восполнить дивизию"""
        division = self._ioc.storage.divisions.load_by_name(tvd_name, division_name)
        division.units *= self.repair_rate(penalties)
        if division.units > DIVISIONS[division_name]:
            division.units = DIVISIONS[division_name]
        self._ioc.storage.divisions.update(division)
