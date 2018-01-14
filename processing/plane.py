"""Сериализация доступных на аэродромах самолётов"""
from .formats import plane_format

SET_INDEX = 'SetIndex'
NUMBER = 'Number'
AI_LEVEL = 'AILevel'
START_IN_AIR = 'StartInAir'
ENGAGEABLE = 'Engageable'
VULNERABLE = 'Vulnerable'
LIMIT_AMMO = 'LimitAmmo'
AI_RTB_DECISION = 'AIRTBDecision'
RENEWABLE = 'Renewable'
PAYLOAD_ID = 'PayloadId'
WM_MASK = 'WMMask'
FUEL = 'Fuel'
ROUTE_TIME = 'RouteTime'
RENEW_TIME = 'RenewTime'
ALTITUDE = 'Altitude'
SPOTTER = 'Spotter'
NAME = 'Name'
MODEL = 'Model'
SCRIPT = 'Script'
AV_MODS = 'AvMods'
AV_SKINS = 'AvSkins'
AV_PAYLOADS = 'AvPayloads'
SKIN = 'Skin'
CALLSIGN = 'Callsign'
CALLNUM = 'Callnum'


class Plane:
    """Самолёт"""
    def __init__(self, number: int, common: dict, uncommon: dict):
        self.common = common
        self.uncommon = uncommon
        self.name = uncommon[NAME]
        self.number = number

    def __str__(self) -> str:
        return '{}: {}'.format(self.name, self.number)

    def format(self) -> str:
        """Сформатировать в строку для MCU аэродрома"""
        return plane_format.format(
            self.common[SET_INDEX],
            self.number,
            self.common[AI_LEVEL],
            self.common[START_IN_AIR],
            self.common[ENGAGEABLE],
            self.common[VULNERABLE],
            self.common[LIMIT_AMMO],
            self.common[AI_RTB_DECISION],
            self.common[RENEWABLE],
            self.common[PAYLOAD_ID],
            self.common[WM_MASK],
            self.common[FUEL],
            self.common[ROUTE_TIME],
            self.common[RENEW_TIME],
            self.common[ALTITUDE],
            self.common[SPOTTER],
            self.uncommon[MODEL],
            self.uncommon[SCRIPT],
            self.name,
            self.common[SKIN],
            self.uncommon[AV_MODS],
            self.uncommon[AV_SKINS],
            self.uncommon[AV_PAYLOADS],
            self.common[CALLSIGN],
            self.common[CALLNUM]
        )
