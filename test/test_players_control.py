from unittest import TestCase
from processing import PlayersController
import pymongo
import rcon


class TestPlayersController(TestCase):
    def test_spawn_player(self):
        mongo = pymongo.MongoClient('localhost', 27017)
        rexpert = mongo['rexpert']
        players = rexpert['Players']
        controller = PlayersController(rcon.Commander(None), players)
        account_id = '_test_id'
        nickname = '_test_nickname1'
        controller.spawn_player(None, None, account_id, None, nickname, None, None, None, None, None, None, None, None,
                                None, None, None, None, None, None, None, None)

    def test_connect_player(self):
        self.fail()

    def test_disconnect_player(self):
        self.fail()
