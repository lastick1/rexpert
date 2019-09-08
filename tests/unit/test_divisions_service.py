"Тестирование сервиса дивизий"
from __future__ import annotations
from typing import List, Dict
import unittest

from core import EventsEmitter, DivisionDamage
from services import DivisionsService
from storage import Storage
from model import CampaignMission, Division, DIVISIONS
from tests.mocks import EventsInterceptor, \
    ConfigMock, \
    StorageMock

TEST_UNIT_NAME1 = 'REXPERT_BTD1_7'
TEST_UNIT_NAME2 = 'test_BID1_2'
TEST_DIVISION_NAME1 = 'BTD1'
TEST_DIVISION_NAME2 = 'BID1'

TEST_TVD_NAME = 'moscow'
TEST_DATE = '01.09.1941'
TEST_TARGET_AIRFIELD_SERVER_INPUT = 'Verbovka'
TEST_TARGET_POS_BTD1 = {'x': 156060.64, 'z': 132392.5}
TEST_TARGET_HP = 3
TEST_TARGET_POS_BTD1_UNITS = [
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
TEST_TARGET_POS_BID1 = {'x': 255453.86, 'z': 230798.2}
TEST_TARGET_POS_BID1_UNITS = [
    {'x': 255453.86, 'z': 230798.2},
    {'x': 256461.58, 'z': 231861.16},
    {'x': 255169.17, 'z': 233163.56},
    {'x': 255055.39, 'z': 232101.14},
    {'x': 255604.38, 'z': 231692.38},
    {'x': 256010.75, 'z': 231154.91},
    {'x': 256484.95, 'z': 233269.22},
    {'x': 256907.78, 'z': 233390.91},
    {'x': 257196.23, 'z': 234433.89},
    {'x': 257767.08, 'z': 232920.91}
]
TEST_DIVISION1 = Division(
    tvd_name=TEST_TVD_NAME,
    name=TEST_DIVISION_NAME2,
    units=DIVISIONS[TEST_DIVISION_NAME2],
    pos=TEST_TARGET_POS_BTD1
)
TEST_DIVISION2 = Division(
    tvd_name=TEST_TVD_NAME,
    name=TEST_DIVISION_NAME2,
    units=DIVISIONS[TEST_DIVISION_NAME2],
    pos=TEST_TARGET_POS_BID1
)
TEST_MISSION = CampaignMission(
    file='result1',
    date=TEST_DATE,
    tvd_name=TEST_TVD_NAME,
    additional=dict(),
    server_inputs=[
        {'name': TEST_DIVISION_NAME2, 'pos': TEST_TARGET_POS_BTD1}
    ],
    objectives=[],
    airfields=[],
    units=[],
    actions=list()
)


class TestDivisionsService(unittest.TestCase):
    "Тесты"

    def setUp(self):
        """Настройка перед тестом"""
        self.config = ConfigMock()
        self._storage: Storage = StorageMock(self.config.main)
        self._storage.divisions.load_by_tvd = self._load_by_tvd
        self._storage.divisions.load_by_name = self._load_by_name
        self.emitter = EventsEmitter()
        self._interceptor = EventsInterceptor(self.emitter)
        self._update_calls: List[Division] = list()
        self._storage.divisions.update = self._update_calls.append
        self._divisions: Dict[Division] = {
            TEST_DIVISION_NAME1: TEST_DIVISION1,
            TEST_DIVISION_NAME2: TEST_DIVISION2,
        }
        TEST_MISSION.units.clear()

    def _load_by_tvd(self, tvd_name: str) -> List[Division]:
        return self._divisions.values()

    def _load_by_name(self, tvd_name: str, name: str) -> Division:
        return self._divisions[name]

    def _init_new_service_instance(self) -> DivisionsService:
        service = DivisionsService(
            self.emitter,
            self.config,
            self._storage
        )
        service.init()
        return service

    def test_division_kill(self):
        """Обрабатывается уничтожение дивизии"""
        TEST_MISSION.units.extend([
            {'name': 'REXPERT_BTD1_3', 'pos': TEST_TARGET_POS_BTD1_UNITS[0]},
            {'name': 'REXPERT_BTD1_15', 'pos': TEST_TARGET_POS_BTD1_UNITS[1]},
            {'name': 'REXPERT_BTD1_2', 'pos': TEST_TARGET_POS_BTD1_UNITS[2]},
            {'name': 'REXPERT_BTD1_10', 'pos': TEST_TARGET_POS_BTD1_UNITS[3]},
            {'name': 'REXPERT_BTD1_17', 'pos': TEST_TARGET_POS_BTD1_UNITS[4]},
            {'name': 'REXPERT_BTD1_9', 'pos': TEST_TARGET_POS_BTD1_UNITS[5]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[6]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[7]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[8]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[9]},
        ])
        self._init_new_service_instance()
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        # Act
        for unit in TEST_MISSION.units:
            self.emitter.gameplay_division_damage.on_next(DivisionDamage(
                123, TEST_MISSION.tvd_name, unit['name']))
        # Assert
        self.assertTrue(self._interceptor.points_gains)

    def test_kill_on_mission_start(self):
        "Отправляется сообщение об уничтоженных дивизиях в начале миссии"
        TEST_MISSION.units.extend([
            {'name': 'REXPERT_BTD1_3', 'pos': TEST_TARGET_POS_BTD1_UNITS[0]},
            {'name': 'REXPERT_BTD1_15', 'pos': TEST_TARGET_POS_BTD1_UNITS[1]},
        ])
        self._init_new_service_instance()
        # Act
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        # Assert
        self.assertTrue(self._interceptor.points_gains)

    def test_damage_notification(self):
        "Отправляется в чат оповещение об уничтожении секции укрепрайона"
        TEST_MISSION.units.extend([
            {'name': 'REXPERT_BTD1_3', 'pos': TEST_TARGET_POS_BTD1_UNITS[0]},
            {'name': 'REXPERT_BTD1_15', 'pos': TEST_TARGET_POS_BTD1_UNITS[1]},
            {'name': 'REXPERT_BTD1_2', 'pos': TEST_TARGET_POS_BTD1_UNITS[2]},
            {'name': 'REXPERT_BTD1_10', 'pos': TEST_TARGET_POS_BTD1_UNITS[3]},
            {'name': 'REXPERT_BTD1_17', 'pos': TEST_TARGET_POS_BTD1_UNITS[4]},
            {'name': 'REXPERT_BTD1_9', 'pos': TEST_TARGET_POS_BTD1_UNITS[5]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[6]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[7]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[8]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[9]},
        ])
        self._init_new_service_instance()
        # Act
        self.emitter.gameplay_division_damage.on_next(DivisionDamage(
            123, TEST_MISSION.tvd_name, TEST_MISSION.units[0]['name']
        ))
        # Assert
        self.assertTrue(self._interceptor.commands)

    def test_initialize_divisions(self):
        """Инициализируются дивизии кампании"""
        controller = self._init_new_service_instance()
        # Act
        controller.initialize_divisions(TEST_TVD_NAME)
        # Assert
        self.assertEqual(len(self._update_calls), 6)

    def test_damage_division(self):
        """Наносится урон дивизии"""
        controller = self._init_new_service_instance()
        controller.initialize_divisions(TEST_TVD_NAME)
        expected = self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units - 1
        # Act
        controller.damage_division(DivisionDamage(100, TEST_TVD_NAME, TEST_UNIT_NAME1))
        # Assert
        self.assertEqual(self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units, expected)

    def test_repair_rate(self):
        """Рассчитывается коэффициент восполнения дивизий"""
        controller = self._init_new_service_instance()
        # Act
        rate0 = controller.repair_rate(0)
        rate1 = controller.repair_rate(1)
        rate2 = controller.repair_rate(2)
        rate3 = controller.repair_rate(3)
        # Assert
        self.assertSequenceEqual((rate0, rate1, rate2, rate3), (1.15, 1.1, 1.05, 1.0))

    def test_repair_division(self):
        """Восполняются дивизии при целых складах"""
        controller = self._init_new_service_instance()
        destroyed_warehouses = 0
        controller.initialize_divisions(TEST_TVD_NAME)
        controller.damage_division(DivisionDamage(100, TEST_TVD_NAME, TEST_UNIT_NAME1))
        controller.damage_division(DivisionDamage(100, TEST_TVD_NAME, TEST_UNIT_NAME1))
        controller.damage_division(DivisionDamage(100, TEST_TVD_NAME, TEST_UNIT_NAME1))
        controller.damage_division(DivisionDamage(100, TEST_TVD_NAME, TEST_UNIT_NAME2))
        current = self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units
        expected1 = current * controller.repair_rate(destroyed_warehouses)
        expected2 = DIVISIONS[TEST_DIVISION_NAME2]
        # Act
        controller.repair_division(TEST_TVD_NAME, TEST_DIVISION_NAME1, destroyed_warehouses)
        controller.repair_division(TEST_TVD_NAME, TEST_DIVISION_NAME2, destroyed_warehouses)
        # Assert
        self.assertEqual(self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units, expected1)
        self.assertEqual(self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME2).units, expected2)
