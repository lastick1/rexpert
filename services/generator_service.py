"Сервис управления генерацией миссий"
from __future__ import annotations
from typing import Dict

from core import EventsEmitter, Generation
from configs import Config
from storage import Storage
from processing import Generator

from .base_event_service import BaseEventService
from .tvd_service import TvdService
from .divisions_service import DivisionsService


class GeneratorService(BaseEventService):
    "Сервис управления генерацией миссий"

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config,
            storage: Storage,
            generator: Generator,
            divisions_service: DivisionsService,
            tvd_services: Dict[str, TvdService]
    ):
        super().__init__(emitter)
        self._config: Config = config
        self._storage: Storage = storage
        self._generator: Generator = generator
        self._divisions_service: DivisionsService = divisions_service
        self._tvd_services: Dict[str, TvdService] = tvd_services

    def init(self) -> None:
        self.register_subscription(
            self.emitter.generations.subscribe_(self._generate)
        )

    def _generate(self, generation: Generation) -> None:
        "Обработать сообщение генерации миссии"
        self.generate(
            generation.mission_name,
            generation.mission_date,
            generation.tvd_name
        )

    def generate(self, mission_name: str, date: str, tvd_name: str):
        """Сгенерировать миссию для указанной даты и ТВД кампании"""
        tvd_builder: TvdService = self._tvd_services[tvd_name]
        tvd = tvd_builder.get_tvd(date)
        airfields = self._storage.airfields.load_by_tvd(tvd_name)
        tvd_builder.update(
            tvd, self._divisions_service.filter_airfields(tvd_name, airfields))
        self._generator.make_ldb(tvd_name)
        self._generator.make_lgb(tvd_name)

        mission_template: str = str(self._config.mgen.tvd_folders[tvd_name].joinpath(
            self._config.mgen.cfg[tvd_name]['mission_template']).absolute())

        self._generator.make_mission(mission_template, mission_name, tvd_name)
