"События на основе Atype из логов"
from .atypes import Atype10, Atype16


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
