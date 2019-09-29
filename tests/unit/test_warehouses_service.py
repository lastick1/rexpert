"Тестирование сервиса складов"
from __future__ import annotations
from typing import List
import unittest


from core import EventsEmitter, WarehouseDamage
from storage import Storage
from model import CampaignMission, Warehouse

from tests.mocks import ConfigMock, EventsInterceptor, TvdMock, return_true

from services import WarehouseService
TEST_TVD_NAME = 'moscow'
TEST_DATE = '01.09.1941'
TEST_RWH1_NAME = 'test_red_warehouse1'
TEST_RWH2_NAME = 'test_red_warehouse2'
TEST_BWH1_NAME = 'test_blue_warehouse1'
TEST_BWH2_NAME = 'test_blue_warehouse2'
TEST_TARGET_RWH1_SERVER_INPUT = 'RWH1'
TEST_TARGET_POS_RWH1 = {'x': 156060.64, 'z': 132392.5}
TEST_TARGET_POS_RWH1_UNITS = [
    {'x': 155453.86, 'z': 130798.2},
    {'x': 156461.58, 'z': 131861.16},
    {'x': 155169.17, 'z': 133163.56},
    {'x': 155055.39, 'z': 132101.14},
    {'x': 155604.38, 'z': 131692.38},
    {'x': 156010.75, 'z': 131154.91},
    {'x': 156484.95, 'z': 133269.22},
    {'x': 156907.78, 'z': 133390.91},
    {'x': 157196.23, 'z': 134433.89},
    {'x': 157767.08, 'z': 132920.91}
]
TEST_MISSION = CampaignMission(
    file='result1',
    date=TEST_DATE,
    tvd_name=TEST_TVD_NAME,
    additional=dict(),
    server_inputs=[
        {'name': TEST_TARGET_RWH1_SERVER_INPUT, 'pos': TEST_TARGET_POS_RWH1}
    ],
    objectives=[],
    airfields=[],
    units=[
        {'name': 'REXPERT_RWH1_3', 'pos': TEST_TARGET_POS_RWH1_UNITS[0]},
        {'name': 'REXPERT_RWH1_15', 'pos': TEST_TARGET_POS_RWH1_UNITS[1]},
        {'name': 'REXPERT_RWH1_2', 'pos': TEST_TARGET_POS_RWH1_UNITS[2]},
        {'name': 'REXPERT_RWH1_10', 'pos': TEST_TARGET_POS_RWH1_UNITS[3]},
        {'name': 'REXPERT_RWH1_17', 'pos': TEST_TARGET_POS_RWH1_UNITS[4]},
    ],
    actions=list()
)


class TestWarehousesService(unittest.TestCase):
    "Тесты"

    def setUp(self):
        "Настройка перед тестом"
        self.emitter = EventsEmitter()
        self.config = ConfigMock()
        self.storage = Storage(self.config.main)
        self.interceptor: EventsInterceptor = EventsInterceptor(self.emitter)
        self._test_warehouse_health = 100
        self._update_calls: List[Warehouse] = []
        self._load_calls = 0

        self.storage.warehouses.load_by_tvd = self._load_warehouses_by_tvd_mock
        self.storage.warehouses.update = self._update_calls.append

    def _load_warehouses_by_tvd_mock(self, tvd_name: str) -> List[Warehouse]:
        self._load_calls += 1
        return [
            Warehouse(
                TEST_RWH1_NAME,
                tvd_name,
                self._test_warehouse_health,
                0,
                101,
                TEST_TARGET_POS_RWH1,
                False,
            ),
            Warehouse(
                TEST_RWH2_NAME,
                tvd_name,
                self._test_warehouse_health,
                0,
                101,
                TEST_TARGET_POS_RWH1,
                False,
            ),
            Warehouse(
                TEST_BWH1_NAME,
                tvd_name,
                self._test_warehouse_health,
                0,
                201,
                TEST_TARGET_POS_RWH1,
                False,
            ),
            Warehouse(
                TEST_BWH2_NAME,
                tvd_name,
                self._test_warehouse_health,
                0,
                201,
                TEST_TARGET_POS_RWH1,
                False,
            ),
        ]

    def test_warehouse_disable(self):
        "Учитывается выведение склада из строя"
        self._test_warehouse_health = 75
        service = WarehouseService(self.emitter, self.config, self.storage)
        service.init()
        # Act
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        for unit in TEST_MISSION.units:
            self.emitter.gameplay_warehouse_damage.on_next(WarehouseDamage(123, unit['name'], unit['pos']))
        # Assert
        self.assertTrue(self.interceptor.points_gains)

    def test_warehouse_no_disable(self):
        "Не выводится из строя целый склад"
        self._test_warehouse_health = 100
        service = WarehouseService(self.emitter, self.config, self.storage)
        service.init()
        # Act
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        for unit in TEST_MISSION.units:
            self.emitter.gameplay_warehouse_damage.on_next(WarehouseDamage(123, unit['name'], unit['pos']))
        # Assert
        self.assertFalse(self.interceptor.points_gains)

    def test_disable_on_mission_start(self):
        "Отправляется сообщение об выведенных из строя складах в начале миссии"
        self._test_warehouse_health = 39
        service = WarehouseService(self.emitter, self.config, self.storage)
        service.init()
        # Act
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        # Assert
        self.assertTrue(self.interceptor.points_gains)

    def test_damage_notification(self):
        "Отправляется в чат оповещение об уничтожении секции склада"
        service = WarehouseService(self.emitter, self.config, self.storage)
        service.init()
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        # Act
        for unit in TEST_MISSION.units:
            self.emitter.gameplay_warehouse_damage.on_next(WarehouseDamage(123, unit['name'], unit['pos']))
        # Assert
        self.assertTrue(self.interceptor.commands)
        self.assertEqual(len(self.interceptor.commands), 5)
        warehouse = self._load_warehouses_by_tvd_mock(TEST_MISSION.tvd_name)[0]
        for command in self.interceptor.commands:
            self.assertIn(warehouse.name, command.message)

    def test_sets_is_current_on_mission_start(self):
        """Обновляются текущие склады при старте миссии"""
        service = WarehouseService(self.emitter, self.config, self.storage)
        service.init()
        # Act
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        # Assert
        self.assertTrue(self._update_calls)
        for update in self._update_calls:
            self.assertTrue(update.is_current)

    def test_next_warehouses_loads_from_db(self):
        """Загружаются из БД склады для выбора следующих"""
        service = WarehouseService(self.emitter, self.config, self.storage)
        service.init()
        tvd = TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        tvd.is_rear = return_true
        # Act
        result = service.next_warehouses(tvd)
        # Assert
        self.assertTrue(result)
        self.assertTrue(self._load_calls)
