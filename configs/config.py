"""Конфигурация приложения"""
from __future__ import annotations
import pathlib

from .main import Main
from .mgen import Mgen, GeneratorParamsConfig
from .planes import Planes
from .gameplay import Gameplay
from .stat import Stats
from .draw import Draw
from .weather import Weather


class Config:
    """Контейнер конфигурации"""
    def __init__(self, main_json: pathlib.Path):
        self.main = Main(main_json)  # основной конфиг приложения
        self.mgen = Mgen(self.main.game_folder)  # настройки генерации миссий
        self.planes = Planes()  # конфигурация самолётов
        self.gameplay = Gameplay()  # настройки игрового процесса
        self.stat = Stats(self.main.stats_static)  # конфиг интеграции со статистикой
        self.generator = GeneratorParamsConfig()  # конфигурация создания defaultparams
        self.draw = Draw(self.mgen)
        self.weather = Weather()
