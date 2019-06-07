"Тестирование сервиса дивизий"
from __future__ import annotations
from typing import List
import unittest

from core import EventsEmitter, DivisionDamage
from services import DivisionsService
from storage import Storage
from model import CampaignMission, Division, DIVISIONS
from tests.mocks import EventsInterceptor, \
    ConfigMock, \
    pass_

TEST_TVD_NAME = 'moscow'
TEST_DATE = '01.09.1941'
TEST_TARGET_AIRFIELD_SERVER_INPUT = 'Verbovka'
TEST_TARGET_BTD1_SERVER_INPUT = 'BTD1'
TEST_TARGET_POS_BTD1 = {'x': 156060.64, 'z': 132392.5}
TEST_TARGET_HP = 3
TEST_TARGET_POS_BTD1_UNITS = [
    {'x': 155453.86, 'z': 130798.2},
    {'x': 156461.58, 'z': 131861.16},
    {'x': 155169.17, 'z': 133163.56},
    {'x': 155055.39, 'z': 132101.14},
    {'x': 155604.38, 'z': 131692.38},
    {'x': 156010.75, 'z': 131154.91},
    {'x': 156484.95, 'z': 133269.22},
    {'x': 156907.78, 'z': 133390.91},
    {'x': 157196.23, 'z': 134433.89},
    {'x': 157767.08, 'z': 132920.91}
]
TEST_DIVISION = Division(
    tvd_name=TEST_TVD_NAME,
    name=TEST_TARGET_BTD1_SERVER_INPUT,
    units=DIVISIONS[TEST_TARGET_BTD1_SERVER_INPUT],
    pos=TEST_TARGET_POS_BTD1
)
TEST_MISSION = CampaignMission(
    file='result1',
    date=TEST_DATE,
    tvd_name=TEST_TVD_NAME,
    additional=dict(),
    server_inputs=[
        {'name': TEST_TARGET_BTD1_SERVER_INPUT, 'pos': TEST_TARGET_POS_BTD1}
    ],
    objectives=[],
    airfields=[],
    units=[],
    actions=list()
)


# pylint: disable=unused-argument
def _load_divisions_by_tvd_mock(tvd_name: str) -> List[Division]:
    return []


# pylint: disable=unused-argument
def _load_division_by_name_mock(tvd_name: str, name: str) -> Division:
    return TEST_DIVISION


class TestDivisionsService(unittest.TestCase):
    "Тесты"

    def setUp(self):
        """Настройка перед тестом"""
        self.config = ConfigMock()
        self.storage: Storage = Storage(self.config.main)
        self.storage.divisions.load_by_tvd = _load_divisions_by_tvd_mock
        self.storage.divisions.load_by_name = _load_division_by_name_mock
        self.storage.divisions.update = pass_
        self.emitter = EventsEmitter()
        self._interceptor = EventsInterceptor(self.emitter)
        TEST_MISSION.units.clear()

    def test_division_kill(self):
        """Обрабатывается уничтожение дивизии"""
        TEST_MISSION.units.extend([
            {'name': 'REXPERT_BTD1_3', 'pos': TEST_TARGET_POS_BTD1_UNITS[0]},
            {'name': 'REXPERT_BTD1_15', 'pos': TEST_TARGET_POS_BTD1_UNITS[1]},
            {'name': 'REXPERT_BTD1_2', 'pos': TEST_TARGET_POS_BTD1_UNITS[2]},
            {'name': 'REXPERT_BTD1_10', 'pos': TEST_TARGET_POS_BTD1_UNITS[3]},
            {'name': 'REXPERT_BTD1_17', 'pos': TEST_TARGET_POS_BTD1_UNITS[4]},
            {'name': 'REXPERT_BTD1_9', 'pos': TEST_TARGET_POS_BTD1_UNITS[5]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[6]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[7]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[8]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[9]},
        ])
        service = DivisionsService(self.emitter,
                                   self.config,
                                   self.storage)
        service.init()
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        # Act
        for unit in TEST_MISSION.units:
            self.emitter.gameplay_division_damage.on_next(DivisionDamage(
                123, TEST_MISSION.tvd_name, unit['name']))
        # Assert
        self.assertTrue(self._interceptor.points_gains)

    def test_kill_on_mission_start(self):
        "Отправляется сообщение об уничтоженных дивизиях в начале миссии"
        TEST_MISSION.units.extend([
            {'name': 'REXPERT_BTD1_3', 'pos': TEST_TARGET_POS_BTD1_UNITS[0]},
            {'name': 'REXPERT_BTD1_15', 'pos': TEST_TARGET_POS_BTD1_UNITS[1]},
        ])
        service = DivisionsService(self.emitter,
                                   self.config,
                                   self.storage)
        service.init()
        # Act
        self.emitter.campaign_mission.on_next(TEST_MISSION)
        # Assert
        self.assertTrue(self._interceptor.points_gains)

    def test_damage_notification(self):
        "Отправляется в чат оповещение об уничтожении секции укрепрайона"
        TEST_MISSION.units.extend([
            {'name': 'REXPERT_BTD1_3', 'pos': TEST_TARGET_POS_BTD1_UNITS[0]},
            {'name': 'REXPERT_BTD1_15', 'pos': TEST_TARGET_POS_BTD1_UNITS[1]},
            {'name': 'REXPERT_BTD1_2', 'pos': TEST_TARGET_POS_BTD1_UNITS[2]},
            {'name': 'REXPERT_BTD1_10', 'pos': TEST_TARGET_POS_BTD1_UNITS[3]},
            {'name': 'REXPERT_BTD1_17', 'pos': TEST_TARGET_POS_BTD1_UNITS[4]},
            {'name': 'REXPERT_BTD1_9', 'pos': TEST_TARGET_POS_BTD1_UNITS[5]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[6]},
            {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[7]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[8]},
            {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[9]},
        ])
        service = DivisionsService(self.emitter,
                                   self.config,
                                   self.storage)
        service.init()
        # Act
        self.emitter.gameplay_division_damage.on_next(DivisionDamage(
            123, TEST_MISSION.tvd_name, TEST_MISSION.units[0]['name']
        ))
        # Assert
        self.assertTrue(self._interceptor.commands)
