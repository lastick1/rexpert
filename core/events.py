"События на основе Atype из логов"
from .atypes import Atype10, Atype16, Atype19


class Capture:
    "Захват территории"
    def __init__(self, tvd_name: str, pos: dict, country: int):
        self.tvd_name: str = tvd_name
        self.pos: dict = pos
        self.country: int = country


class Generation:
    "Генерация новой миссии"
    def __init__(self, mission_name: str, mission_date: str, tvd_name: str, atype: Atype19):
        self.mission_name: str = mission_name
        self.mission_date: str = mission_date
        self.tvd_name: str = tvd_name
        self.atype: Atype19 = atype


class Spawn:
    "Появление игрока на аэродроме"

    def __init__(self, atype: Atype10):
        self.atype: Atype10 = atype


class Finish:
    "Завершение вылета игроком"

    def __init__(self, on_airfield: bool, atype: Atype16):
        self.on_airfield: bool = on_airfield
        self.atype: Atype16 = atype


class DivisionDamage:
    "Повреждение дивизии"

    def __init__(self, tik: int, tvd_name: str, name: str):
        self.tik: int = tik
        self.tvd_name: str = tvd_name
        self.name: str = name


class WarehouseDamage:
    "Повреждение склада"
    def __init__(self, tik: str, unit):
        self.tik: int = tik
        self.unit = unit
