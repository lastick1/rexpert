"""Модель данных управляемого аэродрома"""
import geometry

ID = '_id'
NAME = 'name'
TVD_NAME = 'tvd_name'
POS = 'pos'
PLANES = 'planes'


class ManagedAirfield(geometry.Point):
    """Класс управляемого аэродрома"""
    def __init__(self, name: str, tvd_name: str, x: float, z: float, planes: dict):
        super().__init__(x=x, z=z)
        self.name = name
        self.id = '{}_{}'.format(tvd_name, name)
        self.tvd_name = tvd_name
        self.planes = planes

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            ID: self.id,
            NAME: self.name,
            TVD_NAME: self.tvd_name,
            POS: super().to_dict(),
            PLANES: self.planes
        }
