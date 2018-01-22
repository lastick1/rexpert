"""Тестирование управления кампанией"""
import unittest
import datetime
import pathlib
import shutil

import atypes
import configs
import processing
import tests

DATE_FORMAT = '%d.%m.%Y'

TEMP_DIRECTORY = pathlib.Path('./tmp/').absolute()
IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
IOC.config.main = tests.mocks.MainMock(pathlib.Path('./testdata/conf.ini'))
IOC.config.mgen = tests.mocks.MgenMock(IOC.config.main.game_folder)
PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()

MOSCOW = 'moscow'
STALIN = 'stalingrad'

TEST_TVD_DATE = '01.09.1941'
TEST_TVD_NAME = MOSCOW


def _parse_mock(name: str) -> processing.SourceMission:
    """Фальшивый метод парсинга исходников"""
    return processing.SourceMission(name=name, file=pathlib.Path(), date=TEST_TVD_DATE, guimap=TEST_TVD_NAME)


class TestCampaignController(unittest.TestCase):
    """Тесты бизнес-логики хода кампании"""
    def setUp(self):
        """Настройка перед тестом"""
        self.get_xgml_file_calls = 0
        IOC.generator_mock.generations.clear()
        if not TEMP_DIRECTORY.exists():
            TEMP_DIRECTORY.mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/airfields_red').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/airfields_blue').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/airfields_red').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/airfields_blue').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/icons').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/icons').mkdir(parents=True)
        pathlib.Path('./tmp/red/').mkdir(parents=True)
        pathlib.Path('./tmp/blue/').mkdir(parents=True)

    def tearDown(self):
        """Удаление базы и очистка временной папки после теста"""
        IOC.storage.drop_database()
        tests.utils.clean_directory(str(TEMP_DIRECTORY))

    def _get_xgml_file_mock(self, tvd_name: str) -> str:
        """Подделка метода получения файла графа"""
        self.get_xgml_file_calls = 0
        return str(IOC.config.mgen.xgml[tvd_name])

    def test_next_mission_bin_name(self):
        """Отличается имя следующей миссии от имени текущей"""
        campaign = processing.CampaignController(IOC)
        IOC.source_parser.parse_in_dogfight = _parse_mock
        for tvd_name in IOC.config.mgen.maps:
            IOC.grid_controller.get_file = self._get_xgml_file_mock
            campaign.initialize_map(tvd_name)
        atype = atypes.Atype0(
            tik=0,
            date=datetime.datetime.strptime('01.10.1941', DATE_FORMAT),
            file_path=r'Multiplayer/Dogfight\result2.msnbin',
            game_type_id=2,
            countries=dict(),
            settings=(0, 0),
            mods=False,
            preset_id=0
        )
        # Act
        campaign.start_mission(atype)
        # Assert
        self.assertEqual(campaign.next_name, 'result1')

    def test_reset(self):
        """Сбрасывается состояние кампании"""
        campaign = processing.CampaignController(IOC)
        for tvd_name in IOC.config.mgen.maps:
            IOC.grid_controller.get_file = self._get_xgml_file_mock
            campaign.initialize_map(tvd_name)
        # Act
        campaign.reset()
        # Assert
        self.assertEqual(IOC.storage.campaign_maps.count(), 0)
        self.assertEqual(IOC.storage.airfields.collection.count(), 0)

    def test_generate(self):
        """Генерируется указанная миссия"""
        shutil.copy('./data/scg/1/stalin-base.ldf', './tmp/data/scg/1/')
        shutil.copy('./data/scg/2/moscow-base_v2.ldf', './tmp/data/scg/2/')
        campaign = processing.CampaignController(IOC)
        IOC.grid_controller.get_file = self._get_xgml_file_mock
        campaign.initialize()
        campaign_map = IOC.storage.campaign_maps.load_by_tvd_name(MOSCOW)
        campaign_map.set_date(IOC.config.mgen.cfg[MOSCOW]['end_date'])
        IOC.storage.campaign_maps.update(campaign_map)
        # Act
        campaign.generate('result2')
        # Assert
        self.assertIn(('result2', STALIN), IOC.generator_mock.generations)

    def test_generate_next_with_atype_19(self):
        """Генерируется следующая миссия с AType:19 в логе"""
        campaign = processing.CampaignController(IOC)
        IOC.grid_controller.get_file = self._get_xgml_file_mock
        IOC.source_parser.parse_in_dogfight = _parse_mock
        campaign.initialize_map(MOSCOW)
        atype0 = atypes.Atype0(
            tik=0,
            date=datetime.datetime.strptime('01.10.1941', DATE_FORMAT),
            file_path=r'Multiplayer/Dogfight\result1.msnbin',
            game_type_id=2,
            countries=dict(),
            settings=(0, 0),
            mods=False,
            preset_id=0
        )

        # Act
        campaign.start_mission(atype0)
        campaign.end_round(atypes.Atype19(1312))

        # Assert
        self.assertIn(('result2', MOSCOW), IOC.generator_mock.generations)

    def test_initialize_map(self):
        """Инициализируется карта кампании"""
        order = 1
        campaign = processing.CampaignController(IOC)
        campaign.generator = tests.mocks.GeneratorMock(IOC.config)
        IOC.grid_controller.get_file = self._get_xgml_file_mock
        # Act
        campaign.initialize_map(TEST_TVD_NAME)
        # Assert
        campaign_map = IOC.storage.campaign_maps.load_by_order(order)
        self.assertSequenceEqual(campaign_map.months, [campaign_map.date.strftime(DATE_FORMAT)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
