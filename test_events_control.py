#pylint: disable=missing-docstring
import unittest
import pathlib
from db import PGConnector
from configs.main import Main
from processing import EventsController, PlayersController
import pymongo

CONFIG = Main()
PGConnector.init(CONFIG.connection_string)

TEST_LOG1 = './testdata/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'

class TestEventsController(unittest.TestCase):
    def test_processing(self):
        objects = PGConnector.get_objects_dict()
        mongo = pymongo.MongoClient('localhost', 27017)
        rexpert = mongo['rexpert']
        players = PlayersController(None, rexpert['Players'], rexpert['Squads'])
        controller = EventsController(objects, players, None)
        parsed = []
        text = pathlib.Path(TEST_LOG1).read_text()
        for line in text.split('\n'):
            controller.process_line(line)
            parsed.append(line)
        print(text)

if __name__ == '__main__':
    unittest.main()
