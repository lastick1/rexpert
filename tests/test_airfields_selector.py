"""Тестирование выбора аэродромов на миссию"""
import unittest
import pathlib

import processing
import tests

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
IOC.config.main = tests.mocks.MainMock(pathlib.Path('./testdata/conf.ini'))
IOC.config.mgen = tests.mocks.MgenMock(IOC.config.main.game_folder)

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
    return str(IOC.config.mgen.xgml[tvd_name])


class TestAirfieldsSelector(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.storage = processing.Storage(IOC.config.main)
        self.controller = processing.AirfieldsController(IOC)
        self.storage.airfields.update_airfields(
            self.controller.initialize_managed_airfields(IOC.config.mgen.airfields_data[MOSCOW]))

    def tearDown(self):
        self.storage.drop_database()

    def test_select_rear_east(self):
        """Выбираются тыловые аэродромы для красных"""
        tvd_builder = processing.TvdBuilder(MOSCOW, IOC)
        IOC.grid_controller.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = IOC.config.mgen.cfg[MOSCOW]['right_top']['x']
        east = IOC.config.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        grid = IOC.grid_controller.get_grid(MOSCOW)
        exclude = boundary_builder.confrontation_east(grid=grid)
        include = boundary_builder.influence_east(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('klin', 'kubinka', 'ruza'))
        self.controller.add_aircraft(tvd.name, 101, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self.controller.add_aircraft(tvd.name, 101, airfield2.name, TEST_AIRCRAFT_NAME1, 15)
        self.controller.add_aircraft(tvd.name, 101, airfield3.name, TEST_AIRCRAFT_NAME1, 20)
        selector = processing.AirfieldsSelector(IOC.config.main)
        # Act
        result = selector.select_rear(
            influence=include, front_area=exclude, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_rear_west(self):
        """Выбираются тыловые аэродромы для синих"""
        tvd_builder = processing.TvdBuilder(MOSCOW, IOC)
        IOC.grid_controller.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = IOC.config.mgen.cfg[MOSCOW]['right_top']['x']
        east = IOC.config.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        grid = IOC.grid_controller.get_grid(MOSCOW)
        exclude = boundary_builder.confrontation_west(grid=grid)
        include = boundary_builder.influence_west(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('rjev', 'sychevka', 'karpovo'))
        self.controller.add_aircraft(tvd.name, 201, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self.controller.add_aircraft(tvd.name, 201, airfield2.name, TEST_AIRCRAFT_NAME2, 15)
        self.controller.add_aircraft(tvd.name, 201, airfield3.name, TEST_AIRCRAFT_NAME2, 20)
        selector = processing.AirfieldsSelector(IOC.config.main)
        # Act
        result = selector.select_rear(
            influence=include, front_area=exclude, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_front_east(self):
        """Выбираются фронтовые аэродромы для красных"""
        tvd_builder = processing.TvdBuilder(MOSCOW, IOC)
        IOC.grid_controller.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = IOC.config.mgen.cfg[MOSCOW]['right_top']['x']
        east = IOC.config.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_east(grid=IOC.grid_controller.get_grid(MOSCOW))
        airfield1, airfield2 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW) if x.name in ('kholm', 'kalinin'))
        self.controller.add_aircraft(tvd.name, 101, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self.controller.add_aircraft(tvd.name, 101, airfield2.name, TEST_AIRCRAFT_NAME1, -10)
        selector = processing.AirfieldsSelector(IOC.config.main)
        # Act
        result = selector.select_front(front_area=include, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)

    def test_select_front_west(self):
        """Выбираются фронтовые аэродромы для синих"""
        tvd_builder = processing.TvdBuilder(MOSCOW, IOC)
        IOC.grid_controller.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = IOC.config.mgen.cfg[MOSCOW]['right_top']['x']
        east = IOC.config.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_west(grid=IOC.grid_controller.get_grid(MOSCOW))
        airfield1, airfield2 = (x for x in self.storage.airfields.load_by_tvd(MOSCOW) if
                                x.name in ('lotoshino', 'migalovo'))
        self.controller.add_aircraft(tvd.name, 201, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self.controller.add_aircraft(tvd.name, 201, airfield2.name, TEST_AIRCRAFT_NAME2, -10)
        selector = processing.AirfieldsSelector(IOC.config.main)
        # Act
        result = selector.select_front(front_area=include, airfields=self.storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
