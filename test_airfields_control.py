"""Тестирование управления аэродромами"""
import unittest
import pathlib
import pymongo
from processing import AirfieldsController
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'.\testdata\conf.ini'))
DB_NAME = 'test_rexpert'
TEST_TVD_NAME = 'test_tvd'
TEST_FIELDS = pathlib.Path(r'./testdata/test_fields.csv')


class TestAirfieldsController(unittest.TestCase):
    """Тестовый класс контроллера"""
    def setUp(self):
        self.mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
        rexpert = self.mongo[DB_NAME]
        self.controller = AirfieldsController(airfields=rexpert['Airfields'])

    def tearDown(self):
        self.mongo.drop_database(DB_NAME)
        self.mongo.close()

    def test_initialize(self):
        """Инициализируется коллекция аэродромов"""
        self.controller.initialize(TEST_TVD_NAME, TEST_FIELDS)

    def test_get_airfield_in_radius(self):
        """Определяется аэродром в радиусе от координат"""
        self.controller.initialize(TEST_TVD_NAME, TEST_FIELDS)
        result = self.controller.get_airfield_in_radius(tvd_name=TEST_TVD_NAME, x=112687, z=184308, radius=1000)
        self.assertEqual(result.name, 'Verbovka')

    def test_get_airfield_by_name(self):
        self.controller.initialize(TEST_TVD_NAME, TEST_FIELDS)
        result = self.controller.get_airfield_by_name(tvd_name=TEST_TVD_NAME, name='Verbovka')
        self.assertEqual(result.name, 'Verbovka')


if __name__ == '__main__':
    unittest.main(verbosity=2)
