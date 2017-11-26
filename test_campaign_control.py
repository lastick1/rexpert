"""Тестирование управления кампанией"""
import unittest
import datetime
import pathlib
from tests import mocks
from processing import CampaignController

DATE_FORMAT = '%d.%m.%Y'

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)


class TestCampaignController(unittest.TestCase):
    """Тесты бизнес-логики хода кампании"""
    def setUp(self):
        self.generator = mocks.GeneratorMock(MAIN, MGEN)
        self.campaign = CampaignController(MAIN, MGEN, self.generator)

    def test_next_mission_bin_name(self):
        """Отличается имя следующей миссии от имени текущей"""
        # Arrange
        date = datetime.datetime.strptime('01.10.1941', DATE_FORMAT)
        file_path = r'Multiplayer/Dogfight\result2.msnbin'
        # Act
        self.campaign.start_mission(date, file_path, 2, dict(), (0, 0), False, 0)
        # Assert
        self.assertEqual(self.generator.generations[0][0], 'result1')


if __name__ == '__main__':
    unittest.main(verbosity=2)
