"""Тестирование обработки событий"""
import unittest
import pathlib

import configs
import core
import processing

from tests import mocks

TEST_LOG1 = './testdata/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'
TEST_LOG2 = './testdata/target_bombing_crashlanded_on_af_missionReport(2017-09-23_19-31-30)[0].txt'
TEST_LOG3 = './testdata/multiple_spawns_missionReport(2017-09-24_14-46-12)[0].txt'
TEST_LOG4 = './testdata/gkills_with_disconnect_missionReport(2017-09-26_20-37-23)[0].txt'
TEST_LOG5 = './testdata/gkill_with_altf4_disco_missionReport(2017-09-26_21-10-48)[0].txt'
DB_NAME = 'test_rexpert'

CONFIG = mocks.ConfigMock(pathlib.Path(r'./testdata/conf.ini'))
PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()
OBJECTS = configs.Objects()


TEST_TVD_NAME = 'moscow'
TEST_TVD_DATE = '01.01.1941'
TEST_FIELDS = pathlib.Path(r'./data/moscow_fields.csv')


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(CONFIG.mgen.xgml[tvd_name])


def _load_all_campaign_maps():
    """Фальшивый метод загрузки карт кампании"""
    return [processing.CampaignMap(1, TEST_TVD_DATE, TEST_TVD_DATE, TEST_TVD_NAME, list())]


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.generator = mocks.GeneratorMock(CONFIG)
        self.players = processing.PlayersController(CONFIG.main, mocks.ConsoleMock())
        self.campaign = processing.CampaignController(CONFIG)
        self.campaign.generator = self.generator
        self.campaign.storage.campaign_maps.load_all = _load_all_campaign_maps
        self.airfields = mocks.AirfieldsControllerMock(CONFIG)
        self.storage = processing.Storage(CONFIG.main)

    def tearDown(self):
        """Удаление базы после теста"""
        self.storage.drop_database()

    def test_processing_with_atype_7(self):
        """Завершается корректно миссия с AType:7 в логе"""
        controller = core.EventsController(OBJECTS, CONFIG)
        controller.players_controller = self.players
        controller.airfields_controller = self.airfields
        controller.campaign_controller = self.campaign
        for tvd_name in CONFIG.mgen.maps:
            controller.campaign_controller.tvd_builders[tvd_name].grid_control.get_file = _get_xgml_file_mock
            controller.campaign_controller.initialize_map(tvd_name)
        # Act
        for line in pathlib.Path(TEST_LOG1).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertEqual(True, controller.is_correctly_completed)

    def test_generate_next_with_atype_0(self):
        """Генерируется следующая миссия с AType:0 в логе"""
        controller = core.EventsController(OBJECTS, CONFIG)
        controller.players_controller = self.players
        controller.airfields_controller = self.airfields
        controller.campaign_controller = self.campaign
        for tvd_name in CONFIG.mgen.maps:
            controller.campaign_controller.tvd_builders[tvd_name].grid_control.get_file = _get_xgml_file_mock
            controller.campaign_controller.initialize_map(tvd_name)
        # Act
        for line in pathlib.Path(TEST_LOG1).read_text().split('\n'):
            controller.process_line(line)

        # Assert
        self.assertEqual(len(self.generator.generations), 1)

    def test_bombing(self):
        """Учитываются наземные цели"""
        controller = core.EventsController(OBJECTS, CONFIG)
        controller.players_controller = self.players
        controller.airfields_controller = self.airfields
        controller.campaign_controller = self.campaign
        for tvd_name in CONFIG.mgen.maps:
            controller.campaign_controller.tvd_builders[tvd_name].grid_control.get_file = _get_xgml_file_mock
            self.campaign.initialize_map(tvd_name)
        # Act
        for line in pathlib.Path(TEST_LOG2).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertGreater(len(controller.ground_controller.ground_kills), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)