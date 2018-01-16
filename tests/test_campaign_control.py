"""Тестирование управления кампанией"""
import unittest
import datetime
import pathlib
import shutil

import atypes
import configs
import processing
import ioc
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


class TestCampaignController(unittest.TestCase):
    """Тесты бизнес-логики хода кампании"""
    def setUp(self):
        """Настройка перед тестом"""
        self.get_xgml_file_calls = 0
        if not TEMP_DIRECTORY.exists():
            TEMP_DIRECTORY.mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/airfields_red').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/airfields_blue').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/airfields_red').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/airfields_blue').mkdir(parents=True)

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
        generator = tests.mocks.GeneratorMock(IOC.config)
        campaign = processing.CampaignController(IOC)
        campaign.generator = generator
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
        self.assertEqual(IOC.generator_mock.generations[0][0], 'result1')

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
        pathlib.Path('./tmp/red/').mkdir(parents=True)
        pathlib.Path('./tmp/blue/').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/icons').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/icons').mkdir(parents=True)
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

    @unittest.skip("тест прогонять на рабочей конфигурации")
    def test_initialize(self):
        """Инициализируется кампания"""
        _ioc = ioc.DependencyContainer()
        storage = processing.Storage(_ioc.config.main)
        campaign = processing.CampaignController(_ioc)
        campaign.generator = processing.Generator(_ioc.config)
        # Act
        campaign.initialize()
        # Assert
        self.assertEqual(storage.campaign_maps.count(), len(_ioc.config.mgen.maps))
        campaign_map = storage.campaign_maps.load_by_order(1)
        self.assertSequenceEqual(campaign_map.months, [campaign_map.date.strftime(DATE_FORMAT)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
