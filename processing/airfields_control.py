"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
import configs
import log_objects
from .airfield import ManagedAirfield
from .storage import Storage


class AirfieldsController:
    """Контроллер аэродромов"""
    def __init__(
            self,
            config: configs.Config
    ):
        self.config = config
        self.storage = Storage(config.main)

    @staticmethod
    def initialize_managed_airfields(airfields_data: list) -> list:
        """Инициализировать список управляемых аэродромов из данных конфигурации"""
        return list(
            ManagedAirfield(
                name=data['name'],
                tvd_name=data['tvd_name'],
                x=data['x'],
                z=data['z'],
                planes=dict())
            for data in airfields_data)

    def get_airfield_in_radius(self, tvd_name: str, x: float, z: float, radius: int) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        for airfield in self.storage.airfields.load_by_tvd(tvd_name=tvd_name):
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield

    def spawn(self, tvd, aircraft_name: str, xpos: float, zpos: float):
        """Обработать появление самолёта на аэродроме"""
        managed_airfield = self.get_airfield_in_radius(tvd.name, xpos, zpos, self.config.gameplay.airfield_radius)
        self.add_aircraft(tvd, managed_airfield.name, aircraft_name, -1)

    def finish(self, tvd, bot: log_objects.BotPilot):
        """Обработать деспаун самолёта на аэродроме"""
        xpos = bot.aircraft.pos['x']
        zpos = bot.aircraft.pos['z']
        managed_airfield = self.get_airfield_in_radius(tvd.name, xpos, zpos, self.config.gameplay.airfield_radius)
        if managed_airfield:
            self.add_aircraft(tvd, managed_airfield.name, bot.aircraft.log_name, 1)

    @staticmethod
    def get_country(airfield, tvd) -> int:
        """Получить страну аэродрома в соответствии с графом"""
        return tvd.get_country(airfield)

    def _add_aircraft(self, airfield, airfield_country, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром без сохранения в БД"""
        aircraft_key = self.config.planes.name_to_key(aircraft_name)
        aircraft_country = self.config.planes.cfg['uncommon'][aircraft_name.lower()]['country']
        if aircraft_country == airfield_country:
            if aircraft_key not in airfield.planes:
                airfield.planes[aircraft_key] = 0
            airfield.planes[aircraft_key] += aircraft_count

    def add_aircraft(self, tvd, airfield_name: str, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром"""
        airfield = self.storage.airfields.load_by_name(tvd.name, airfield_name)
        airfield_country = tvd.get_country(airfield)
        self._add_aircraft(airfield, airfield_country, aircraft_name, aircraft_count)
        self.storage.airfields.update_airfield(airfield)
