"""Тестирование начисления самолётов"""
import pathlib
import unittest

import processing
import configs
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
        campaign_map = processing.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list())
        vendor = processing.AircraftVendor(PLANES, GAMEPLAY)
        # Act
        supply = vendor.get_month_supply(TEST_MONTH, campaign_map)
        # Assert
        self.assertNotEqual(supply, None)

    def test_deliver_month_supply(self):
        """Начисляются самолёты ежемесячной поставки"""
        campaign_map = processing.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list())
        vendor = processing.AircraftVendor(PLANES, GAMEPLAY)
        supply = vendor.get_month_supply(CAMPAIGN_DATE, campaign_map)
        prior_red_af_1 = processing.ManagedAirfield('test_red_af1', TEST_TVD_NAME, 123, 321, dict())
        prior_red_af_2 = processing.ManagedAirfield('test_red_af2', TEST_TVD_NAME, 123, 321, dict())
        prior_red_af_3 = processing.ManagedAirfield('test_red_af3', TEST_TVD_NAME, 123, 321, dict())
        prior_blue_af_1 = processing.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321, dict())
        prior_blue_af_2 = processing.ManagedAirfield('test_blue_af2', TEST_TVD_NAME, 123, 321, dict())
        prior_blue_af_3 = processing.ManagedAirfield('test_blue_af3', TEST_TVD_NAME, 123, 321, dict())
        airfields = {
            101: [
                prior_red_af_1, prior_red_af_2, prior_red_af_3,
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
                prior_blue_af_1, prior_blue_af_2, prior_blue_af_3,
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
        priority = ['test_blue_af1', 'test_blue_af2', 'test_blue_af3', 'test_red_af1', 'test_red_af2', 'test_red_af3']
        GAMEPLAY.initial_priority[TEST_TVD_NAME] = priority
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
        for airfield in (prior_red_af_1, prior_red_af_2, prior_red_af_3, prior_blue_af_1, prior_blue_af_2, prior_blue_af_3):
            if airfield.planes_count <= GAMEPLAY.rear_max_power * 2:
                print()
            self.assertTrue(airfield.planes_count > GAMEPLAY.rear_max_power * 2)

    def test_transfer_to_front(self):
        """Переводятся самолёты с тылового на фронтовой"""
        front_airfields = [
            processing.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321,
                                       {'i-16type24': 20}, supplies=10),
            processing.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321,
                                       {'pe-2ser35': 20, 'p-40e-1': 10}),
            processing.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321,
                                       {'pe-2ser35': 10, 'il-2mod1941': 20})
        ]
        rear_airfields = [
            processing.ManagedAirfield('test_blue_af1', TEST_TVD_NAME, 123, 321,
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
                processing.ManagedAirfield('test_red_af1', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af2', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af3', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af4', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af5', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af6', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af7', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af8', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af9', TEST_TVD_NAME, 123, 321, dict()),
                processing.ManagedAirfield('test_red_af10', TEST_TVD_NAME, 123, 321, dict())
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
                processing.ManagedAirfield('test_blue_af10', TEST_TVD_NAME, 123, 321, dict())
            ]
        }
        campaign_map = processing.CampaignMap(1, CAMPAIGN_DATE, CAMPAIGN_DATE, TEST_TVD_NAME, list())
        vendor = processing.AircraftVendor(PLANES, GAMEPLAY)
        # Act
        vendor.initial_front_supply(campaign_map, airfields)
        # Assert
        for country in airfields:
            for managed_airfield in airfields[country]:
                self.assertEqual(managed_airfield.planes_count, GAMEPLAY.front_start_planes)

        # TODO см ниже
        """
[08.01.2018, 19:38:36] Максим Crusader 72AG Иконников: ну ещё вариант - сделать начальный разброс самолётов только на определённые филды
[08.01.2018, 19:39:10] Максим Crusader 72AG Иконников: выбрать 5 филдов поближе к удобному расположению и туда 50% начальной поставки херануть
[08.01.2018, 19:39:22] Alexander Fedorovsky: так лучше
[08.01.2018, 19:39:29] Alexander Fedorovsky: чем по 2 тыловых мутить
[08.01.2018, 19:40:21] Максим Crusader 72AG Иконников: но тогда филд должен отдавать не в % от своего количества, а абсолютное значение
[08.01.2018, 19:41:02] Alexander Fedorovsky: не понял
[08.01.2018, 19:41:13] Alexander Fedorovsky: он же отдает часть самолетов на фронтовые филды
[08.01.2018, 19:41:20] Максим Crusader 72AG Иконников: сейчас тыловой отдаёт 60% своих запасов
[08.01.2018, 19:41:28] Alexander Fedorovsky: и что то остается на нем - доступное к перегону
[08.01.2018, 19:41:41] Alexander Fedorovsky: если он отдаст все - он останется без самолетов - это неправильно
[08.01.2018, 19:41:50] Максим Crusader 72AG Иконников: если на тыловом будет значительная доля от начальной поставки - то пополнение фронтового будет слишком жирно
[08.01.2018, 19:41:59] Максим Crusader 72AG Иконников: при отдаче 50% самолётов
[08.01.2018, 19:42:11] Максим Crusader 72AG Иконников: а не, допустим, фиксированно по 30 самолётов
[08.01.2018, 19:42:25] Alexander Fedorovsky: так можно
[08.01.2018, 19:42:40] Alexander Fedorovsky: я не так понял про абсолютное значение)
[08.01.2018, 19:43:00] Alexander Fedorovsky: но ты заибешься выстраивать логику
[08.01.2018, 19:43:09] Максим Crusader 72AG Иконников: запишу в TODO себе, сделаю как время будет
[08.01.2018, 19:43:11] Alexander Fedorovsky: эти филды в %, а эти в штуках...
[08.01.2018, 19:43:20] Максим Crusader 72AG Иконников: все в штуках
[08.01.2018, 19:43:43] Alexander Fedorovsky: я не против
[08.01.2018, 19:43:52] Alexander Fedorovsky: а остальное и перегнать можно, если понадобится
[08.01.2018, 19:44:03] Максим Crusader 72AG Иконников: тыловой отдаёт пока у него не останется минимальное количество самолётов
[08.01.2018, 19:44:29] Максим Crusader 72AG Иконников: как упёрся в минимум - всё хлопцы, ваши запасы кончились
[08.01.2018, 19:44:39] Максим Crusader 72AG Иконников: пополнение фронта кончается
[08.01.2018, 19:44:48] Максим Crusader 72AG Иконников: начинается проёб
[08.01.2018, 19:45:38] Alexander Fedorovsky: норм
[08.01.2018, 19:45:47] Максим Crusader 72AG Иконников: и гоняйте остатки руками))
[08.01.2018, 19:45:52] Alexander Fedorovsky: ))
[08.01.2018, 19:46:15] Alexander Fedorovsky: так даже лучше - не надо лишних округлений
[08.01.2018, 19:46:35] Alexander Fedorovsky: есть число самолетов на отдачу, и его можно гибко настраивать
[08.01.2018, 19:46:57] Alexander Fedorovsky: грубо - 25+5 истребителей, 20 штурмов
[08.01.2018, 19:47:00] Alexander Fedorovsky: 10 бобров"""


if __name__ == '__main__':
    unittest.main(verbosity=2)
