"""Тестирование управления аэродромами"""
import unittest
import pathlib
import pymongo
from processing import AirfieldsController
from processing.objects import Airfield
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
PLANES = mocks.PlanesMock()
DB_NAME = 'test_rexpert'
TEST_TVD_NAME = 'test_tvd'
TEST_FIELDS = pathlib.Path(r'./testdata/test_fields.csv')
TEST_AIRFIELD_NAME = 'Verbovka'


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

    def test_decrease_planes(self):
        """Уменьшается количество самолётов на аэродроме при появлении на нём"""
        result = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name=TEST_AIRFIELD_NAME)
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = PLANES.name_to_key(aircraft_name)
        # Act
        self.controller.spawn(aircraft_name, TEST_TVD_NAME, Airfield(1, 101, 1, {'x': 112687, 'z': 184308}))
        # Assert
        document = self.airfields.find_one({'_id': result.id})
        self.assertEqual(result.planes[aircraft_key], document['planes'][aircraft_key])


if __name__ == '__main__':
    unittest.main(verbosity=2)
