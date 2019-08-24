import pymongo
from configs import Main
from .airfields import Airfields
from .campaign_maps import CampaignMaps
from .campaign_missions import CampaignMissions
from .divisions import Divisions
from .players import Players
from .warehouses import Warehouses


class Storage:
    """Класс работы с БД"""

    def __init__(self, main: Main):
        if not main:
            print('main: {}'.format(main))
        self._main = main
        self._mongo = pymongo.MongoClient(
            self._main.mongo_host, self._main.mongo_port)
        self._database = self._mongo[main.mongo_database]
        self.airfields = Airfields(self._database[Airfields.__name__])
        self.players = Players(self._database[Players.__name__])
        self.campaign_maps = CampaignMaps(
            self._database[CampaignMaps.__name__])
        self.campaign_missions = CampaignMissions(
            self._database[CampaignMissions.__name__])
        self.divisions = Divisions(self._database[Divisions.__name__])
        self.warehouses = Warehouses(self._database[Warehouses.__name__])

    def drop_database(self):
        """Удалить базу данных (использовать только в тестах)"""
        self._mongo.drop_database(self._main.mongo_database)
