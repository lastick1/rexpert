"""Контроль объектов из логов миссии"""
import logging

import configs
import atypes
import log_objects


def _to_aircraft(obj) -> log_objects.Aircraft:
    return obj


class ObjectsController:
    """Класс, обрабатывающий события с объектами из логов сервера"""

    def __init__(self, _ioc):
        self._objects = dict()
        self._bots = set()
        self._airfields = set()
        self._aircrafts = set()
        self._ioc = _ioc

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def objects(self) -> configs.Objects:
        """Словарь объёктов логах"""
        return self._ioc.objects

    def create_object(self, atype: atypes.Atype12) -> log_objects.Object:
        obj = self.objects[atype.object_name]
        """Создать объект соответствующего типа"""
        if 'BotPilot' in obj.log_name and 'aircraft' in obj.cls:
            self._objects[atype.object_id] = log_objects.BotPilot(
                atype.object_id, obj, self._objects[atype.parent_id], atype.country_id, atype.coal_id, atype.name)
            self._bots.add(self._objects[atype.object_id])
        if obj.playable and 'aircraft' in obj.cls and 'pilot' not in obj.cls:
            self._objects[atype.object_id] = log_objects.Aircraft(
                atype.object_id, obj, atype.country_id, atype.coal_id, atype.name)
            self._aircrafts.add(self._objects[atype.object_id])
        if 'airfield' in obj.cls:
            self._objects[atype.object_id] = log_objects.Airfield(
                atype.object_id, atype.country_id, atype.coal_id, dict())
            self._airfields.add(self._objects[atype.object_id])
        if obj.cls in log_objects.GROUND_CLASSES:
            self._objects[atype.object_id] = log_objects.Ground(
                atype.object_id, obj, atype.country_id, atype.coal_id, atype.name)
        if atype.object_id not in self._objects:
            self._objects[atype.object_id] = log_objects.Object(
                atype.object_id, atype.country_id, atype.coal_id, atype.name)
        return self._objects[atype.object_id]

    def get_object(self, object_id) -> log_objects.Object:
        """Получить объект"""
        if object_id in self._objects:
            return self._objects[object_id]

    def get_ground(self, ground_id) -> log_objects.Ground:
        """Получить наземный объект"""
        if ground_id in self._objects:
            return self._objects[ground_id]

    def get_bot(self, bot_id) -> log_objects.BotPilot:
        """Получить бота"""
        if bot_id in self._objects:
            return self._objects[bot_id]

    def get_aircraft(self, aircraft_id) -> log_objects.Aircraft:
        """Получить самолёт"""
        if aircraft_id in self._objects:
            return self._objects[aircraft_id]

    def get_airfield(self, airfield_id) -> log_objects.Airfield:
        """Получить аэродром"""
        if airfield_id in self._objects:
            return self._objects[airfield_id]

    def start_mission(self) -> None:
        """Обработать начало миссии"""

    def damage(self, atype: atypes.Atype2) -> None:
        """Обработать событие урона"""
        target = self._objects[atype.target_id]
        target.update_pos(atype.pos)
        if atype.attacker_id:
            attacker = self.get_object(atype.attacker_id)
            attacker.update_pos(atype.pos)
            if isinstance(attacker, log_objects.Aircraft):
                _to_aircraft(attacker).add_damage(target, atype.damage)

    def kill(self, atype: atypes.Atype3) -> None:
        """Обработать событие убийства"""
        target = self.get_object(atype.target_id)
        target.kill(pos=atype.pos)
        if atype.attacker_id:
            attacker = self.get_object(atype.attacker_id)
            attacker.update_pos(atype.pos)
            if isinstance(attacker, log_objects.Aircraft):
                _to_aircraft(attacker).add_kill(target)

    def takeoff(self, atype: atypes.Atype5) -> None:
        """Обработать взлёт"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.takeoff(atype.pos)

    def land(self, atype: atypes.Atype6) -> None:
        """Посадить самолёт"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.land(atype.pos, list(self._airfields), self.config.gameplay.airfield_radius)

    def end_mission(self) -> None:
        """Завершить миссию"""
        for aircraft in self._aircrafts:
            aircraft.landed = True
            aircraft.is_safe = True
        self._objects.clear()
        self._bots.clear()
        self._airfields.clear()
        self._aircrafts.clear()

    def airfield(self, atype: atypes.Atype9) -> None:
        """Создать/обновленить аэродром"""
        if atype.airfield_id in self._objects:
            airfield = self.get_airfield(atype.airfield_id)
            airfield.update(atype.country_id, atype.coal_id)
        else:
            airfield = log_objects.Airfield(atype.airfield_id, atype.country_id, atype.coal_id, atype.pos)
            self._objects[atype.airfield_id] = airfield
            self._airfields.add(airfield)

    def spawn(self, atype: atypes.Atype10) -> None:
        """Обработать появление игрока"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.update_pos(atype.pos)
        bot = self.get_bot(atype.bot_id)
        if bot:
            bot.update_pos(atype.pos)
        else:
            logging.warning('not found bot')

    def deinitialize(self, atype: atypes.Atype16) -> None:
        """Деинициализировать бота"""
        bot = self.get_bot(atype.bot_id)
        bot.deinitialize(atype.pos)

    def change_pos(self, atype: atypes.Atype17) -> None:
        """Измененить позицию объекта"""
        self.get_object(atype.object_id).update_pos(atype.pos)

    def eject_leave(self, atype: atypes.Atype18) -> None:
        """Обработать прыжок с парашютом"""
        aircraft = self.get_aircraft(atype.parent_id)
        bot = self.get_bot(atype.bot_id)
        if aircraft:
            aircraft.ejected = True
        else:
            logging.warning('Warning! not found aircraft')
        if bot:
            bot.ejected = True
            logging.warning('Warning! not found bot')

    def end_sortie(self, atype: atypes.Atype4) -> None:
        """Обработать завершение вылета"""
        pass

    def hit(self, atype: atypes.Atype1) -> None:
        """Обработать попадание"""
        pass

    def group(self, atype: atypes.Atype11) -> None:
        """Обработать появление группы в логах"""
        pass

    def version(self, atype: atypes.Atype15):
        """Обработать версию в логах"""
        pass
