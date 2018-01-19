"""Тестирование событий, связанных с игроками"""
import unittest
import datetime
import pathlib

import atypes
import configs
import log_objects
import tests

import processing
from processing.player import ID, NICKNAME, KNOWN_NICKNAMES, ONLINE, BAN_DATE, UNLOCKS

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
MAIN = IOC.config.main
TEST_NICKNAME = '_test_nickname'
TEST_ACCOUNT_ID = '_test_id1'
TEST_PROFILE_ID = '_test_profile_id1'
TEST_PLAYER = processing.Player.initialize(TEST_ACCOUNT_ID)
FILTER = {ID: TEST_ACCOUNT_ID}
OBJECTS = configs.Objects()


def _create(_filter: dict, _player: dict):
    IOC.storage.players.collection.update_one(_filter, {'$set': _player}, upsert=True)


def _atype_10_stub(aircraft_id: int, bot_id: int, pos: dict, aircraft_name: str,
                   country: int, parent_id: int, nickname=TEST_NICKNAME) -> atypes.Atype10:
    """Заглушка события спауна игрока"""
    return atypes.Atype10(
        123, aircraft_id, bot_id, TEST_ACCOUNT_ID, TEST_PROFILE_ID, nickname, pos, aircraft_name, country,
        int(country/100), 1234, False, parent_id, 0, 1, '', [1, 5], 200, 100, 4, 8, '')


def _atype_12_stub(object_id: int, object_name: str, country: int, name: str, parent_id: int) -> atypes.Atype12:
    """Заглушка события инициализации объекта"""
    return atypes.Atype12(120, object_id, object_name, country, int(country/100), name, parent_id)


class TestPlayersController(unittest.TestCase):
    """Тесты событий с обработкой данных игроков"""
    def setUp(self):
        IOC.console_mock.received_private_messages.clear()

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
        IOC.storage.players.collection.update_one(FILTER, update={'$set': {BAN_DATE: date}})
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
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.spawn(atype10)
        # Assert
        player = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(TEST_NICKNAME, player[NICKNAME])

    def test_spawn_player(self):
        """Отправляется приветственное сообщение игроку на спауне"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.spawn(atype10)
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
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.spawn(atype10)
        controller.spawn(atype10)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual([], document[KNOWN_NICKNAMES])

    def test_multiple_spawn_new_nick(self):
        """Пополняются известные ники при спауне с новым ником"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        IOC.objects_controller.spawn(atype10)
        # Act
        controller.spawn(atype10)
        atype10.name = 'new_nickname'
        controller.spawn(atype10)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual([TEST_NICKNAME], document[KNOWN_NICKNAMES])

    def test_disconnect_player(self):
        """Ставится статус offline при дисконнекте игрока"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        # Act
        controller.disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(False, document[ONLINE])

    def test_give_unlock_for_damage(self):
        """Даётся модификация за вылет с уроном"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = _atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        bot = IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        target = IOC.objects_controller.create_object(atype12_static, OBJECTS[target_name])
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        damage = 80.0
        expect = TEST_PLAYER[UNLOCKS] + 1
        # Act
        controller.spawn(atype10)
        IOC.objects_controller.damage(atypes.Atype2(8999, damage, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_give_unlock_for_kill(self):
        """Даётся модификация за вылет с килом"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = _atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        bot = IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        target = IOC.objects_controller.create_object(atype12_static, OBJECTS[target_name])
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[UNLOCKS] + 1
        # Act
        controller.spawn(atype10)
        IOC.objects_controller.kill(atypes.Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_do_not_give_for_disco(self):
        """Не даётся модификация за вылет с килом и диско"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = _atype_12_stub(3, target_name, 101, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        bot = IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        target = IOC.objects_controller.create_object(atype12_static, OBJECTS[target_name])
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[UNLOCKS]
        # Act
        controller.spawn(atype10)
        IOC.objects_controller.takeoff(atypes.Atype5(3333, aircraft.obj_id, pos))
        IOC.objects_controller.kill(atypes.Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_do_not_give_for_friendly(self):
        """Не даётся модификация за вылет со стрельбой по своим"""
        _create(FILTER, TEST_PLAYER)
        controller = processing.PlayersController(IOC)
        aircraft_name = 'I-16 type 24'
        bot_name = 'BotPilot'
        target_name = 'static_il2'
        atype12_aircraft = _atype_12_stub(1, aircraft_name, 201, 'test_aircraft', -1)
        atype12_bot = _atype_12_stub(2, bot_name, 201, 'test_bot', 1)
        atype12_static = _atype_12_stub(3, target_name, 201, 'test_target', -1)
        atype10 = _atype_10_stub(1, 2, {'x': 100, 'z': 100}, aircraft_name, 201, 3)
        aircraft = IOC.objects_controller.create_object(atype12_aircraft, OBJECTS[aircraft_name])
        bot = IOC.objects_controller.create_object(atype12_bot, OBJECTS[bot_name])
        target = IOC.objects_controller.create_object(atype12_static, OBJECTS[target_name])
        IOC.objects_controller.spawn(atype10)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        expect = TEST_PLAYER[UNLOCKS]
        # Act
        controller.spawn(atype10)
        IOC.objects_controller.kill(atypes.Atype3(7888, aircraft.obj_id, target.obj_id, pos))
        controller.finish(atypes.Atype16(9222, bot.obj_id, pos))
        controller.disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = IOC.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_msg_restricted_takeoff(self):
        """Отправляется предупреждение о запрете взлёта"""
        self.assertGreater(len(IOC.console_mock.received_private_messages), 0)

    @unittest.skip("not implemented")
    def test_kick_restricted_takeoff(self):
        """Отправляется команда кика при запрещённом взлёте"""
        self.fail('not implemented')

    @unittest.skip("not implemented")
    def test_reset(self):
        """Сбрасывается состояние игроков в кампании"""
        self.fail()


if __name__ == '__main__':
    unittest.main(verbosity=2)
