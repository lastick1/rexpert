"""Тестирование событий, связанных с игроками"""
# pylint:disable=R0914,R0913
import datetime
import logging
import unittest

from core import EventsEmitter, \
    Atype2, \
    Atype3, \
    Atype5, \
    Atype6, \
    Atype16, \
    Atype20, \
    Atype21, \
    Finish
from configs import Objects
from services import ObjectsService, \
    PlayersService
import constants
from model import Player, PlayerBanP15M, MessagePrivate
from tests.mocks import ConfigMock, \
    EventsInterceptor, \
    StorageMock, \
    PlayersMock, \
    atype_10_stub, \
    atype_12_stub, \
    TEST_NICKNAME, \
    TEST_ACCOUNT_ID, \
    TEST_PROFILE_ID

CONFIG = ConfigMock()
OBJECTS = Objects()

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)


class TestPlayersController(unittest.TestCase):
    """Тесты событий с обработкой данных игроков"""

    def setUp(self):
        self._storage: StorageMock = StorageMock(CONFIG.main)
        self._emitter: EventsEmitter = EventsEmitter()
        self._objects_service: ObjectsService = ObjectsService(self._emitter, CONFIG, OBJECTS)
        self._objects_service.init()
        self._interceptor: EventsInterceptor = EventsInterceptor(self._emitter)
        self._player_dict = Player.initialize(TEST_ACCOUNT_ID)
        self._player = Player(TEST_ACCOUNT_ID, self._player_dict)

        self.update_calls = []
        self.reset_mods_for_all_calls = []
        self.players_mock.update = self._update
        self.players_mock.find = self._find
        self.players_mock.reset_mods_for_all = self._reset_mods_for_all

    @property
    def players_mock(self) -> PlayersMock:
        "Мок коллекции игроков"
        return self._storage.players

    def _count_zero(self, account_id) -> 0:
        return 0

    def _update(self, player: Player) -> None:
        self.update_calls.append(player)

    def _find(self, account_id) -> Player:
        return Player(account_id, self._player_dict)

    def _reset_mods_for_all(self, unlocks: int) -> None:
        self.reset_mods_for_all_calls.append(unlocks)

    def test_connect_player(self):
        """Отправляется приветственное сообщение игроку на подключении"""
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        # Act
        self._emitter.events_player_connected.on_next(Atype20(150, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertTrue(self._interceptor.commands)
        command: MessagePrivate = self._interceptor.commands[0]
        self.assertTupleEqual((TEST_ACCOUNT_ID, 'Hello {}!'.format(TEST_NICKNAME)),
                              (command.account_id, command.message))

    def test_connect_player_check_ban(self):
        """Отправляется команда бана заблокированного пользователя через консоль"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self._player_dict[constants.Player.BAN_DATE] = date
        # Act
        self._emitter.events_player_connected.on_next(Atype20(150, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertTrue(self._interceptor.commands)
        command: PlayerBanP15M = self._interceptor.commands[0]
        self.assertEqual(TEST_ACCOUNT_ID, command.account_id)

    def test_connect_player_init(self):
        """Инициализируется игрок на первом входе на сервер"""
        self.players_mock.count = self._count_zero
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        # Act
        self._emitter.events_player_connected.on_next(Atype20(150, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertNotEqual(len(self.update_calls), 0)

    def test_disconnect_player(self):
        """Ставится статус offline при выходе игрока с сервера"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        # Act
        self._emitter.events_player_disconnected.on_next(Atype21(1500, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertEqual(False, self.update_calls[0].online)

    def test_do_not_give_for_disco(self):
        """Не даётся модификация за вылет с килом и диско"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        atype16 = Atype16(9222, atype12_bot.object_id, pos)
        expect = self._player_dict[constants.Player.UNLOCKS]
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_takeoff.on_next(Atype5(3333, atype12_aircraft.object_id, pos))
        self._emitter.events_kill.on_next(Atype3(7888, atype12_aircraft.object_id, atype12_static.object_id, pos))
        self._emitter.events_bot_deinitialization.on_next(atype16)
        self._emitter.player_finish.on_next(Finish(False, atype16))
        self._emitter.events_player_disconnected.on_next(Atype21(9999, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertEqual(self.update_calls[0].unlocks, expect)

    def test_do_not_give_for_friendly(self):
        """Не даётся модификация за вылет со стрельбой по своим"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(3, target_name, 201, 'test_target', -1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        atype16 = Atype16(9222, atype12_bot.object_id, pos)
        expect = self._player_dict[constants.Player.UNLOCKS]
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_kill.on_next(Atype3(7888, atype12_aircraft.object_id, atype12_static.object_id, pos))
        self._emitter.player_finish.on_next(Finish(True, atype16))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertEqual(self.update_calls[0].unlocks, expect)

    def test_do_not_give_for_dead_end(self):
        """Не даётся модификация за вылет с убийством и смертью"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        atype16 = Atype16(9222, atype12_bot.object_id, pos)
        atype5 = Atype5(3333, atype12_aircraft.object_id, pos)
        atype_kill_target_by_player = Atype3(7888, atype12_aircraft.object_id, atype12_static.object_id, pos)
        atype_kill_player = Atype3(8777, atype12_aircraft.object_id, atype12_bot.object_id, pos)
        atype6 = Atype6(9911, atype12_aircraft.object_id, pos)
        expect = self._player_dict[constants.Player.UNLOCKS]
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(atype5)
        self._emitter.events_kill.on_next(atype_kill_target_by_player)
        self._emitter.events_kill.on_next(atype_kill_player)
        self._emitter.events_landing.on_next(atype6)
        self._emitter.player_finish.on_next(Finish(False, atype16))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertEqual(self.update_calls[0].unlocks, expect)

    @unittest.skip('not implemented')
    def test_do_not_give_for_bailout(self):
        """Не даётся модификация за вылет с убийством и прыжком"""
        self.fail('not implemented')

    def test_give_unlock_for_damage(self):
        """Даётся модификация за вылет с уроном"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        damage = 80.0
        expect = self._player_dict[constants.Player.UNLOCKS] + 1
        atype16 = Atype16(9222, atype12_bot.object_id, pos)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_damage.on_next(
            Atype2(8999, damage, atype12_aircraft.object_id, atype12_static.object_id, pos))
        self._emitter.events_bot_deinitialization.on_next(atype16)
        self._emitter.player_finish.on_next(Finish(True, atype16))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertEqual(expect, self.update_calls[0].unlocks)

    def test_give_unlock_for_kill(self):
        """Даётся модификация за вылет с килом"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype16 = Atype16(9222, atype12_bot.object_id, pos)
        expect = self._player_dict[constants.Player.UNLOCKS] + 1
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_game_object.on_next(atype12_static)
        self._emitter.events_kill.on_next(Atype3(7888, atype12_aircraft.object_id, atype12_static.object_id, pos))
        self._emitter.player_finish.on_next(Finish(True, atype16))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertEqual(expect, self.update_calls[0].unlocks)

    def test_gunner_does_not_receive_message(self):
        """Стрелкам не выдаётся сообщение о разрешении/запрете взлёта"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'Pe-2 ser.35'
        bot_pilot_name = 'BotPilot'
        bot_gunner_name = 'BotGunner'
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_pilot_bot = atype_12_stub(2, bot_pilot_name, 201, 'test_bot_pilot', 1)
        atype12_gunner_bot = atype_12_stub(3, bot_gunner_name, 201, 'test_bot_gunner', 1)
        atype10 = atype_10_stub(1, 3, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_pilot_bot)
        self._emitter.events_game_object.on_next(atype12_gunner_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        # Assert
        self.assertFalse(self._interceptor.commands)

    def test_msg_restricted_takeoff(self):
        """Отправляется предупреждение о запрете взлёта"""
        self._player_dict[constants.Player.UNLOCKS] = 0
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = atype_10_stub(1, 2, pos, aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        # Assert
        self.assertTrue(self._interceptor.commands)
        self.assertEqual(
            self._interceptor.commands[0].message,
            f'{TEST_NICKNAME} TAKEOFF is FORBIDDEN FOR YOU on this aircraft. Available modifications 0')

    def test_kick_restricted_takeoff(self):
        """Отправляется команда кика при запрещённом взлёте"""
        self._player_dict[constants.Player.UNLOCKS] = 0
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        atype5 = Atype5(2132, atype12_aircraft.object_id, pos)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        self._emitter.events_takeoff.on_next(atype5)
        # Assert
        # приветствие + предупреждение
        self.assertTrue(self._interceptor.commands)
        welcome: MessagePrivate = self._interceptor.commands[0]
        warning: MessagePrivate = self._interceptor.commands[1]
        self.assertEqual(TEST_ACCOUNT_ID, welcome.account_id)
        self.assertEqual(TEST_ACCOUNT_ID, warning.account_id)

    def test_multiple_spawn_new_nick(self):
        """Пополняются известные ники при появлении с новым ником"""
        new_nickname = 'new_nickname'
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        atype10.name = new_nickname
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        # Assert
        self.assertListEqual(self.update_calls[0].previous_nicknames, [TEST_NICKNAME])

    def test_multiple_spawn_nickname(self):
        """Не добавляется лишний известный ник при неоднократном появлении"""
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        # Assert
        self.assertTrue(self.update_calls)
        self.assertFalse(self.update_calls[0].previous_nicknames)

    def test_player_initialization(self):
        """Обновляется ник игрока на появлении"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        # Act
        self._emitter.events_game_object.on_next(atype12_aircraft)
        self._emitter.events_game_object.on_next(atype12_bot)
        self._emitter.events_player_spawn.on_next(atype10)
        # Assert
        self.assertTrue(self.update_calls)

    def test_reset(self):
        """Сбрасывается состояние игроков в кампании"""
        self._player_dict[constants.Player.UNLOCKS] = 4
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        # Act
        controller.reset()
        # Assert
        self.assertTrue(self.reset_mods_for_all_calls)


if __name__ == '__main__':
    unittest.main(verbosity=2)
