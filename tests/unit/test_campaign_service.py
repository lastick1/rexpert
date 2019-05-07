"""Тестирование управления кампанией"""
from __future__ import annotations
from typing import Dict
import unittest

from configs import Objects
from core import EventsEmitter
from services import CampaignService, \
    ObjectsService, \
    AircraftVendorService, \
    AirfieldsService, \
    GraphService, \
    WarehouseService, \
    TvdService
from storage import Storage
from processing import SourceParser

from tests.mocks import ConfigMock


class TestCampaignService(unittest.TestCase):
    "Тесты сервиса управления кампании"

    def setUp(self):
        "Настройка перед тестами"
        self.emitter: EventsEmitter = EventsEmitter()
        self.config: ConfigMock = ConfigMock()
        self.storage: Storage = Storage(self.config)
        self.objects_service: ObjectsService = ObjectsService(
            self.emitter,
            self.config,
            Objects()
        )
        self.vendor: AircraftVendorService = AircraftVendorService(self.config)
        self.airfields_service: AirfieldsService = AirfieldsService(
            self.emitter,
            self.config,
            self.storage,
            self.objects_service,
            self.vendor,
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
        self.source_parser: SourceParser = SourceParser(self.config)

    def test_sends_victory_input(self):
        "Отправляется server input на победу при наборе 13 очков"
        service = CampaignService(
            self.emitter,
            self.config,
            self.storage,
            self.airfields_service,
            self.tvd_services,
            self.source_parser,
        )
