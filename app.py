"Приложение"
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from app_base import AppBase
from model import CampaignMap
from constants import DATE_FORMAT


START_DATE = 'start_date'


class App(AppBase):
    "Основной класс приложения"

    def generate(self, mission_name: str, date: str, tvd_name: str):
        "Сгенерировать миссию"
        self.generator_service.generate(mission_name, date, tvd_name)

    def initialize_map(self, tvd_name: str):
        """Инициализировать карту кампании"""
        self.graph_service.initialize(tvd_name)
        self.warehouse_service.initialize_warehouses(tvd_name)
        start = self.config.mgen.cfg[tvd_name][START_DATE]
        order = list(self.config.mgen.maps).index(tvd_name) + 1
        campaign_map = CampaignMap(
            order=order, date=start, mission_date=start, tvd_name=tvd_name, months=list())
        tvd = self.tvd_services[campaign_map.tvd_name].get_tvd(
            campaign_map.date.strftime(DATE_FORMAT))
        self.airfields_service.initialize_tvd(tvd, campaign_map)
        self.storage.campaign_maps.update(campaign_map)
        self.divisions_service.initialize_divisions(tvd_name)
        logging.info(f'{tvd_name} initialized')

    def initialize_campaign(self) -> None:
        """Инициализировать кампанию в БД, обновить файлы в data/scg и сгенерировать первую миссию"""
        scg_path = Path(
            self.config.main.game_folder.joinpath('data/scg'))
        if not scg_path.exists():
            logging.info('Copy data/scg to game/data/scg.')
            shutil.copytree(r'./data/scg', str(scg_path.absolute()))
        for tvd_name in self.config.mgen.maps:
            self.initialize_map(tvd_name)

        campaign_map = self.storage.campaign_maps.load_by_order(2)
        self.generate('result1',
                      campaign_map.date.strftime(DATE_FORMAT),
                      campaign_map.tvd_name)
        self.players_service.reset()

    def reset(self):
        """Сбросить состояние кампании"""
        self.storage.airfields.collection.drop()
        self.storage.campaign_maps.collection.drop()
        self.storage.campaign_missions.collection.drop()
        self.storage.divisions.collection.drop()
        self.storage.warehouses.collection.drop()
        logging.info('Database cleaned.')
