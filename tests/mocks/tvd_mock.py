"""Заглушка ТВД"""
from pathlib import Path
from model import Tvd, Grid

class TvdMock(Tvd):
    """Заглушка ТВД"""
    def __init__(self, name: str):
        super().__init__(
            name, '', '10.11.1941', {'x': 281600, 'z': 281600}, dict(), Grid(name, dict(), list(), 0),
            Path())
        self.country = 201

    def get_country(self, point):
        return self.country
