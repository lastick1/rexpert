"""Тестирование управления аэродромами"""
from __future__ import annotations
from typing import List
from pathlib import Path
import unittest

from configs import Objects
from core import EventsEmitter, \
    Spawn, \
    Finish, \
    Atype9
from model import ManagedAirfield
from storage import Storage
from services import ObjectsService, \
    AirfieldsService, \
    AircraftVendorService, \
    GraphService, \
    WarehouseService, \
    TvdService

from log_objects import Aircraft

from tests.mocks import ConfigMock, \
    EventsInterceptor, \
    StorageMock, \
    ObjectsServiceMock, \
    TvdMock

CONFIG = ConfigMock()
OBJECTS = Objects()

TEST = 'test'
TEST_TVD_NAME = 'stalingrad'
MOSCOW = 'moscow'
TEST_TVD_DATE = '10.11.1941'
TEST_FIELDS = Path(r'./tests/data/csv/test_fields.csv')
TEST_AIRFIELD_1_NAME = 'Verbovka'
TEST_AIRFIELD_1_X = 112687
TEST_AIRFIELD_1_Z = 184308
TEST_AIRFIELD_2_NAME = 'Solodovka'
TEST_AIRFIELD_2_X = 131848
TEST_AIRFIELD_2_Z = 318121


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(CONFIG.mgen.xgml[tvd_name])


class TestAirfieldsService(unittest.TestCase):
    """Тестовый класс контроллера"""

    def setUp(self):
        """Настройка базы перед тестом"""
        self._storage: Storage = StorageMock(CONFIG.main)
        self._emitter: EventsEmitter = EventsEmitter()
        self._interceptor: EventsInterceptor = EventsInterceptor(self._emitter)
        self._objects_service: ObjectsService = ObjectsServiceMock(self._emitter, CONFIG, OBJECTS)
        self._vendor: AircraftVendorService = AircraftVendorService(CONFIG)
        self._graph_service: GraphService = GraphService(self._emitter, CONFIG)
        self._warehouses_service: WarehouseService = WarehouseService(self._emitter, CONFIG, self._storage)

        self._update_calls: List[ManagedAirfield] = []
        self._storage.airfields.load_by_tvd = self._load_by_tvd
        self._storage.airfields.load_by_name = self._load_by_name
        self._storage.airfields.load_by_id = self._load_by_id
        self._storage.airfields.update_airfield = self._update_calls.append

        self._test_airfield_1: ManagedAirfield = ManagedAirfield(
            TEST_AIRFIELD_1_NAME,
            TEST_TVD_NAME,
            TEST_AIRFIELD_1_X,
            TEST_AIRFIELD_1_Z,
            dict(),
        )
        self._test_airfield_2: ManagedAirfield = ManagedAirfield(
            TEST_AIRFIELD_2_NAME,
            TEST_TVD_NAME,
            TEST_AIRFIELD_2_X,
            TEST_AIRFIELD_2_Z,
            dict(),
        )

        self._aircraft_name = 'Pe-2 ser.35'
        self._aircraft = Aircraft(
            1,
            OBJECTS[self._aircraft_name],
            101,
            1,
            self._aircraft_name,
            pos={'x': self._test_airfield_1.x, 'z': self._test_airfield_1.z}
        )

    def _load_by_tvd(self, tvd_name: str) -> List[ManagedAirfield]:
        return [self._test_airfield_1, self._test_airfield_2]

    def _load_by_name(self, tvd_name: str, name: str) -> ManagedAirfield:
        return self._test_airfield_1

    def _load_by_id(self, id: str) -> ManagedAirfield:
        return self._test_airfield_1

    def _init_new_service_instance(self) -> AirfieldsService:
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._vendor
        )
        controller.init()
        return controller

    def test_get_airfield_in_radius(self):
        """Определяется аэродром в радиусе от координат"""
        controller = self._init_new_service_instance()
        # Act
        result = controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_1_X, z=TEST_AIRFIELD_1_Z, radius=1000)
        # Assert
        self.assertEqual(result.name, 'Verbovka')

    def test_spawn_planes(self):
        """Уменьшается количество самолётов на аэродроме при появлении на нём"""
        self._init_new_service_instance()
        aircraft_key = CONFIG.planes.name_to_key(self._aircraft_name)
        managed_airfield = self._storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_1_NAME)
        managed_airfield.planes[aircraft_key] = 10
        self._storage.airfields.update_airfield(managed_airfield)
        expected = self._test_airfield_1.planes[aircraft_key] - 1
        tvd_mock = TvdMock(TEST_TVD_NAME)
        tvd_mock.country = 101
        # Act
        self._emitter.current_tvd.on_next(tvd_mock)
        self._emitter.sortie_spawn.on_next(Spawn('account_id', 'nickname', 0, self._aircraft_name, managed_airfield))
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_1_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], expected)
        airfield = self._storage.airfields.load_by_id(managed_airfield.id)
        self.assertEqual(airfield.planes[aircraft_key], expected)

    def test_return_planes(self):
        """Восполняется количество самолётов на аэродроме при возврате на него (деспаун)"""
        self._init_new_service_instance()

        aircraft_key = CONFIG.planes.name_to_key(self._aircraft_name)
        managed_airfield = self._storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_1_NAME)
        managed_airfield.planes[aircraft_key] = 10
        expected = managed_airfield.planes[aircraft_key] + 1
        self._storage.airfields.update_airfield(managed_airfield)
        tvd_mock = TvdMock(TEST_TVD_NAME)
        tvd_mock.country = 101
        # Act
        self._emitter.current_tvd.on_next(tvd_mock)
        self._emitter.sortie_deinitialize.on_next(
            Finish('_test_account_id', True, True, self._aircraft_name, managed_airfield)
        )
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_1_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], expected)

    @unittest.skip("Тесты ТВД должны быть в своём тестовом классе, которого пока нет")
    def test_get_country(self):
        """Определяется страна аэродрома по узлу графа"""
        controller = self._init_new_service_instance()
        builder = TvdService(TEST_TVD_NAME, CONFIG, self._storage, self._graph_service, self._warehouses_service)
        tvd = builder.get_tvd(TEST_TVD_DATE)
        self._graph_service.get_file = _get_xgml_file_mock
        verbovka = controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_1_X, z=TEST_AIRFIELD_1_Z, radius=10)
        # Act
        result = tvd.get_country(verbovka)
        # Assert
        self.assertEqual(201, result)

    def test_add_aircraft(self):
        """Добавляется самолёт на аэродром"""
        controller = self._init_new_service_instance()
        self._graph_service.get_file = _get_xgml_file_mock
        aircraft_name = 'bf 109 f-4'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        managed_airfield = self._storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_1_NAME)
        managed_airfield.planes[aircraft_key] = 10
        self._storage.airfields.update_airfield(managed_airfield)
        expected = managed_airfield.planes[aircraft_key] + 5
        # Act
        controller.add_aircraft(TEST_TVD_NAME, 201, TEST_AIRFIELD_1_NAME, aircraft_name, 5)
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_1_NAME)
        self.assertEqual(expected, managed_airfield.planes[aircraft_key])

    def test_add_aircraft_wrong(self):
        """НЕ добавляется самолёт на аэродром другой страны"""
        controller = self._init_new_service_instance()
        self._graph_service.get_file = _get_xgml_file_mock
        aircraft_name = 'lagg-3 ser.29'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        # Act
        controller.add_aircraft(TEST_TVD_NAME, 201, TEST_AIRFIELD_1_NAME, aircraft_name, 5)
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(TEST_TVD_NAME, TEST_AIRFIELD_1_NAME)
        self.assertNotIn(aircraft_key, managed_airfield.planes)

    def _make_atype9(self) -> Atype9:
        return Atype9(10, 1, 201, 2, list(), {'x': self._test_airfield_1.x, 'z': self._test_airfield_1.z})

    def test_airfield_atype(self):
        """Обрабатывается появление аэродрома в логе"""
        controller = self._init_new_service_instance()
        self._emitter.current_tvd.on_next(TvdMock(MOSCOW))
        self._graph_service.get_file = _get_xgml_file_mock
        # Act
        self._emitter.events_airfield.on_next(self._make_atype9())
        # Assert
        self.assertGreater(len(controller.current_airfields), 0)

    def test_emits_airfield_gain(self):
        """Возникает событие получения аэродрома при победе в миссии"""
        captures = []
        self._init_new_service_instance()
        self._emitter.gameplay_capture.subscribe_(captures.append)
        self._emitter.current_tvd.on_next(TvdMock(MOSCOW))
        self._emitter.events_airfield.on_next(self._make_atype9())
        # Act
        self._emitter.mission_victory.on_next(101)
        # Assert
        self.assertTrue(captures)


if __name__ == '__main__':
    unittest.main(verbosity=2)
