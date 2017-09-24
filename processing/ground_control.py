"Обработка событий с наземкой (дамаг, киллы)"
from configs import Objects
from .objects import Ground, Object

class GroundController:
    "Контроллер обработки событий с наземными объектамиW"
    def __init__(self, objects: Objects):
        self.objects = objects
        self.units = list()

    def ground_object(self, tik: int, obj: Ground, object_name: str, country_id: int,
                      coal_id: int, name: str, parent_id: int):
        "Появление объекта"
        self.units.append(obj)

    def ground_kill(self, attacker: Object, target: Ground, pos: dict):
        "Уничтожение наземного объекта"
        pass
