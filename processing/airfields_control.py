"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
import atypes
import log_objects
from .airfield import ManagedAirfield


class AirfieldsController:
    """Контроллер аэродромов"""
    def __init__(self, ioc):
        self._ioc = ioc

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
        for airfield in self._ioc.storage.airfields.load_by_tvd(tvd_name=tvd_name):
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield

    def spawn_aircraft(self, tvd_name: str, airfield_country: int, atype: atypes.Atype10):
        """Обработать появление самолёта на аэродроме"""
        managed_airfield = self.get_airfield_in_radius(
            tvd_name, atype.pos['x'], atype.pos['z'], self._ioc.config.gameplay.airfield_radius)
        self.add_aircraft(tvd_name, airfield_country, managed_airfield.name, atype.aircraft_name, -1)

    def finish(self, tvd_name: str, airfield_country: int, bot: log_objects.BotPilot):
        """Обработать деспаун самолёта на аэродроме"""
        xpos = bot.aircraft.pos['x']
        zpos = bot.aircraft.pos['z']
        managed_airfield = self.get_airfield_in_radius(tvd_name, xpos, zpos, self._ioc.config.gameplay.airfield_radius)
        if managed_airfield:
            self.add_aircraft(tvd_name, airfield_country, managed_airfield.name, bot.aircraft.log_name, 1)

    @staticmethod
    def get_country(airfield, tvd) -> int:
        """Получить страну аэродрома в соответствии с графом"""
        return tvd.get_country(airfield)

    def _add_aircraft(self, airfield, airfield_country: int, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром без сохранения в БД"""
        aircraft_key = self._ioc.config.planes.name_to_key(aircraft_name)
        aircraft_country = self._ioc.config.planes.cfg['uncommon'][aircraft_name.lower()]['country']
        if aircraft_country == airfield_country:
            if aircraft_key not in airfield.planes:
                airfield.planes[aircraft_key] = 0
            airfield.planes[aircraft_key] += aircraft_count

    def add_aircraft(
            self, tvd_name: str, airfield_country: int, airfield_name: str, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром"""
        airfield = self._ioc.storage.airfields.load_by_name(tvd_name, airfield_name)
        self._add_aircraft(airfield, airfield_country, aircraft_name, aircraft_count)
        self._ioc.storage.airfields.update_airfield(airfield)

    def end_round(self):
        """Обработать завершение раунда - перераспределить самолёты с тылового на фронтовые аэродромы"""
        raise NotImplemented
