"""Работа с БД"""
import pymongo

import configs
from .airfield import ManagedAirfield, NAME, PLANES, POS
from .player import Player
from .campaign import CampaignMap, ORDER, DATE, MISSION_DATE, MONTHS

ID = '_id'
TVD_NAME = 'tvd_name'


def _filter_by_id(_id: str) -> dict:
    """Получить фильтр документов по идентификатору"""
    return {ID: _id}


def _filter_by_tvd(tvd_name: str) -> dict:
    """Получить фильтр документов по театру военных действий (ТВД)"""
    return {TVD_NAME: tvd_name}


def _update_request_body(document: dict) -> dict:
    """Построить запрос обновления документа"""
    return {'$set': document}


class CollectionWrapper:
    """Класс работы с коллекцией"""
    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection

    def update_one(self, _filter, document):
        """Обновить документ в коллекции"""
        self.collection.update_one(_filter, document, upsert=True)


class CampaignMaps(CollectionWrapper):
    """Работа с документами карт кампании в БД"""
    @staticmethod
    def _convert_from_document(document) -> CampaignMap:
        """Конвертировать документ из БД в объект класса карты кампании"""
        return CampaignMap(
            order=document[ORDER],
            date=document[DATE],
            mission_date=document[MISSION_DATE],
            tvd_name=document[TVD_NAME],
            months=document[MONTHS]
        )

    def update(self, campaign_map: CampaignMap):
        """Обновить/создать документ в БД"""
        self.collection.update_one(
            {TVD_NAME: campaign_map.tvd_name}, _update_request_body(campaign_map.to_dict()), upsert=True)

    def load_all(self):
        """Загрузить все данные по картам кампаний"""
        return list(self._convert_from_document(document)
                    for document in self.collection.find()
                    .sort(ORDER, pymongo.ASCENDING))


class Players(CollectionWrapper):
    """Работа с документами игроков в БД"""
    def count(self, account_id) -> int:
        """Посчитать документы игрока в БД"""
        _filter = _filter_by_id(account_id)
        return self.collection.count(_filter)

    def find(self, account_id) -> Player:
        """Найти документ игрока в БД"""
        _filter = _filter_by_id(account_id)
        document = self.collection.find_one(_filter)
        return Player(account_id, document)

    def update(self, player: Player):
        """Обновить/создать игрока в БД"""
        _filter = _filter_by_id(player.account_id)
        document = _update_request_body(player.to_dict())
        self.collection.update_one(_filter, document, upsert=True)


class Airfields(CollectionWrapper):
    """Работа с документами аэродромов в БД"""
    @staticmethod
    def _filter_by_tvd(tvd_name: str) -> dict:
        """Получить фильтр по театру военных действий"""
        return {TVD_NAME: tvd_name}

    def update_airfield(self, managed_airfield: ManagedAirfield):
        """Обновить аэродром"""
        _filter = _filter_by_id(managed_airfield.id)
        update = _update_request_body(managed_airfield.to_dict())
        self.update_one(_filter, update)

    @staticmethod
    def _convert_from_document(document) -> ManagedAirfield:
        """Конвертировать документ из БД в объект класса управляемого аэродрома"""
        return ManagedAirfield(
            name=document[NAME],
            tvd_name=document[TVD_NAME],
            x=float(document[POS]['x']),
            z=float(document[POS]['z']),
            planes=document[PLANES]
        )

    def load_by_id(self, airfield_id) -> ManagedAirfield:
        """Загрузить аэродром по его идентификатору из базы данных"""
        return self._convert_from_document(self.collection.find_one(_filter_by_id(_id=airfield_id)))

    def load_by_tvd(self, tvd_name: str) -> list:
        """Загрузить аэродромы для ТВД из базы данных"""
        return list(self._convert_from_document(document)
                    for document in self.collection.find(_filter_by_tvd(tvd_name=tvd_name)))


class Storage:
    """Класс работы с БД"""
    def __init__(self, main: configs.Main):
        self._main = main
        self._mongo = pymongo.MongoClient(self._main.mongo_host, self._main.mongo_port)
        self._database = self._mongo[main.mongo_database]
        self.airfields = Airfields(self._database['Airfields'])
        self.players = Players(self._database['Players'])
        self.campaign_maps = CampaignMaps(self._database['CampaignMaps'])

    def drop_database(self):
        """Удалить базу данных (использовать только в тестах)"""
        self._mongo.drop_database(self._main.mongo_database)
