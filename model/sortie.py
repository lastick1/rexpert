"""Модель данных самолётовылета"""
from __future__ import annotations
from typing import List

from core import Atype10, Atype5, Atype6, Atype16, Atype18


class Sortie:
    """Самолётовылет"""

    def __init__(self, atype10: Atype10):
        self._atype10: Atype10 = atype10
        self.success: bool = False
        self.in_air: bool = atype10.airstart
        self.on_airfield: bool = not atype10.airstart
        self.takeoffs: List[Atype5] = list()
        self.landings: List[Atype6] = list()
        self.bailouts: List[Atype16] = list()
        self._end: Atype16 = None
        self._end_after_mission_end: bool = False

    @property
    def active(self) -> bool:
        """Бот и самолёт в игре"""
        return not self._end

    @property
    def account_id(self) -> str:
        """Идентификатор игрока"""
        return self._atype10.account_id

    @property
    def aircraft_id(self) -> str:
        """Идентификатор самолёта в логе"""
        return self._atype10.aircraft_id

    @property
    def bot_id(self) -> str:
        """Идентификатор бота в логе"""
        return self._atype10.bot_id

    @property
    def unlocks(self) -> int:
        """Количество модификаций, взятых в вылет"""
        return len(self._atype10.weapon_mods_id)

    def takeoff(self, atype: Atype5) -> None:
        """Записать взлёт"""
        self.in_air = True
        self.on_airfield = False
        self.takeoffs.append(atype)

    def land(self, atype: Atype6, on_airfield: bool) -> None:
        """Записать посадку"""
        self.in_air = False
        self.on_airfield = on_airfield
        self.landings.append(atype)

    def bailout(self, atype: Atype18) -> None:
        """Записать прыжок"""
        self.bailouts.append(atype)

    def deinitialize(self, atype: Atype16, success: bool, mission_ended: bool) -> None:
        """Записать завершение вылета"""
        self._end = atype
        self.success = success
        self._end_after_mission_end = mission_ended
