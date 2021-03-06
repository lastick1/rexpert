"""Тестирование парсинга исходников миссий"""
from __future__ import annotations
import pathlib
import unittest

from processing import SourceParser
from tests.mocks import ConfigMock

CONFIG = ConfigMock()

DATE_FORMAT = '%d.%m.%Y'
TEST_TVD_NAME = 'kuban'

CONFIG.mgen.maps = [TEST_TVD_NAME]


class TestSourceParser(unittest.TestCase):
    """Тестовый класс"""

    def setUp(self):
        """Настройка перед тестами"""

    def tearDown(self):
        """Очистка после тестов"""

    def test_parse(self):
        """Определяется карта и дата из исходника миссии"""
        parser = SourceParser(CONFIG)
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path(
            './tests/data/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertEqual(result.date.strftime(DATE_FORMAT), '01.06.1943')

    def test_parse_server_input(self):
        """Определяются MCU ServerInput из исходника миссии"""
        parser = SourceParser(CONFIG)
        expected = [
            {'name': 'test_input', 'pos': {'x': 50, 'z': 50}},
            {'name': 'REXPERT_DEACT_kubinka', 'pos': {'x': 250.0, 'z': 520.0}},
        ]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path(
            './tests/data/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.server_inputs, expected)

    def test_parse_mission_objective(self):
        """Определяются MCU MissionObjective из исходника миссии"""
        parser = SourceParser(CONFIG)
        expected = [{'coalition': 2, 'obj_type': 15,
                     'pos': {'x': 100.0, 'z': 100.0}, 'success': 1}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path(
            './tests/data/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.objectives, expected)

    def test_parse_airfields(self):
        """Определяются аэродромы из исходника миссии"""
        parser = SourceParser(CONFIG)
        expected = [{'country': 101, 'name': 'kubinka',
                     'pos': {'x': 150.0, 'z': 150.0}}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path(
            './tests/data/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.airfields, expected)

    def test_parse_division_units(self):
        """Определяются юниты дивизий из исходника миссии"""
        parser = SourceParser(CONFIG)
        expected = [{'name': 'REXPERT_BTD1_7',
                     'pos': {'x': 200.0, 'z': 200.0}}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path(
            './tests/data/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.units, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
