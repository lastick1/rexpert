"""Сборка групп аэродромов"""
from .mcu import Airfield


class AirfieldsBuilder:
    """Сборщик групп аэродромов"""
    def __init__(self, airfields: list):
        self.airfields = airfields

    def make(self) -> Airfield:
        """Сформировать MCU аэродрома"""
        return Airfield(0, 0, 2, [], 0)
