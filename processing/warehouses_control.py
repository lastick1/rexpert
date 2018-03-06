"""Контроль складов"""
import logging
import re

import configs
import model
import rcon
import storage
from model import CampaignMission
from processing.ground_control import WarehouseUnit
from .warehouses_selector import WarehousesSelector


WAREHOUSE_INPUT_RE = re.compile(
    '^(?P<side>[BR])WH(?P<number>\d)$'
)


def _warehouse_compare(left: model.Warehouse, right: model.Warehouse) -> int:
    if left.deaths < right.deaths:
        return -1
    if left.deaths > right.deaths:
        return 1
    return 0


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


def _to_warehouse(warehouse) -> model.Warehouse:
    return warehouse


class WarehouseController:
    """Контроллер складов"""
    def __init__(self, ioc):
        self._ioc = ioc
        self._current_tvd_warehouses = dict()
        self._current_mission_warehouses = list()
        self._warehouses_by_inputs = dict()
        self._sent_inputs = set()

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def storage(self) -> storage.Storage:
        """Объект для работы с БД"""
        return self._ioc.storage

    @property
    def rcon(self) -> rcon.DServerRcon:
        """Консоль сервера"""
        return self._ioc.rcon

    def initialize_warehouses(self, tvd_name: str):
        """Инициализировать склады в кампании для указанного ТВД"""
        for data in self.config.mgen.warehouses_data[tvd_name]:
            self.storage.warehouses.update(
                model.Warehouse(
                    tvd_name=tvd_name,
                    name=data['name'],
                    health=100.0,
                    deaths=0,
                    country=data['country'],
                    pos={'x': data['x'], 'z': data['z']}
                )
            )
        logging.info(f'{tvd_name} warehouses initialized')

    def start_mission(self):
        """Обработать начало миссии - обновить положение складов из исходников"""
        self._current_tvd_warehouses.clear()
        self._current_mission_warehouses.clear()
        self._sent_inputs.clear()
        campaign_mission = _to_campaign_mission(self._ioc.campaign_controller.mission)
        warehouses = self.storage.warehouses.load_by_tvd(campaign_mission.tvd_name)
        for warehouse in warehouses:
            self._current_tvd_warehouses[_to_warehouse(warehouse).name] = warehouse
        for server_input in campaign_mission.server_inputs:
            if WAREHOUSE_INPUT_RE.match(server_input['name']):
                warehouse = self.get_warehouse_by_coordinates(server_input['pos'])
                self._current_mission_warehouses.append(warehouse)
                self._warehouses_by_inputs[server_input['name']] = warehouse

    def damage_warehouse(self, unit: WarehouseUnit):
        """Зачесть уничтожение секции склада"""
        server_input_name = unit.name.split(sep='_')[1]
        warehouse = self._warehouses_by_inputs[server_input_name]
        warehouse.health -= 15.0
        logging.info(f'{warehouse.name} section destroyed: {warehouse.health}')
        if warehouse.health < 20 and warehouse.name not in self._sent_inputs:
            self._sent_inputs.add(warehouse.name)
            self.rcon.server_input(warehouse.name)
        self.storage.warehouses.update(warehouse)

    def get_warehouse(self, warehouse_name: str) -> model.Warehouse:
        """Получить склад по имени для текущего ТВД"""
        return self._current_tvd_warehouses[warehouse_name]

    def get_warehouse_by_coordinates(self, pos: dict) -> model.Warehouse:
        """Получить склад по координатам"""
        for name in self._current_tvd_warehouses:
            warehouse = _to_warehouse(self._current_tvd_warehouses[name])
            if warehouse.distance_to(pos['x'], pos['z']) < 10:
                return warehouse

    def next_warehouses(self, tvd: model.Tvd) -> list:
        """Склады для следующей миссии"""
        selector = WarehousesSelector(self.storage.warehouses.load_by_tvd(tvd.name), self._current_mission_warehouses)
        return selector.select(tvd)
