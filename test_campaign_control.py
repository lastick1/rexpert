"""Тестирование управления кампанией"""
import unittest
import datetime
import pathlib
import configs
import processing

from tests import mocks

DATE_FORMAT = '%d.%m.%Y'

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
        self.storage = processing.Storage(CONFIG.main)

    def tearDown(self):
        """Удаление базы после теста"""
        self.storage.drop_database()

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

    # тест прогонять на рабочей конфигурации
    def _test_initialize(self):
        """Инициализируется кампания"""
        main = configs.Main(pathlib.Path(r'./configs/conf.ini'))
        mgen = configs.Mgen(main.game_folder)
        storage = processing.Storage(main)
        generator = processing.Generator(CONFIG)
        campaign = processing.CampaignController(CONFIG, generator)
        # Act
        campaign.initialize()
        # Assert
        self.assertEqual(storage.campaign_maps.count(), len(mgen.maps))
        campaign_map = storage.campaign_maps.load_by_order(1)
        self.assertSequenceEqual(campaign_map.months, [campaign_map.date.strftime(DATE_FORMAT)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
