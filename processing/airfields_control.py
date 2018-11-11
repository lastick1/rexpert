"""Контроль состояния аэродромов (доступные самолёты, повреждения)"""
import logging

import atypes
import configs
import log_objects
import storage
import model

from .aircraft_vendor import AircraftVendor


class AirfieldsController:
    """Контроллер аэродромов"""

    def __init__(self, ioc):
        self._ioc = ioc
        self.current_airfields = list()

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def campaign_controller(self):
        return self._ioc.campaign_controller

    @property
    def aircraft_vendor(self) -> AircraftVendor:
        """Поставщик самолётов"""
        return self._ioc.aircraft_vendor

    @property
    def storage(self) -> storage.Storage:
        """Объект для работы с БД"""
        return self._ioc.storage

    @staticmethod
    def initialize_managed_airfields(airfields_data: list) -> list:
        """Инициализировать список управляемых аэродромов из данных конфигурации"""
        return list(
            model.ManagedAirfield(
                name=data['name'],
                tvd_name=data['tvd_name'],
                x=data['x'],
                z=data['z'],
                planes=dict())
            for data in airfields_data)

    def get_airfield_in_radius(self, tvd_name: str, x: float, z: float, radius: int) -> model.ManagedAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        for airfield in self.storage.airfields.load_by_tvd(tvd_name=tvd_name):
            if airfield.distance_to(x=x, z=z) < radius:
                return airfield

    def get_airfield_by_name(self, tvd_name: str, airfield_name) -> model.ManagedAirfield:
        """Получить аэродром по имени"""
        return self.storage.airfields.load_by_name(tvd_name, airfield_name)

    def start_mission(self):
        """Обработать начало миссии"""
        self.current_airfields.clear()

    def spawn_aircraft(self, tvd_name: str, airfield_country: int, atype: atypes.Atype10):
        """Обработать появление самолёта на аэродроме"""
        managed_airfield = self.get_airfield_in_radius(
            tvd_name, atype.pos['x'], atype.pos['z'], self.config.gameplay.airfield_radius)
        if not managed_airfield:
            logging.warning(f'airfield not found: {atype}')
        else:
            self.add_aircraft(tvd_name, airfield_country,
                              managed_airfield.name, atype.aircraft_name, -1)

    def finish(self, tvd_name: str, airfield_country: int, bot: log_objects.BotPilot) -> bool:
        """Обработать деспаун самолёта на аэродроме"""
        xpos = bot.aircraft.pos['x']
        zpos = bot.aircraft.pos['z']
        managed_airfield = self.get_airfield_in_radius(
            tvd_name, xpos, zpos, self.config.gameplay.airfield_radius)
        if managed_airfield:
            self.add_aircraft(tvd_name, airfield_country,
                              managed_airfield.name, bot.aircraft.log_name, 1)
            return True
        return False

    @staticmethod
    def get_country(airfield, tvd) -> int:
        """Получить страну аэродрома в соответствии с графом"""
        return tvd.get_country(airfield)

    def _add_aircraft(self, airfield, airfield_country: int, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром без сохранения в БД"""
        aircraft_key = self.config.planes.name_to_key(aircraft_name)
        aircraft_country = self.config.planes.cfg['uncommon'][aircraft_name.lower(
        )]['country']
        if aircraft_country == airfield_country:
            if aircraft_key not in airfield.planes:
                airfield.planes[aircraft_key] = 0
            airfield.planes[aircraft_key] += aircraft_count

    def add_aircraft(
            self, tvd_name: str, airfield_country: int, airfield_name: str, aircraft_name: str, aircraft_count: int):
        """Добавить самолёт на аэродром"""
        airfield = self.storage.airfields.load_by_name(tvd_name, airfield_name)
        self._add_aircraft(airfield, airfield_country,
                           aircraft_name, aircraft_count)
        self.storage.airfields.update_airfield(airfield)

    def end_round(self):
        """Обработать завершение раунда - перераспределить самолёты с тылового на фронтовые аэродромы"""
        tvd = self.campaign_controller.current_tvd
        front = tvd.to_country_dict_front(self.current_airfields)
        rear = tvd.to_country_dict_rear(self.current_airfields)
        for country in (101, 201):
            self.aircraft_vendor.transfer_to_front(
                front[country], rear[country])
        self.storage.airfields.update_airfields(self.current_airfields)

    def initialize_tvd(self, tvd: model.Tvd, campaign_map: model.CampaignMap):
        """Инициализировать аэродромы указанного ТВД"""
        airfields = self.initialize_managed_airfields(
            self.config.mgen.airfields_data[campaign_map.tvd_name])
        supply = self.aircraft_vendor.get_month_supply(
            campaign_map.current_month, campaign_map)
        self.aircraft_vendor.deliver_month_supply(
            campaign_map, tvd.to_country_dict_rear(airfields), supply)
        self.aircraft_vendor.initial_front_supply(
            campaign_map, tvd.to_country_dict_front(airfields))
        self.storage.airfields.update_airfields(airfields)

    def spawn_airfield(self, atype: atypes.Atype9):
        """Обработать появление аэродрома в начале миссии"""
        tvd_name = self.campaign_controller.current_tvd.name
        airfield = self.get_airfield_in_radius(
            tvd_name, atype.point.x, atype.point.z, 50)
        if airfield:
            self.current_airfields.append(airfield)
        else:
            NameError(
                f'Аэродром не найден:{tvd_name}{{"x":{atype.point.x}, "z":{atype.point.z}}}')
