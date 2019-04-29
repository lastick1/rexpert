"События на основе Atype из логов"
from .atypes import Atype16


class Finish:
    "Завершение вылета игроком"
    def __init__(self, on_airfield: bool, atype: Atype16):
        self.on_airfield: bool = on_airfield
        self.atype: Atype16 = atype
