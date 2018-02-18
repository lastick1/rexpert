"""Модель данных склада"""
import constants


WAREHOUSES = {
    'RWH1': 5,
    'RWH2': 5,
    'RWH3': 5,
    'BWH1': 5,
    'BWH2': 5,
    'BWH3': 5
}


class Warehouse:
    """Склад ресурсов"""
    def __init__(self, name: str, tvd_name: str, health: float, pos: dict):
        self.name = name
        self.tvd_name = tvd_name
        self.health = health
        self.pos = pos

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.ID: '{}_{}'.format(self.tvd_name, self.name),
            constants.TVD_NAME: self.tvd_name,
            constants.Warehouse.HEALTH: self.health,
            constants.POS: self.pos
        }
