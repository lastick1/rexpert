"Классы объектов в логах"
from .helpers import is_pos_correct, distance

class Airfield:
    "Аэродром"
    def __init__(self, airfield_id, country_id, coal_id, pos):
        self.id = airfield_id
        self.country_id = country_id
        self.coal_id = coal_id
        self.pos = pos

    def on_airfield(self, pos):
        "Находится ли точка на аэродроме"
        if is_pos_correct(pos=self.pos) and is_pos_correct(pos=pos):
            return distance(self.pos, pos) <= 4000
        else:
            return False

    def update(self, country_id, coal_id):
        "Обновить страну и коалицию"
        self.country_id = country_id
        self.coal_id = coal_id
