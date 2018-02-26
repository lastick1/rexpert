"""Контроль складов"""
import logging
import random
import re

import configs
import model
import storage
from model import CampaignMission


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
        campaign_mission = _to_campaign_mission(self._ioc.campaign_controller.mission)
        self._current_tvd_warehouses.clear()
        self._current_mission_warehouses.clear()
        warehouses = self.storage.warehouses.load_by_tvd(campaign_mission.tvd_name)
        for warehouse in warehouses:
            self._current_tvd_warehouses[_to_warehouse(warehouse).name] = warehouse
        for server_input in campaign_mission.server_inputs:
            if WAREHOUSE_INPUT_RE.match(server_input['name']):
                self._current_mission_warehouses.append(self.get_warehouse_by_coordinates(server_input['pos']))

    def damage_warehouse(self, tvd_name: str, unit_name: str):
        """Зачесть уничтожение секции склада"""
        warehouse_name = unit_name.split(sep='_')[1]
        warehouse = self.storage.warehouses.load_by_name(tvd_name, warehouse_name)
        warehouse.health -= 1

    def get_warehouse(self, warehouse_name: str) -> model.Warehouse:
        """Получить склад по имени для текущего ТВД"""
        return self._current_tvd_warehouses[warehouse_name]

    def get_warehouse_by_coordinates(self, pos: dict) -> model.Warehouse:
        """Получить склад по координатам"""
        for name in self._current_tvd_warehouses:
            warehouse = _to_warehouse(self._current_tvd_warehouses[name])
            if warehouse.point.distance_to(pos['x'], pos['z']) < 10:
                return warehouse

    def next_warehouses(self, tvd_name: str) -> list:
        """Склады для следующей миссии"""
        # выбираются те склады, которые убивались меньшее количество раз, текущие склады в приоритете
        warehouses = self.storage.warehouses.load_by_tvd(tvd_name)
        max_deaths = max(x.deaths for x in warehouses) + 1
        warehouses = list(x for x in warehouses if _to_warehouse(x).deaths < max_deaths)
        current = list(x for x in self._current_mission_warehouses if _to_warehouse(x).deaths < max_deaths)
        while len(current) < 2:
            random.shuffle(warehouses)
            current.append(warehouses.pop())
        return current
