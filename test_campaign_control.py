"""Тестирование управления кампанией"""
import unittest
import datetime
import pathlib
import processing

from tests import mocks

DATE_FORMAT = '%d.%m.%Y'

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)


class TestCampaignController(unittest.TestCase):
    """Тесты бизнес-логики хода кампании"""
    def setUp(self):
        """Настройка перед тестом"""
        self.generator = mocks.GeneratorMock(MAIN, MGEN)
        self.storage = processing.Storage(MAIN)

    def tearDown(self):
        """Удаление базы после теста"""
        self.storage.drop_database()

    def test_next_mission_bin_name(self):
        """Отличается имя следующей миссии от имени текущей"""
        campaign = processing.CampaignController(MAIN, MGEN, self.generator)
        date = datetime.datetime.strptime('01.10.1941', DATE_FORMAT)
        file_path = r'Multiplayer/Dogfight\result2.msnbin'
        # Act
        campaign.start_mission(date, file_path, 2, dict(), (0, 0), False, 0)
        # Assert
        self.assertEqual(self.generator.generations[0][0], 'result1')

    def test_initialize(self):
        """Инициализируется кампания"""
        campaign = processing.CampaignController(MAIN, MGEN, self.generator)
        # Act
        campaign.initialize()
        # Assert
        self.assertEqual(self.storage.campaign_maps.count(), len(MGEN.maps))


if __name__ == '__main__':
    unittest.main(verbosity=2)
