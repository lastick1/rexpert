"""Тестирование обработки событий"""
import unittest
import pathlib
from processing import EventsController, PlayersController, CampaignController, GroundController, AirfieldsController
from tests import mocks
import configs
import pymongo

TEST_LOG1 = './testdata/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'
TEST_LOG2 = './testdata/target_bombing_crashlanded_on_af_missionReport(2017-09-23_19-31-30)[0].txt'
TEST_LOG3 = './testdata/multiple_spawns_missionReport(2017-09-24_14-46-12)[0].txt'
TEST_LOG4 = './testdata/gkills_with_disconnect_missionReport(2017-09-26_20-37-23)[0].txt'
TEST_LOG5 = './testdata/gkill_with_altf4_disco_missionReport(2017-09-26_21-10-48)[0].txt'
DB_NAME = 'test_rexpert'

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)
PLANES = configs.Planes()
OBJECTS = configs.Objects()


TEST_TVD_NAME = 'moscow'
TEST_FIELDS = pathlib.Path(r'./configs/moscow_fields.csv')


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
        rexpert = self.mongo[DB_NAME]
        console = mocks.ConsoleMock()
        self.grounds = GroundController(OBJECTS)
        self.generator = mocks.GeneratorMock(MAIN, MGEN)
        self.players = PlayersController(True, console, rexpert['Players'], rexpert['Squads'])
        self.airfields = AirfieldsController(MAIN, PLANES, rexpert['Airfields'])
        self.campaign = CampaignController(MAIN, MGEN, self.generator)

    def tearDown(self):
        """Удаление базы после теста"""
        self.mongo.drop_database(DB_NAME)
        self.mongo.close()

    def test_processing_with_atype_7(self):
        """Завершается корректно миссия с AType:7 в логе"""
        self.airfields.initialize(TEST_TVD_NAME, TEST_FIELDS)
        controller = EventsController(OBJECTS, self.players, self.grounds, self.campaign, self.airfields, MAIN)
        # Act
        for line in pathlib.Path(TEST_LOG1).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertEqual(True, controller.is_correctly_completed)

    def test_generate_next_with_atype_0(self):
        """Генерируется следующая миссия с AType:0 в логе"""
        self.airfields.initialize(TEST_TVD_NAME, TEST_FIELDS)
        controller = EventsController(OBJECTS, self.players, self.grounds, self.campaign, self.airfields, MAIN)
        # Act
        for line in pathlib.Path(TEST_LOG1).read_text().split('\n'):
            controller.process_line(line)

        # Assert
        self.assertEqual(len(self.generator.generations), 1)

    def test_bombing(self):
        """Учитываются наземные цели"""
        self.airfields.initialize(TEST_TVD_NAME, TEST_FIELDS)
        controller = EventsController(OBJECTS, self.players, self.grounds, self.campaign, self.airfields, MAIN)
        # Act
        for line in pathlib.Path(TEST_LOG2).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertGreater(len(controller.ground_controller.units), 0)

    # TODO Отправляется предупреждение о запрете взлёта
    # TODO Отправляется команда кика при запрещённом взлёте


if __name__ == '__main__':
    unittest.main(verbosity=2)
