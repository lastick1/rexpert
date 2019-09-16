"""Тестирование управления кампанией"""
from __future__ import annotations
import unittest
from typing import Dict, List
from pathlib import Path
from datetime import datetime
from constants import DATE_FORMAT

from geometry import Point
from configs import Objects
from core import EventsEmitter, \
    Atype0, \
    Atype8, \
    Atype19, \
    PointsGain
from services import CampaignService, \
    ObjectsService, \
    GraphService, \
    WarehouseService, \
    TvdService
from model import SourceMission, CampaignMap, Division, ServerInput
from storage import Storage
from processing import SourceParser

from tests.mocks import ConfigMock, TvdMock, EventsInterceptor

TEST_TVD_NAME = 'moscow'
TEST_TVD_DATE = '01.01.1941'


def _parse_mock(name: str) -> SourceMission:
    """Фальшивый метод парсинга исходников"""
    return SourceMission(name=name, file=Path(), date=TEST_TVD_DATE, guimap=TEST_TVD_NAME)


def _get_tvd_mock(name: str) -> TvdMock:
    return TvdMock(name)


# pylint: disable=unused-argument
def _load_campaign_map_by_tvd_mock(tvd_name: str) -> CampaignMap:
    return CampaignMap(1, TEST_TVD_DATE, TEST_TVD_DATE, TEST_TVD_NAME, list(), list())

# pylint: disable=unused-argument
def _load_divisions_by_tvd_mock(tvd_name: str) -> List[Division]:
    return []

def _get_weakest_airfield_mock(contry: int):
    return Point()


class TestCampaignService(unittest.TestCase):
    "Тесты сервиса управления кампании"

    def setUp(self):
        "Настройка перед тестами"
        self.emitter: EventsEmitter = EventsEmitter()
        self.interceptor: EventsInterceptor = EventsInterceptor(self.emitter)
        self.config: ConfigMock = ConfigMock()
        self.storage: Storage = Storage(self.config.main)
        self.storage.divisions.load_by_tvd = _load_divisions_by_tvd_mock
        self.storage.campaign_maps.load_by_tvd_name = _load_campaign_map_by_tvd_mock
        self.update_calls: list = list()
        self.storage.campaign_maps.update = self.update_calls.append
        self.objects_service: ObjectsService = ObjectsService(
            self.emitter,
            self.config,
            Objects()
        )
        self.graph_service: GraphService = GraphService(
            self.emitter,
            self.config,
        )
        self.warehouses_service: WarehouseService = WarehouseService(
            self.emitter,
            self.config,
            self.storage,
        )
        self.tvd_services: Dict[str, TvdService] = {tvd_name: TvdService(tvd_name,
                                                                         self.config,
                                                                         self.storage,
                                                                         self.graph_service,
                                                                         self.warehouses_service)
                                                    for tvd_name in self.config.mgen.maps}
        for x in self.tvd_services:
            self.tvd_services[x].get_tvd = _get_tvd_mock
        self.source_parser: SourceParser = SourceParser(self.config)
        self.source_parser.parse_in_dogfight = _parse_mock

        self._pos: dict = {'x': 10.1, 'z': 11.1}

    def _init_new_service_instance(self) -> CampaignService:
        service = CampaignService(
            self.emitter,
            self.config,
            self.storage,
            self.tvd_services,
            self.source_parser,
        )
        service.init()
        return service

    def _make_atype0(self) -> Atype0:
        return Atype0(
            tik=0,
            date=datetime.strptime('01.10.1941', DATE_FORMAT),
            file_path=r'Multiplayer/Dogfight\result2.msnbin',
            game_type_id=2,
            countries=dict(),
            settings=(0, 0),
            mods=False,
            preset_id=0
        )

    def test_sends_victory_input(self):
        """Отправляет server input на победу в конце миссии при наборе 13 очков"""
        coal_id = 1
        atype0 = self._make_atype0()
        atype8 = Atype8(20, 1, coal_id, 4, True, 1, self._pos)
        self._init_new_service_instance()
        # Act
        self.emitter.events_mission_start.on_next(atype0)
        self.emitter.gameplay_points_gain.on_next(PointsGain(coal_id * 100 + 1, 13, atype8))
        self.emitter.events_round_end.on_next(Atype19(22))
        # Assert
        self.assertTrue(self.interceptor.commands)
        self.assertIsInstance(self.interceptor.commands[0], ServerInput)

    def test_update_campaign_map(self):
        """Обновляет карту кампании при старте миссии"""
        self._init_new_service_instance()
        # Act
        self.emitter.events_mission_start.on_next(self._make_atype0())
        # Assert
        self.assertTrue(self.update_calls)

    def test_emits_current_tvd(self):
        """Отправляет объект ТВД при старте миссии"""
        tvds = []
        self.emitter.current_tvd.subscribe_(tvds.append)
        self._init_new_service_instance()
        # Act
        self.emitter.events_mission_start.on_next(self._make_atype0())
        # Assert
        self.assertTrue(tvds)

    def test_emits_mission(self):
        """Отправляет объект миссии при старте миссии"""
        missions = []
        self.emitter.campaign_mission.subscribe_(missions.append)
        self._init_new_service_instance()
        # Act
        self.emitter.events_mission_start.on_next(self._make_atype0())
        # Assert
        self.assertTrue(missions)

    def test_emits_mission_victory(self):
        """Отправляет победившую страну в миссии в конце раунда"""
        emissions = []
        coal_id = 1
        atype8 = Atype8(20, 1, coal_id, 4, True, 1, self._pos)
        self.emitter.mission_victory.subscribe_(emissions.append)
        self._init_new_service_instance()
        # Act
        self.emitter.events_mission_start.on_next(self._make_atype0())
        self.emitter.gameplay_points_gain.on_next(PointsGain(coal_id * 100 + 1, 13, atype8))
        self.emitter.events_round_end.on_next(Atype19(22))
        # Assert
        self.assertTrue(emissions)
        self.assertEqual(emissions[0], coal_id * 100 + 1)
