"""Модель данных склада"""
import constants


class Warehouse:
    """Склад ресурсов"""
    def __init__(self, name: str, tvd_name: str, health: float):
        self.name = name
        self.tvd_name = tvd_name
        self.health = health

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.ID: '{}_{}'.format(self.tvd_name, self.name),
            constants.TVD_NAME: self.tvd_name,
            constants.Warehouse.HEALTH: self.health
        }
