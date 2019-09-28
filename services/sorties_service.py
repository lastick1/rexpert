"""Учёт самолётовылетов"""
from __future__ import annotations
from typing import Dict
import logging

from log_objects import BotPilot
from core import EventsEmitter, \
    Spawn, \
    Takeoff, \
    Finish, \
    Atype0, \
    Atype5, \
    Atype6, \
    Atype7, \
    Atype10, \
    Atype16, \
    Atype18
from model import Sortie

from .objects_service import ObjectsService
from .base_event_service import BaseEventService
from .airfields_service import AirfieldsService


class SortiesService(BaseEventService):
    """Сервис обработки вылетов"""

    def __init__(
            self,
            emitter: EventsEmitter,
            objects_service: ObjectsService,
            airfields_service: AirfieldsService,
    ):
        super().__init__(emitter)
        self._objects_service: ObjectsService = objects_service
        self._airfields_service: AirfieldsService = airfields_service
        self._sorties: Dict[str, Sortie] = dict()
        self._aircraft_ids: Dict[str, str] = dict()
        self._atype0: Atype0 = None
        self._atype7: Atype7 = None

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.events_mission_start.subscribe_(self._start),
            self.emitter.events_mission_end.subscribe_(self._end),
            self.emitter.events_player_spawn.subscribe_(self._spawn),
            self.emitter.events_takeoff.subscribe_(self._takeoff),
            self.emitter.events_landing.subscribe_(self._landing),
            self.emitter.events_bot_eject_leave.subscribe_(self._bailout),
            self.emitter.events_bot_deinitialization.subscribe_(self._deinitialize)
        ])

    def get_sortie(self, aircraft_id: str) -> Sortie:
        """Получить вылет самолёта"""
        if aircraft_id in self._sorties:
            return self._sorties[aircraft_id]

    def _start(self, atype: Atype0) -> None:
        """Обработка начала миссии"""
        self._sorties.clear()
        self._aircraft_ids.clear()
        self._atype0 = atype
        self._atype7 = None

    def _end(self, atype: Atype7) -> None:
        """Фиксация завершения миссии"""
        self._atype7 = atype

    def _spawn(self, atype: Atype10) -> None:
        """Обработка появления самолёта"""
        bot: BotPilot = self._objects_service.get_bot(atype.bot_id)
        if bot.__class__ == BotPilot:
            sortie = Sortie(atype)
            if atype.aircraft_id in self._sorties:
                obj = self._objects_service.get_object(atype.bot_id)
                logging.warning(f'second sortie for one aircraft {obj.name if obj else None}')
                return
            self._aircraft_ids[atype.bot_id] = sortie.aircraft_id
            self._sorties[atype.aircraft_id] = sortie
            self.emitter.sortie_spawn.on_next(
                Spawn(sortie.account_id, atype.name, sortie.unlocks, bot.aircraft.log_name, atype.point)
            )

    def _takeoff(self, atype: Atype5) -> None:
        """Обработка взлёта"""
        sortie = self._sorties[atype.aircraft_id]
        sortie.takeoff(atype)
        self.emitter.sortie_takeoff.on_next(Takeoff(sortie.account_id, sortie.unlocks))

    def _landing(self, atype: Atype6) -> None:
        """Обработка посадки"""
        aircraft = self._objects_service.get_aircraft(atype.aircraft_id)
        on_airfield = self._airfields_service.is_on_airfield(
            atype.pos['x'],
            atype.pos['z'],
            aircraft.country_id
        )
        self._sorties[atype.aircraft_id].land(atype, on_airfield)

    def _bailout(self, atype: Atype18) -> None:
        """Обработка прыжка"""
        self._sorties[self._aircraft_ids[atype.bot_id]].bailout(atype)

    def _deinitialize(self, atype: Atype16) -> None:
        """Обработка завершения вылета"""
        sortie = self._sorties[self._aircraft_ids[atype.bot_id]]
        bot: BotPilot = self._objects_service.get_bot(sortie.bot_id)

        has_kills = len(bot.aircraft.killboard) > 0
        has_damage = len(bot.aircraft.damageboard) > 0
        ff_kills = len(bot.aircraft.friendly_fire_kills) > 0
        ff_damage = len(bot.aircraft.friendly_fire_damages) > 0
        friendly_fire = ff_damage or ff_kills

        mission_ended = self._atype7 is not None

        sortie.deinitialize(
            atype,
            not friendly_fire and bot.aircraft.landed and (has_kills or has_damage),
            mission_ended
        )
        self.emitter.sortie_deinitialize.on_next(
            Finish(sortie.account_id, sortie.on_airfield, sortie.success, bot.aircraft.log_name, atype.point)
        )
