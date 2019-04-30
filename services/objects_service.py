"Сервис работы с объектами, обнаруженными в логах"
from __future__ import annotations
from typing import Any, List, Dict, Set

import logging

from core import EventsEmitter, Atype0, Atype1, Atype2, Atype3, Atype5, Atype6, Atype7, Atype9, \
    Atype10, Atype11, Atype12, Atype16, Atype17, Atype18
from configs import Config, Objects
from log_objects import Object, Airfield, Aircraft, BotPilot, Ground, GROUND_CLASSES


from .base_event_service import BaseEventService


def _to_aircraft(obj) -> Aircraft:
    return obj


class ObjectsService(BaseEventService):
    "Сервис работы с объектами, обнаруженными в логах"

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config,
            objects: Objects
    ):
        super().__init__(emitter)
        self._config: Config = config
        self._bots: Set[BotPilot] = set()
        self._airfields: Set[Airfield] = set()
        self._aircrafts: Set[Aircraft] = set()
        self._objects: Dict[int, Any] = dict()
        self.objects: Objects = objects

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.events_mission_start.subscribe_(
                self._start_mission, self._on_error),
            self.emitter.events_hit.subscribe_(self._hit, self._on_error),
            self.emitter.events_damage.subscribe_(
                self._damage, self._on_error),
            self.emitter.events_kill.subscribe_(self._kill, self._on_error),
            self.emitter.events_takeoff.subscribe_(
                self._takeoff, self._on_error),
            self.emitter.events_landing.subscribe_(self._land, self._on_error),
            self.emitter.events_mission_end.subscribe_(
                self._end_mission, self._on_error),
            self.emitter.events_airfield.subscribe_(
                self._airfield, self._on_error),
            self.emitter.events_player_spawn.subscribe_(
                self._spawn, self._on_error),
            self.emitter.events_group.subscribe_(self._group, self._on_error),
            self.emitter.events_game_object.subscribe_(
                self._create_object, self._on_error),
            self.emitter.events_bot_deinitialization.subscribe_(
                self._deinitialize, self._on_error),
            self.emitter.events_pos_changed.subscribe_(
                self._change_pos, self._on_error),
            self.emitter.events_bot_eject_leave.subscribe_(
                self._eject_leave, self._on_error),
        ])

    def _on_error(self, error: Any) -> None:
        logging.error(error)

    def _create_object(self, atype: Atype12) -> Object:
        """Создать объект соответствующего типа"""
        obj = self.objects[atype.object_name]

        if 'BotPilot' in obj.log_name or 'BotGunner' in obj.log_name and 'aircraft' in obj.cls:
            self._objects[atype.object_id] = BotPilot(
                atype.object_id, obj, self._objects[atype.parent_id], atype.country_id, atype.coal_id, atype.name)
            self._bots.add(self._objects[atype.object_id])
            return self._objects[atype.object_id]

        if obj.playable and 'aircraft' in obj.cls and 'pilot' not in obj.cls:
            self._objects[atype.object_id] = Aircraft(
                atype.object_id, obj, atype.country_id, atype.coal_id, atype.name)
            self._aircrafts.add(self._objects[atype.object_id])
            return self._objects[atype.object_id]

        if 'airfield' in obj.cls:
            self._objects[atype.object_id] = Airfield(
                atype.object_id, atype.country_id, atype.coal_id, dict())
            self._airfields.add(self._objects[atype.object_id])
            return self._objects[atype.object_id]

        if obj.cls in GROUND_CLASSES:
            self._objects[atype.object_id] = Ground(
                atype.object_id, obj, atype.country_id, atype.coal_id, atype.name)
            return self._objects[atype.object_id]

        if atype.object_id not in self._objects:
            self._objects[atype.object_id] = Object(
                atype.object_id, atype.country_id, atype.coal_id, atype.name)
            return self._objects[atype.object_id]

        raise NameError('Unknown object')

    def _hit(self, atype: Atype1) -> None:
        """Обработать попадание"""

    def _damage(self, atype: Atype2) -> None:
        """Обработать событие урона"""
        if atype.target_id in self._objects:
            target = self._objects[atype.target_id]
            target.update_pos(atype.pos)
            if atype.attacker_id:
                attacker = self.get_object(atype.attacker_id)
                attacker.update_pos(atype.pos)
                if isinstance(attacker, Aircraft):
                    _to_aircraft(attacker).add_damage(target, atype.damage)

    def _kill(self, atype: Atype3) -> None:
        """Обработать событие убийства"""
        target = self.get_object(atype.target_id)
        target.kill(pos=atype.pos)
        if atype.attacker_id:
            attacker = self.get_object(atype.attacker_id)
            attacker.update_pos(atype.pos)
            if isinstance(attacker, Aircraft):
                _to_aircraft(attacker).add_kill(target)

    def _takeoff(self, atype: Atype5) -> None:
        """Обработать взлёт"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.takeoff(atype.pos)

    def _land(self, atype: Atype6) -> None:
        """Посадить самолёт"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.land(atype.pos, list(self._airfields),
                      self._config.gameplay.airfield_radius)

    def _start_mission(self, atype: Atype0) -> None:
        """Начать миссию"""
        self._objects.clear()
        self._bots.clear()
        self._airfields.clear()
        self._aircrafts.clear()

    def _end_mission(self, atype: Atype7) -> None:
        """Завершить миссию"""
        for aircraft in self._aircrafts:
            aircraft.landed = True
            aircraft.is_safe = True

    def _airfield(self, atype: Atype9) -> None:
        """Создать/обновить аэродром"""
        if atype.airfield_id in self._objects:
            airfield = self.get_airfield(atype.airfield_id)
            airfield.update(atype.country_id, atype.coal_id)
        else:
            airfield = Airfield(atype.airfield_id,
                                atype.country_id, atype.coal_id, atype.pos)
            self._objects[atype.airfield_id] = airfield
            self._airfields.add(airfield)

    def _spawn(self, atype: Atype10) -> None:
        """Обработать появление игрока"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.update_pos(atype.pos)
        bot = self.get_bot(atype.bot_id)
        if bot:
            bot.update_pos(atype.pos)
        else:
            logging.warning(
                f'not found bot on spawn [{atype}]')

    def _group(self, atype: Atype11) -> None:
        """Обработать появление группы в логах"""

    def _deinitialize(self, atype: Atype16) -> None:
        """Деинициализировать бота"""
        bot = self.get_bot(atype.bot_id)
        bot.deinitialize(atype.pos)

    def _change_pos(self, atype: Atype17) -> None:
        """Изменить позицию объекта"""
        self.get_object(atype.object_id).update_pos(atype.pos)

    def _eject_leave(self, atype: Atype18) -> None:
        """Обработать прыжок с парашютом"""
        aircraft = self.get_aircraft(atype.parent_id)
        bot = self.get_bot(atype.bot_id)
        if aircraft:
            aircraft.ejected = True
        else:
            logging.error(
                f'not found aircraft on eject [{atype}]')
        if bot:
            bot.ejected = True
            logging.error(
                f'not found bot on eject [{atype}]')

    def get_object(self, object_id) -> Object:
        """Получить объект"""
        if object_id in self._objects:
            return self._objects[object_id]
        return None

    def get_ground(self, ground_id) -> Ground:
        """Получить наземный объект"""
        if ground_id in self._objects:
            return self._objects[ground_id]
        return None

    def get_bot(self, bot_id) -> BotPilot:
        """Получить бота"""
        if bot_id in self._objects:
            return self._objects[bot_id]
        return None

    def get_aircraft(self, aircraft_id) -> Aircraft:
        """Получить самолёт"""
        if aircraft_id in self._objects:
            return self._objects[aircraft_id]
        return None

    def get_airfield(self, airfield_id) -> Airfield:
        """Получить аэродром"""
        if airfield_id in self._objects:
            return self._objects[airfield_id]
        return None

    def get_all(self) -> List[Any]:
        """Получить все объекты"""
        return list(self._objects[x] for x in self._objects)
