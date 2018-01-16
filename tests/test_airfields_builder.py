"""Тесты сборки аэродромов"""
import unittest
import pathlib
import processing
from tests.mocks import PlanesMock

PLANES = PlanesMock()
COMMON = 'common'
UNCOMMON = 'uncommon'
TEST_PLANE_1 = 'lagg-3 ser.29'
TEST_PLANE_2 = 'bf 109 f-4'


class TestAirfield(unittest.TestCase):
    """Тестирование форматирования MCU аэродрома"""
    def test_plane_formatting(self):
        """Сериализуется самолёт в MCU аэродрома"""
        expected = pathlib.Path(r'./testdata/mcu/plane_in_airfield.txt').read_text(encoding='utf-8')
        common = PLANES.cfg[COMMON]
        uncommon = PLANES.cfg[UNCOMMON][TEST_PLANE_1]
        # act
        result = processing.Plane(10, common, uncommon)
        # assert
        self.assertEqual(result.format(), expected)

    def test_airfield_formatting(self):
        """Сериализуется MCU аэродрома"""
        expected = pathlib.Path(r'./testdata/mcu/airfield.txt').read_text(encoding='utf-8')
        common = PLANES.cfg[COMMON]
        uncommon = PLANES.cfg[UNCOMMON][TEST_PLANE_1]
        # act
        result = processing.Airfield(
            name='Airfield',
            country=101,
            radius=1000,
            planes=[processing.Plane(10, common, uncommon)])
        self.assertEqual(result.format(), expected)

    def test_airfield_formatting_two_planes(self):
        """Сериализуется MCU аэродрома с 2мя самолётами"""
        expected = pathlib.Path(r'./testdata/mcu/airfield_two_planes.txt').read_text(encoding='utf-8')
        common = PLANES.cfg[COMMON]
        uncommon = PLANES.cfg[UNCOMMON][TEST_PLANE_1]
        # act
        result = processing.Airfield(
            name='Airfield',
            country=101,
            radius=1000,
            planes=[
                processing.Plane(10, common, uncommon),
                processing.Plane(10, common, uncommon)
            ])
        self.assertEqual(result.format(), expected)


class TestAirfieldsBuilder(unittest.TestCase):
    """Тестирование сборщика аэродромов"""
    @staticmethod
    def _get_planes() -> list:
        """Получить тестовый список самолётов аэродрома"""
        return [
            processing.Plane(10, PLANES.cfg[COMMON], PLANES.cfg[UNCOMMON][TEST_PLANE_1]),
            processing.Plane(10, PLANES.cfg[COMMON], PLANES.cfg[UNCOMMON][TEST_PLANE_2])
        ]

    def test_make_airfield_group(self):
        """Создаётся координатная группа аэродрома"""
        planes = self._get_planes()
        airfield = processing.Airfield(name='test_af', country=101, radius=4000, planes=planes)
        builder = processing.AirfieldsBuilder({'red': pathlib.Path(r'./tmp')}, pathlib.Path('r./tmp'), PLANES)
        # act
        builder.make_airfield_group(airfield, 25001.1, 25001.1)

    def test_make_subtitle_group(self):
        """Создаётся координатная группа субтитров"""
        planes = self._get_planes()
        builder = processing.AirfieldsBuilder({101: pathlib.Path(r'./tmp')}, pathlib.Path(r'./tmp'), PLANES)
        airfield = processing.Airfield(name='test_af', country=101, radius=4000, planes=planes)
        # act
        builder.make_subtitle_group(airfield, 24001.1, 24001.1, pathlib.Path(r'./data/sub_templates/fields_sub.Group'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
