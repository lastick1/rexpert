"""Тестирование управления кампанией"""
import unittest
import datetime
import pathlib
import shutil
import configs
import processing

from tests import mocks, utils

DATE_FORMAT = '%d.%m.%Y'

TEMP_DIRECTORY = pathlib.Path(r'./tmp/').absolute()
CONFIG = mocks.ConfigMock(pathlib.Path(r'./testdata/conf.ini'))
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
        if not TEMP_DIRECTORY.exists():
            TEMP_DIRECTORY.mkdir(parents=True)
        self.storage = processing.Storage(CONFIG.main)

    def tearDown(self):
        """Удаление базы и очистка временной папки после теста"""
        self.storage.drop_database()
        utils.clean_directory(str(TEMP_DIRECTORY))

    def test_next_mission_bin_name(self):
        """Отличается имя следующей миссии от имени текущей"""
        generator = mocks.GeneratorMock(CONFIG)
        campaign = processing.CampaignController(CONFIG, generator)
        date = datetime.datetime.strptime('01.10.1941', DATE_FORMAT)
        file_path = r'Multiplayer/Dogfight\result2.msnbin'
        # Act
        campaign.start_mission(date, file_path, 2, dict(), (0, 0), False, 0)
        # Assert
        self.assertEqual(generator.generations[0][0], 'result1')

    def test_reset(self):
        """Сбрасывается состояние кампании"""
        generator = mocks.GeneratorMock(CONFIG)
        campaign = processing.CampaignController(CONFIG, generator)
        for tvd_name in CONFIG.mgen.maps:
            campaign.initialize_map(tvd_name)
        # Act
        campaign.reset()
        # Assert
        self.assertEqual(self.storage.campaign_maps.count(), 0)
        self.assertEqual(self.storage.airfields.collection.count(), 0)

    def test_generate(self):
        """Генерируется указанная миссия"""
        pathlib.Path('./tmp/red/').mkdir(parents=True)
        pathlib.Path('./tmp/blue/').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/icons').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/icons').mkdir(parents=True)
        shutil.copy('./data/scg/1/stalin-base.ldf', './tmp/data/scg/1/')
        shutil.copy('./data/scg/2/moscow-base_v2.ldf', './tmp/data/scg/2/')
        generator = mocks.GeneratorMock(CONFIG)
        campaign = processing.CampaignController(CONFIG, generator)
        campaign.initialize()
        campaign_map = self.storage.campaign_maps.load_by_tvd_name(MOSCOW)
        campaign_map.set_date(CONFIG.mgen.cfg[MOSCOW]['end_date'])
        self.storage.campaign_maps.update(campaign_map)
        # Act
        campaign.generate('result2')
        # Assert
        self.assertIn(('result2', STALIN), generator.generations)

    def test_initialize_map(self):
        """Инициализируется карта кампании"""
        generator = mocks.GeneratorMock(CONFIG)
        order = 1
        campaign = processing.CampaignController(CONFIG, generator)
        # Act
        campaign.initialize_map(TEST_TVD_NAME)
        # Assert
        campaign_map = self.storage.campaign_maps.load_by_order(order)
        self.assertSequenceEqual(campaign_map.months, [campaign_map.date.strftime(DATE_FORMAT)])

    # @unittest.skip("тест прогонять на рабочей конфигурации")
    def test_initialize(self):
        """Инициализируется кампания"""
        config = configs.Config(pathlib.Path(r'./configs/conf.ini'))
        storage = processing.Storage(config.main)
        generator = processing.Generator(config)
        campaign = processing.CampaignController(config, generator)
        # Act
        campaign.initialize()
        # Assert
        self.assertEqual(storage.campaign_maps.count(), len(config.mgen.maps))
        campaign_map = storage.campaign_maps.load_by_order(1)
        self.assertSequenceEqual(campaign_map.months, [campaign_map.date.strftime(DATE_FORMAT)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
