"""Тестирование управления дивизиями"""
import unittest
import pathlib

import processing
import tests

CONFIG = tests.mocks.ConfigMock(pathlib.Path('./testdata/conf.ini'))
TEST_TVD_NAME = 'moscow'


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
        expected = controller.storage.divisions.load_by_name(TEST_TVD_NAME, 'BTD1').units - 1
        # Act
        controller.damage_division(TEST_TVD_NAME, 'REXPERT_BTD1_7')
        # Assert
        self.assertEqual(controller.storage.divisions.load_by_name(TEST_TVD_NAME, 'BTD1').units, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
