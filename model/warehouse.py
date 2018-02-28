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
