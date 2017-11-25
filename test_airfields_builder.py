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
        self.maxDiff = None
        self.assertEqual(result.format(), expected)

    def test_airfield_ctor(self):
        """Создаётся класс MCU аэродрома"""
        airfield = generation.Airfield(0, 0, 0, [], 0)
        self.fail()


class TestAirfieldsBuilder(unittest.TestCase):
    """Тестирование сборщика аэродромов"""


if __name__ == '__main__':
    unittest.main(verbosity=2)
