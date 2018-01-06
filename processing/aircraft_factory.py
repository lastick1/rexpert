"""Распределение самолётов по аэродромам"""
import configs


class AircraftFactory:
    """Класс, распределяющий самолёты по аэродромам"""
    def __init__(self, config: configs.Planes, gameplay: configs.Gameplay):
        self.config = config
        self.gameplay = gameplay

    def get_month_supply(self, month, campaign_map):
        """Сформировать месячную поставку"""
