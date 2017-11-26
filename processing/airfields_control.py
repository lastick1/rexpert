"""Контрооль состояния аэродромов (самолёты, повреждения)"""
from .airfield import ManageableAirfield


class AirfieldsController:
    def __init__(self):
        pass

    def get_airfield_by_coords(self, x: float, z: float, radius: int) -> ManageableAirfield:
        """Получить аэродром по его координатам с заданным отклонением"""
        return ManageableAirfield()
