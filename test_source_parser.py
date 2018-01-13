"""Тестирование парсинга исходников миссий"""
import unittest
import pathlib

import processing
import tests

DATE_FORMAT = '%d.%m.%Y'
TEST_TVD_NAME = 'kuban'

CONFIG = tests.mocks.ConfigMock(pathlib.Path('./testdata/conf.ini'))
CONFIG.mgen.maps = [TEST_TVD_NAME]


class TestSourceParser(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка перед тестами"""

    def tearDown(self):
        """Очистка после тестов"""

    def test_parse(self):
        """Определяется карта и дата из исходника миссии"""
        parser = processing.SourceParser(CONFIG)
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertEqual(result.date.strftime(DATE_FORMAT), '01.06.1943')

    def test_parse_server_input(self):
        """Определяются MCU ServerInput из исходника миссии"""
        parser = processing.SourceParser(CONFIG)
        expected = [{'name': 'test_input', 'pos': {'x': 50, 'z': 50}}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.server_inputs, expected)

    def test_parse_mission_objective(self):
        """Определяются MCU MissionObjective из исходника миссии"""
        parser = processing.SourceParser(CONFIG)
        expected = [{'coalition': 2, 'obj_type': 15, 'pos': {'x': 100.0, 'z': 100.0}, 'success': 1}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.objectives, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
