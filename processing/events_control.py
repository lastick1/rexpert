"""Обработка событий"""
# pylint: disable=W0613
import logging
import datetime
import processing.parse_mission_log_line
import configs
from .players_control import PlayersController
from .ground_control import GroundController
from .campaign_control import CampaignController
from .airfields_control import AirfieldsController
from .objects import Aircraft, BotPilot, Airfield, Ground, Object, GROUND_CLASSES


class EventsController:
    """Контроллер обработки событий из логов"""
    def __init__(
            self,
            objects: dict,
            players_controller: PlayersController,
            ground_controller: GroundController,
            campaign_controller: CampaignController,
            airfields_controller: AirfieldsController,
            config: configs.Main
    ):
        """
        :param objects: Справочник объектов в логах
        :param players_controller: Контроллер игроков
        :param ground_controller: Контроллер наземки
        :param campaign_controller: Контроллер кампании и миссий
        """
        self.objects = objects
        self.objects_id_ref = dict()
        self.tik_last = 0
        self.players_controller = players_controller
        self.ground_controller = ground_controller
        self.campaign_controller = campaign_controller
        self.airfields_controller = airfields_controller
        self.is_correctly_completed = False
        self.countries = dict()
        self.airfields = dict()
        self.config = config

        # порядок важен т.к. позиция в tuple соответствует ID события
        self.events_handlers = (
            self.event_mission_start, self.event_hit, self.event_damage, self.event_kill,
            self.event_sortie_end, self.event_takeoff, self.event_landing, self.event_mission_end,
            self.event_mission_result, self.event_airfield, self.event_player, self.event_group,
            self.event_game_object, self.event_influence_area, self.event_influence_area_boundary,
            self.event_log_version, self.event_bot_deinitialization, self.event_pos_changed,
            self.event_bot_eject_leave, self.event_round_end, self.event_player_connected,
            self.event_player_disconnected)

    def process_line(self, line: str):
        """Точка входа обработки события"""
        # pylint: disable=W0511
        # TODO добавить проверку на одинаковые записи подряд
        # TODO можно либо собирать список всех записей, либо использовать очередь
        # TODO https://docs.python.org/3/library/collections.html#deque-objects
        # TODO и собирать только 5-10 последних
        if 'AType' not in line:
            logging.warning('ignored bad string: [%s]', line)
            return

        try:
            atype = processing.parse_mission_log_line.parse(line)
            atype_id = atype.pop('atype_id')
            if atype_id is 0:
                self.countries = atype['countries']
            if 'country_id' in atype.keys():
                atype['coal_id'] = self.countries[atype['country_id']]
            self.events_handlers[atype_id](**atype)

        except processing.parse_mission_log_line.UnexpectedATypeWarning:
            logging.warning('unexpected atype: [%s]', line)

    def update_tik(self, tik: int) -> None:
        """Обновить тик"""
        self.tik_last = tik

    def event_mission_start(self, tik: int, date: datetime.datetime, file_path: str,
                            game_type_id, countries: dict, settings, mods, preset_id) -> None:
        """AType 0 handler"""
        self.update_tik(tik)
        self.campaign_controller.start_mission(
            date, file_path, game_type_id, countries, settings, mods, preset_id)

    def event_hit(self, tik: int, ammo: str, attacker_id: int, target_id: int) -> None:
        """AType 1 handler"""
        self.update_tik(tik)

    def event_damage(self, tik: int, damage: float, attacker_id: int, target_id: int,
                     pos: dict) -> None:
        """AType 2 handler"""
        target = self.objects_id_ref[target_id]
        target.update_pos(pos)
        attacker = None
        if attacker_id:
            attacker = self.objects_id_ref[attacker_id]
            attacker.update_pos(pos)
            attacker.add_damage(target, damage)

        self.ground_controller.damage(attacker, damage, target, pos)

        self.update_tik(tik)
        # дамага может не быть из-за бага логов

    def event_kill(self, tik: int, attacker_id: int, target_id: int, pos: dict) -> None:
        """AType 3 handler"""
        target = self.objects_id_ref[target_id]
        target.update_pos(pos)
        attacker = None
        if attacker_id:
            attacker = self.objects_id_ref[attacker_id]
            attacker.update_pos(pos)
            attacker.add_kill(target)

        self.ground_controller.kill(attacker, target, pos)

        self.update_tik(tik)
        # в логах так бывает что кто-то умер, а кто не известно :)

    def event_sortie_end(self, tik: int, aircraft_id: int, bot_id: int, cartridges: int,
                         shells: int, bombs: int, rockets: int, pos: dict) -> None:
        """AType 4 handler"""
        self.update_tik(tik)
        # бывают события дубли - проверяем

    def event_takeoff(self, tik: int, aircraft_id: int, pos: dict) -> None:
        """AType 5 handler"""
        aircraft = self._get_aircraft(aircraft_id)
        aircraft.takeoff(pos)
        self.update_tik(tik)

    def event_landing(self, tik: int, aircraft_id: int, pos: dict) -> None:
        """AType 6 handler"""
        aircraft = self._get_aircraft(aircraft_id)
        aircraft.land(pos, list(self.airfields.values()), self.config.airfield_radius)
        self.update_tik(tik)

    def event_mission_end(self, tik: int) -> None:
        """AType 7 handler"""
        self.update_tik(tik)
        self.campaign_controller.end_mission()
        self.is_correctly_completed = True

    def event_mission_result(self, tik: int, object_id: int, coal_id: int, task_type_id: int,
                             success: int, icon_type_id: int, pos: dict) -> None:
        """AType 8 handler"""
        self.update_tik(tik)

    def event_airfield(self, tik: int, airfield_id: int, country_id: int, coal_id: int,
                       aircraft_id_list: list, pos: dict) -> None:
        """AType 9 handler"""
        self.update_tik(tik)
        if airfield_id in self.airfields.keys():
            self.airfields[airfield_id].update(country_id, coal_id)
        else:
            airfield = Airfield(airfield_id, country_id, coal_id, pos)
            self.airfields[airfield_id] = airfield

    def _get_aircraft(self, aircraft_id) -> Aircraft:
        """Получить самолёт"""
        return self.objects_id_ref[aircraft_id]

    def _get_bot(self, bot_id) -> BotPilot:
        """Получить бота"""
        return self.objects_id_ref[bot_id]

    def event_player(self, tik: int, aircraft_id: int, bot_id: int, account_id: str,
                     profile_id: str, name: str, pos: dict, aircraft_name: str, country_id: int,
                     coal_id: int, airfield_id: int, airstart: bool, parent_id: int,
                     payload_id: int, fuel: float, skin: str, weapon_mods_id: list,
                     cartridges: int, shells: int, bombs: int, rockets: int, form: str) -> None:
        """AType 10 handler"""
        aircraft = self._get_aircraft(aircraft_id)
        aircraft.update_pos(pos)
        bot = self._get_bot(bot_id)
        bot.update_pos(pos)

        self.players_controller.spawn(bot, account_id, name)
        self.airfields_controller.spawn(aircraft_name, self.campaign_controller.current_tvd, self.airfields[airfield_id])
        self.update_tik(tik)

    def event_group(self, tik: int, group_id: int, members_id: int, leader_id: int) -> None:
        """AType 11 handler"""
        self.update_tik(tik)

    def event_game_object(self, tik: int, object_id: int, object_name: str, country_id: int,
                          coal_id: int, name: str, parent_id: int) -> None:
        """AType 12 handler"""
        game_object = self.create_object(object_id, self.objects[object_name],
                                         parent_id, country_id, coal_id, name)
        self.objects_id_ref[object_id] = game_object
        if game_object.cls_base == 'ground':
            self.ground_controller.ground_object(
                tik, game_object, object_name, country_id, coal_id, name, parent_id)
        self.update_tik(tik)

    def event_influence_area(self, tik: int, area_id: int, country_id: int, coal_id: int,
                             enabled: bool, in_air: bool) -> None:
        """AType 13 handler"""
        self.update_tik(tik)

    def event_influence_area_boundary(self, tik: int, area_id: int, boundary) -> None:
        """AType 14 handler"""
        self.update_tik(tik)

    def event_log_version(self, tik: int, version) -> None:
        """AType 15 handler"""
        self.update_tik(tik)

    def event_bot_deinitialization(self, tik: int, bot_id: int, pos: dict) -> None:
        """AType 16 handler"""
        bot = self.objects_id_ref[bot_id]
        bot.update_pos(pos)
        self.players_controller.finish(bot)
        self.airfields_controller.finish(self.campaign_controller.current_tvd, bot)
        self.update_tik(tik)

    def event_pos_changed(self, tik: int, object_id: int, pos: dict) -> None:
        """AType 17 handler"""
        self.update_tik(tik)

    def event_bot_eject_leave(self, tik: int, bot_id: int, parent_id: int, pos: dict) -> None:
        """AType 18 handler"""
        self.update_tik(tik)

    def event_round_end(self, tik: int) -> None:
        """AType 19 handler"""
        self.update_tik(tik)

    def event_player_connected(self, tik: int, account_id: str, profile_id: str) -> None:
        """AType 20 handler"""
        self.update_tik(tik)
        self.players_controller.connect(account_id)

    def event_player_disconnected(self, tik: int, account_id: str, profile_id: str) -> None:
        """AType 21 handler"""
        self.update_tik(tik)
        self.players_controller.disconnect(account_id)

    def create_object(self, obj_id: int, obj: configs.Object, parent_id: int, country_id: int,
                      coal_id: int, name: str) -> Object:
        """Создать объект соответствующего типа"""
        if 'BotPilot' in obj.log_name and 'aircraft' in obj.cls:
            return BotPilot(obj_id, obj, self.objects_id_ref[parent_id], country_id, coal_id, name)
        if obj.playable and 'aircraft' in obj.cls:
            return Aircraft(obj_id, obj, country_id, coal_id, name)
        if 'airfield' in obj.cls:
            return Airfield(obj_id, country_id, coal_id, None)
        _cls = obj.cls
        if obj.cls in GROUND_CLASSES:
            return Ground(obj_id, obj, country_id, coal_id, name)
        return Object(obj_id, obj, country_id, coal_id, name)
