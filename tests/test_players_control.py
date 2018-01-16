"""Тестирование событий, связанных с игроками"""
import unittest
import datetime
import pathlib

import configs
import log_objects

from processing import PlayersController, Player, Storage
from processing.player import ID, NICKNAME, KNOWN_NICKNAMES, ONLINE, BAN_DATE, UNLOCKS
from processing.player import PLANES
from tests import mocks

CONFIG = mocks.ConfigMock(pathlib.Path(r'./testdata/conf.ini'))
MAIN = CONFIG.main
TEST_NICKNAME = '_test_nickname'
TEST_ACCOUNT_ID = '_test_id1'
TEST_PROFILE_ID = '_test_profile_id1'
TEST_PLAYER = Player.initialize(TEST_ACCOUNT_ID)
FILTER = {ID: TEST_ACCOUNT_ID}
OBJECTS = configs.Objects()


class TestPlayersController(unittest.TestCase):
    """Тесты событий с обработкой данных игроков"""
    def setUp(self):

        self.console_mock = mocks.ConsoleMock()
        self.storage = Storage(MAIN)
        self.controller = PlayersController(MAIN, self.console_mock)

    def tearDown(self):
        self.console_mock.socket.close()
        self.storage.drop_database()

    def _create(self, _filter: dict, _player: dict):
        self.storage.players.collection.update_one(_filter, {'$set': _player}, upsert=True)

    def test_connect_player_init(self):
        """Инициализируется игрок на первом входе на сервер"""
        # Act
        self.controller.connect(TEST_ACCOUNT_ID)
        document = self.storage.players.collection.find_one(FILTER)
        # Assert
        self.assertNotEqual(None, document)

    def test_connect_player_check_ban(self):
        """Отправляется команда бана забаненого пользователя через консоль"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.storage.players.collection.update_one(FILTER, update={'$set': {BAN_DATE: date}})
        # Act
        self.controller.connect(TEST_ACCOUNT_ID)
        # Assert
        self.assertIn(TEST_ACCOUNT_ID, self.console_mock.banned)

    def test_player_initialization(self):
        """Обновляется ник игрока на спауне"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        # Assert
        player = self.storage.players.collection.find_one(FILTER)
        self.assertEqual(TEST_NICKNAME, player[NICKNAME])

    def test_spawn_player(self):
        """Отправляется приветственное сообщение игроку на спауне"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        # Assert
        self.assertIn(
            (TEST_ACCOUNT_ID, 'Hello {}!'.format(TEST_NICKNAME)),
            self.console_mock.received_private_messages)

    def test_multiple_spawn_nickname(self):
        """Не добавляетcя лишний известный ник при неоднократном спауне"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        # Assert
        document = self.storage.players.collection.find_one(FILTER)
        self.assertEqual([], document[KNOWN_NICKNAMES])

    def test_multiple_spawn_new_nick(self):
        """Пополняются известные ники при спауне с новым ником"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        self.controller.spawn(bot, TEST_ACCOUNT_ID, 'new_nickname')
        # Assert
        document = self.storage.players.collection.find_one(FILTER)
        self.assertEqual([TEST_NICKNAME], document[KNOWN_NICKNAMES])

    def test_disconnect_player(self):
        """Ставится статус offline при дисконнекте игрока"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        # Act
        self.controller.disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = self.storage.players.collection.find_one(FILTER)
        self.assertEqual(False, document[ONLINE])

    def test_give_unlock_for_damage(self):
        """Даётся модификация за вылет с уроном"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        damage = 80.0
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        target = log_objects.Ground(3, OBJECTS['static_il2'], 101, 1, 'Test target', pos)
        expect = TEST_PLAYER[UNLOCKS] + 1
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        aircraft.add_damage(target, damage)
        self.controller.finish(bot)
        # Assert
        document = self.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_give_unlock_for_kill(self):
        """Даётся модификация за вылет с килом"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        target = log_objects.Ground(3, OBJECTS['static_il2'], 101, 1, 'Test target', pos)
        expect = TEST_PLAYER[UNLOCKS] + 1
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        aircraft.add_kill(target)
        self.controller.finish(bot)
        # Assert
        document = self.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_do_not_give_for_disco(self):
        """Не даётся модификация за вылет с килом и диско"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        target = log_objects.Ground(3, OBJECTS['static_il2'], 101, 1, 'Test target', pos)
        expect = TEST_PLAYER[UNLOCKS]
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        aircraft.takeoff(pos)
        aircraft.add_kill(target)
        self.controller.finish(bot)
        # Assert
        document = self.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_do_not_give_for_friendly(self):
        """Не даётся модификация за вылет со стрельбой по своим"""
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        aircraft = log_objects.Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = log_objects.BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        target = log_objects.Ground(3, OBJECTS['static_il2'], 201, 2, 'Test target', pos)
        expect = TEST_PLAYER[UNLOCKS]
        # Act
        self.controller.spawn(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        aircraft.add_kill(target)
        self.controller.finish(bot)
        self.controller.disconnect(TEST_ACCOUNT_ID)
        # Assert
        document = self.storage.players.collection.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    @unittest.skip("not implemented")
    def test_msg_restricted_takeoff(self):
        """Отправляется предупреждение о запрете взлёта"""
        self.fail('not implemented')

    @unittest.skip("not implemented")
    def test_kick_restricted_takeoff(self):
        """Отправляется команда кика при запрещённом взлёте"""
        self.fail('not implemented')

    # TODO test_reset_players


if __name__ == '__main__':
    unittest.main(verbosity=2)