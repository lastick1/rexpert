"""Тестирование управления аэродромами"""
import unittest
import pathlib
import pymongo
import configs
from generation import TvdBuilder
from processing import AirfieldsController
from processing.objects import Airfield, BotPilot, Aircraft
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)
PLANES = mocks.PlanesMock()
PARAMS = mocks.ParamsMock()
DB_NAME = 'test_rexpert'
TEST = 'test'
TEST_TVD_NAME = 'stalingrad'
TEST_TVD_DATE = '10.11.1941'
TEST_FIELDS = pathlib.Path(r'./testdata/test_fields.csv')
TEST_AIRFIELD_NAME = 'Verbovka'
TEST_AIRFIELD_X = 112687
TEST_AIRFIELD_Z = 184308
OBJECTS = configs.Objects()


class TestAirfieldsController(unittest.TestCase):
    """Тестовый класс контроллера"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
        rexpert = self.mongo[DB_NAME]
        self.airfields = rexpert['Airfields']
        self.controller = AirfieldsController(main=MAIN, mgen=MGEN, config=PLANES, airfields=self.airfields)

    def tearDown(self):
        """Удаление базы после теста"""
        self.mongo.drop_database(DB_NAME)
        self.mongo.close()

    def test_get_airfield_in_radius(self):
        """Определяется аэродром в радиусе от координат"""
        tvd = mocks.TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        self.controller.initialize_airfields(tvd)
        # Act
        result = self.controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_X, z=TEST_AIRFIELD_Z, radius=1000)
        # Assert
        self.assertEqual(result.name, 'Verbovka')

    def test_get_airfield_by_name(self):
        """Определяется аэродром по его наименованию"""
        tvd = mocks.TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        self.controller.initialize_airfields(tvd)
        # Act
        result = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        # Assert
        self.assertEqual(result.name, 'Verbovka')

    def test_spawn_planes(self):
        """Уменьшается количество самолётов на аэродроме при появлении на нём"""
        tvd = mocks.TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        self.controller.initialize_airfields(tvd)
        managed_airfield = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = PLANES.name_to_key(aircraft_name)
        expected = self.airfields.find_one({'_id': managed_airfield.id})['planes'][aircraft_key] - 1
        # Act
        self.controller.spawn(tvd, aircraft_name, TEST_AIRFIELD_X, TEST_AIRFIELD_Z)
        # Assert
        managed_airfield = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], expected)
        document = self.airfields.find_one({'_id': managed_airfield.id})
        self.assertEqual(document['planes'][aircraft_key], expected)

    def test_return_planes(self):
        """Восполняется количество самолётов на аэродроме при возврате на него (деспаун)"""
        tvd = mocks.TvdMock(TEST_TVD_NAME)
        tvd.country = 101
        self.controller.initialize_airfields(tvd)
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = PLANES.name_to_key(aircraft_name)
        bot_name = 'BotPilot_Pe2'
        managed_airfield = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        document = self.airfields.find_one({'_id': managed_airfield.id})
        aircraft = Aircraft(
            1, OBJECTS[aircraft_name], 101, 1, aircraft_name, pos={'x': managed_airfield.x, 'z': managed_airfield.z})
        bot = BotPilot(
            2, OBJECTS[bot_name], aircraft, 101, 1, bot_name, pos={'x': managed_airfield.x, 'z': managed_airfield.z})

        # Act
        self.controller.finish(tvd, bot)
        # Assert
        managed_airfield = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], document['planes'][aircraft_key] + 1)
        document = self.airfields.find_one({'_id': managed_airfield.id})
        self.assertEqual(managed_airfield.planes[aircraft_key], document['planes'][aircraft_key])

    def test_get_country(self):
        """Определяется страна аэродрома по узлу графа"""
        builder = TvdBuilder(TEST_TVD_NAME, MGEN, MAIN, PARAMS, PLANES)
        self.controller.initialize_airfields(builder.get_tvd(TEST_TVD_DATE))
        verbovka = self.controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_X, z=TEST_AIRFIELD_Z, radius=10)
        # Act
        result = self.controller.get_country(verbovka, builder.get_tvd(TEST_TVD_DATE))
        # Assert
        self.assertEqual(201, result)

    def test_add_aircraft(self):
        """Добавляется самолёт на аэродром"""
        builder = TvdBuilder(TEST_TVD_NAME, MGEN, MAIN, PARAMS, PLANES)
        tvd = builder.get_tvd(TEST_TVD_DATE)
        self.controller.initialize_airfields(tvd)
        aircraft_name = 'bf 109 f-4'
        aircraft_key = PLANES.name_to_key(aircraft_name)
        document = self.airfields.find_one({'name': TEST_AIRFIELD_NAME})
        expected = document['planes'][aircraft_key] + 5
        # Act
        self.controller.add_aircraft(tvd, TEST_AIRFIELD_NAME, aircraft_name, 5)
        # Assert
        document = self.airfields.find_one({'name': TEST_AIRFIELD_NAME})
        self.assertEqual(expected, document['planes'][aircraft_key])

    def test_add_aircraft_wrong(self):
        """НЕ добавляется самолёт на аэродром другой страны"""
        builder = TvdBuilder(TEST_TVD_NAME, MGEN, MAIN, PARAMS, PLANES)
        tvd = builder.get_tvd(TEST_TVD_DATE)
        aircraft_name = 'lagg-3 ser.29'
        aircraft_key = PLANES.name_to_key(aircraft_name)
        self.controller.initialize_airfields(tvd)
        # Act
        self.controller.add_aircraft(tvd, TEST_AIRFIELD_NAME, aircraft_name, 5)
        # Assert
        document = self.airfields.find_one({'name': TEST_AIRFIELD_NAME})
        self.assertNotIn(aircraft_key, document['planes'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
