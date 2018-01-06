"""Тестирование выбора аэродромов на миссию"""
import unittest
import pathlib

import pymongo

import generation
import processing
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)
PLANES = mocks.PlanesMock()
DB_NAME = 'test_rexpert'
MOSCOW = 'moscow'
TEST_FIELDS = pathlib.Path(r'./data/moscow_fields.csv')
TEST_AIRFIELD_NAME = 'kubinka'
TEST_AIRFIELD_X = 114768
TEST_AIRFIELD_Z = 192197
TEST_AIRCRAFT_KEY = PLANES.name_to_key('Pe-2 ser.35')


class TestAirfieldsSelector(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
        rexpert = self.mongo[DB_NAME]
        self.airfields = rexpert['Airfields']
        self.controller = processing.AirfieldsController(main=MAIN, config=PLANES, airfields=self.airfields)
        self.controller.initialize(MOSCOW, TEST_FIELDS)

    def test_calc_airfield_power(self):
        """Рассчитывается показатель приоритета аэродрома"""
        selector = generation.AirfieldsSelector(MAIN)
        airfield = processing.ManagedAirfield(
            name=TEST_AIRFIELD_NAME,
            tvd_name=MOSCOW,
            x=TEST_AIRFIELD_X,
            z=TEST_AIRFIELD_Z,
            planes=PLANES.default,
            supplies=1000)
        # Act
        result = selector.calc_power(airfield)
        # Assert
        # ресурсы + количество самолетов по-умолчанию
        self.assertEqual(result, 1000 + len(PLANES.default) * 150)

    def test_select_rear_east(self):
        """Выбираются тыловые аэродромы для красных"""
        selector = generation.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = generation.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = generation.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = generation.BoundaryBuilder(north=north, east=east, south=0, west=0)
        exclude = boundary_builder.confrontation_east(grid=grid)
        include = boundary_builder.influence_east(border=grid.border)
        airfields = self.controller.get_airfields(MOSCOW)
        airfield1, airfield2, airfield3 = (x for x in airfields if x.name in ('klin', 'kubinka', 'ruza'))
        airfield1.planes[TEST_AIRCRAFT_KEY] += 10
        airfield2.planes[TEST_AIRCRAFT_KEY] += 15
        airfield3.planes[TEST_AIRCRAFT_KEY] += 20
        # Act
        result = selector.select_rear(influence=include, front_area=exclude, airfields=airfields)
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_rear_west(self):
        """Выбираются тыловые аэродромы для синих"""
        selector = generation.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = generation.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = generation.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = generation.BoundaryBuilder(north=north, east=east, south=0, west=0)
        exclude = boundary_builder.confrontation_west(grid=grid)
        include = boundary_builder.influence_west(border=grid.border)
        airfields = self.controller.get_airfields(MOSCOW)
        airfield1, airfield2, airfield3 = (x for x in airfields if x.name in ('rjev', 'sychevka', 'karpovo'))
        airfield1.planes[TEST_AIRCRAFT_KEY] += 10
        airfield2.planes[TEST_AIRCRAFT_KEY] += 15
        airfield3.planes[TEST_AIRCRAFT_KEY] += 20
        # Act
        result = selector.select_rear(influence=include, front_area=exclude, airfields=airfields)
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_front_east(self):
        """Выбираются фронтовые аэродромы для красных"""
        selector = generation.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = generation.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = generation.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = generation.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_east(grid=grid)
        airfields = self.controller.get_airfields(MOSCOW)
        airfield1, airfield2 = (x for x in airfields if x.name in ('kholm', 'kalinin'))
        airfield1.planes[TEST_AIRCRAFT_KEY] += 10
        airfield2.supplies -= 40
        # Act
        result = selector.select_front(front_area=include, airfields=airfields)
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)

    def test_select_front_west(self):
        """Выбираются фронтовые аэродромы для синих"""
        selector = generation.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = generation.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = generation.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = generation.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_west(grid=grid)
        airfields = self.controller.get_airfields(MOSCOW)
        airfield1, airfield2 = (x for x in airfields if x.name in ('lotoshino', 'migalovo'))
        airfield1.planes[TEST_AIRCRAFT_KEY] += 10
        airfield2.supplies -= 40
        # Act
        result = selector.select_front(front_area=include, airfields=airfields)
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
