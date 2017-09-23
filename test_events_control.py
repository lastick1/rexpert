"Тестирование обработки событий"
import unittest
import pathlib
from processing import EventsController, PlayersController, CampaignController
from tests import mocks
import pymongo

TEST_LOG1 = './testdata/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'

MAIN = mocks.MainMock(pathlib.Path(r'.\testdata\conf.ini'))
MGEN = mocks.MgenMock(MAIN)

class TestEventsController(unittest.TestCase):
    "Тесты базовой обработки логов с новой базой на каждом тесте"
    def setUp(self):
        "Настройка базы перед тестом"
        mongo = pymongo.MongoClient('localhost', 27017)
        mongo.drop_database('test_rexpert')
        rexpert = mongo['test_rexpert']
        console = mocks.ConsoleMock()
        self.main = MAIN
        self.mgen = MGEN
        self.generator = mocks.GeneratorMock(self.main, self.mgen)
        self.players = PlayersController(True, console, rexpert['Players'], rexpert['Squads'])
        self.campaign = CampaignController(self.main, self.mgen, self.generator)
        self.objects = {}

    def test_processing_with_atype_7(self):
        "Завершается корректно миссия с AType:7 в логе"
        # Arrange
        controller = EventsController(self.objects, self.players, None, self.campaign)
        # Act
        for line in pathlib.Path(TEST_LOG1).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertEqual(True, controller.is_correctly_completed)

    def test_generate_next_with_atype_0(self):
        "Генерируется следующая миссия с AType:0 в логе"
        # Arrange
        controller = EventsController(self.objects, self.players, None, self.campaign)
        # Act
        for line in pathlib.Path(TEST_LOG1).read_text().split('\n'):
            controller.process_line(line)

        # Assert
        self.assertEqual(len(self.generator.generations), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
