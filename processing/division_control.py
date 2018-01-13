"""Управление дивизиями"""
import configs

from .division import Division, DIVISIONS
from .storage import Storage


class DivisionsController:
    """Управляение созданием, уроном, состоянием дивизий"""
    def __init__(self, config: configs.Config):
        self.config = config
        self.storage = Storage(config.main)

    def initialize_divisions(self, tvd_name: str):
        """Инициализировать дивизии в кампании для указанного ТВД"""
        for name in DIVISIONS:
            self.storage.divisions.update(
                Division(
                    tvd_name=tvd_name,
                    name=name,
                    units=DIVISIONS[name]
                )
            )

    def damage_division(self, tvd_name: str, unit_name: str):
        """Зачесть уничтожение подразделения дивизии"""
        division_name = unit_name.split(sep='_')[1]
        division = self.storage.divisions.load_by_name(tvd_name, division_name)
        division.units -= 1
        if division.units < 0:
            division.units = 0
        self.storage.divisions.update(division)

    def repair_rate(self, penalties: int):
        """Получить множитель восстановления с учётом уничтоженных складов"""
        result = 1 + (self.config.gameplay.division_repair - penalties * 5) / 100
        return result if result > 1 else 1

    def repair_division(self, tvd_name: str,  division_name: str, penalties: int):
        """Восполнить дивизию"""
        division = self.storage.divisions.load_by_name(tvd_name, division_name)
        division.units *= self.repair_rate(penalties)
        if division.units > DIVISIONS[division_name]:
            division.units = DIVISIONS[division_name]
        self.storage.divisions.update(division)
