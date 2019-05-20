"""Сервис контроля складов"""
from __future__ import annotations
from typing import List, Dict
import logging
import re

from rx import interval

from constants import INVERT
from core import EventsEmitter, WarehouseDamage, PointsGain, Atype19
from configs import Config
from storage import Storage
from model import CampaignMission, \
    Tvd, \
    Warehouse, \
    WarehouseDisable, \
    MessageAll, \
    ServerInput
from processing.warehouses_selector import WarehousesSelector

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
        self._current_tvd_warehouses: Dict[str, Warehouse] = dict()
        self._current_mission_warehouses: List[Warehouse] = list()
        self._warehouses_by_inputs: Dict[str, Warehouse] = dict()
        self._sent_inputs = set()
        self._round_ended: bool = False
        self.event_notify = interval(self._config.main.chat.warehouse_notification_interval)

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.campaign_mission.subscribe_(self.start_mission),
            self.emitter.gameplay_warehouse_damage.subscribe_(self.damage_warehouse),
            self.emitter.events_round_end.subscribe_(self.end_round),
            self.event_notify.subscribe_(self.notify),
        ])

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

    def start_mission(self, campaign_mission: CampaignMission):
        """Обработать начало миссии - обновить положение складов из исходников"""
        self._campaign_mission = campaign_mission
        self._round_ended = False
        self._current_tvd_warehouses.clear()
        self._current_mission_warehouses.clear()
        self._sent_inputs.clear()
        warehouses = self._storage.warehouses.load_by_tvd(self._campaign_mission.tvd_name)
        for warehouse in warehouses:
            self._current_tvd_warehouses[warehouse.name] = warehouse
        for server_input in self._campaign_mission.server_inputs:
            if WAREHOUSE_INPUT_RE.match(server_input['name']):
                warehouse = self.get_warehouse_by_coordinates(
                    server_input['pos'])
                self._current_mission_warehouses.append(warehouse)
                self._warehouses_by_inputs[server_input['name']] = warehouse
                self._check_warehouse(0, warehouse)

    def end_round(self, atype: Atype19):
        """Завершить раунд"""
        self._round_ended = True

    def notify(self, *args):
        """Отправить состояние складов в чат"""
        for warehouse in self._current_mission_warehouses:
            self.emitter.commands_rcon.on_next(MessageAll(
                f'{warehouse.name} warehouse state is {warehouse.health}/100'))

    def damage_warehouse(self, damage: WarehouseDamage):
        """Зачесть уничтожение секции склада"""
        server_input_name = damage.unit_name.split(sep='_')[1]
        warehouse = self._warehouses_by_inputs[server_input_name]
        if self._round_ended:
            logging.info(
                f'{warehouse.name} section {damage.unit_name} {damage.pos} destroyed after round end')
            return
        damage_step = warehouse.next_damage
        warehouse.health -= damage_step
        self.emitter.commands_rcon.on_next(MessageAll(f'{warehouse.name} damaged by {damage_step}%'))
        logging.info(f'{warehouse.name} section destroyed: {warehouse.health}')
        self._check_warehouse(damage.tik, warehouse)
        self._storage.warehouses.update(warehouse)

    def _check_warehouse(self, tik: int, warehouse: Warehouse) -> None:
        "Проверить состояние склада и отправить сообщения/команды"
        if warehouse.health < 20 and warehouse.name not in self._sent_inputs:
            self._sent_inputs.add(warehouse.name)
            self.emitter.commands_rcon.on_next(ServerInput(warehouse.name))
        if warehouse.health < 40:
            self.emitter.gameplay_points_gain.on_next(PointsGain(
                INVERT[warehouse.country],
                4,
                WarehouseDisable(tik, warehouse.country, warehouse.name)))

    def get_warehouse(self, warehouse_name: str) -> Warehouse:
        """Получить склад по имени для текущего ТВД"""
        return self._current_tvd_warehouses[warehouse_name]

    def get_warehouse_by_coordinates(self, pos: dict) -> Warehouse:
        """Получить склад по координатам"""
        for name in self._current_tvd_warehouses:
            warehouse = self._current_tvd_warehouses[name]
            if warehouse.distance_to(pos['x'], pos['z']) < 10:
                return warehouse

    def next_warehouses(self, tvd: Tvd) -> list:
        """Склады для следующей миссии"""
        selector = WarehousesSelector(self._storage.warehouses.load_by_tvd(
            tvd.name), self._current_mission_warehouses)
        return selector.select(tvd)
