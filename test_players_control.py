"Тестирование событий, связанных с игроками"
import unittest
import datetime
import pathlib
import pymongo
from processing import PlayersController, Player
from processing.player import ID, NICKNAME, KNOWN_NICKNAMES
from processing.objects import Aircraft, BotPilot
from configs.objects import Objects
from tests import mocks
from tests import ConsoleMock

MAIN = mocks.MainMock(pathlib.Path(r'.\testdata\conf.ini'))
DB_NAME = 'test_rexpert'
TEST_NICKNAME = '_test_nickname'
TEST_ACCOUNT_ID = '_test_id1'
TEST_PROFILE_ID = '_test_profile_id1'
FILTER = {ID: TEST_ACCOUNT_ID}

class TestPlayersController(unittest.TestCase):
    "Тесты событий с обработкой данных игроков"
    def setUp(self):
        self.mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
        rexpert = self.mongo[DB_NAME]
        self.players = rexpert['Players']
        self.squads = rexpert['Squads']
        self.console_mock = ConsoleMock()
        self.controller = PlayersController(False, self.console_mock, self.players, self.squads)
        self.objects = Objects()
        self._player = Player.create_document(TEST_ACCOUNT_ID)

    def tearDown(self):
        self.console_mock.socket.close()
        self.mongo.drop_database(DB_NAME)
        self.mongo.close()

    def test_player_initialization(self):
        "Обновляется ник игрока на спауне"
        # Arrange
        self.players.update_one(FILTER, {'$set': self._player}, upsert=True)
        aircraft = Aircraft(1, self.objects['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, self.objects['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(aircraft, bot, TEST_ACCOUNT_ID, None, TEST_NICKNAME, None,
                                     None, None, None, None, None, None, None, None, None, None,
                                     None, None, None, None, None)
        # Assert
        player = self.players.find_one(FILTER)
        self.assertEqual(TEST_NICKNAME, player[NICKNAME])

    def test_spawn_player(self):
        "Отправляется приветственное сообщение игроку на спауне"
        # Arrange
        self.players.update_one(FILTER, {'$set': self._player}, upsert=True)
        aircraft = Aircraft(1, self.objects['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, self.objects['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(aircraft, bot, TEST_ACCOUNT_ID, None, TEST_NICKNAME, None,
                                     None, None, None, None, None, None, None, None, None, None,
                                     None, None, None, None, None)
        # Assert
        self.assertIn(
            (TEST_ACCOUNT_ID, 'Hello {}!'.format(TEST_NICKNAME)),
            self.console_mock.recieved_private_messages)

    def test_connect_player_init(self):
        "Инициализируется игрок на первом входе на сервер"
        # Act
        self.controller.connect_player(TEST_ACCOUNT_ID, TEST_PROFILE_ID)
        document = self.players.find_one(FILTER)
        # Assert
        self.assertNotEqual(None, document)

    def test_connect_player_check_ban(self):
        "Отправляется команда бана забаненого пользователя через консоль"
        # Arrange
        self.players.update_one(FILTER, {'$set': self._player}, upsert=True)
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.players.update_one(FILTER, update={'$set': {'ban_expire_date': date}})
        # Act
        self.controller.connect_player(TEST_ACCOUNT_ID, TEST_PROFILE_ID)
        # Assert
        self.assertIn(TEST_ACCOUNT_ID, self.console_mock.banned)

    def test_multiple_spawn_nickname(self):
        "Неоднократный спаун не добавляет лишний ник в массив известных ников"
        # Arrange
        self.players.update_one(FILTER, {'$set': self._player}, upsert=True)
        aircraft = Aircraft(1, self.objects['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, self.objects['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(aircraft, bot, TEST_ACCOUNT_ID, TEST_PROFILE_ID,
                                     TEST_NICKNAME, None, None, 201, 2, None, None, None, 0, 1,
                                     None, [], 0, 0, 0, 0, None)
        self.controller.spawn_player(aircraft, bot, TEST_ACCOUNT_ID, TEST_PROFILE_ID,
                                     TEST_NICKNAME, None, None, 201, 2, None, None, None, 0, 1,
                                     None, [], 0, 0, 0, 0, None)
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual([], document[KNOWN_NICKNAMES])

    def test_multiple_spawn_new_nick(self):
        "Пополняются известные ники при спауне с новым ником"
        # Arrange
        self.players.update_one(FILTER, {'$set': self._player}, upsert=True)
        aircraft = Aircraft(1, self.objects['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, self.objects['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(aircraft, bot, TEST_ACCOUNT_ID, TEST_PROFILE_ID,
                                     TEST_NICKNAME, None, None, 201, 2, None, None, None, 0, 1,
                                     None, [], 0, 0, 0, 0, None)
        self.controller.spawn_player(aircraft, bot, TEST_ACCOUNT_ID, TEST_PROFILE_ID,
                                     'new_nickname', None, None, 201, 2, None, None, None, 0, 1,
                                     None, [], 0, 0, 0, 0, None)
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual([TEST_NICKNAME], document[KNOWN_NICKNAMES])

    def test_disconnect_player(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
