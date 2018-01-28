"""Тестирование обработки событий"""
import pathlib
import shutil
import unittest

import configs
import core
import model
import tests

TEST_LOG1 = './testdata/logs/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'
TEST_LOG2 = './testdata/logs/target_bombing_crashlanded_on_af_missionReport(2017-09-23_19-31-30)[0].txt'
TEST_LOG3 = './testdata/logs/multiple_spawns_missionReport(2017-09-24_14-46-12)[0].txt'
TEST_LOG4 = './testdata/logs/gkills_with_disconnect_missionReport(2017-09-26_20-37-23)[0].txt'
TEST_LOG5 = './testdata/logs/gkill_with_altf4_disco_missionReport(2017-09-26_21-10-48)[0].txt'
TEST_LOG6 = './testdata/logs/mission_rotation_atype19.txt'
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
    return [model.CampaignMap(1, TEST_TVD_DATE, TEST_TVD_DATE, TEST_TVD_NAME, list())]


def _parse_mock(name: str) -> model.SourceMission:
    """Фальшивый метод парсинга исходников"""
    return model.SourceMission(name=name, file=pathlib.Path(), date=TEST_TVD_DATE, guimap=TEST_TVD_NAME)


def _make_dirs(dirs: list):
    for directory in dirs:
        path = pathlib.Path(directory)
        if not path.exists():
            path.mkdir(parents=True)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    def setUp(self):
        """Настройка базы перед тестом"""
        self.directory = pathlib.Path(r'./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        _make_dirs([
            './tmp/data/scg/1/blocks_quickmission/airfields_red',
            './tmp/data/scg/1/blocks_quickmission/airfields_blue',
            './tmp/data/scg/2/blocks_quickmission/airfields_red',
            './tmp/data/scg/2/blocks_quickmission/airfields_blue',
            './tmp/data/scg/1/blocks_quickmission/icons',
            './tmp/data/scg/2/blocks_quickmission/icons',
            './tmp/red/',
            './tmp/blue/'
        ])
        IOC.generator_mock.generations.clear()

    def tearDown(self):
        """Удаление базы после теста"""
        tests.utils.clean_directory(str(self.directory))
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
        self.assertEqual(True, IOC.campaign_controller.mission.is_correctly_completed)

    def test_bombing(self):
        """Учитываются наземные цели"""
        IOC.source_parser.parse_in_dogfight = _parse_mock
        controller = core.EventsController(IOC)
        for tvd_name in IOC.config.mgen.maps:
            IOC.grid_controller.get_file = _get_xgml_file_mock
            IOC.campaign_controller.initialize_map(tvd_name)
        # Act
        for line in pathlib.Path(TEST_LOG2).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        self.assertGreater(len(IOC.ground_controller.ground_kills), 1)

    def test_end_round(self):
        """Перераспределяются самолёты по аэродромам в конце миссии"""
        shutil.copy('./data/scg/1/stalin-base.ldf', './tmp/data/scg/1/')
        shutil.copy('./data/scg/2/moscow-base_v2.ldf', './tmp/data/scg/2/')
        IOC.source_parser.parse_in_dogfight = _parse_mock
        controller = core.EventsController(IOC)
        for tvd_name in IOC.config.mgen.maps:
            IOC.grid_controller.get_file = _get_xgml_file_mock
            IOC.campaign_controller.initialize_map(tvd_name)
        # Act
        for line in pathlib.Path(TEST_LOG6).read_text().split('\n'):
            controller.process_line(line)
        # Assert
        airfield = controller.airfields_controller.get_airfield_in_radius(TEST_TVD_NAME, 21649, 108703, 50)
        self.assertGreater(airfield.planes_count, 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)
