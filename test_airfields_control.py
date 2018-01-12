"""Тестирование управления аэродромами"""
import unittest
import pathlib
import configs
from processing import AirfieldsController, TvdBuilder, Storage
from processing.objects import BotPilot, Aircraft
from tests import mocks


CONFIG = mocks.ConfigMock(pathlib.Path(r'./testdata/conf.ini'))

TEST = 'test'
TEST_TVD_NAME = 'stalingrad'
TEST_TVD_DATE = '10.11.1941'
TEST_FIELDS = pathlib.Path(r'./testdata/test_fields.csv')
TEST_AIRFIELD_NAME = 'Verbovka'
TEST_AIRFIELD_X = 112687
TEST_AIRFIELD_Z = 184308
OBJECTS = configs.Objects()


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(CONFIG.mgen.xgml[tvd_name])


class TestAirfieldsController(unittest.TestCase):
    """Тестовый класс контроллера"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.storage = Storage(CONFIG.main)
        self.storage.airfields.update_airfields(
            AirfieldsController.initialize_managed_airfields(CONFIG.mgen.airfields_data[TEST_TVD_NAME]))

    def tearDown(self):
        """Удаление базы после теста"""
        self.storage.drop_database()

    def test_get_airfield_in_radius(self):
        """Определяется аэродром в радиусе от координат"""
        controller = AirfieldsController(CONFIG)
        tvd = mocks.TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        # Act
        result = controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_X, z=TEST_AIRFIELD_Z, radius=1000)
        # Assert
        self.assertEqual(result.name, 'Verbovka')

    def test_spawn_planes(self):
        """Уменьшается количество самолётов на аэродроме при появлении на нём"""
        controller = AirfieldsController(CONFIG)
        tvd = mocks.TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        managed_airfield = self.storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        managed_airfield.planes[aircraft_key] = 10
        self.storage.airfields.update_airfield(managed_airfield)
        expected = self.storage.airfields.load_by_id(managed_airfield.id).planes[aircraft_key] - 1
        # Act
        controller.spawn(tvd, aircraft_name, TEST_AIRFIELD_X, TEST_AIRFIELD_Z)
        # Assert
        managed_airfield = self.storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], expected)
        airfield = self.storage.airfields.load_by_id(managed_airfield.id)
        self.assertEqual(airfield.planes[aircraft_key], expected)

    def test_return_planes(self):
        """Восполняется количество самолётов на аэродроме при возврате на него (деспаун)"""
        controller = AirfieldsController(CONFIG)
        tvd = mocks.TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        bot_name = 'BotPilot_Pe2'
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        managed_airfield = self.storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        managed_airfield.planes[aircraft_key] = 10
        expected = managed_airfield.planes[aircraft_key] + 1
        self.storage.airfields.update_airfield(managed_airfield)
        aircraft = Aircraft(
            1, OBJECTS[aircraft_name], 101, 1, aircraft_name, pos={'x': managed_airfield.x, 'z': managed_airfield.z})
        bot = BotPilot(
            2, OBJECTS[bot_name], aircraft, 101, 1, bot_name, pos={'x': managed_airfield.x, 'z': managed_airfield.z})
        # Act
        controller.finish(tvd, bot)
        # Assert
        managed_airfield = self.storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], expected)

    def test_get_country(self):
        """Определяется страна аэродрома по узлу графа"""
        controller = AirfieldsController(CONFIG)
        builder = TvdBuilder(TEST_TVD_NAME, CONFIG)
        builder.grid_control.get_file = _get_xgml_file_mock
        verbovka = controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_X, z=TEST_AIRFIELD_Z, radius=10)
        # Act
        result = controller.get_country(verbovka, builder.get_tvd(TEST_TVD_DATE))
        # Assert
        self.assertEqual(201, result)

    def test_add_aircraft(self):
        """Добавляется самолёт на аэродром"""
        controller = AirfieldsController(CONFIG)
        builder = TvdBuilder(TEST_TVD_NAME, CONFIG)
        builder.grid_control.get_file = _get_xgml_file_mock
        tvd = builder.get_tvd(TEST_TVD_DATE)
        aircraft_name = 'bf 109 f-4'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        managed_airfield = self.storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        managed_airfield.planes[aircraft_key] = 10
        self.storage.airfields.update_airfield(managed_airfield)
        expected = managed_airfield.planes[aircraft_key] + 5
        # Act
        controller.add_aircraft(tvd, TEST_AIRFIELD_NAME, aircraft_name, 5)
        # Assert
        managed_airfield = self.storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertEqual(expected, managed_airfield.planes[aircraft_key])

    def test_add_aircraft_wrong(self):
        """НЕ добавляется самолёт на аэродром другой страны"""
        controller = AirfieldsController(CONFIG)
        builder = TvdBuilder(TEST_TVD_NAME, CONFIG)
        builder.grid_control.get_file = _get_xgml_file_mock
        tvd = builder.get_tvd(TEST_TVD_DATE)
        aircraft_name = 'lagg-3 ser.29'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        # Act
        controller.add_aircraft(tvd, TEST_AIRFIELD_NAME, aircraft_name, 5)
        # Assert
        managed_airfield = self.storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertNotIn(aircraft_key, managed_airfield.planes)

    @unittest.skip("реализовать")
    def test_return_disco_aircraft(self):
        """Возвращаются на аэродром при диско неповреждённые самолёты"""
        self.fail()


if __name__ == '__main__':
    unittest.main(verbosity=2)
