"Классы объектов в логах"
import configs
from .helpers import is_pos_correct, distance

class Object:
    "Базовый объект"
    def __init__(self, obj_id: int, obj: configs.Object, country_id: int, coal_id: int, name: str):
        self.deinitialized = False
        self.obj_id = obj_id
        self.country_id = country_id
        self.coal_id = coal_id
        self.name = name

    def deinitialize(self):
        "Пометить объект как удалённый из игрового мира"
        self.deinitialized = True

class Aircraft(Object):
    "Самолёт"
    def __init__(self, obj_id: int, obj: configs.Object, country_id: int, coal_id: int, name: str):
        super().__init__(obj_id, obj, country_id, coal_id, name)
        self.cls_base, self.type = obj.cls.split('_')
        self.name = obj.name
        self.log_name = obj.log_name

class BotPilot(Object):
    "Пилот"
    def __init__(self, obj_id: int, obj: configs.Object, parent: Aircraft, country_id: int,
                 coal_id: int, name: str):
        super().__init__(obj_id, obj, country_id, coal_id, name)
        self.aircraft = parent

    def deinitialize(self):
        "Пометить объект как удалённый из игрового мира"
        self.aircraft.deinitialize()
        super().deinitialize()

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
