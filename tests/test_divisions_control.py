"""Тестирование управления дивизиями"""
import unittest
import pathlib

import processing
import tests

CONFIG = tests.mocks.ConfigMock(pathlib.Path('./testdata/conf.ini'))
TEST_TVD_NAME = 'moscow'
TEST_UNIT_NAME1 = 'REXPERT_BTD1_7'
TEST_UNIT_NAME2 = 'test_BTD2_2'
TEST_DIVISION_NAME1 = 'BTD1'
TEST_DIVISION_NAME2 = 'BTD2'


class TestDivisionsControl(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка перед тестами"""
        self.storage = processing.Storage(CONFIG.main)

    def tearDown(self):
        """Очистка после тестов"""
        self.storage.drop_database()

    def test_initialize_divisions(self):
        """Инициализируются дивизии кампании"""
        controller = processing.DivisionsController(CONFIG)
        # Act
        controller.initialize_divisions(TEST_TVD_NAME)
        # Assert
        self.assertEqual(controller.storage.divisions.collection.count(), 8)

    def test_damage_division(self):
        """Наносится урон дивизии"""
        controller = processing.DivisionsController(CONFIG)
        controller.initialize_divisions(TEST_TVD_NAME)
        expected = controller.storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units - 1
        # Act
        controller.damage_division(TEST_TVD_NAME, TEST_UNIT_NAME1)
        # Assert
        self.assertEqual(controller.storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units, expected)

    def test_repair_rate(self):
        """Рассчитывается коэффициент восполнения дивизий"""
        controller = processing.DivisionsController(CONFIG)
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
        controller = processing.DivisionsController(CONFIG)
        controller.initialize_divisions(TEST_TVD_NAME)
        controller.damage_division(TEST_TVD_NAME, TEST_UNIT_NAME1)
        controller.damage_division(TEST_TVD_NAME, TEST_UNIT_NAME1)
        controller.damage_division(TEST_TVD_NAME, TEST_UNIT_NAME2)
        current = controller.storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units
        expected1 = current * controller.repair_rate(destroyed_warehouses)
        expected2 = processing.DIVISIONS[TEST_DIVISION_NAME2]
        # Act
        controller.repair_division(TEST_TVD_NAME, TEST_DIVISION_NAME1, destroyed_warehouses)
        controller.repair_division(TEST_TVD_NAME, TEST_DIVISION_NAME2, destroyed_warehouses)
        # Assert
        self.assertEqual(controller.storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME1).units, expected1)
        self.assertEqual(controller.storage.divisions.load_by_name(TEST_TVD_NAME, TEST_DIVISION_NAME2).units, expected2)


if __name__ == '__main__':
    unittest.main(verbosity=2)