"""Модель данных управляемого аэродрома"""
import geometry
from .storage import ID, TVD_NAME


NAME = 'name'
POS = 'pos'
PLANES = 'planes'
SUPPLIES = 'supplies'


class ManagedAirfield(geometry.Point):
    """Класс управляемого аэродрома"""
    def __init__(self, name: str, tvd_name: str, x: float, z: float, planes: dict, supplies: float = 100):
        super().__init__(x=x, z=z)
        self.name = name
        self.id = '{}_{}'.format(tvd_name, name)
        self.tvd_name = tvd_name
        self.planes = planes
        self.supplies = supplies

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            ID: self.id,
            NAME: self.name,
            TVD_NAME: self.tvd_name,
            POS: super().to_dict(),
            PLANES: self.planes,
            SUPPLIES: self.supplies
        }

    @property
    def power(self) -> float:
        """Рассчитанная сила аэродрома в зависимости от его состояния"""
        result = self.supplies
        for name in self.planes:
            result += self.planes[name]
        return result

    @property
    def planes_count(self) -> int:
        """Общее количество самолётов на аэродроме"""
        return sum(self.planes[name] for name in self.planes)

    @property
    def remain_planes(self) -> list:
        """Ключи (названия) самолётов, которые есть на аэродроме"""
        result = list()
        for key in self.planes:
            if self.planes[key] > 0:
                result.append(key)
        return result
