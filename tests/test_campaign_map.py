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

    def test_red_succeeded(self):
        """ВВС РККА достигают успеха в миссии противостояния"""
        campaign_map = _make_campaign_map(constants.TvdNames.MOSCOW)
        campaign_map.actions.append(model.DivisionKill(10000, 101, 'BTD1'))
        campaign_map.actions.append(model.DivisionKill(11000, 101, 'BAD1'))
        campaign_map.actions.append(model.WarehouseDisable(11100, 101, 'klin'))

