"""Классы для работы с БД"""
import pymongo
from configs import Main
from .airfields import Airfields
from .campaign_maps import CampaignMaps
from .campaign_missions import CampaignMissions
from .divisions import Divisions
from .players import Players
from .warehouses import Warehouses


class StorageBase:
    """Базовый класс для работы с БД"""

    def __init__(self, main: Main):
        self._database_name = main.mongo_database
        self._host = main.mongo_host
        self._port = main.mongo_port
        self._mongo = pymongo.MongoClient(self._host, self._port)
        self._database = None

    @property
    def database(self):
        """Объектная модель БД"""
        if not self._database:
            self._database = self._mongo[self._database_name]
        return self._database

    def drop_database(self):
        """Удалить базу данных (использовать только в тестах)"""
        self._mongo.drop_database(self._database_name)


class Storage(StorageBase):
    """Класс работы с БД"""

    def __init__(self, main: Main):
        super().__init__(main)
        self._airfields: Airfields = None
        self._players: Players = None
        self._campaign_maps: CampaignMaps = None
        self._campaign_missions: CampaignMissions = None
        self._divisions: Divisions = None
        self._warehouses: Warehouses = None

    @property
    def airfields(self):
        """Коллекция аэродромов"""
        if not self._airfields:
            self._airfields = Airfields(self.database[Airfields.__name__])
        return self._airfields

    @property
    def players(self):
        """Коллекция игроков"""
        if not self._players:
            self._players = Players(self.database[Players.__name__])
        return self._players

    @property
    def campaign_maps(self):
        """Коллекция карт кампании"""
        if not self._campaign_maps:
            self._campaign_maps = CampaignMaps(self.database[CampaignMaps.__name__])
        return self._campaign_maps

    @property
    def campaign_missions(self):
        """Коллекция миссий кампании"""
        if not self._campaign_missions:
            self._campaign_missions = CampaignMissions(self.database[CampaignMissions.__name__])
        return self._campaign_missions

    @property
    def divisions(self):
        """Коллекция дивизий"""
        if not self._divisions:
            self._divisions = Divisions(self.database[Divisions.__name__])
        return self._divisions

    @property
    def warehouses(self):
        """Коллекция складов"""
        if not self._warehouses:
            self._warehouses = Warehouses(self.database[Warehouses.__name__])
        return self._warehouses
