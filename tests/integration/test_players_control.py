"""Тестирование событий, связанных с игроками"""
# pylint:disable=R0914,R0913
import datetime
import logging
import pathlib
import unittest

import atypes
import configs
import constants
import model
import processing
import tests

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
MAIN = IOC.config.main
TEST_NICKNAME = '_test_nickname'
TEST_ACCOUNT_ID = '_test_id1'
TEST_PROFILE_ID = '_test_profile_id1'
TEST_PLAYER = model.Player.initialize(TEST_ACCOUNT_ID)
FILTER = {constants.ID: TEST_ACCOUNT_ID}
OBJECTS = configs.Objects()


def _create(_filter: dict, _player: dict):
    IOC.storage.players.collection.update_one(_filter, {'$set': _player}, upsert=True)


def _atype_10_stub(aircraft_id: int, bot_id: int, pos: dict, aircraft_name: str,
                   country: int, parent_id: int, nickname=TEST_NICKNAME) -> atypes.Atype10:
    """Заглушка события спауна игрока"""
    return atypes.Atype10(
        123, aircraft_id, bot_id, TEST_ACCOUNT_ID, TEST_PROFILE_ID, nickname, pos, aircraft_name, country,
        int(country/100), 1234, False, parent_id, 0, 1, '', [1, 5], 200, 100, 4, 8, '')


class TestPlayersController(unittest.TestCase):
    """Тесты событий с обработкой данных игроков"""
    def setUp(self):
        TEST_PLAYER[constants.Player.UNLOCKS] = 1
        if constants.Player.NICKNAME in TEST_PLAYER:
            del TEST_PLAYER[constants.Player.NICKNAME]
        IOC.console_mock.received_private_messages.clear()
        IOC.console_mock.kicks.clear()

    def tearDown(self):
        IOC.storage.drop_database()

    def test_connect_player_init(self):
        """Инициализируется игрок на первом входе на сервер"""
        controller = processing.PlayersController(IOC)
        # Act
        controller.connect(TEST_ACCOUNT_ID)
        document = IOC.storage.players.collection.find_one(FILTER)
        # Assert
        self.assertNotEqual(None, document)

    def test_connect_player_check_ban(self):
        """Отправляется команда бана забаненого пользователя через консоль"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        IOC.storage.players.collection.update_one(FILTER, update={'$set': {constants.Player.BAN_DATE: date}})
        # Act
        controller.connect(TEST_ACCOUNT_ID)
        # Assert
        self.assertIn(TEST_ACCOUNT_ID, IOC.console_mock.banned)

    def test_player_initialization(self):
        """Обновляется ник игрока на спауне"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft)
        IOC.objects_controller.create_object(atype12_bot)
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        # Assert
        player = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(TEST_NICKNAME, player[constants.Player.NICKNAME])

    def test_connect_player(self):
        """Отправляется приветственное сообщение игроку на подключении"""
        TEST_PLAYER[constants.Player.NICKNAME] = TEST_NICKNAME
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft)
        IOC.objects_controller.create_object(atype12_bot)
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.start_mission()
        controller.connect(TEST_ACCOUNT_ID)
        # Assert
        self.assertIn(
            (TEST_ACCOUNT_ID, 'Hello {}!'.format(TEST_NICKNAME)),
            IOC.console_mock.received_private_messages)

    def test_multiple_spawn_nickname(self):
        """Не добавляетcя лишний известный ник при неоднократном спауне"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft)
        IOC.objects_controller.create_object(atype12_bot)
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        controller.spawn(atype10)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual([], document[constants.Player.KNOWN_NICKNAMES])

    def test_multiple_spawn_new_nick(self):
        """Пополняются известные ники при спауне с новым ником"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft)
        IOC.objects_controller.create_object(atype12_bot)
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        atype10.name = 'new_nickname'
        controller.spawn(atype10)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual([TEST_NICKNAME], document[constants.Player.KNOWN_NICKNAMES])

    def test_disconnect_player(self):
        """Ставится статус offline при дисконнекте игрока"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        # Act
        controller.disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(False, document[constants.Player.ONLINE])

    def test_give_unlock_for_damage(self):
        """Даётся модификация за вылет с уроном"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = tests.mocks.atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft)
        bot = IOC.objects_controller.create_object(atype12_bot)
        target = IOC.objects_controller.create_object(atype12_static)
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        damage = 80.0
        expect = TEST_PLAYER[constants.Player.UNLOCKS] + 1
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        IOC.objects_controller.damage(atypes.Atype2(8999, damage, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_give_unlock_for_kill(self):
        """Даётся модификация за вылет с килом"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = tests.mocks.atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft)
        bot = IOC.objects_controller.create_object(atype12_bot)
        target = IOC.objects_controller.create_object(atype12_static)
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS] + 1
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        IOC.objects_controller.kill(atypes.Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_do_not_give_for_disco(self):
        """Не даётся модификация за вылет с килом и диско"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = tests.mocks.atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft)
        bot = IOC.objects_controller.create_object(atype12_bot)
        target = IOC.objects_controller.create_object(atype12_static)
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS]
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        IOC.objects_controller.takeoff(atypes.Atype5(3333, aircraft.obj_id, pos))
        IOC.objects_controller.kill(atypes.Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_do_not_give_for_friendly(self):
        """Не даётся модификация за вылет со стрельбой по своим"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = tests.mocks.atype_12_stub(3, target_name, 201, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft)
        bot = IOC.objects_controller.create_object(atype12_bot)
        target = IOC.objects_controller.create_object(atype12_static)
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS]
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        IOC.objects_controller.kill(atypes.Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        controller.disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    def test_do_not_give_for_dead_end(self):
        """Не даётся модификация за вылет с киллом и смертью"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = tests.mocks.atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft)
        bot = IOC.objects_controller.create_object(atype12_bot)
        target = IOC.objects_controller.create_object(atype12_static)
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[constants.Player.UNLOCKS]
        # Act
        controller.start_mission()
        controller.spawn(atype10)
        IOC.objects_controller.takeoff(atypes.Atype5(3333, aircraft.obj_id, pos))
        IOC.objects_controller.kill(atypes.Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        IOC.objects_controller.kill(atypes.Atype3(8777, aircraft.obj_id, bot.obj_id, pos))
        IOC.objects_controller.land(atypes.Atype6(9911, aircraft.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[constants.Player.UNLOCKS])

    @unittest.skip('not implemented')
    def test_do_not_give_for_bailout(self):
        """Не даётся модификация за вылет с киллом и прыжком"""
        self.fail('not implemented')

    def test_msg_restricted_takeoff(self):
        """Отправляется предупреждение о запрете взлёта"""
        TEST_PLAYER[constants.Player.UNLOCKS] = 0
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft)
        IOC.objects_controller.create_object(atype12_bot)
        atype5 = atypes.Atype5(2132, aircraft.obj_id, pos)
        # Act
        controller.start_mission()
        IOC.objects_controller.spawn(atype10)
        controller.spawn(atype10)
        IOC.objects_controller.takeoff(atype5)
        controller.takeoff(atype5)
        # Assert
        self.assertGreater(len(IOC.console_mock.received_private_messages), 0)

    def test_kick_restricted_takeoff(self):
        """Отправляется команда кика при запрещённом взлёте"""
        TEST_PLAYER[constants.Player.UNLOCKS] = 0
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        atype12_aircraft = tests.mocks.atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = tests.mocks.atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft)
        IOC.objects_controller.create_object(atype12_bot)
        atype5 = atypes.Atype5(2132, aircraft.obj_id, pos)
        # Act
        controller.start_mission()
        IOC.objects_controller.spawn(atype10)
        controller.spawn(atype10)
        IOC.objects_controller.takeoff(atype5)
        controller.takeoff(atype5)
        # Assert
        self.assertGreater(len(IOC.console_mock.kicks), 0)  # приветствие + предупреждение

    def test_reset(self):
        """Сбрасывается состояние игроков в кампании"""
        TEST_PLAYER[constants.Player.UNLOCKS] = 4
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        # Act
        controller.reset()
        # Assert
        self.assertEqual(IOC.storage.players.find(TEST_ACCOUNT_ID).unlocks, IOC.config.gameplay.unlocks_start)


if __name__ == '__main__':
    unittest.main(verbosity=2)
