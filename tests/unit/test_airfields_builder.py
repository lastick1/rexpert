"""Тесты сборки аэродромов"""
from __future__ import annotations
import pathlib
import unittest

from processing import Airfield, Plane, AirfieldsBuilder
from tests.mocks import ConfigMock

CONFIG = ConfigMock()
COMMON = 'common'
UNCOMMON = 'uncommon'
TEST_PLANE_1 = 'lagg-3 ser.29'
TEST_PLANE_2 = 'bf 109 f-4'


class TestAirfield(unittest.TestCase):
    """Тестирование форматирования MCU аэродрома"""

    def test_plane_formatting(self):
        """Сериализуется самолёт в MCU аэродрома"""
        expected = pathlib.Path(
            r'./tests/data/mcu/plane_in_airfield.txt').read_text(encoding='utf-8')
        common = CONFIG.planes.cfg[COMMON]
        uncommon = CONFIG.planes.cfg[UNCOMMON][TEST_PLANE_1]
        # act
        result = Plane(10, common, uncommon)
        # assert
        self.assertEqual(result.format(), expected)

    def test_airfield_formatting(self):
        """Сериализуется MCU аэродрома"""
        expected = pathlib.Path(
            r'./tests/data/mcu/airfield.txt').read_text(encoding='utf-8')
        common = CONFIG.planes.cfg[COMMON]
        uncommon = CONFIG.planes.cfg[UNCOMMON][TEST_PLANE_1]
        # act
        result = Airfield(
            name='Airfield',
            country=101,
            radius=1000,
            planes=[Plane(10, common, uncommon)])
        self.assertEqual(result.format(), expected)

    def test_airfield_formatting_two_planes(self):
        """Сериализуется MCU аэродрома с 2мя самолётами"""
        expected = pathlib.Path(
            r'./tests/data/mcu/airfield_two_planes.txt').read_text(encoding='utf-8')
        common = CONFIG.planes.cfg[COMMON]
        uncommon = CONFIG.planes.cfg[UNCOMMON][TEST_PLANE_1]
        # act
        result = Airfield(
            name='Airfield',
            country=101,
            radius=1000,
            planes=[
                Plane(10, common, uncommon),
                Plane(10, common, uncommon)
            ])
        self.assertEqual(result.format(), expected)


class TestAirfieldsBuilder(unittest.TestCase):
    """Тестирование сборщика аэродромов"""
    @staticmethod
    def _get_planes() -> list:
        """Получить тестовый список самолётов аэродрома"""
        return [
            Plane(10, CONFIG.planes.cfg[COMMON],
                  CONFIG.planes.cfg[UNCOMMON][TEST_PLANE_1]),
            Plane(10, CONFIG.planes.cfg[COMMON],
                  CONFIG.planes.cfg[UNCOMMON][TEST_PLANE_2])
        ]

    def test_make_airfield_group(self):
        """Создаётся координатная группа аэродрома"""
        planes = self._get_planes()
        airfield = Airfield(name='test_af', country=101,
                            radius=4000, planes=planes)
        builder = AirfieldsBuilder({'red': pathlib.Path(
            r'./tmp')}, pathlib.Path('r./tmp'), CONFIG.planes)
        # act
        builder.make_airfield_group(airfield, 25001.1, 25001.1)

    def test_make_subtitle_group(self):
        """Создаётся координатная группа субтитров"""
        planes = self._get_planes()
        builder = AirfieldsBuilder(
            {101: pathlib.Path(r'./tmp')}, pathlib.Path(r'./tmp'), CONFIG.planes)
        airfield = Airfield(name='test_af', country=101,
                            radius=4000, planes=planes)
        # act
        builder.make_subtitle_group(airfield, 24001.1, 24001.1, pathlib.Path(
            r'./data/sub_templates/fields_sub.Group'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
