"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
import configs
from processing.objects import BotPilot
from .airfield import ManagedAirfield
from .storage import Storage


class AirfieldsController:
    """Контроллер аэродромов"""
    def __init__(
            self,
            main: configs.Main,
            mgen: configs.Mgen,
            config: configs.Planes
    ):
        self.planes = config
        self.main = main
        self.mgen = mgen
        self.storage = Storage(main)

    def initialize_airfields(self, tvd):
        """Инициализировать аэродромы из файла"""
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
            self.storage.airfields.update_airfield(airfield)

    def get_airfield_in_radius(self, tvd_name: str, x: float, z: float, radius: int) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        for airfield in self.storage.airfields.load_by_tvd(tvd_name=tvd_name):
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield

    def get_airfield_by_name(self, tvd_name: str, name: str) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        for airfield in self.storage.airfields.load_by_tvd(tvd_name=tvd_name):
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
        self.storage.airfields.update_airfield(airfield)
