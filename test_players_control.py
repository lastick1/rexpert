"Тестирование событий, связанных с игроками"
import unittest
import datetime
import pathlib
import pymongo
from processing import PlayersController, Player
from processing.player import ID, NICKNAME
from processing.objects import Aircraft, BotPilot
from configs.objects import Objects
from tests import mocks
from tests import ConsoleMock

MAIN = mocks.MainMock(pathlib.Path(r'.\testdata\conf.ini'))
DB_NAME = 'test_rexpert'

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
        self._account_id = '_test_id1'
        self._player = Player.create_document(self._account_id)

    def tearDown(self):
        self.console_mock.socket.close()
        # self.mongo.drop_database(DB_NAME)
        self.mongo.close()

    def test_player_initialization(self):
        "Обновляется ник игрока на спауне"
        # Arrange
        nickname = '_test_nickname'
        self.players.update_one({ID: self._account_id}, {'$set': self._player})
        aircraft = Aircraft(1, self.objects['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, self.objects['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(aircraft, bot, self._account_id, None, nickname, None, None,
                                     None, None, None, None, None, None, None, None, None, None,
                                     None, None, None, None)
        # Assert
        player = self.players.find_one(filter={'_id': self._account_id})
        self.assertEqual(nickname, player[NICKNAME])

    def test_spawn_player(self):
        "Отправляется сообщение игроку на спауне"
        # Arrange
        nickname = '_test_nickname'
        self.players.update_one({ID: self._account_id}, {'$set': self._player})
        aircraft = Aircraft(1, self.objects['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, self.objects['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(aircraft, bot, self._account_id, None, nickname, None, None,
                                     None, None, None, None, None, None, None, None, None, None,
                                     None, None, None, None)
        # Assert
        self.assertEqual(1, self.console_mock.recieved_private_messages)

    def test_connect_player_initialization(self):
        "Инициализируется игрок на первом входе на сервер"
        # Arrange
        profile_id = '_test_profile_id1'
        # Act
        self.controller.connect_player(self._account_id, profile_id)
        document = self.players.find_one({ID: self._account_id})
        # Assert
        self.assertNotEqual(None, document)

    def test_connect_player_check_ban(self):
        "Отправляется команда бана забаненого пользователя через консоль"
        # Arrange
        profile_id = '_test_profile_id1'
        self.players.update_one({ID: self._account_id}, {'$set': self._player})
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.players.update_one(
            filter={'_id': self._account_id},
            update={'$set': {'ban_expire_date': date}})
        # Act
        self.controller.connect_player(self._account_id, profile_id)
        # Assert
        self.assertIn(self._account_id, self.console_mock.banned)

    def test_disconnect_player(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
