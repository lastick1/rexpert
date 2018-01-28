"""Модель данных управляемого аэродрома"""
import geometry
import constants


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
            constants.ID: self.id,
            constants.Airfield.NAME: self.name,
            constants.TVD_NAME: self.tvd_name,
            constants.POS: super().to_dict(),
            constants.Airfield.PLANES: self.planes,
            constants.Airfield.SUPPLIES: self.supplies
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
