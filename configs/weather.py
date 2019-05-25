"""Конфиг погоды в миссиях"""
from __future__ import annotations
from typing import Dict, Any
from pathlib import Path
from json import load, loads
from random import randint


class WeatherPreset:
    """Класс предустановок настроек погоды"""

    def __init__(self, preset: Dict[str, Any]):
        self.preset = preset

        turbulence = loads(preset['Turbulence'])
        if isinstance(turbulence, list):
            self.turbulences = turbulence
        else:
            self.turbulences = [turbulence, turbulence]

        cloudlevel = loads(preset['CloudLevel'])
        if isinstance(cloudlevel, list):
            self.cloudlevels = cloudlevel
        else:
            self.cloudlevels = [cloudlevel, cloudlevel]

        cloudheight = loads(preset['CloudHeight'])
        if isinstance(cloudheight, list):
            self.cloudheights = cloudheight
        else:
            self.cloudheights = [cloudheight, cloudheight]

    @property
    def turbulence(self):
        """Случайный турбулентности в заданном диапазоне"""
        return randint(self.turbulences[0], self.turbulences[1])

    @property
    def cloudlevel(self):
        """Случайный уровень облаков в заданном диапазоне"""
        return randint(self.cloudlevels[0], self.cloudlevels[1])

    @property
    def cloudheight(self):
        """Случайная высота облаков в заданном диапазоне"""
        return randint(self.cloudheights[0], self.cloudheights[1])


class Weather:
    """Конфиг погоды в миссиях"""

    def __init__(self, path: Path = Path('./configs/weather.json')):
        with path.open() as stream:
            src = load(stream)
        self.cfg = src
        self.map_seasons: Dict[str, Dict[str, Dict[int, WeatherPreset]]] = {_name: {
            _season: {
                int(_id): WeatherPreset(src[_name][_season][_id]) for _id in src[_name][_season]
            } for _season in src[_name]
        } for _name in src['maps']}
