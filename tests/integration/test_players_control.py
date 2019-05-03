"""Тестирование событий, связанных с игроками"""
# pylint:disable=R0914,R0913
import datetime
import logging
from pathlib import Path
import unittest

from core import EventsEmitter, \
    Atype2, \
    Atype3, \
    Atype5, \
    Atype6, \
    Atype10, \
    Atype16
from configs import Objects
from storage import Storage
from services import ObjectsService, \
    PlayersService
import constants
from model import Player, PlayerBanP15M, MessagePrivate
from tests.mocks import ConfigMock, EventsInterceptor, atype_12_stub

CONFIG = ConfigMock()
OBJECTS = Objects()

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

TEST_NICKNAME = '_test_nickname'
TEST_ACCOUNT_ID = '_test_id1'
TEST_PROFILE_ID = '_test_profile_id1'
TEST_PLAYER = Player.initialize(TEST_ACCOUNT_ID)
FILTER = {constants.ID: TEST_ACCOUNT_ID}


def _create(storage: Storage, _filter: dict, _player: dict):
    storage.players.collection.update_one(
        _filter, {'$set': _player}, upsert=True)


def _atype_10_stub(aircraft_id: int, bot_id: int, pos: dict, aircraft_name: str,
                   country: int, parent_id: int, nickname=TEST_NICKNAME) -> Atype10:
    """Заглушка события появления игрока"""
    return Atype10(
        123, aircraft_id, bot_id, TEST_ACCOUNT_ID, TEST_PROFILE_ID, nickname, pos, aircraft_name, country,
        int(country/100), 1234, False, parent_id, True, True, 0, 1, '', [1, 5], 200, 100, 4, 8, '')


class TestPlayersController(unittest.TestCase):
    """Тесты событий с обработкой данных игроков"""

    def setUp(self):
        self._storage: Storage = Storage(CONFIG)
        self._emitter: EventsEmitter = EventsEmitter()
        self._objects_service: ObjectsService = ObjectsService(
            self._emitter, CONFIG, OBJECTS)
        self._interceptor: EventsInterceptor = EventsInterceptor(self._emitter)
        TEST_PLAYER[constants.Player.UNLOCKS] = 1
        if constants.Player.NICKNAME in TEST_PLAYER:
            del TEST_PLAYER[constants.Player.NICKNAME]

    def tearDown(self):
        self._storage.drop_database()

    def test_connect_player_init(self):
        """Инициализируется игрок на первом входе на сервер"""
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        # Act
        controller._connect(TEST_ACCOUNT_ID)
        document = self._storage.players.collection.find_one(FILTER)
        # Assert
        self.assertNotEqual(None, document)

    def test_connect_player_check_ban(self):
        """Отправляется команда бана заблокированного пользователя через консоль"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self._storage.players.collection.update_one(
            FILTER, update={'$set': {constants.Player.BAN_DATE: date}})
        # Act
        controller._connect(TEST_ACCOUNT_ID)
        # Assert
        self.assertTrue(self._interceptor.commands)
        command: PlayerBanP15M = self._interceptor.commands[0]
        self.assertEqual(TEST_ACCOUNT_ID, command.account_id)

    def test_player_initialization(self):
        """Обновляется ник игрока на появлении"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        self._objects_service._create_object(atype12_aircraft)
        self._objects_service._create_object(atype12_bot)
        self._objects_service._spawn(atype10)
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        # Assert
        player = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(TEST_NICKNAME, player[constants.Player.NICKNAME])

    def test_connect_player(self):
        """Отправляется приветственное сообщение игроку на подключении"""
        TEST_PLAYER[constants.Player.NICKNAME] = TEST_NICKNAME
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        self._objects_service._create_object(atype12_aircraft)
        self._objects_service._create_object(atype12_bot)
        self._objects_service._spawn(atype10)
        # Act
        controller._start_mission(None)
        controller._connect(TEST_ACCOUNT_ID)
        # Assert
        self.assertTrue(self._interceptor.commands)
        command: MessagePrivate = self._interceptor.commands[0]
        self.assertIn(
            (TEST_ACCOUNT_ID, 'Hello {}!'.format(TEST_NICKNAME)),
            (command.account_id, command.message))

    def test_multiple_spawn_nickname(self):
        """Не добавляется лишний известный ник при неоднократном появлении"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        self._objects_service._create_object(atype12_aircraft)
        self._objects_service._create_object(atype12_bot)
        self._objects_service._spawn(atype10)
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        controller._spawn(atype10)
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual([], document[constants.Player.KNOWN_NICKNAMES])

    def test_multiple_spawn_new_nick(self):
        """Пополняются известные ники при появлении с новым ником"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        self._objects_service._create_object(atype12_aircraft)
        self._objects_service._create_object(atype12_bot)
        self._objects_service._spawn(atype10)
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        atype10.name = 'new_nickname'
        controller._spawn(atype10)
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(
            [TEST_NICKNAME], document[constants.Player.KNOWN_NICKNAMES])

    def test_disconnect_player(self):
        """Ставится статус offline при выходе игрока с сервера"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        # Act
        controller._disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(False, document[constants.Player.ONLINE])

    def test_give_unlock_for_damage(self):
        """Даётся модификация за вылет с уроном"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(
            3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = self._objects_service._create_object(atype12_aircraft)
        bot = self._objects_service._create_object(atype12_bot)
        target = self._objects_service._create_object(atype12_static)
        self._objects_service._spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        damage = 80.0
        expect = TEST_PLAYER[constants.Player.UNLOCKS] + 1
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        self._objects_service._damage(
            Atype2(8999, damage, aircraft.obj_id, target.obj_id, pos))
        controller._finish(Atype16(9222, bot.obj_id, pos))
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_give_unlock_for_kill(self):
        """Даётся модификация за вылет с килом"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(
            3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = self._objects_service._create_object(atype12_aircraft)
        bot = self._objects_service._create_object(atype12_bot)
        target = self._objects_service._create_object(atype12_static)
        self._objects_service._spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS] + 1
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        self._objects_service._kill(
            Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller._finish(Atype16(9222, bot.obj_id, pos))
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_do_not_give_for_disco(self):
        """Не даётся модификация за вылет с килом и диско"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(
            3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = self._objects_service._create_object(atype12_aircraft)
        bot = self._objects_service._create_object(atype12_bot)
        target = self._objects_service._create_object(atype12_static)
        self._objects_service._spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS]
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        self._objects_service._takeoff(Atype5(3333, aircraft.obj_id, pos))
        self._objects_service._kill(
            Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller._finish(Atype16(9222, bot.obj_id, pos))
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_do_not_give_for_friendly(self):
        """Не даётся модификация за вылет со стрельбой по своим"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(
            3, target_name, 201, 'test_target', -1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = self._objects_service._create_object(atype12_aircraft)
        bot = self._objects_service._create_object(atype12_bot)
        target = self._objects_service._create_object(atype12_static)
        self._objects_service._spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS]
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        self._objects_service._kill(
            Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller._finish(Atype16(9222, bot.obj_id, pos))
        controller._disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_do_not_give_for_dead_end(self):
        """Не даётся модификация за вылет с убийством и смертью"""
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype12_static = atype_12_stub(
            3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = self._objects_service._create_object(atype12_aircraft)
        bot = self._objects_service._create_object(atype12_bot)
        target = self._objects_service._create_object(atype12_static)
        self._objects_service._spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS]
        # Act
        controller._start_mission(None)
        controller._spawn(atype10)
        self._objects_service._takeoff(Atype5(3333, aircraft.obj_id, pos))
        self._objects_service._kill(
            Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        self._objects_service._kill(
            Atype3(8777, aircraft.obj_id, bot.obj_id, pos))
        self._objects_service._land(Atype6(9911, aircraft.obj_id, pos))
        controller._finish(Atype16(9222, bot.obj_id, pos))
        # Assert
        document = self._storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    @unittest.skip('not implemented')
    def test_do_not_give_for_bailout(self):
        """Не даётся модификация за вылет с убийством и прыжком"""
        self.fail('not implemented')

    def test_msg_restricted_takeoff(self):
        """Отправляется предупреждение о запрете взлёта"""
        TEST_PLAYER[constants.Player.UNLOCKS] = 0
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = self._objects_service._create_object(atype12_aircraft)
        self._objects_service._create_object(atype12_bot)
        atype5 = Atype5(2132, aircraft.obj_id, pos)
        # Act
        controller._start_mission(None)
        self._objects_service._spawn(atype10)
        controller._spawn(atype10)
        self._objects_service._takeoff(atype5)
        controller._takeoff(atype5)
        # Assert
        self.assertTrue(self._interceptor.commands)

    def test_kick_restricted_takeoff(self):
        """Отправляется команда кика при запрещённом взлёте"""
        TEST_PLAYER[constants.Player.UNLOCKS] = 0
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = atype_12_stub(
            1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = atype_12_stub(
            2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(
            1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = self._objects_service._create_object(atype12_aircraft)
        self._objects_service._create_object(atype12_bot)
        atype5 = Atype5(2132, aircraft.obj_id, pos)
        # Act
        controller._start_mission(None)
        self._objects_service._spawn(atype10)
        controller._spawn(atype10)
        self._objects_service._takeoff(atype5)
        controller._takeoff(atype5)
        # Assert
        # приветствие + предупреждение
        self.assertTrue(self._interceptor.commands)
        welcome: MessagePrivate = self._interceptor.commands[0]
        warning: MessagePrivate = self._interceptor.commands[1]
        self.assertEqual(TEST_ACCOUNT_ID, welcome.account_id)
        self.assertEqual(TEST_ACCOUNT_ID, warning.account_id)

    def test_reset(self):
        """Сбрасывается состояние игроков в кампании"""
        TEST_PLAYER[constants.Player.UNLOCKS] = 4
        _create(self._storage, FILTER, TEST_PLAYER)
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        # Act
        controller.reset()
        # Assert
        self.assertEqual(self._storage.players.find(
            TEST_ACCOUNT_ID).unlocks, CONFIG.gameplay.unlocks_start)


if __name__ == '__main__':
    unittest.main(verbosity=2)
