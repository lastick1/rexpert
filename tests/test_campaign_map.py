"""Тестирование логики зачёта победы миссии кампании"""
import unittest

import constants
import model


def _make_regular_mission(tvd_name: str) -> model.CampaignMission:
    """Упрощение конструктора миссий"""
    return model.CampaignMission(
            kind=constants.CampaignMission.Kinds.REGULAR,
            file='result1',
            date='01.09.1941',
            tvd_name=tvd_name,
            additional=dict(),
            server_inputs=list(),
            objectives=list(),
            airfields=list(),
            units=list())


def _make_campaign_map(tvd_name: str) -> model.CampaignMap:
    """Упрощение конструктора карт кампании"""
    return model.CampaignMap(
        order=1,
        date='01.09.1941',
        mission_date='01.09.1941',
        tvd_name=tvd_name,
        months=list(),
        actions=list()
    )


class TestCampaignMap(unittest.TestCase):
    """Тестовый класс"""

    def test_red_completed(self):
        """ВВС РККА достигают успеха в миссии противостояния"""
        campaign_map = _make_campaign_map(constants.TvdNames.MOSCOW)
        # Act
        campaign_map.register_action(model.DivisionKill(10000, constants.Country.USSR, 'BTD1'))
        campaign_map.register_action(model.DivisionKill(11000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.WarehouseDisable(11100, constants.Country.USSR, 'klin'))
        # Assert
        self.assertEqual(campaign_map.red_completed, True)
        self.assertEqual(campaign_map.blue_completed, False)

    def test_blue_completed(self):
        """Люфтваффе достигают успеха в миссии противостояния"""
        campaign_map = _make_campaign_map(constants.TvdNames.MOSCOW)
        # Act
        campaign_map.register_action(model.DivisionKill(10000, constants.Country.GERMANY, 'RTD1'))
        campaign_map.register_action(model.DivisionKill(11000, constants.Country.GERMANY, 'RAD1'))
        campaign_map.register_action(model.WarehouseDisable(11100, constants.Country.GERMANY, 'rzhev'))

        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.WarehouseDisable(22200, constants.Country.USSR, 'klin'))
        # Assert
        self.assertEqual(campaign_map.blue_completed, True)
        self.assertEqual(campaign_map.red_completed, True)

    def test_country_attacked(self):
        """Определяется наступающая сторона по результатам миссии"""
        campaign_map = _make_campaign_map(constants.TvdNames.MOSCOW)
        # Act
        campaign_map.register_action(model.DivisionKill(10000, constants.Country.GERMANY, 'RTD1'))
        campaign_map.register_action(model.DivisionKill(11000, constants.Country.GERMANY, 'RAD1'))
        campaign_map.register_action(model.WarehouseDisable(11100, constants.Country.GERMANY, 'rzhev'))

        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.WarehouseDisable(22200, constants.Country.USSR, 'klin'))

        result = campaign_map.country_attacked()
        # Assert
        self.assertEqual(result, constants.Country.GERMANY)

    def test_country_attacked_counterattack(self):
        """Определяется наступающая сторона по результатам миссии с успешной обороной"""
        campaign_map = _make_campaign_map(constants.TvdNames.MOSCOW)
        # Act
        campaign_map.register_action(model.DivisionKill(10000, constants.Country.GERMANY, 'RTD1'))
        campaign_map.register_action(model.DivisionKill(11000, constants.Country.GERMANY, 'RAD1'))
        campaign_map.register_action(model.WarehouseDisable(11100, constants.Country.GERMANY, 'rzhev'))

        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.WarehouseDisable(22200, constants.Country.USSR, 'klin'))

        campaign_map.country_attacked()
        result = campaign_map.country_attacked()
        # Assert
        self.assertEqual(result, constants.Country.USSR)

    def test_country_attacked_capture(self):
        """Обнуляются игровые действия по результатам миссии с захватом"""
        campaign_map = _make_campaign_map(constants.TvdNames.MOSCOW)
        # Act
        campaign_map.register_action(model.DivisionKill(10000, constants.Country.GERMANY, 'RTD1'))
        campaign_map.register_action(model.DivisionKill(11000, constants.Country.GERMANY, 'RAD1'))
        campaign_map.register_action(model.WarehouseDisable(11100, constants.Country.GERMANY, 'rzhev'))

        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.DivisionKill(22000, constants.Country.USSR, 'BAD1'))
        campaign_map.register_action(model.WarehouseDisable(22200, constants.Country.USSR, 'klin'))

        campaign_map.country_attacked()
        campaign_map.register_capture()
        result = campaign_map.country_attacked()
        # Assert
        self.assertEqual(result, 0)

