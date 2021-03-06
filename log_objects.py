"""Классы объектов в логах"""
from __future__ import annotations
import configs
import geometry


class Object:
    """Базовый объект"""

    def __init__(self, obj_id: int, country_id: int, coal_id: int, name: str, pos: dict = None):
        self.deinitialized = False
        self.obj_id = obj_id
        self.country_id = country_id
        self.coal_id = coal_id
        self.name = name
        self.taken_damage = 0.0
        self.pos = pos
        self.killed = False

    def deinitialize(self, pos: dict):
        """Пометить объект как удалённый из игрового мира"""
        self.update_pos(pos)
        self.deinitialized = True

    def update_pos(self, pos: dict) -> None:
        """Обновить позицию"""
        if geometry.is_pos_correct(pos):
            self.pos = pos

    def damage(self, damage: float, pos: dict) -> None:
        """Повредить объект"""
        self.taken_damage += damage
        self.update_pos(pos)

    def kill(self, pos: dict) -> None:
        """Убить объект"""
        self.update_pos(pos)
        self.killed = True


class Ground(Object):
    """Наземный объект"""

    def __init__(self, obj_id: int, obj: configs.Object, country_id: int, coal_id: int, name: str, pos: dict = None):
        super().__init__(obj_id, country_id, coal_id, name)
        self.obj = obj
        self.pos = pos


class Airfield(Object):
    """Аэродром"""

    def __init__(self, airfield_id: int, country_id: int, coal_id: int, pos: dict):
        super().__init__(airfield_id, country_id, coal_id, 'airfield')
        self.pos = pos

    def is_in_range(self, radius: float, pos: dict) -> bool:
        """Находится ли точка на аэродроме"""
        if geometry.is_pos_correct(pos=self.pos) and geometry.is_pos_correct(pos=pos):
            return geometry.distance(self.pos, pos) <= radius
        else:
            return False

    def update(self, country_id: int, coal_id: int) -> None:
        """Обновить страну и коалицию"""
        self.country_id = country_id
        self.coal_id = coal_id


def _to_airfield(obj) -> Airfield:
    return obj


class Aircraft(Object):
    """Самолёт"""

    def __init__(self, obj_id: int, obj: configs.Object, country_id: int, coal_id: int, name: str, pos: dict = None):
        super().__init__(obj_id, country_id, coal_id, name)
        self.obj = obj
        self.cls_base, self.type = obj.cls.split('_')
        if self.type == 'medium':
            self.type = 'heavy'
        self.name = obj.name
        self.log_name = obj.log_name
        self.pos = pos
        self.killboard = list()
        self.friendly_fire_kills = list()
        self.damageboard = dict()
        self.friendly_fire_damages = dict()
        self.landed = True
        self.damaged_by_enemy = False
        self.is_safe = True
        self.ejected = False

    def add_kill(self, target: Object) -> None:
        """Добавить убитый объект"""
        if target.coal_id == self.coal_id:
            self.friendly_fire_kills.append(target)
        else:
            self.killboard.append(target)

    def add_damage(self, target: Object, damage: float) -> None:
        """Добавить нанесённый урон"""
        if target.pos:
            key = str(target.pos)
            if target.coal_id == self.coal_id:
                if key not in self.friendly_fire_damages:
                    self.friendly_fire_damages[key] = 0.0
                self.friendly_fire_damages[key] += damage
            else:
                if key not in self.damageboard:
                    self.damageboard[key] = 0.0
                self.damageboard[key] += damage
        else:
            NameError('Damage nowhere {} {}'.format(target.pos, damage))

    def takeoff(self, pos: dict) -> None:
        """Взлёт"""
        self.landed = False
        self.is_safe = False
        self.update_pos(pos)

    def land(self, pos: dict, airfields: list, landing_radius: float) -> None:
        """Посадка"""
        self.landed = True
        self.update_pos(pos)
        for item in airfields:
            airfield = _to_airfield(item)
            if airfield.coal_id == self.coal_id and airfield.is_in_range(landing_radius, pos):
                self.is_safe = True


class BotPilot(Object):
    """Пилот"""

    def __init__(self, obj_id: int, obj: configs.Object, parent: Aircraft, country_id: int,
                 coal_id: int, name: str, pos: dict = None):
        super().__init__(obj_id, country_id, coal_id, name)
        self.obj = obj
        self.aircraft = parent
        self.pos = pos
        self.ejected = False

    def deinitialize(self, pos: dict) -> None:
        """Пометить объект как удалённый из игрового мира"""
        self.aircraft.deinitialize(pos)
        super().deinitialize(pos)


ALL_CLASSES = {
    'aaa_light', 'tank_turret', 'ship', 'shell', 'tank_heavy', 'aircraft_light', 'tank_medium',
    'aircraft_pilot', 'aircraft_heavy', 'car', 'rocket', 'artillery_howitzer', 'flare', 'aaa_mg',
    'aircraft_turret', 'vehicle_turret', 'trash', 'tank_light', 'tank_driver', 'wagon',
    'searchlight', 'locomotive', 'artillery_field', 'bomb', 'airfield', 'aircraft_transport',
    'explosion', 'artillery_rocket', 'parachute', 'aircraft_gunner', 'aircraft_static',
    'industrial', 'bridge', 'machine_gunner', 'bullet', 'armoured_vehicle', 'vehicle_static',
    'vehicle_crew', 'truck', 'aircraft_medium', 'aaa_heavy'}

GROUND_CLASSES = {
    'aaa_light', 'tank_turret', 'ship', 'tank_heavy', 'tank_medium', 'car', 'artillery_howitzer',
    'aaa_mg', 'aircraft_turret', 'vehicle_turret', 'trash', 'tank_light', 'tank_driver', 'wagon',
    'searchlight', 'locomotive', 'artillery_field', 'airfield', 'aircraft_transport',
    'artillery_rocket', 'aircraft_gunner', 'aircraft_static', 'industrial', 'bridge',
    'machine_gunner', 'armoured_vehicle', 'vehicle_static', 'vehicle_crew', 'truck', 'aaa_heavy'}
