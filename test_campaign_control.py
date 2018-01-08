"""Тестирование управления кампанией"""
import unittest
import datetime
import pathlib
import configs
import processing

from tests import mocks

DATE_FORMAT = '%d.%m.%Y'

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)
PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()

TEST_TVD_DATE = '01.09.1941'
TEST_TVD_NAME = 'moscow'


class TestCampaignController(unittest.TestCase):
    """Тесты бизнес-логики хода кампании"""
    def setUp(self):
        """Настройка перед тестом"""
        self.storage = processing.Storage(MAIN)

    def tearDown(self):
        """Удаление базы после теста"""
        self.storage.drop_database()

    def test_next_mission_bin_name(self):
        """Отличается имя следующей миссии от имени текущей"""
        generator = mocks.GeneratorMock(MAIN, MGEN)
        campaign = processing.CampaignController(MAIN, MGEN, PLANES, GAMEPLAY, generator)
        date = datetime.datetime.strptime('01.10.1941', DATE_FORMAT)
        file_path = r'Multiplayer/Dogfight\result2.msnbin'
        # Act
        campaign.start_mission(date, file_path, 2, dict(), (0, 0), False, 0)
        # Assert
        self.assertEqual(generator.generations[0][0], 'result1')

    def test_initialize_map(self):
        """Инициализируется карта кампании"""
        generator = mocks.GeneratorMock(MAIN, MGEN)
        order = 1
        campaign = processing.CampaignController(MAIN, MGEN, PLANES, GAMEPLAY, generator)
        # Act
        campaign.initialize_map(TEST_TVD_NAME)
        # Assert
        campaign_map = self.storage.campaign_maps.load_by_order(order)
        self.assertSequenceEqual(campaign_map.months, [campaign_map.date.strftime(DATE_FORMAT)])

    # тест прогонять на рабочей конфигурации
    def _test_initialize(self):
        """Инициализируется кампания"""
        main = configs.Main(pathlib.Path(r'./configs/conf.ini'))
        mgen = configs.Mgen(main)
        storage = processing.Storage(main)
        generator = processing.Generator(main, mgen)
        campaign = processing.CampaignController(main, mgen, PLANES, GAMEPLAY, generator)
        # Act
        campaign.initialize()
        # Assert
        self.assertEqual(storage.campaign_maps.count(), len(mgen.maps))
        campaign_map = storage.campaign_maps.load_by_order(1)
        self.assertSequenceEqual(campaign_map.months, [campaign_map.date.strftime(DATE_FORMAT)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
