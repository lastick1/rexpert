"""Контроль складов"""
import logging
import re

import configs
import model
import storage
from model import CampaignMission


WAREHOUSE_INPUT_RE = re.compile(
    '^(?P<side>[BR])WH(?P<number>\d)$'
)


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


def _to_warehouse(warehouse) -> model.Warehouse:
    return warehouse


class WarehouseController:
    """Контроллер складов"""
    def __init__(self, ioc):
        self._ioc = ioc
        self._current_warehouses = dict()

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def storage(self) -> storage.Storage:
        """Объект для работы с БД"""
        return self._ioc.storage

    def initialize_warehouses(self, tvd_name: str):
        """Инициализировать склады в кампании для указанного ТВД"""
        for name in model.WAREHOUSES:
            self.storage.warehouses.update(
                model.Warehouse(
                    tvd_name=tvd_name,
                    name=name,
                    health=model.WAREHOUSES[name],
                    pos=self.config.mgen.cfg[tvd_name]['warehouses_start_locations'][name]
                )
            )
        logging.info(f'{tvd_name} warehouses initialized')

    def start_mission(self):
        """Обработать начало миссии - обновить положение складов из исходников"""
        campaign_mission = _to_campaign_mission(self._ioc.campaign_controller.mission)
        self._current_warehouses.clear()
        for server_input in campaign_mission.server_inputs:
            if WAREHOUSE_INPUT_RE.match(server_input['name']):
                warehouse = self.storage.warehouses.load_by_name(campaign_mission.tvd_name, server_input['name'])
                warehouse.pos = server_input['pos']
                self.storage.warehouses.update(warehouse)
        warehouses = self.storage.warehouses.load_by_tvd(campaign_mission.tvd_name)
        for warehouse in warehouses:
            self._current_warehouses[_to_warehouse(warehouse).name] = warehouse

    def damage_warehouse(self, tvd_name: str, unit_name: str):
        """Зачесть уничтожение секции склада"""
        warehouse_name = unit_name.split(sep='_')[1]
        warehouse = self.storage.warehouses.load_by_name(tvd_name, warehouse_name)
        warehouse.health -= 1

    def get_warehouse(self, warehouse_name: str) -> model.Warehouse:
        """Получить склад по имени для текущего ТВД"""
        return self._current_warehouses[warehouse_name]
