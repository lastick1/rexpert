"""Сервис контроля складов"""
from __future__ import annotations
import logging
import re

from core import EventsEmitter
from configs import Config
from storage import Storage
from model import CampaignMission, \
    Tvd, \
    Warehouse, \
    WarehouseDisable, \
    MessageAll, \
    ServerInput
from processing.warehouses_selector import WarehousesSelector

from .ground_targets_service import WarehouseUnit
from .base_event_service import BaseEventService

WAREHOUSE_INPUT_RE = re.compile(
    r'^(?P<side>[BR])WH(?P<number>\d)$'
)


def _warehouse_compare(left: Warehouse, right: Warehouse) -> int:
    if left.deaths < right.deaths:
        return -1
    if left.deaths > right.deaths:
        return 1
    return 0


def _to_campaign_mission(mission) -> CampaignMission:
    return mission


def _to_warehouse(warehouse) -> Warehouse:
    return warehouse


class WarehouseService(BaseEventService):
    """Сервис контроля складов"""

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config,
            storage: Storage,
    ):
        super().__init__(emitter)
        self._config: Config = config
        self._storage: Storage = storage
        self._campaign_mission: CampaignMission = None
        self._current_tvd_warehouses = dict()
        self._current_mission_warehouses = list()
        self._warehouses_by_inputs = dict()
        self._sent_inputs = set()
        self._round_ended: bool = False
        self._notify_counter = 0

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.campaign_mission.subscribe_(
                self._update_campaign_mission),
            self.emitter.gameplay_warehouse_damage.subscribe_(
                self.damage_warehouse),
        ])

    def _update_campaign_mission(self, campaign_mission: CampaignMission) -> None:
        self._campaign_mission = campaign_mission

    def initialize_warehouses(self, tvd_name: str):
        """Инициализировать склады в кампании для указанного ТВД"""
        for data in self._config.mgen.warehouses_data[tvd_name]:
            self._storage.warehouses.update(
                Warehouse(
                    tvd_name=tvd_name,
                    name=data['name'],
                    health=100.0,
                    deaths=0,
                    country=data['country'],
                    pos={'x': data['x'], 'z': data['z']}
                )
            )
        logging.debug(f'{tvd_name} warehouses initialized')

    def start_mission(self):
        """Обработать начало миссии - обновить положение складов из исходников"""
        self._round_ended = False
        self._current_tvd_warehouses.clear()
        self._current_mission_warehouses.clear()
        self._sent_inputs.clear()
        warehouses = self._storage.warehouses.load_by_tvd(
            self._campaign_mission.tvd_name)
        for warehouse in warehouses:
            self._current_tvd_warehouses[_to_warehouse(
                warehouse).name] = warehouse
        for server_input in self._campaign_mission.server_inputs:
            if WAREHOUSE_INPUT_RE.match(server_input['name']):
                warehouse = self.get_warehouse_by_coordinates(
                    server_input['pos'])
                self._current_mission_warehouses.append(warehouse)
                self._warehouses_by_inputs[server_input['name']] = warehouse

    def end_round(self):
        """Завершить раунд"""
        self._round_ended = True

    def notify(self):
        """Отправить состояние складов в чат"""
        self._notify_counter += 1
        warehouses = list()
        if self._notify_counter % 4 == 3:
            warehouses.extend(
                x for x in self._current_mission_warehouses if x.country == 101)
        if self._notify_counter % 4 == 2:
            warehouses.extend(
                x for x in self._current_mission_warehouses if x.country == 201)
        if self._notify_counter % 4 == 0:
            self._notify_counter = 0
        for warehouse in warehouses:
            self.emitter.commands_rcon.on_next(MessageAll(
                f'{warehouse.name} warehouse state is {warehouse.health}/100'))
            logging.info(
                f'{self._notify_counter},{len(warehouses)} notify warehouses state')

    def damage_warehouse(self, tik: int, unit: WarehouseUnit):
        """Зачесть уничтожение секции склада"""
        server_input_name = unit.name.split(sep='_')[1]
        warehouse = self._warehouses_by_inputs[server_input_name]
        if self._round_ended:
            logging.info(
                f'{warehouse.name} section {unit.name} {unit.pos} destroyed after round end')
            return
        warehouse.health -= warehouse.next_damage
        logging.info(f'{warehouse.name} section destroyed: {warehouse.health}')
        if warehouse.health < 20 and server_input_name not in self._sent_inputs:
            self._sent_inputs.add(server_input_name)
            self.emitter.commands_rcon.on_next(ServerInput(server_input_name))
        if warehouse.health < 40:
            self.emitter.gameplay_warehouse_disable.on_next(
                WarehouseDisable(tik, warehouse.country, warehouse.name))
        self._storage.warehouses.update(warehouse)

    def get_warehouse(self, warehouse_name: str) -> Warehouse:
        """Получить склад по имени для текущего ТВД"""
        return self._current_tvd_warehouses[warehouse_name]

    def get_warehouse_by_coordinates(self, pos: dict) -> Warehouse:
        """Получить склад по координатам"""
        for name in self._current_tvd_warehouses:
            warehouse = _to_warehouse(self._current_tvd_warehouses[name])
            if warehouse.distance_to(pos['x'], pos['z']) < 10:
                return warehouse

    def next_warehouses(self, tvd: Tvd) -> list:
        """Склады для следующей миссии"""
        selector = WarehousesSelector(self._storage.warehouses.load_by_tvd(
            tvd.name), self._current_mission_warehouses)
        return selector.select(tvd)