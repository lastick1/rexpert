"Классы объектов в логах"
import configs
from .helpers import is_pos_correct, distance

class Object:
    "Базовый объект"
    def __init__(self, obj_id: int, obj: configs.Object, country_id: int, coal_id: int, name: str):
        self.cls_base = None
        self.deinitialized = False
        self.obj_id = obj_id
        self.country_id = country_id
        self.coal_id = coal_id
        self.name = name

    def deinitialize(self):
        "Пометить объект как удалённый из игрового мира"
        self.deinitialized = True

class Ground(Object):
    "Наземный объект"
    def __init__(self,
                 obj_id: int, obj: configs.Object, country_id: int,
                 coal_id: int, name: str, pos: dict = None):
        super().__init__(obj_id, obj, country_id, coal_id, name)
        self.cls_base = 'ground'
        self.killed = False
        self.pos = pos

    def update_pos(self, pos: dict) -> None:
        "Обновить позицию"
        if is_pos_correct(pos):
            self.pos = pos

class Aircraft(Object):
    "Самолёт"
    def __init__(self,
                 obj_id: int, obj: configs.Object, country_id: int,
                 coal_id: int, name: str, pos: dict = None):
        super().__init__(obj_id, obj, country_id, coal_id, name)
        self.cls_base, self.type = obj.cls.split('_')
        self.name = obj.name
        self.log_name = obj.log_name
        self.pos = pos
        self.killboard = list()
        self.damageboard = dict()

    def add_kill(self, target: Object):
        "Добавить убитый объект"
        self.killboard.append(target)

    def add_damage(self, target: Object, damage: float):
        "Добавить нанесённый урон"
        if hasattr(target, 'pos'):
            key = str(target.pos)
            if key not in self.damageboard:
                self.damageboard[key] = 0.0
            self.damageboard[key] += damage
        else:
            NameError('Damage nowhere {} {}'.format(target.pos, damage))

    def update_pos(self, pos: dict) -> None:
        "Обновить позицию"
        if is_pos_correct(pos):
            self.pos = pos

class BotPilot(Object):
    "Пилот"
    def __init__(self, obj_id: int, obj: configs.Object, parent: Aircraft, country_id: int,
                 coal_id: int, name: str, pos: dict = None):
        super().__init__(obj_id, obj, country_id, coal_id, name)
        self.aircraft = parent
        self.pos = pos

    def deinitialize(self):
        "Пометить объект как удалённый из игрового мира"
        self.aircraft.deinitialize()
        super().deinitialize()

    def update_pos(self, pos: dict) -> None:
        "Обновить позицию"
        if is_pos_correct(pos):
            self.pos = pos

class Airfield(Object):
    "Аэродром"
    def __init__(self, airfield_id: int, country_id: int, coal_id: int, pos: dict):
        super().__init__(airfield_id, None, country_id, coal_id, 'airfield')
        self.pos = pos

    def on_airfield(self, pos: dict):
        "Находится ли точка на аэродроме"
        if is_pos_correct(pos=self.pos) and is_pos_correct(pos=pos):
            return distance(self.pos, pos) <= 4000
        else:
            return False

    def update(self, country_id: int, coal_id: int):
        "Обновить страну и коалицию"
        self.country_id = country_id
        self.coal_id = coal_id

    def update_pos(self, pos: dict) -> None:
        "Обновить позицию"
        if is_pos_correct(pos):
            self.pos = pos

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
