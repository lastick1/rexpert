"""Модель данных склада"""
import constants
import geometry

WAREHOUSES = {
    'RWH1': 5,
    'RWH2': 5,
    'RWH3': 5,
    'BWH1': 5,
    'BWH2': 5,
    'BWH3': 5
}


class Warehouse(geometry.Point):
    """Склад ресурсов"""
    def __init__(self, name: str, tvd_name: str, health: float, deaths: int, country: int, pos: dict):
        super().__init__(pos['x'], pos['z'])
        self.name = name
        self.tvd_name = tvd_name
        self.health = health
        self.deaths = deaths
        self.country = country
        self.pos = pos
        self.server_input: str = None  # имя сервер инпута для генерации

    @property
    def damage_level(self) -> int:
        """Уровень повреждений склада"""
        if self.health < 20:
            return 5
        if self.health < 40:
            return 4
        if self.health < 60:
            return 3
        if self.health < 80:
            return 2
        if self.health < 100:
            return 1
        return 0

    @property
    def next_damage(self) -> float:
        """Потеря хп при следующем уничтожении секции"""
        result = 15.0 - self.damage_level * 3
        if result > 0:
            return result
        return 2

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.ID: '{}_{}'.format(self.tvd_name, self.name),
            constants.TVD_NAME: self.tvd_name,
            constants.Warehouse.HEALTH: self.health,
            constants.Warehouse.DEATHS: self.deaths,
            constants.COUNTRY: self.country,
            constants.POS: self.pos
        }
