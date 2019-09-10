"""Контейнер зависимостей"""
from __future__ import annotations
from typing import Dict

from pathlib import Path
from core import EventsEmitter
from configs import Config, Objects
from rcon import DServerRcon
from storage import Storage
from services import ObjectsService, \
    PlayersService, \
    GroundTargetsService, \
    GraphService, \
    WarehouseService, \
    AircraftVendorService, \
    AirfieldsService, \
    DivisionsService, \
    TvdService, \
    DServerService, \
    CampaignService, \
    GeneratorService
from processing import SourceParser, \
    Generator
from reader import LogsReaderRx


class AppBase:
    "Базовый класс приложения со всеми зависимостями"

    def __init__(self, main_json: Path):
        self.config: Config = Config(main_json)
        self.objects: Objects = Objects()
        self.events_emitter: EventsEmitter = EventsEmitter()
        self.rcon: DServerRcon = DServerRcon(
            self.config.main.rcon_ip,
            self.config.main.rcon_port,
        )
        self.storage: Storage = Storage(self.config.main)
        self.objects_service: ObjectsService = ObjectsService(
            self.events_emitter,
            self.config,
            self.objects,
        )
        self.players_service: PlayersService = PlayersService(
            self.events_emitter,
            self.config,
            self.storage,
            self.objects_service
        )
        self.graph_service: GraphService = GraphService(
            self.events_emitter,
            self.config,
        )
        self.warehouse_service: WarehouseService = WarehouseService(
            self.events_emitter,
            self.config,
            self.storage,
        )
        self.aircrafts_vendor_service: AircraftVendorService = AircraftVendorService(
            self.config,
        )
        self.airfields_service: AirfieldsService = AirfieldsService(
            self.events_emitter,
            self.config,
            self.storage,
            self.aircrafts_vendor_service,
        )
        self.divisions_service: DivisionsService = DivisionsService(
            self.events_emitter,
            self.config,
            self.storage
        )
        self.tvd_services: Dict[str, TvdService] = {tvd_name: TvdService(tvd_name,
                                                                         self.config,
                                                                         self.storage,
                                                                         self.graph_service,
                                                                         self.warehouse_service)
                                                    for tvd_name in self.config.mgen.maps}
        self.source_parser: SourceParser = SourceParser(self.config)
        self.generator: Generator = Generator(self.config)
        self.campaign_service: CampaignService = CampaignService(
            self.events_emitter,
            self.config,
            self.storage,
            self.tvd_services,
            self.source_parser
        )
        self.ground_targets_service: GroundTargetsService = GroundTargetsService(
            self.events_emitter,
            self.config,
            self.objects_service,
        )
        self.dserver_service: DServerService = DServerService(
            self.events_emitter,
            self.config
        )
        self.generator_service: GeneratorService = GeneratorService(
            self.events_emitter,
            self.config,
            self.storage,
            self.generator,
            self.divisions_service,
            self.tvd_services
        )
        self.reader: LogsReaderRx = LogsReaderRx(
            self.config,
            self.events_emitter,
            self.airfields_service
        )
        self.objects_service.init()
        self.campaign_service.init()
        self.airfields_service.init()
        self.ground_targets_service.init()
        self.players_service.init()
        self.divisions_service.init()
        self.warehouse_service.init()
        self.dserver_service.init()
        self.graph_service.init()
        self.generator_service.init()
