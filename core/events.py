"События на основе Atype из логов"
from typing import Any
from dataclasses import dataclass
from geometry import Point
from .atypes import Atype19


@dataclass
class Capture:
    "Захват территории"
    tvd_name: str
    country: int
    point: Point


@dataclass
class PointsGain:
    "Набор очков какой либо из сторон"

    country: int
    capture_points: int
    reason: Any


class Generation:
    "Генерация новой миссии"

    def __init__(self, mission_name: str, mission_date: str, tvd_name: str, atype: Atype19):
        self.mission_name: str = mission_name
        self.mission_date: str = mission_date
        self.tvd_name: str = tvd_name
        self.atype: Atype19 = atype


@dataclass
class Spawn:
    """Появление игрока на аэродроме"""
    account_id: str
    name: str
    unlocks: int
    aircraft_name: str
    point: Point


@dataclass
class Takeoff:
    """Взлёт игрока"""
    account_id: str
    unlocks: int


@dataclass
class Finish:
    """Завершение вылета игроком"""
    account_id: str
    on_airfield: bool
    gain_unlocks: bool
    aircraft_name: str
    point: Point


class DivisionDamage:
    "Повреждение дивизии"

    def __init__(self, tik: int, tvd_name: str, unit_name: str):
        self.tik: int = tik
        self.tvd_name: str = tvd_name
        self.unit_name: str = unit_name


class WarehouseDamage:
    "Повреждение склада"

    def __init__(self, tik: str, unit_name: str, pos: dict):
        self.tik: int = tik
        self.unit_name: str = unit_name
        self.pos: dict = pos
