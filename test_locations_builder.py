"""Тестирование сборки базы локаций"""
import unittest
import pathlib
import generation
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)


class TestLocation(unittest.TestCase):
    """Тестирование локаций"""

    def test_location_type(self):
        """Выбрасывается исключение на создание локации недопустимого типа"""
        def init_location():
            generation.Location('wrong_type', 0, 0, 0, 0, 10, 10)
        self.assertRaises(Exception, init_location)


class TestLocationBuilder(unittest.TestCase):
    """Тестирование сборки базы локаций"""

    def test_add_incorrect(self):
        """Выбрасывается исключение на добавление локации недопустимого типа"""
        builder = generation.LocationsBuilder()

        def add_location():
            builder.add(0, 0, 0, 'wrong_type')

        self.assertRaises(Exception, add_location)


if __name__ == '__main__':
    unittest.main(verbosity=2)
