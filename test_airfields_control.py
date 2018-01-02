"""Тестирование управления аэродромами"""
import unittest
import pathlib
import pymongo
import configs
from processing import AirfieldsController
from processing.objects import Airfield, BotPilot, Aircraft
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
PLANES = mocks.PlanesMock()
DB_NAME = 'test_rexpert'
TEST_TVD_NAME = 'test_tvd'
TEST_FIELDS = pathlib.Path(r'./testdata/test_fields.csv')
TEST_AIRFIELD_NAME = 'Verbovka'
OBJECTS = configs.Objects()


class TestAirfieldsController(unittest.TestCase):
    """Тестовый класс контроллера"""
    def setUp(self):
        self.mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
        rexpert = self.mongo[DB_NAME]
        self.airfields = rexpert['Airfields']
        self.controller = AirfieldsController(main=MAIN, config=PLANES, airfields=self.airfields)
        self.controller.initialize(TEST_TVD_NAME, TEST_FIELDS)

    def tearDown(self):
        """Удаление базы после теста"""
        self.mongo.drop_database(DB_NAME)
        self.mongo.close()

    def test_get_airfield_in_radius(self):
        """Определяется аэродром в радиусе от координат"""
        # Act
        result = self.controller.get_airfield_in_radius(tvd_name=TEST_TVD_NAME, x=112687, z=184308, radius=1000)
        # Assert
        self.assertEqual(result.name, 'Verbovka')

    def test_get_airfield_by_name(self):
        """Определяется аэродром по его наименованию"""
        # Act
        result = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        # Assert
        self.assertEqual(result.name, 'Verbovka')

    def test_spawn_planes(self):
        """Уменьшается количество самолётов на аэродроме при появлении на нём"""
        managed_airfield = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = PLANES.name_to_key(aircraft_name)
        document = self.airfields.find_one({'_id': managed_airfield.id})
        # Act
        self.controller.spawn(aircraft_name, TEST_TVD_NAME, Airfield(1, 101, 1, {'x': 112687, 'z': 184308}))
        # Assert
        self.assertEqual(managed_airfield.planes[aircraft_key], document['planes'][aircraft_key] - 1)
        document = self.airfields.find_one({'_id': managed_airfield.id})
        self.assertEqual(managed_airfield.planes[aircraft_key], document['planes'][aircraft_key])

    def test_return_planes(self):
        """Восполняется количество самолётов на аэродроме при возврате на него (деспаун)"""
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
        self.controller.finish(TEST_TVD_NAME, bot)
        # Assert
        self.assertEqual(managed_airfield.planes[aircraft_key], document['planes'][aircraft_key] + 1)
        document = self.airfields.find_one({'_id': managed_airfield.id})
        self.assertEqual(managed_airfield.planes[aircraft_key], document['planes'][aircraft_key])


if __name__ == '__main__':
    unittest.main(verbosity=2)
