"""Тестирование выбора аэродромов на миссию"""
from pathlib import Path
import unittest

from configs import Objects
from core import EventsEmitter
from storage import Storage
from services import ObjectsService, \
    AirfieldsService, \
    AircraftVendorService, \
    TvdService, \
    WarehouseService, \
    GraphService

from processing import AirfieldsSelector, \
    BoundaryBuilder

from tests.mocks import ConfigMock, \
    EventsInterceptor

CONFIG = ConfigMock()
OBJECTS = Objects()

MOSCOW = 'moscow'
TEST_FIELDS = Path(r'./data/moscow_fields.csv')
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
        self._storage = Storage(CONFIG.main)
        self._emitter: EventsEmitter = EventsEmitter()
        self._interceptor: EventsInterceptor = EventsInterceptor(self._emitter)
        self._objects_service: ObjectsService = ObjectsService(
            self._emitter, CONFIG, OBJECTS)
        self._vendor: AircraftVendorService = AircraftVendorService(CONFIG)
        self._airfields_service: AirfieldsService = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._vendor
        )
        self._graph_service: GraphService = GraphService(self._emitter, CONFIG)
        self._warehouses_service: WarehouseService = WarehouseService(
            self._emitter, CONFIG, self._storage)
        self._storage.airfields.update_airfields(
            self._airfields_service.initialize_managed_airfields(CONFIG.mgen.airfields_data[MOSCOW]))

    def tearDown(self):
        """Очистка базы после теста"""
        self._storage.drop_database()

    def test_select_rear_east(self):
        """Выбираются тыловые аэродромы для красных"""
        tvd_builder = TvdService(MOSCOW, CONFIG, self._storage,
                                 self._graph_service, self._warehouses_service)
        self._graph_service.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = BoundaryBuilder(
            north=north, east=east, south=0, west=0)
        grid = self._graph_service.get_grid(MOSCOW)
        exclude = boundary_builder.confrontation_east(grid=grid)
        include = boundary_builder.influence_east(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self._storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('klin', 'kubinka', 'ruza'))
        self._airfields_service.add_aircraft(
            tvd.name, 101, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self._airfields_service.add_aircraft(
            tvd.name, 101, airfield2.name, TEST_AIRCRAFT_NAME1, 15)
        self._airfields_service.add_aircraft(
            tvd.name, 101, airfield3.name, TEST_AIRCRAFT_NAME1, 20)
        selector = AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_rear(
            influence=include,
            front_area=exclude,
            airfields=self._storage.airfields.load_by_tvd(MOSCOW),
            warehouses=self._warehouses_service.next_warehouses(tvd))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_rear_west(self):
        """Выбираются тыловые аэродромы для синих"""
        tvd_builder = TvdService(MOSCOW, CONFIG, self._storage,
                                 self._graph_service, self._warehouses_service)
        self._graph_service.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = BoundaryBuilder(
            north=north, east=east, south=0, west=0)
        grid = self._graph_service.get_grid(MOSCOW)
        exclude = boundary_builder.confrontation_west(grid=grid)
        include = boundary_builder.influence_west(border=grid.border)
        airfield1, airfield2, airfield3 = (x for x in self._storage.airfields.load_by_tvd(MOSCOW)
                                           if x.name in ('rjev', 'sychevka', 'karpovo'))
        self._airfields_service.add_aircraft(
            tvd.name, 201, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self._airfields_service.add_aircraft(
            tvd.name, 201, airfield2.name, TEST_AIRCRAFT_NAME2, 15)
        self._airfields_service.add_aircraft(
            tvd.name, 201, airfield3.name, TEST_AIRCRAFT_NAME2, 20)
        selector = AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_rear(
            influence=include,
            front_area=exclude,
            airfields=self._storage.airfields.load_by_tvd(MOSCOW),
            warehouses=self._warehouses_service.next_warehouses(tvd))
        # Assert
        self.assertIn(result, [airfield1, airfield2, airfield3])

    def test_select_front_east(self):
        """Выбираются фронтовые аэродромы для красных"""
        tvd_builder = TvdService(MOSCOW, CONFIG, self._storage,
                                 self._graph_service, self._warehouses_service)
        self._graph_service.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = BoundaryBuilder(
            north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_east(
            grid=self._graph_service.get_grid(MOSCOW))
        airfield1, airfield2 = (x for x in self._storage.airfields.load_by_tvd(
            MOSCOW) if x.name in ('kholm', 'kalinin'))
        self._airfields_service.add_aircraft(
            tvd.name, 101, airfield1.name, TEST_AIRCRAFT_NAME1, 10)
        self._airfields_service.add_aircraft(
            tvd.name, 101, airfield2.name, TEST_AIRCRAFT_NAME1, -10)
        selector = AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_front(divisions=tvd.divisions,
                                       influence=tvd.influences[101][0].polygon,
                                       front_area=include,
                                       airfields=self._storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)

    def test_select_front_west(self):
        """Выбираются фронтовые аэродромы для синих"""
        tvd_builder = TvdService(MOSCOW, CONFIG, self._storage,
                                 self._graph_service, self._warehouses_service)
        self._graph_service.get_file = _get_xgml_file_mock
        tvd = tvd_builder.get_tvd('11.11.1941')
        north = CONFIG.mgen.cfg[MOSCOW]['right_top']['x']
        east = CONFIG.mgen.cfg[MOSCOW]['right_top']['z']
        boundary_builder = BoundaryBuilder(
            north=north, east=east, south=0, west=0)
        include = boundary_builder.confrontation_west(
            grid=self._graph_service.get_grid(MOSCOW))
        airfield1, airfield2 = (x for x in self._storage.airfields.load_by_tvd(MOSCOW) if
                                x.name in ('lotoshino', 'migalovo'))
        self._airfields_service.add_aircraft(
            tvd.name, 201, airfield1.name, TEST_AIRCRAFT_NAME2, 10)
        self._airfields_service.add_aircraft(
            tvd.name, 201, airfield2.name, TEST_AIRCRAFT_NAME2, -10)
        selector = AirfieldsSelector(CONFIG.main)
        # Act
        result = selector.select_front(divisions=tvd.divisions,
                                       influence=tvd.influences[101][0].polygon,
                                       front_area=include,
                                       airfields=self._storage.airfields.load_by_tvd(MOSCOW))
        # Assert
        self.assertEqual(3, len(result))
        self.assertIn(airfield1, result)
        self.assertIn(airfield2, result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
