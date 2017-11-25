"""Тесты сборки аэродромов"""
import unittest
import pathlib
import generation
from tests.mocks import PlanesMock

PLANES = PlanesMock()
COMMON = 'common'
UNCOMMON = 'uncommon'


class TestAirfield(unittest.TestCase):
    """Тестирование форматирования MCU аэродрома"""
    def test_plane_formatting(self):
        """Сериализуется самолёт в MCU аэродрома"""
        expected = pathlib.Path(r'./testdata/mcu/plane_in_airfield.txt').read_text(encoding='utf-8')
        test_plane = 'lagg-3 ser.29'
        common = PLANES.cfg[COMMON]
        uncommon = PLANES.cfg[UNCOMMON][test_plane]
        # act
        result = generation.Plane(10, common, uncommon)
        # assert
        self.assertEqual(result.format(), expected)

    def test_airfield_formatting(self):
        """Сериализуется MCU аэродрома"""
        expected = pathlib.Path(r'./testdata/mcu/airfield.txt').read_text(encoding='utf-8')
        test_plane = 'lagg-3 ser.29'
        common = PLANES.cfg[COMMON]
        uncommon = PLANES.cfg[UNCOMMON][test_plane]
        # act
        result = generation.Airfield(
            name='Airfield',
            country=101,
            radius=1000,
            planes=[generation.Plane(10, common, uncommon)])
        self.maxDiff = None
        self.assertEqual(result.format(), expected)

    def test_airfield_formatting_two_planes(self):
        """Сериализуется MCU аэродрома с 2мя самолётами"""
        expected = pathlib.Path(r'./testdata/mcu/airfield_two_planes.txt').read_text(encoding='utf-8')
        test_plane = 'lagg-3 ser.29'
        common = PLANES.cfg[COMMON]
        uncommon = PLANES.cfg[UNCOMMON][test_plane]
        # act
        result = generation.Airfield(
            name='Airfield',
            country=101,
            radius=1000,
            planes=[
                generation.Plane(10, common, uncommon),
                generation.Plane(10, common, uncommon)
            ])
        self.assertEqual(result.format(), expected)


class TestAirfieldsBuilder(unittest.TestCase):
    """Тестирование сборщика аэродромов"""


if __name__ == '__main__':
    unittest.main(verbosity=2)
