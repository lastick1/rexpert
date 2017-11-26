"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
import pathlib
import pymongo
from .airfield import ManageableAirfield, ID, NAME, TVD_NAME, POS


def _filter_by_id(airfield_id: str) -> dict:
    """Получить фильтр документов по ИД аэродрома"""
    return {ID: airfield_id}


def _filter_by_tvd(tvd_name: str) -> dict:
    """Получить фильтр по театру военных действий"""
    return {TVD_NAME: tvd_name}


def _update_request_body(document: dict) -> dict:
    """Построить запрос обновления документа"""
    return {'$set': document}


class AirfieldsController:
    def __init__(
            self,
            airfields: pymongo.collection.Collection
    ):
        self.__airfields = airfields
        self.airfields = dict()
        self._loaded_tvds = set()

    def _update(self, airfield: ManageableAirfield):
        """Обновить/создать аэродром в БД"""
        _filter = _filter_by_id(airfield.id)
        document = _update_request_body(airfield.to_dict())
        self.__airfields.update_one(_filter, document, upsert=True)

    def _load_by_tvd(self, tvd_name: str):
        """Загрузить аэродромы для ТВД из базы данных"""
        self.airfields[tvd_name] = list(
            ManageableAirfield(
                name=data[NAME],
                tvd_name=data[TVD_NAME],
                x=float(data[POS]['x']),
                z=float(data[POS]['z'])
            )
            for data in self.__airfields.find(_filter_by_tvd(tvd_name=tvd_name))
        )

    def get_airfield_in_radius(self, tvd_name: str, x: float, z: float, radius: int) -> ManageableAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        if tvd_name not in self._loaded_tvds:
            self._load_by_tvd(tvd_name=tvd_name)
        for airfield in self.airfields[tvd_name]:
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield

    def get_airfield_by_name(self, tvd_name: str, name: str) -> ManageableAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        if tvd_name not in self._loaded_tvds:
            self._load_by_tvd(tvd_name=tvd_name)
        for airfield in self.airfields[tvd_name]:
            if airfield.name == name:
                return airfield

    def initialize(self, tvd_name: str, fields_csv: pathlib.Path):
        """Инициализировать филды заданного ТВД"""
        self.__airfields.delete_many(_filter_by_tvd(tvd_name=tvd_name))
        with fields_csv.open() as stream:
            airfields = tuple(
                (lambda string: ManageableAirfield(name=string[0], tvd_name=tvd_name, x=string[1], z=string[2]))
                (line.split(sep=';'))
                for line in stream.readlines()
            )
        self.__airfields.insert_many(tuple(x.to_dict() for x in airfields))
