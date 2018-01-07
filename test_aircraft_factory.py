"""Тестирование начисления самолётов"""
import pathlib
import unittest

import processing
import configs
import tests

MAIN = tests.mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = tests.mocks.MgenMock(MAIN)

PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()
CAMPAIGN_DATE = '01.09.1941'
TEST_MONTH = '01.09.1941'
TEST_TVD_NAME = 'moscow'


class TestAircraftFactory(unittest.TestCase):
    """Тестовый класс"""
    def test_get_month_supply(self):
        """Формируется месячная поставка самолётов"""
        campaign_map = processing.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list())
        factory = processing.AircraftFactory(PLANES, GAMEPLAY)
        # Act
        supply = factory.get_month_supply(TEST_MONTH, campaign_map)
        # Assert
        self.assertNotEqual(supply, None)

    def test_deliver_month_supply(self):
        """Начисляются самолёты ежемесячной поставки"""
        campaign_map = processing.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list())
        factory = processing.AircraftFactory(PLANES, GAMEPLAY)
        supply = factory.get_month_supply(CAMPAIGN_DATE, campaign_map)
        airfields = {
            101: [
                processing.ManagedAirfield('test_red_af1', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af2', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af3', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af4', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af5', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af6', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af7', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af8', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af9', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af10', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af11', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af12', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af13', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af14', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af15', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af16', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af17', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af18', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af19', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af20', TEST_TVD_NAME, 123, 321, dict())
            ],
            201: [
                processing.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af2', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af3', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af4', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af5', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af6', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af7', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af8', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af9', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af10', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af11', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af12', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af13', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af14', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af15', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af16', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af17', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af18', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af19', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_blue_af20', TEST_TVD_NAME, 123, 321, dict())
            ]
        }
        # Act
        factory.deliver_month_supply(campaign_map, airfields, supply)
        # Assert
        self.assertFalse(supply.has_aircrafts)
        self.assertIn(CAMPAIGN_DATE, campaign_map.months)


if __name__ == '__main__':
    unittest.main(verbosity=2)
