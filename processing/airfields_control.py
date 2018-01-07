"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
import pymongo
import configs
from processing.objects import Airfield, BotPilot
from .airfield import ManagedAirfield, ID, NAME, TVD_NAME, POS, PLANES


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
            mgen: configs.Mgen,
            config: configs.Planes,
            airfields: pymongo.collection.Collection
    ):
        self.__airfields = airfields
        self.planes = config
        self.main = main
        self.mgen = mgen
        self._loaded_tvds = set()

    def _update(self, airfield: ManagedAirfield):
        """Обновить/создать аэродром в БД"""
        _filter = _filter_by_id(airfield.id)
        document = _update_request_body(airfield.to_dict())
        self.__airfields.update_one(_filter, document, upsert=True)

    def _load_by_tvd(self, tvd_name: str) -> list:
        """Загрузить аэродромы для ТВД из базы данных"""
        return list(
            ManagedAirfield(
                name=data[NAME],
                tvd_name=data[TVD_NAME],
                x=float(data[POS]['x']),
                z=float(data[POS]['z']),
                planes=data[PLANES]
            )
            for data in self.__airfields.find(_filter_by_tvd(tvd_name=tvd_name))
        )

    def initialize_airfields(self, tvd):
        with self.mgen.af_csv[tvd.name].open() as stream:
            airfields = list(
                (lambda string: ManagedAirfield(
                    name=string[0],
                    tvd_name=tvd.name,
                    x=float(string[1]),
                    z=float(string[2]),
                    planes=dict()
                ))
                (line.split(sep=';'))
                for line in stream.readlines()
            )
        for airfield in airfields:
            for aircraft_name in self.planes.cfg['uncommon']:
                aircraft = self.planes.cfg['uncommon'][aircraft_name]
                self._add_aircraft(airfield, tvd.get_country(airfield), aircraft_name, aircraft['_default_number'])
            self._update(airfield)

    def get_airfield_in_radius(self, tvd_name: str, x: float, z: float, radius: int) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        for airfield in self._load_by_tvd(tvd_name=tvd_name):
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield

    def get_airfield_by_name(self, tvd_name: str, name: str) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        for airfield in self._load_by_tvd(tvd_name=tvd_name):
            if airfield.name == name:
                return airfield

    def spawn(self, tvd, aircraft_name: str, xpos: float, zpos: float):
        """Обработать появление самолёта на аэродроме"""
        managed_airfield = self.get_airfield_in_radius(tvd.name, xpos, zpos, self.main.airfield_radius)
        self.add_aircraft(tvd, managed_airfield.name, aircraft_name, -1)

    def finish(self, tvd, bot: BotPilot):
        """Обработать деспаун самолёта на аэродроме"""
        xpos = bot.aircraft.pos['x']
        zpos = bot.aircraft.pos['z']
        managed_airfield = self.get_airfield_in_radius(tvd.name, xpos, zpos, self.main.airfield_radius)
        if managed_airfield:
            self.add_aircraft(tvd, managed_airfield.name, bot.aircraft.log_name, 1)

    def get_airfields(self, tvd_name: str) -> list:
        """Получить аэродромы для указанного ТВД"""
        return list(
            ManagedAirfield(
                name=data[NAME],
                tvd_name=data[TVD_NAME],
                x=float(data[POS]['x']),
                z=float(data[POS]['z']),
                planes=data[PLANES]
            )
            for data in self.__airfields.find(_filter_by_tvd(tvd_name=tvd_name)))

    @staticmethod
    def get_country(airfield, tvd) -> int:
        """Получить страну аэродрома в соответствии с графом"""
        return tvd.get_country(airfield)

    def _add_aircraft(self, airfield, airfield_country, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром без сохранения в БД"""
        aircraft_key = self.planes.name_to_key(aircraft_name)
        aircraft_country = self.planes.cfg['uncommon'][aircraft_name.lower()]['country']
        if aircraft_country == airfield_country:
            if aircraft_key not in airfield.planes:
                airfield.planes[aircraft_key] = 0
            airfield.planes[aircraft_key] += aircraft_count

    def add_aircraft(self, tvd, airfield_name: str, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром"""
        airfield = self.get_airfield_by_name(tvd.name, airfield_name)
        airfield_country = tvd.get_country(airfield)
        self._add_aircraft(airfield, airfield_country, aircraft_name, aircraft_count)
        self._update(airfield)

    def update_airfields(self, managed_airfields: list):
        """Обновить аэродромы"""
        for airfield in managed_airfields:
            self._update(airfield)
