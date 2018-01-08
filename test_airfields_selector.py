"""Тестирование выбора аэродромов на миссию"""
import unittest
import pathlib

import processing
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN.game_folder)
PLANES = mocks.PlanesMock()
MOSCOW = 'moscow'
TEST_FIELDS = pathlib.Path(r'./data/moscow_fields.csv')
TEST_TVD_NAME = MOSCOW
TEST_AIRFIELD_NAME = 'kubinka'
TEST_AIRFIELD_X = 114768
TEST_AIRFIELD_Z = 192197
TEST_AIRCRAFT_NAME1 = 'Pe-2 ser.35'
TEST_AIRCRAFT_NAME2 = 'bf 109 f-4'


class TestAirfieldsSelector(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.storage = processing.Storage(MAIN)
        self.controller = processing.AirfieldsController(main=MAIN, mgen=MGEN, config=PLANES)

    def tearDown(self):
        self.storage.drop_database()

    def test_select_rear_east(self):
        """Выбираются тыловые аэродромы для красных"""
        tvd_builder = processing.TvdBuilder(MOSCOW, MGEN, MAIN, mocks.ParamsMock(), PLANES)
        tvd = tvd_builder.get_tvd('11.11.1941')
        self.controller.initialize_airfields(tvd)
        selector = processing.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = processing.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = processing.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        exclude = boundary_builder.confrontation_east(grid=grid)
        include = boundary_builder.influence_east(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('klin', 'kubinka', 'ruza'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME1, 15)
        self.controller.add_aircraft(tvd, airfield3.name, TEST_AIRCRAFT_NAME1, 20)
        # Act
        result = selector.select_rear(
            influence=include, front_area=exclude, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_rear_west(self):
        """Выбираются тыловые аэродромы для синих"""
        tvd_builder = processing.TvdBuilder(MOSCOW, MGEN, MAIN, mocks.ParamsMock(), PLANES)
        tvd = tvd_builder.get_tvd('11.11.1941')
        self.controller.initialize_airfields(tvd)
        selector = processing.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = processing.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = processing.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        exclude = boundary_builder.confrontation_west(grid=grid)
        include = boundary_builder.influence_west(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('rjev', 'sychevka', 'karpovo'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME2, 15)
        self.controller.add_aircraft(tvd, airfield3.name, TEST_AIRCRAFT_NAME2, 20)
        # Act
        result = selector.select_rear(
            influence=include, front_area=exclude, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_front_east(self):
        """Выбираются фронтовые аэродромы для красных"""
        tvd_builder = processing.TvdBuilder(MOSCOW, MGEN, MAIN, mocks.ParamsMock(), PLANES)
        tvd = tvd_builder.get_tvd('11.11.1941')
        self.controller.initialize_airfields(tvd)
        selector = processing.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = processing.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = processing.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_east(grid=grid)
        airfield1, airfield2 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW) if x.name in ('kholm', 'kalinin'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME1, -10)
        # Act
        result = selector.select_front(front_area=include, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)

    def test_select_front_west(self):
        """Выбираются фронтовые аэродромы для синих"""
        tvd_builder = processing.TvdBuilder(MOSCOW, MGEN, MAIN, mocks.ParamsMock(), PLANES)
        tvd = tvd_builder.get_tvd('11.11.1941')
        self.controller.initialize_airfields(tvd)
        selector = processing.AirfieldsSelector(MAIN)
        north = MGEN.cfg[MOSCOW]['right_top']['x']
        east = MGEN.cfg[MOSCOW]['right_top']['z']
        xgml = processing.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = processing.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_west(grid=grid)
        airfield1, airfield2 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW) if x.name in ('lotoshino', 'migalovo'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME2, -10)
        # Act
        result = selector.select_front(front_area=include, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
