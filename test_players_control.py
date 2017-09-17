"Тестирование событий, связанных с игроками"
import unittest
from processing import PlayersController
import pymongo
# import rcon


class TestPlayersController(unittest.TestCase):
    "Тесты событий с обработкой данных игроков"
    def setUp(self):
        mongo = pymongo.MongoClient('localhost', 27017)
        rexpert = mongo['rexpert']
        self.players = rexpert['Players']
        self.squads = rexpert['Squads']

    def test_spawn_player(self):
        "Респаун игрока"
        controller = PlayersController(True, None, self.players, self.squads)
        account_id = '_test_id1'
        nickname = '_test_nickname'
        controller.spawn_player(None, None, account_id, None, nickname, None, None, None, None,
                                None, None, None, None, None, None, None, None, None, None, None,
                                None)

    def test_connect_player(self):
        pass

    def test_disconnect_player(self):
        pass
