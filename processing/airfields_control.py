"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
import pathlib
import pymongo
import configs
from processing.objects import Airfield, BotPilot
from .airfield import ManagedAirfield, ID, NAME, TVD_NAME, POS


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
            main: configs.Main,
            config: configs.Planes,
            airfields: pymongo.collection.Collection
    ):
        self.__airfields = airfields
        self._airfields = dict()
        self.planes = config
        self.main = main
        self._loaded_tvds = set()

    def _get_default_planes(self) -> dict:
        """Получить доступные на аэродроме самолёты на старте кампании"""
        return {str(name): self.planes.default[name] for name in self.planes.available}

    def _update(self, airfield: ManagedAirfield):
        """Обновить/создать аэродром в БД"""
        _filter = _filter_by_id(airfield.id)
        document = _update_request_body(airfield.to_dict())
        self.__airfields.update_one(_filter, document, upsert=True)

    def _load_by_tvd(self, tvd_name: str):
        """Загрузить аэродромы для ТВД из базы данных"""
        self._airfields[tvd_name] = list(
            ManagedAirfield(
                name=data[NAME],
                tvd_name=data[TVD_NAME],
                x=float(data[POS]['x']),
                z=float(data[POS]['z']),
                planes=self.planes.default
            )
            for data in self.__airfields.find(_filter_by_tvd(tvd_name=tvd_name))
        )

    def get_airfield_in_radius(self, tvd_name: str, x: float, z: float, radius: int) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        if tvd_name not in self._loaded_tvds:
            self._load_by_tvd(tvd_name=tvd_name)
        for airfield in self._airfields[tvd_name]:
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield

    def get_airfield_by_name(self, tvd_name: str, name: str) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        if tvd_name not in self._loaded_tvds:
            self._load_by_tvd(tvd_name=tvd_name)
        for airfield in self._airfields[tvd_name]:
            if airfield.name == name:
                return airfield

    def initialize(self, tvd_name: str, fields_csv: pathlib.Path):
        """Инициализировать филды заданного ТВД"""
        self.__airfields.delete_many(_filter_by_tvd(tvd_name=tvd_name))
        with fields_csv.open() as stream:
            airfields = tuple(
                (lambda string: ManagedAirfield(
                    name=string[0],
                    tvd_name=tvd_name,
                    x=string[1],
                    z=string[2],
                    planes=self._get_default_planes()
                ))
                (line.split(sep=';'))
                for line in stream.readlines()
            )
        self.__airfields.insert_many(tuple(x.to_dict() for x in airfields))

    def spawn(self, aircraft_name: str, tvd_name: str, airfield: Airfield):
        """Обработать появление самолёта на аэродроме"""
        xpos = airfield.pos['x']
        zpos = airfield.pos['z']
        managed_airfield = self.get_airfield_in_radius(tvd_name, xpos, zpos, self.main.airfield_radius)
        managed_airfield.planes[configs.Planes.name_to_key(aircraft_name)] -= 1
        self._update(managed_airfield)

    def finish(self, tvd_name: str, bot: BotPilot):
        """Обработать деспаун самолёта на аэродроме"""
        xpos = bot.aircraft.pos['x']
        zpos = bot.aircraft.pos['z']
        managed_airfield = self.get_airfield_in_radius(tvd_name, xpos, zpos, self.main.airfield_radius)
        if managed_airfield:
            managed_airfield.planes[configs.Planes.name_to_key(bot.aircraft.log_name)] += 1
            self._update(managed_airfield)

    def get_airfields(self, tvd_name: str) -> list:
        """Получить аэродромы для указанного ТВД"""
        if tvd_name in self._airfields:
            return self._airfields[tvd_name]
        self._airfields[tvd_name] = list(
            ManagedAirfield(
                name=data[NAME],
                tvd_name=data[TVD_NAME],
                x=float(data[POS]['x']),
                z=float(data[POS]['z']),
                planes=self._get_default_planes()
            )
            for data in self.__airfields.find(_filter_by_tvd(tvd_name=tvd_name))
        )
        return self._airfields[tvd_name]
