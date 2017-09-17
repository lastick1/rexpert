#pylint: disable=missing-docstring
import unittest
from processing import PlayersController
import pymongo
# import rcon


class TestPlayersController(unittest.TestCase):
    def test_spawn_player(self):
        mongo = pymongo.MongoClient('localhost', 27017)
        rexpert = mongo['rexpert']
        players = rexpert['Players']
        squads = rexpert['Squads']
        controller = PlayersController(None, players, squads)
        account_id = '_test_id1'
        nickname = '_test_nickname'
        controller.spawn_player(None, None, account_id, None, nickname, None, None, None, None,
                                None, None, None, None, None, None, None, None, None, None, None,
                                None)

    def test_connect_player(self):
        pass

    def test_disconnect_player(self):
        pass
