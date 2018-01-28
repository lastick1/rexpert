"""Тестирование парсинга исходников миссий"""
import pathlib
import unittest

import processing
import tests

DATE_FORMAT = '%d.%m.%Y'
TEST_TVD_NAME = 'kuban'

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
IOC.config.mgen.maps = [TEST_TVD_NAME]


class TestSourceParser(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка перед тестами"""

    def tearDown(self):
        """Очистка после тестов"""

    def test_parse(self):
        """Определяется карта и дата из исходника миссии"""
        parser = processing.SourceParser(IOC.config)
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertEqual(result.date.strftime(DATE_FORMAT), '01.06.1943')

    def test_parse_server_input(self):
        """Определяются MCU ServerInput из исходника миссии"""
        parser = processing.SourceParser(IOC.config)
        expected = [{'name': 'test_input', 'pos': {'x': 50, 'z': 50}}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.server_inputs, expected)

    def test_parse_mission_objective(self):
        """Определяются MCU MissionObjective из исходника миссии"""
        parser = processing.SourceParser(IOC.config)
        expected = [{'coalition': 2, 'obj_type': 15, 'pos': {'x': 100.0, 'z': 100.0}, 'success': 1}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.objectives, expected)

    def test_parse_airfields(self):
        """Определяются аэродромы из исходника миссии"""
        parser = processing.SourceParser(IOC.config)
        expected = [{'country': 101, 'name': 'kubinka', 'pos': {'x': 150.0, 'z': 150.0}}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.airfields, expected)

    def test_parse_division_units(self):
        """Определяются юниты дивизий из исходника миссии"""
        parser = processing.SourceParser(IOC.config)
        expected = [{'name': 'REXPERT_BTD1_7', 'pos': {'x': 200.0, 'z': 200.0}}]
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.division_units, expected)

    def test_parse_mission_kind(self):
        """Определяется вид миссии - противостояние или захват"""
        parser = processing.SourceParser(IOC.config)
        # Act
        result = parser.parse(TEST_TVD_NAME, pathlib.Path('./testdata/mission_source/{}.Mission'.format(TEST_TVD_NAME)))
        # Assert
        self.assertSequenceEqual(result.kind, 'assault')


if __name__ == '__main__':
    unittest.main(verbosity=2)
