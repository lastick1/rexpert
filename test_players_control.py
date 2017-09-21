"Тестирование событий, связанных с игроками"
import unittest
import datetime
from processing import PlayersController
from processing.player import UNLOCKS
from tests import ConsoleMock
import pymongo
# import rcon


class TestPlayersController(unittest.TestCase):
    "Тесты событий с обработкой данных игроков"
    def setUp(self):
        mongo = pymongo.MongoClient('localhost', 27017)
        rexpert = mongo['test_rexpert']
        self.players = rexpert['Players']
        self.squads = rexpert['Squads']
        self.console_mock = ConsoleMock()
        self.controller = PlayersController(True, self.console_mock, self.players, self.squads)

    def tearDown(self):
        self.console_mock.socket.close()

    def test_player_initialization(self):
        "Тест инициализации игрока на спауне"
        # Arrange
        account_id = '_test_id1'
        nickname = '_test_nickname'
        # Act
        self.controller.spawn_player(None, None, account_id, None, nickname, None, None, None,
                                     None, None, None, None, None, None, None, None, None, None,
                                     None, None, None)
        # Assert
        player = self.players.find_one(filter={'_id': account_id})
        self.assertEqual(1, player[UNLOCKS])

    def test_spawn_player(self):
        "Респаун игрока"
        # Arrange
        account_id = '_test_id1'
        nickname = '_test_nickname'
        # Act
        self.controller.spawn_player(None, None, account_id, None, nickname, None, None, None,
                                     None, None, None, None, None, None, None, None, None, None,
                                     None, None, None)
        # Assert
        self.assertEqual(0, self.console_mock.recieved_private_messages)

    def test_connect_player_check_ban(self):
        "Забаненого пользователя должно забанить через консоль"
        # Arrange
        account_id = '_test_id1'
        profile_id = '_test_profile_id1'
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.players.update_one(
            filter={'_id': account_id},
            update={'$set': {'ban_expire_date': date}})
        # Act
        self.controller.connect_player(account_id, profile_id)
        # Assert
        self.assertIn(account_id, self.console_mock.banned)

    def test_disconnect_player(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
