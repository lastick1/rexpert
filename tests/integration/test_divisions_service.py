"""Тестирование управления дивизиями"""
import unittest

from core import EventsEmitter
from model import DIVISIONS
from storage import Storage
from services import DivisionsService

from tests.mocks import ConfigMock

CONFIG = ConfigMock()

TEST_TVD_NAME = 'moscow'
TEST_UNIT_NAME1 = 'REXPERT_BTD1_7'
TEST_UNIT_NAME2 = 'test_BTD2_2'
TEST_DIVISION_NAME1 = 'BTD1'
TEST_DIVISION_NAME2 = 'BTD2'


class TestDivisionsControl(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка перед тестами"""
        self._emitter: EventsEmitter = EventsEmitter()
        self._storage: Storage = Storage(CONFIG.main)

    def tearDown(self):
        """Очистка после тестов"""
        self._storage.drop_database()

    def test_initialize_divisions(self):
        """Инициализируются дивизии кампании"""
        controller = DivisionsService(
            self._emitter,
            CONFIG,
            self._storage
        )
        # Act
        controller.initialize_divisions(TEST_TVD_NAME)
        # Assert
        self.assertEqual(self._storage.divisions.collection.count(), 8)

    def test_damage_division(self):
        """Наносится урон дивизии"""
        controller = DivisionsService(
            self._emitter,
            CONFIG,
            self._storage
        )
        controller.initialize_divisions(TEST_TVD_NAME)
        expected = self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units - 1
        # Act
        controller.damage_division(100, TEST_TVD_NAME, TEST_UNIT_NAME1)
        # Assert
        self.assertEqual(self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units, expected)

    def test_repair_rate(self):
        """Рассчитывается коэффициент восполнения дивизий"""
        controller = DivisionsService(
            self._emitter,
            CONFIG,
            self._storage
        )
        # Act
        r0 = controller.repair_rate(0)
        r1 = controller.repair_rate(1)
        r2 = controller.repair_rate(2)
        r3 = controller.repair_rate(3)
        # Assert
        self.assertSequenceEqual((r0, r1, r2, r3), (1.15, 1.1, 1.05, 1.0))

    def test_repair_division(self):
        """Восполняются дивизии при целых складах"""
        destroyed_warehouses = 0
        controller = DivisionsService(
            self._emitter,
            CONFIG,
            self._storage
        )
        controller.initialize_divisions(TEST_TVD_NAME)
        controller.damage_division(100, TEST_TVD_NAME, TEST_UNIT_NAME1)
        controller.damage_division(100, TEST_TVD_NAME, TEST_UNIT_NAME1)
        controller.damage_division(100, TEST_TVD_NAME, TEST_UNIT_NAME1)
        controller.damage_division(100, TEST_TVD_NAME, TEST_UNIT_NAME2)
        current = self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units
        expected1 = current * controller.repair_rate(destroyed_warehouses)
        expected2 = DIVISIONS[TEST_DIVISION_NAME2]
        # Act
        controller.repair_division(TEST_TVD_NAME, TEST_DIVISION_NAME1, destroyed_warehouses)
        controller.repair_division(TEST_TVD_NAME, TEST_DIVISION_NAME2, destroyed_warehouses)
        # Assert
        self.assertEqual(self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units, expected1)
        self.assertEqual(self._storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME2).units, expected2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
