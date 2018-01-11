"""Тестирование выбора аэродромов на миссию"""
import unittest
import pathlib

import processing
from tests import mocks

CONFIG = mocks.ConfigMock(pathlib.Path(r'./testdata/conf.ini'))
MOSCOW = 'moscow'
TEST_FIELDS = pathlib.Path(r'./data/moscow_fields.csv')
TEST_TVD_NAME = MOSCOW
TEST_AIRFIELD_NAME = 'kubinka'
TEST_AIRFIELD_X = 114768
TEST_AIRFIELD_Z = 192197
TEST_AIRCRAFT_NAME1 = 'Pe-2 ser.35'
TEST_AIRCRAFT_NAME2 = 'bf 109 f-4'


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(CONFIG.mgen.xgml[tvd_name])


class TestAirfieldsSelector(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.storage = processing.Storage(CONFIG.main)
        self.controller = processing.AirfieldsController(main=CONFIG.main, mgen=CONFIG.mgen, config=CONFIG.planes)
        self.storage.airfields.update_airfields(
            self.controller.initialize_managed_airfields(CONFIG.mgen.airfields_data[MOSCOW]))

    def tearDown(self):
        self.storage.drop_database()

    def test_select_rear_east(self):
        """Выбираются тыловые аэродромы для красных"""
        tvd_builder = processing.TvdBuilder(MOSCOW, CONFIG)
        tvd_builder.grid_control.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        grid = tvd_builder.grid_control.get_grid(MOSCOW)
        exclude = boundary_builder.confrontation_east(grid=grid)
        include = boundary_builder.influence_east(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('klin', 'kubinka', 'ruza'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME1, 15)
        self.controller.add_aircraft(tvd, airfield3.name, TEST_AIRCRAFT_NAME1, 20)
        selector = processing.AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_rear(
            influence=include, front_area=exclude, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_rear_west(self):
        """Выбираются тыловые аэродромы для синих"""
        tvd_builder = processing.TvdBuilder(MOSCOW, CONFIG)
        tvd_builder.grid_control.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        grid = tvd_builder.grid_control.get_grid(MOSCOW)
        exclude = boundary_builder.confrontation_west(grid=grid)
        include = boundary_builder.influence_west(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('rjev', 'sychevka', 'karpovo'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME2, 15)
        self.controller.add_aircraft(tvd, airfield3.name, TEST_AIRCRAFT_NAME2, 20)
        selector = processing.AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_rear(
            influence=include, front_area=exclude, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_front_east(self):
        """Выбираются фронтовые аэродромы для красных"""
        tvd_builder = processing.TvdBuilder(MOSCOW, CONFIG)
        tvd_builder.grid_control.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_east(grid=tvd_builder.grid_control.get_grid(MOSCOW))
        airfield1, airfield2 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW) if x.name in ('kholm', 'kalinin'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME1, -10)
        selector = processing.AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_front(front_area=include, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)

    def test_select_front_west(self):
        """Выбираются фронтовые аэродромы для синих"""
        tvd_builder = processing.TvdBuilder(MOSCOW, CONFIG)
        tvd_builder.grid_control.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_west(grid=tvd_builder.grid_control.get_grid(MOSCOW))
        airfield1, airfield2 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW) if
                                x.name in ('lotoshino', 'migalovo'))
        self.controller.add_aircraft(tvd, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self.controller.add_aircraft(tvd, airfield2.name, TEST_AIRCRAFT_NAME2, -10)
        selector = processing.AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_front(front_area=include, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
