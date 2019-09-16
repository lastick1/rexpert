"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
from __future__ import annotations
from typing import List
import logging
import json

from core import EventsEmitter, Atype0, Atype9, Spawn, Finish, Capture
from constants import INVERT
from configs import Config
from storage import Storage
from model import ManagedAirfield, Tvd, CampaignMap

from .base_event_service import BaseEventService
from .aircrafts_vendor_service import AircraftVendorService


class AirfieldsService(BaseEventService):
    """Контроллер аэродромов"""

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config,
            storage: Storage,
            aircrafts_vendor_service: AircraftVendorService
    ):
        super().__init__(emitter)
        self._config: Config = config
        self._storage: Storage = storage
        self._aircrafts_vendor_service: AircraftVendorService = aircrafts_vendor_service
        self._current_tvd: Tvd = None
        self.current_airfields = list()

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.current_tvd.subscribe_(self._update_current_tvd),
            self.emitter.events_mission_start.subscribe_(self.start_mission),
            self.emitter.events_airfield.subscribe_(self.spawn_airfield),
            self.emitter.sortie_spawn.subscribe_(self.spawn_aircraft),
            self.emitter.sortie_deinitialize.subscribe_(self._finish),
            self.emitter.mission_victory.subscribe_(self._mission_victory),
        ])

    def _update_current_tvd(self, tvd: Tvd) -> None:
        self._current_tvd = tvd

    def initialize_managed_airfields(self, tvd_name: str) -> List[ManagedAirfield]:
        """Инициализировать список управляемых аэродромов из данных конфигурации"""
        return list(
            ManagedAirfield(
                name=data['name'],
                tvd_name=data['tvd_name'],
                x=data['x'],
                z=data['z'],
                planes=dict())
            for data in self._config.mgen.airfields_data[tvd_name])

    def get_airfield_in_radius(self, tvd_name: str, x: float, z: float, radius: int) -> ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        for airfield in self._storage.airfields.load_by_tvd(tvd_name=tvd_name):
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield
        return None

    def is_on_airfield(self, x: float, z: float, country: int) -> bool:
        """Находится ли точка на аэродроме страны"""
        airfield = self.get_airfield_in_radius(self._current_tvd.name, x, z, self._config.gameplay.airfield_radius)
        if airfield:
            return self._current_tvd.get_country(airfield) == country
        return False

    def get_airfield_by_name(self, tvd_name: str, airfield_name) -> ManagedAirfield:
        """Получить аэродром по имени"""
        return self._storage.airfields.load_by_name(tvd_name, airfield_name)

    def start_mission(self, atype: Atype0):
        """Обработать начало миссии"""
        self.current_airfields.clear()
        mission_airfields = list()
        for airfield in self._storage.airfields.load_by_tvd(tvd_name=self._current_tvd.name):
            mission_airfields.append({
                'country': self._current_tvd.get_country(airfield),
                'name': airfield.name,
                'x': airfield.x,
                'z': airfield.z
            })
        with open(self._config.stat.current_airfields, mode='w') as stream:
            stream.write(json.dumps(mission_airfields))

    def spawn_aircraft(self, spawn: Spawn):
        """Обработать появление самолёта на аэродроме"""
        managed_airfield = self.get_airfield_in_radius(
            self._current_tvd.name,
            spawn.point.x,
            spawn.point.z,
            self._config.gameplay.airfield_radius
        )
        if not managed_airfield:
            logging.warning(f'airfield not found: {spawn}')
        else:
            self.add_aircraft(
                self._current_tvd.name,
                self._current_tvd.get_country(managed_airfield),
                managed_airfield.name,
                spawn.aircraft_name,
                -1
            )

    def _finish(self, finish: Finish) -> None:
        """Обработать деспаун самолёта на аэродроме"""
        managed_airfield = self.get_airfield_in_radius(
            self._current_tvd.name,
            finish.point.x,
            finish.point.z,
            self._config.gameplay.airfield_radius
        )
        if managed_airfield:
            self.add_aircraft(
                self._current_tvd.name,
                self._current_tvd.get_country(finish.point),
                managed_airfield.name,
                finish.aircraft_name,
                1
            )

    def _add_aircraft(self, airfield, airfield_country: int, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром без сохранения в БД"""
        aircraft_key = self._config.planes.name_to_key(aircraft_name)
        aircraft_country = self._config.planes.cfg['uncommon'][aircraft_name.lower()]['country']
        if aircraft_country == airfield_country:
            if aircraft_key not in airfield.planes:
                airfield.planes[aircraft_key] = 0
            airfield.planes[aircraft_key] += aircraft_count

    def add_aircraft(
            self, tvd_name: str, airfield_country: int, airfield_name: str, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром"""
        airfield = self._storage.airfields.load_by_name(
            tvd_name, airfield_name)
        self._add_aircraft(airfield, airfield_country,
                           aircraft_name, aircraft_count)
        self._storage.airfields.update_airfield(airfield)

    def end_round(self):
        """Обработать завершение раунда - перераспределить самолёты с тылового на фронтовые аэродромы"""
        front = self._current_tvd.to_country_dict_front(self.current_airfields)
        rear = self._current_tvd.to_country_dict_rear(self.current_airfields)
        for country in (101, 201):
            self._aircrafts_vendor_service.transfer_to_front(
                front[country], rear[country])
        self._storage.airfields.update_airfields(self.current_airfields)

    def initialize_tvd(self, tvd: Tvd, campaign_map: CampaignMap):
        """Инициализировать аэродромы указанного ТВД"""
        airfields = self.initialize_managed_airfields(campaign_map.tvd_name)
        supply = self._aircrafts_vendor_service.get_month_supply(
            campaign_map.current_month, campaign_map)
        self._aircrafts_vendor_service.deliver_month_supply(
            campaign_map, tvd.to_country_dict_rear(airfields), supply)
        self._aircrafts_vendor_service.initial_front_supply(
            campaign_map, tvd.to_country_dict_front(airfields))
        self._storage.airfields.update_airfields(airfields)

    def spawn_airfield(self, atype: Atype9):
        """Обработать появление аэродрома в начале миссии"""
        airfield = self.get_airfield_in_radius(
            self._current_tvd.name, atype.point.x, atype.point.z, 50)
        if airfield:
            self.current_airfields.append(airfield)
        else:
            raise NameError(f'Аэродром не найден:{self._current_tvd.name}{{"x":{atype.point.x}, "z":{atype.point.z}}}')

    @property
    def inactive_airfield_by_countries(self) -> dict:
        "Список неактивных аэродромов по странам"
        current_names = set({x.name for x in self.current_airfields})
        inactive = list([x for x in self._storage.airfields.load_by_tvd(
            tvd_name=self._current_tvd.name) if x.name not in current_names])
        result = {101: list(), 201: list()}
        for airfield in inactive:
            result[self._current_tvd.get_country(airfield)].append(airfield)
        return result

    def get_weakest_airfield(self, country: int) -> ManagedAirfield:
        "Самый слабый аэродром"
        result: ManagedAirfield = None
        for managed_airfield in self.current_airfields:
            if country == self._current_tvd.get_country(managed_airfield):
                if not result:
                    result = managed_airfield
                if result.planes_count > managed_airfield.planes_count:
                    result = managed_airfield
        return result

    def _mission_victory(self, country: int) -> None:
        """Обработать победу стороны в миссии"""
        if country:
            airfield: ManagedAirfield = self.get_weakest_airfield(INVERT[country])
            self.emitter.gameplay_capture.on_next(Capture(airfield.tvd_name, country, airfield))
