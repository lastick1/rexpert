"""Тестирование обработки событий"""
import unittest
import pathlib

import configs
import core
import processing
import tests

TEST_LOG1 = './testdata/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'
TEST_LOG2 = './testdata/target_bombing_crashlanded_on_af_missionReport(2017-09-23_19-31-30)[0].txt'
TEST_LOG3 = './testdata/multiple_spawns_missionReport(2017-09-24_14-46-12)[0].txt'
TEST_LOG4 = './testdata/gkills_with_disconnect_missionReport(2017-09-26_20-37-23)[0].txt'
TEST_LOG5 = './testdata/gkill_with_altf4_disco_missionReport(2017-09-26_21-10-48)[0].txt'
DB_NAME = 'test_rexpert'

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()
OBJECTS = configs.Objects()


TEST_TVD_NAME = 'moscow'
TEST_TVD_DATE = '01.01.1941'
TEST_FIELDS = pathlib.Path('./data/moscow_fields.csv')


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(IOC.config.mgen.xgml[tvd_name])


def _load_all_campaign_maps():
    """Фальшивый метод загрузки карт кампании"""
    return [processing.CampaignMap(1, TEST_TVD_DATE, TEST_TVD_DATE, TEST_TVD_NAME, list())]


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    def setUp(self):
        """Настройка базы перед тестом"""
        IOC.generator_mock.generations.clear()

    def tearDown(self):
        """Удаление базы после теста"""
        IOC.storage.drop_database()

    def test_processing_with_atype_7(self):
        """Завершается корректно миссия с AType:7 в логе"""
        controller = core.EventsController(IOC)
        for tvd_name in IOC.config.mgen.maps:
            IOC.grid_controller.get_file = _get_xgml_file_mock
            IOC.campaign_controller.initialize_map(tvd_name)
        # Act
        for line in pathlib.Path(TEST_LOG1).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertEqual(True, controller.is_correctly_completed)

    def test_bombing(self):
        """Учитываются наземные цели"""
        controller = core.EventsController(IOC)
        for tvd_name in IOC.config.mgen.maps:
            IOC.grid_controller.get_file = _get_xgml_file_mock
            IOC.campaign_controller.initialize_map(tvd_name)
        # Act
        for line in pathlib.Path(TEST_LOG2).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertGreater(len(IOC.ground_controller.ground_kills), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
