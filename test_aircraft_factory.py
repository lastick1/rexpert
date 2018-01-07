"""Тестирование начисления самолётов"""
import unittest
import processing
import configs

PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()
CAMPAIGN_DATE = '01.09.1941'
TEST_MONTH = '01.09.1941'
TEST_TVD_NAME = 'moscow'


class TestAircraftFactory(unittest.TestCase):
    """Тестовый класс"""
    def test_get_month_supply(self):
        """Формируется месячная поставка самолётов"""
        months = list()
        campaign_map = processing.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, months)
        factory = processing.AircraftFactory(PLANES, GAMEPLAY)
        # Act
        supply = factory.get_month_supply(TEST_MONTH, campaign_map)
        # Assert
        self.assertNotEqual(supply, None)

    def test_deliver_month_supply(self):
        """Начисляются самолёты ежемесячной поставки"""


if __name__ == '__main__':
    unittest.main(verbosity=2)
