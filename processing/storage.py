"""Работа с БД"""
import pymongo

import configs
from processing import ManagedAirfield

ID = '_id'
TVD_NAME = 'tvd_name'


def _filter_by_id(_id: str) -> dict:
    """Получить фильтр документов по идентификатору"""
    return {ID: _id}


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


class Airfields(CollectionWrapper):
    """Работа с аэродромами"""
    @staticmethod
    def _filter_by_tvd(tvd_name: str) -> dict:
        """Получить фильтр по театру военных действий"""
        return {TVD_NAME: tvd_name}

    def update_airfield(self, managed_airfield: ManagedAirfield):
        """Обновить аэродром"""
        _filter = _filter_by_id(managed_airfield.id)
        update = _update_request_body(managed_airfield.to_dict())
        self.update_one(_filter, update)


class Storage:
    """Класс работы с БД"""
    def __init__(self, main: configs.Main):
        self._main = main
        self._mongo = pymongo.MongoClient(self._main.mongo_host, self._main.mongo_port)
        self.airfields = Airfields(self._mongo['Airfields'])
