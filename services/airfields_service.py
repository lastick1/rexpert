"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
from __future__ import annotations
import logging
import json

from core import EventsEmitter, Atype0, Atype9, Atype10, Atype16, Finish
from configs import Config
from log_objects import BotPilot
from storage import Storage
from model import ManagedAirfield, Tvd, CampaignMap

from .base_event_service import BaseEventService
from .aircrafts_vendor_service import AircraftVendorService
from .objects_service import ObjectsService


class AirfieldsService(BaseEventService):
    """Контроллер аэродромов"""

    def __init__(self,
                 emitter: EventsEmitter,
                 config: Config,
                 storage: Storage,
                 objects_service: ObjectsService,
                 aircrafts_vendor_service: AircraftVendorService):
        super().__init__(emitter)
        self._config: Config = config
        self._storage: Storage = storage
        self._objects_service: ObjectsService = objects_service
        self._aircrafts_vendor_service: AircraftVendorService = aircrafts_vendor_service
        self._current_tvd: Tvd = None
        self.current_airfields = list()

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.current_tvd.subscribe_(self._update_current_tvd),
            self.emitter.events_bot_deinitialization.subscribe_(self._finish),
        ])

    def _update_current_tvd(self, tvd: Tvd) -> None:
        self._current_tvd = tvd

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
        for airfield in self._storage.airfields.load_by_tvd(tvd_name=tvd_name):
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield
        return None

    def get_airfield_by_name(self, tvd_name: str, airfield_name) -> ManagedAirfield:
        """Получить аэродром по имени"""
        return self._storage.airfields.load_by_name(tvd_name, airfield_name)

    def start_mission(self):
        """Обработать начало миссии"""
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
        self.current_airfields.clear()

    def spawn_aircraft(self, tvd_name: str, airfield_country: int, atype: Atype10):
        """Обработать появление самолёта на аэродроме"""
        managed_airfield = self.get_airfield_in_radius(
            tvd_name, atype.pos['x'], atype.pos['z'], self._config.gameplay.airfield_radius)
        if not managed_airfield:
            logging.warning(f'airfield not found: {atype}')
        else:
            self.add_aircraft(tvd_name, airfield_country,
                              managed_airfield.name, atype.aircraft_name, -1)

    def _finish(self, atype: Atype16) -> None:
        """Обработать деспаун самолёта на аэродроме"""
        bot: BotPilot = self._objects_service.get_bot(atype.bot_id)
        managed_airfield = self.get_airfield_in_radius(
            self._current_tvd.name, atype.point.x, atype.point.z, self._config.gameplay.airfield_radius)
        if managed_airfield:
            self.add_aircraft(self._current_tvd.name, self._current_tvd.get_country(atype.point),
                              managed_airfield.name, bot.aircraft.log_name, 1)
            self.emitter.player_finish.on_next(Finish(True, atype))
        else:
            self.emitter.player_finish.on_next(Finish(False, atype))

    def _add_aircraft(self, airfield, airfield_country: int, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром без сохранения в БД"""
        aircraft_key = self._config.planes.name_to_key(aircraft_name)
        aircraft_country = self._config.planes.cfg['uncommon'][aircraft_name.lower(
        )]['country']
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
        airfields = self.initialize_managed_airfields(
            self._config.mgen.airfields_data[campaign_map.tvd_name])
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
            NameError(
                f'Аэродром не найден:{self._current_tvd.name}{{"x":{atype.point.x}, "z":{atype.point.z}}}')

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
