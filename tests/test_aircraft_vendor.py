"""Тестирование начисления самолётов"""
import pathlib
import unittest

import configs
import model
import processing
import tests

MAIN = tests.mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = tests.mocks.MgenMock(MAIN.game_folder)

PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()
CAMPAIGN_DATE = '01.09.1941'
TEST_MONTH = '01.09.1941'
TEST_TVD_NAME = 'moscow'


class TestAircraftVendor(unittest.TestCase):
    """Тестовый класс"""

    def test_get_month_supply(self):
        """Формируется месячная поставка самолётов"""
        campaign_map = model.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list(), list())
        vendor = processing.AircraftVendor(PLANES, GAMEPLAY)
        # Act
        supply = vendor.get_month_supply(TEST_MONTH, campaign_map)
        # Assert
        self.assertNotEqual(supply, None)

    def test_deliver_month_supply(self):
        """Начисляются самолёты ежемесячной поставки"""
        campaign_map = model.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list(), list())
        vendor = processing.AircraftVendor(PLANES, GAMEPLAY)
        supply = vendor.get_month_supply(CAMPAIGN_DATE, campaign_map)
        test_red_af1 = model.ManagedAirfield('test_red_af1', TEST_TVD_NAME, 123, 321, dict())
        test_red_af2 = model.ManagedAirfield('test_red_af2', TEST_TVD_NAME, 123, 321, dict())
        test_red_af3 = model.ManagedAirfield('test_red_af3', TEST_TVD_NAME, 123, 321, dict())
        test_blue_af1 = model.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321, dict())
        test_blue_af2 = model.ManagedAirfield('test_blue_af2', TEST_TVD_NAME, 123, 321, dict())
        test_blue_af3 = model.ManagedAirfield('test_blue_af3', TEST_TVD_NAME, 123, 321, dict())
        airfields = {
            101: [
                test_red_af1, test_red_af2, test_red_af3,
                model.ManagedAirfield('test_red_af4', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af5', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af6', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af7', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af8', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af9', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af10', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af11', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af12', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af13', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af14', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af15', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af16', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af17', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af18', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af19', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af20', TEST_TVD_NAME, 123, 321, dict())
            ],
            201: [
                test_blue_af1, test_blue_af2, test_blue_af3,
                model.ManagedAirfield('test_blue_af4', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af5', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af6', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af7', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af8', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af9', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af10', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af11', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af12', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af13', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af14', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af15', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af16', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af17', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af18', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af19', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af20', TEST_TVD_NAME, 123, 321, dict())
            ]
        }
        GAMEPLAY.initial_priority[TEST_TVD_NAME] = list(x.name for x in (
            test_red_af1, test_red_af2, test_red_af3, test_blue_af1, test_blue_af2, test_blue_af3))
        # Act
        vendor.deliver_month_supply(campaign_map, airfields, supply)
        # Assert
        self.assertFalse(supply.has_aircrafts)
        self.assertIn(CAMPAIGN_DATE, campaign_map.months)
        self.assertSequenceEqual(supply.amounts, len(supply.amounts) * [0])
        for country in airfields:
            for airfield in airfields[country]:
                for key in airfield.planes:
                    for name in PLANES.cfg['uncommon']:
                        if PLANES.name_to_key(name) == key:
                            self.assertEqual(country, PLANES.cfg['uncommon'][name]['country'])
        for airfield in test_red_af1, test_red_af2, test_red_af3, test_blue_af1, test_blue_af2, test_blue_af3:
            self.assertTrue(airfield.planes_count >= GAMEPLAY.rear_max_power * 2)

    def test_transfer_to_front(self):
        """Переводятся самолёты с тылового на фронтовой"""
        front_airfields = [
            model.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321, {'i-16type24': 20}, supplies=10),
            model.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321, {'pe-2ser35': 20, 'p-40e-1': 10}),
            model.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321, {'pe-2ser35': 10, 'il-2mod1941': 20})
        ]
        rear_airfields = [
            model.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321,
                                  {'il-2mod1941': 29, 'i-16type24': 41, 'pe-2ser35': 11, 'p-40e-1': 19})
        ]
        front_planes_count_before = sum(x.planes_count for x in front_airfields)
        rear_planes_count_before = sum(x.planes_count for x in rear_airfields)
        vendor = processing.AircraftVendor(PLANES, GAMEPLAY)
        # Act
        vendor.transfer_to_front(front_airfields, rear_airfields)
        # Assert
        front_planes_count_after = sum(x.planes_count for x in front_airfields)
        rear_planes_count_after = sum(x.planes_count for x in rear_airfields)
        self.assertTrue(front_planes_count_before < front_planes_count_after)
        self.assertTrue(rear_planes_count_before > rear_planes_count_after)

    def test_initial_front_supply(self):
        """Выполняется начальная поставка на фронтовые аэродромы"""
        airfields = {
            101: [
                model.ManagedAirfield('test_red_af1', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af2', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af3', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af4', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af5', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af6', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af7', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af8', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af9', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_red_af10', TEST_TVD_NAME, 123, 321, dict())
            ],
            201: [
                model.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af2', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af3', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af4', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af5', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af6', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af7', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af8', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af9', TEST_TVD_NAME, 123, 321, dict()),
                model.ManagedAirfield('test_blue_af10', TEST_TVD_NAME, 123, 321, dict())
            ]
        }
        campaign_map = model.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list(), list())
        vendor = processing.AircraftVendor(PLANES, GAMEPLAY)
        # Act
        vendor.initial_front_supply(campaign_map, airfields)
        # Assert
        for country in airfields:
            for managed_airfield in airfields[country]:
                self.assertEqual(managed_airfield.planes_count, 80)


if __name__ == '__main__':
    unittest.main(verbosity=2)
