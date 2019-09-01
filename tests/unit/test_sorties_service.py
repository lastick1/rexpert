"""Тестирование событий по самолётовылетам"""
from __future__ import annotations
from typing import Tuple
import unittest
from core import EventsEmitter, Atype2, Atype3, Atype5, Atype6, Atype7, Atype12, Atype16, Atype18
from configs import Objects
from services import ObjectsService, SortiesService, AirfieldsService

from tests.mocks import ConfigMock, \
    EventsInterceptor, \
    AirfieldsServiceMock, \
    atype_10_stub, \
    atype_12_stub, \
    return_true, \
    return_false

CONFIG = ConfigMock()
OBJECTS = Objects()


class TestSortiesService(unittest.TestCase):
    """Тесты сервиса самолётовылетов"""

    def setUp(self):
        self._emitter: EventsEmitter = EventsEmitter()
        self._objects_service: ObjectsService = ObjectsService(self._emitter, CONFIG, OBJECTS)
        self._objects_service.init()
        self._airfields_service: AirfieldsService = AirfieldsServiceMock(CONFIG)
        self._interceptor: EventsInterceptor = EventsInterceptor(self._emitter)

        self._aircraft_name: str = 'I-16 type 24'
        self._pos: dict = {'x': 100.0, 'y': 100.0, 'z': 100.0}

    def _init_new_service_instance(self) -> SortiesService:
        sorties_service = SortiesService(
            self._emitter,
            self._objects_service,
            self._airfields_service,
        )
        sorties_service.init()
        return sorties_service

    def _make_atype12(self) -> Tuple[Atype12]:
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(1, self._aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        return (atype12_aircraft, atype12_bot)

    def test_emits_spawn_event(self):
        """Возникает событие появления самолёта с ботом"""
        self._init_new_service_instance()
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        # Assert
        self.assertTrue(self._interceptor.spawns)

    def test_emits_takeoff_event(self):
        """Возникает событие взлёта"""
        self._init_new_service_instance()
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(Atype5(200, atype12_aircraft.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.takeoffs)

    def test_emits_deinitialize_event(self):
        """Возникает событие деинициализации бота (завершения вылета)"""
        self._init_new_service_instance()
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_bot_deinitialization.on_next(Atype16(300, atype12_bot.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.deinitializations)

    def test_kill_in_sortie(self):
        """Учитываются килы в самолётовылете"""
        self._init_new_service_instance()
        self._airfields_service.is_on_airfield = return_true
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        atype12_static = atype_12_stub(3, 'static_il2', 101, 'test_target', -1)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(Atype5(130, atype12_aircraft.object_id, self._pos))
        self._emitter.events_kill.on_next(Atype3(150, atype12_aircraft.object_id, atype12_static.object_id, self._pos))
        self._emitter.events_landing.on_next(Atype6(280, atype12_aircraft.object_id, self._pos))
        self._emitter.events_bot_deinitialization.on_next(Atype16(300, atype12_bot.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.deinitializations)
        self.assertTrue(self._interceptor.deinitializations[0].gain_unlocks)

    def test_damage_in_sortie(self):
        """Учитывается урон в самолётовылете"""
        self._init_new_service_instance()
        self._airfields_service.is_on_airfield = return_true
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        atype12_static = atype_12_stub(3, 'static_il2', 101, 'test_target', -1)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(Atype5(130, atype12_aircraft.object_id, self._pos))
        self._emitter.events_damage.on_next(
            Atype2(150, 0.1, atype12_aircraft.object_id, atype12_static.object_id, self._pos)
        )
        self._emitter.events_landing.on_next(Atype6(280, atype12_aircraft.object_id, self._pos))
        self._emitter.events_bot_deinitialization.on_next(Atype16(300, atype12_bot.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.deinitializations)
        self.assertTrue(self._interceptor.deinitializations[0].gain_unlocks)

    def test_gunners_has_no_sortie(self):
        """Отсутствуют самолётовылеты у стрелков"""
        sorties_service = self._init_new_service_instance()
        aircraft_name = 'Pe-2 ser.35'
        bot_pilot_name = 'BotPilot'
        bot_gunner_name = 'BotGunner'
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_pilot_bot = atype_12_stub(2, bot_pilot_name, 201, 'test_bot_pilot', 1)
        atype12_gunner_bot = atype_12_stub(3, bot_gunner_name, 201, 'test_bot_gunner', 1)
        atype10_pilot = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        atype10_bot = atype_10_stub(1, 3, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_pilot_bot)
        self._emitter.events_game_object.on_next(atype12_gunner_bot)
        self._emitter.events_player_spawn.on_next(atype10_pilot)
        self._emitter.events_player_spawn.on_next(atype10_bot)
        # Assert
        sortie = sorties_service.get_sortie(atype12_aircraft.object_id)
        self.assertEqual(sortie.bot_id, atype12_pilot_bot.object_id)
        self.assertNotEqual(sortie.bot_id, atype12_gunner_bot.object_id)

    def test_sortie_with_bailout_is_not_success(self) -> None:
        """Считается провальным вылет с килом и прыжком"""
        self._init_new_service_instance()
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        atype12_static = atype_12_stub(3, 'static_il2', 201, 'test_target', -1)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(Atype5(130, atype12_aircraft.object_id, self._pos))
        self._emitter.events_kill.on_next(Atype3(150, atype12_aircraft.object_id, atype12_static.object_id, self._pos))
        self._emitter.events_kill.on_next(Atype2(160, 0.1, None, atype12_aircraft.object_id, self._pos))
        self._emitter.events_bot_eject_leave.on_next(
            Atype18(280, atype12_bot.object_id, atype12_aircraft.object_id, self._pos)
        )
        self._emitter.events_mission_end.on_next(Atype7(9999))
        self._emitter.events_bot_deinitialization.on_next(Atype16(300, atype12_bot.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.deinitializations)
        self.assertFalse(self._interceptor.deinitializations[0].gain_unlocks)

    def test_sortie_with_death_is_not_success(self):
        """Считается провальным вылет со смертью вне аэродрома"""
        self._init_new_service_instance()
        self._airfields_service.is_on_airfield = return_false
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        atype12_static = atype_12_stub(3, 'static_il2', 201, 'test_target', -1)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(Atype5(130, atype12_aircraft.object_id, self._pos))
        self._emitter.events_kill.on_next(Atype3(150, atype12_aircraft.object_id, atype12_static.object_id, self._pos))
        self._emitter.events_kill.on_next(Atype3(160, None, atype12_aircraft.object_id, self._pos))
        self._emitter.events_landing.on_next(Atype6(280, atype12_aircraft.object_id, self._pos))
        self._emitter.events_bot_deinitialization.on_next(Atype16(300, atype12_bot.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.deinitializations)
        self.assertFalse(self._interceptor.deinitializations[0].gain_unlocks)

    def test_sortie_with_disco_is_not_success(self):
        """Считается провальным вылет с килом и диско"""
        self._init_new_service_instance()
        self._airfields_service.is_on_airfield = return_false
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        atype12_static = atype_12_stub(3, 'static_il2', 101, 'test_target', -1)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(Atype5(130, atype12_aircraft.object_id, self._pos))
        self._emitter.events_kill.on_next(Atype3(150, atype12_aircraft.object_id, atype12_static.object_id, self._pos))
        self._emitter.events_bot_deinitialization.on_next(Atype16(300, atype12_bot.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.deinitializations)
        self.assertFalse(self._interceptor.deinitializations[0].gain_unlocks)

    def test_sortie_with_ff_is_not_success(self):
        """Считается провальным вылет с уроном по своим"""
        self._init_new_service_instance()
        self._airfields_service.is_on_airfield = return_true
        atype12_aircraft, atype12_bot = self._make_atype12()
        atype10 = atype_10_stub(1, 2, self._pos, self._aircraft_name, 201, 3)
        atype12_static = atype_12_stub(3, 'static_il2', 201, 'test_target', -1)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(Atype5(130, atype12_aircraft.object_id, self._pos))
        self._emitter.events_kill.on_next(Atype3(150, atype12_aircraft.object_id, atype12_static.object_id, self._pos))
        self._emitter.events_landing.on_next(Atype6(280, atype12_aircraft.object_id, self._pos))
        self._emitter.events_bot_deinitialization.on_next(Atype16(300, atype12_bot.object_id, self._pos))
        # Assert
        self.assertTrue(self._interceptor.deinitializations)
        self.assertFalse(self._interceptor.deinitializations[0].gain_unlocks)
