"""Управление дивизиями"""
import logging
import re

import configs
import storage
import model

from model.campaign_mission import CampaignMission


DIVISION_INPUT_RE = re.compile(
    '^(?P<side>[BR])(?P<type>[TAI])D(?P<number>\d)$'
)


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


def _to_division(division) -> model.Division:
    return division


class DivisionsController:
    """Управляение созданием, уроном, состоянием дивизий"""
    def __init__(self, ioc):
        self._ioc = ioc
        self._current_divisions = dict()

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def storage(self) -> storage.Storage:
        """Объект для работы с БД"""
        return self._ioc.storage

    def filter_airfields(self, tvd_name: str, airfields: list) -> list:
        """Отбросить аэродромы, расположенные близко к дивизиям"""
        result = list()
        divisions = self.storage.divisions.load_by_tvd(tvd_name)
        for airfield in airfields:
            close = False
            for division in divisions:
                if division.point.distance_to(airfield.x, airfield.z) < self.config.gameplay.division_margin:
                    close = True
                    break
            if not close:
                result.append(airfield)
        return result

    def initialize_divisions(self, tvd_name: str):
        """Инициализировать дивизии в кампании для указанного ТВД"""
        for name in model.DIVISIONS:
            self.storage.divisions.update(
                model.Division(
                    tvd_name=tvd_name,
                    name=name,
                    units=model.DIVISIONS[name],
                    pos=self.config.mgen.cfg[tvd_name]['division_start_locations'][name]  # {'x': 0.0, 'z': 0.0}
                )
            )
        logging.info(f'{tvd_name} divisions initialized')

    def start_mission(self):
        """Обработать начало миссии - обновить положение дивизий из исходников"""
        campaign_mission = _to_campaign_mission(self._ioc.campaign_controller.mission)
        self._current_divisions.clear()
        for server_input in campaign_mission.server_inputs:
            if DIVISION_INPUT_RE.match(server_input['name']):
                division = self.storage.divisions.load_by_name(campaign_mission.tvd_name, server_input['name'])
                division.pos = server_input['pos']
                self.storage.divisions.update(division)
        divisions = self.storage.divisions.load_by_tvd(campaign_mission.tvd_name)
        for division in divisions:
            self._current_divisions[_to_division(division).name] = division

    def damage_division(self, tvd_name: str, unit_name: str):
        """Зачесть уничтожение подразделения дивизии"""
        division_name = unit_name.split(sep='_')[1]
        division = self.storage.divisions.load_by_name(tvd_name, division_name)
        division.units -= 1
        if division.units < 0:
            division.units = 0
        logging.debug(f'{division.tvd_name} division {division.name} lost unit:{unit_name}')
        self.storage.divisions.update(division)

    def repair_rate(self, penalties: int):
        """Получить множитель восстановления с учётом уничтоженных складов"""
        result = 1 + (self.config.gameplay.division_repair - penalties * 5) / 100
        return result if result > 1 else 1

    def repair_division(self, tvd_name: str, division_name: str, penalties: int):
        """Восполнить дивизию"""
        division = self.storage.divisions.load_by_name(tvd_name, division_name)
        division.units *= self.repair_rate(penalties)
        if division.units > model.DIVISIONS[division_name]:
            division.units = model.DIVISIONS[division_name]
        self.storage.divisions.update(division)

    def get_division(self, division_name: str) -> model.Division:
        """Получить дивизию по имени для текущего ТВД"""
        return self._current_divisions[division_name]
