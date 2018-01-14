"""Контроль объектов из логов миссии"""
import configs
import atypes
import log_objects


def _to_aircraft(obj) -> log_objects.Aircraft:
    return obj


class ObjectsController:
    """Класс, обрабатывающий события с объектами из логов сервера"""

    def __init__(self, config: configs.Config):
        self._objects = dict()
        self._bots = set()
        self._airfields = set()
        self._aircrafts = set()
        self.config = config

    def create_object(self, atype: atypes.Atype12, obj: configs.Object) -> log_objects.Object:
        """Создать объект соответствующего типа"""
        if 'BotPilot' in obj.log_name and 'aircraft' in obj.cls:
            self._objects[atype.object_id] = log_objects.BotPilot(
                atype.object_id, obj, self._objects[atype.parent_id], atype.country_id, atype.coal_id, atype.name)
            self._bots.add(self._objects[atype.object_id])
        if obj.playable and 'aircraft' in obj.cls:
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

    def damage(self, atype: atypes.Atype2):
        """Обработать событие урона"""
        target = self._objects[atype.target_id]
        target.update_pos(atype.pos)
        if atype.attacker_id:
            attacker = self.get_object(atype.attacker_id)
            attacker.update_pos(atype.pos)
            if type(attacker) is log_objects.Aircraft:
                _to_aircraft(attacker).add_damage(target, atype.damage)

    def kill(self, atype: atypes.Atype3):
        """Обработать событие убийства"""
        target = self.get_object(atype.target_id)
        target.kill(pos=atype.pos)
        if atype.attacker_id:
            attacker = self.get_object(atype.attacker_id)
            attacker.update_pos(atype.pos)
            if type(attacker) is log_objects.Aircraft:
                _to_aircraft(attacker).add_kill(target)

    def takeoff(self, atype: atypes.Atype5):
        """Обработать взлёт"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.takeoff(atype.pos)

    def land(self, atype: atypes.Atype6):
        """Посадить самолёт"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.land(atype.pos, list(self.airfields.values()), self.config.gameplay.airfield_radius)

    def end_mission(self):
        """Завершить миссию"""
        for aircraft in self._aircrafts:
            aircraft.landed = True
            aircraft.is_safe = True
        self._objects.clear()

    def airfield(self, atype: atypes.Atype9):
        """Создать/обновленить аэродром"""
        if atype.airfield_id in self._objects:
            airfield = self.get_airfield(atype.airfield_id)
            airfield.update(atype.country_id, atype.coal_id)
        else:
            airfield = log_objects.Airfield(atype.airfield_id, atype.country_id, atype.coal_id, atype.pos)
            self._objects[atype.airfield_id] = airfield
            self._airfields.add(airfield)

    def spawn(self, atype: atypes.Atype10):
        """Обработать появление игрока"""
        aircraft = self.get_aircraft(atype.aircraft_id)
        aircraft.update_pos(atype.pos)
        bot = self.get_bot(atype.bot_id)
        bot.update_pos(atype.pos)

    def deinitialize(self, atype: atypes.Atype16):
        """Деинициализировать бота"""
        bot = self.get_bot(atype.bot_id)
        bot.deinitialize(atype.pos)

    def change_pos(self, atype: atypes.Atype17):
        """Измененить позицию объекта"""
        self.get_object(atype.object_id).update_pos(atype.pos)

    def eject_leave(self, atype: atypes.Atype18):
        """Обработать прыжок с парашютом"""
        aircraft = self.get_aircraft(atype.parent_id)
        bot = self.get_bot(atype.bot_id)
        aircraft.ejected = True
        bot.ejected = True
