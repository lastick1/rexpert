"""Тестирование сборки базы локаций"""
import pathlib
import unittest

import processing


class TestLocation(unittest.TestCase):
    """Тестирование локаций"""

    def test_location_type(self):
        """Выбрасывается исключение на создание локации недопустимого типа"""
        def init_location():
            """Инициализировать локацию"""
            processing.Location('wrong_type', 0, 0, 0, 0, 10, 10)
        self.assertRaises(Exception, init_location)


class TestLocationBuilder(unittest.TestCase):
    """Тестирование сборки базы локаций"""

    def test_add_incorrect(self):
        """Выбрасывается исключение на добавление локации недопустимого типа"""
        builder = processing.LocationsBuilder()

        def add_location():
            """Добавить локацию"""
            builder.add('wrong_type', 0, 0, 0)

        self.assertRaises(Exception, add_location)

    def test_add_correct(self):
        """Добавляются корректные локации"""
        builder = processing.LocationsBuilder()
        try:
            for name in processing.LOCATION_TYPES:
                builder.add(name, 0, 0, 0)
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)
        count = 0
        for name in builder.locations:
            count += len(builder.locations[name])
        self.assertEqual(count, len(processing.LOCATION_TYPES))

    def test_locations_database(self):
        """Создаётся база локаций"""
        with pathlib.Path('./testdata/ldf/test_locations.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_air_objective(self):
        """Обрабатываются локации AirObjective"""
        with pathlib.Path('./testdata/ldf/test_location_air_objective.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_airfield(self):
        """Обрабатываются локации Airfield"""
        with pathlib.Path('./testdata/ldf/test_location_airfield.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_decoration(self):
        """Обрабатываются локации Airfield"""
        with pathlib.Path('./testdata/ldf/test_location_decoration.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_ground_objective(self):
        """Обрабатываются локации GroundObjective"""
        with pathlib.Path('./testdata/ldf/test_location_ground_objective.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_reference_location(self):
        """Обрабатываются локации ReferenceLocation"""
        with pathlib.Path('./testdata/ldf/test_location_reference_location.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_substrate(self):
        """Обрабатываются локации Substrate"""
        with pathlib.Path('./testdata/ldf/test_location_substrate.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_terrain_leveler(self):
        """Обрабатываются локации TerrainLeveler"""
        with pathlib.Path('./testdata/ldf/test_location_terrain_leveler.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)

    def test_locations_navigation(self):
        """Обрабатываются локации Navigation"""
        with pathlib.Path('./testdata/ldf/test_location_navigation.ldf').absolute().open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        result = builder.make_text()
        self.assertEqual(result, ldf)


if __name__ == '__main__':
    unittest.main(verbosity=2)