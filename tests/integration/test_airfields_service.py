"""Тестирование управления аэродромами"""
from pathlib import Path
import unittest

from configs import Objects
from core import EventsEmitter, \
    Atype9, \
    Atype10, \
    Atype16
from storage import Storage
from services import ObjectsService, \
    AirfieldsService, \
    AircraftVendorService, \
    GraphService, \
    WarehouseService, \
    TvdService

from log_objects import Aircraft, BotPilot

from tests.mocks import ConfigMock, \
    EventsInterceptor, \
    TvdMock

CONFIG = ConfigMock()
OBJECTS = Objects()

TEST = 'test'
TEST_TVD_NAME = 'stalingrad'
MOSCOW = 'moscow'
TEST_TVD_DATE = '10.11.1941'
TEST_FIELDS = Path(r'./tests/data/csv/test_fields.csv')
TEST_AIRFIELD_NAME = 'Verbovka'
TEST_AIRFIELD_X = 112687
TEST_AIRFIELD_Z = 184308


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(CONFIG.mgen.xgml[tvd_name])


class TestAirfieldsService(unittest.TestCase):
    """Тестовый класс контроллера"""

    def setUp(self):
        """Настройка базы перед тестом"""
        self._storage: Storage = Storage(CONFIG.main)
        self._emitter: EventsEmitter = EventsEmitter()
        self._interceptor: EventsInterceptor = EventsInterceptor(self._emitter)
        self._objects_service: ObjectsService = ObjectsService(
            self._emitter, CONFIG, OBJECTS)
        self._vendor: AircraftVendorService = AircraftVendorService(CONFIG)
        self._graph_service: GraphService = GraphService(CONFIG)
        self._warehouses_service: WarehouseService = WarehouseService(
            self._emitter, CONFIG, self._storage)
        self._storage.airfields.update_airfields(
            AirfieldsService.initialize_managed_airfields(
                CONFIG.mgen.airfields_data[TEST_TVD_NAME]))
        self._storage.airfields.update_airfields(
            AirfieldsService.initialize_managed_airfields(
                CONFIG.mgen.airfields_data[MOSCOW]))

    def tearDown(self):
        """Удаление базы после теста"""
        self._storage.drop_database()

    def test_get_airfield_in_radius(self):
        """Определяется аэродром в радиусе от координат"""
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service,
            self._vendor
        )
        # Act
        result = controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_X, z=TEST_AIRFIELD_Z, radius=1000)
        # Assert
        self.assertEqual(result.name, 'Verbovka')

    def test_spawn_planes(self):
        """Уменьшается количество самолётов на аэродроме при появлении на нём"""
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service,
            self._vendor
        )
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        managed_airfield.planes[aircraft_key] = 10
        self._storage.airfields.update_airfield(managed_airfield)
        expected = self._storage.airfields.load_by_id(
            managed_airfield.id).planes[aircraft_key] - 1
        atype = Atype10(
            tik=150, aircraft_id=2, bot_id=3, account_id='123', profile_id='123', name='nickname',
            pos={'x': TEST_AIRFIELD_X, 'z': TEST_AIRFIELD_Z}, aircraft_name=aircraft_name, country_id=101, coal_id=1,
            airfield_id=4, airstart=False, parent_id=5, is_player=True, is_tracking_stat=True, fuel=1, skin='',
            weapon_mods_id=[1], cartridges=1, shells=1, bombs=0, rockets=0, form='', payload_id=1
        )
        # Act
        controller.spawn_aircraft(TEST_TVD_NAME, 101, atype)
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], expected)
        airfield = self._storage.airfields.load_by_id(managed_airfield.id)
        self.assertEqual(airfield.planes[aircraft_key], expected)

    def test_return_planes(self):
        """Восполняется количество самолётов на аэродроме при возврате на него (деспаун)"""
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service,
            self._vendor
        )
        bot_name = 'BotPilot_Pe2'
        aircraft_name = 'Pe-2 ser.35'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        managed_airfield.planes[aircraft_key] = 10
        expected = managed_airfield.planes[aircraft_key] + 1
        self._storage.airfields.update_airfield(managed_airfield)
        aircraft = Aircraft(
            1, OBJECTS[aircraft_name], 101, 1, aircraft_name, pos={'x': managed_airfield.x, 'z': managed_airfield.z})
        bot = BotPilot(
            2, OBJECTS[bot_name], aircraft, 101, 1, bot_name, pos={'x': managed_airfield.x, 'z': managed_airfield.z})
        # Act
        # TEST_TVD_NAME, 101, bot
        controller._finish(Atype16(222, bot.obj_id, bot.pos))
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertEqual(managed_airfield.planes[aircraft_key], expected)

    def test_get_country(self):
        """Определяется страна аэродрома по узлу графа"""
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service,
            self._vendor
        )
        builder = TvdService(TEST_TVD_NAME, CONFIG, self._storage,
                             self._graph_service, self._warehouses_service)
        tvd = builder.get_tvd(TEST_TVD_DATE)
        self._graph_service.get_file = _get_xgml_file_mock
        verbovka = controller.get_airfield_in_radius(
            tvd_name=TEST_TVD_NAME, x=TEST_AIRFIELD_X, z=TEST_AIRFIELD_Z, radius=10)
        # Act
        result = tvd.get_country(verbovka)
        # Assert
        self.assertEqual(201, result)

    def test_add_aircraft(self):
        """Добавляется самолёт на аэродром"""
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service,
            self._vendor
        )
        self._graph_service.get_file = _get_xgml_file_mock
        aircraft_name = 'bf 109 f-4'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        managed_airfield.planes[aircraft_key] = 10
        self._storage.airfields.update_airfield(managed_airfield)
        expected = managed_airfield.planes[aircraft_key] + 5
        # Act
        controller.add_aircraft(
            TEST_TVD_NAME, 201, TEST_AIRFIELD_NAME, aircraft_name, 5)
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertEqual(expected, managed_airfield.planes[aircraft_key])

    def test_add_aircraft_wrong(self):
        """НЕ добавляется самолёт на аэродром другой страны"""
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service,
            self._vendor
        )
        self._graph_service.get_file = _get_xgml_file_mock
        aircraft_name = 'lagg-3 ser.29'
        aircraft_key = CONFIG.planes.name_to_key(aircraft_name)
        # Act
        controller.add_aircraft(
            TEST_TVD_NAME, 201, TEST_AIRFIELD_NAME, aircraft_name, 5)
        # Assert
        managed_airfield = self._storage.airfields.load_by_name(
            TEST_TVD_NAME, TEST_AIRFIELD_NAME)
        self.assertNotIn(aircraft_key, managed_airfield.planes)

    def test_airfield_atype(self):
        """Обрабатывается появление аэродрома в логе"""
        controller = AirfieldsService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service,
            self._vendor
        )
        self._emitter.current_tvd.on_next(TvdMock(MOSCOW))
        self._graph_service.get_file = _get_xgml_file_mock
        # Act
        controller.spawn_airfield(Atype9(
            10, 1, 201, 2, list(), {'x': 154415, 'z': 104560}))
        # Assert
        self.assertGreater(len(controller.current_airfields), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
