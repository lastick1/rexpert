"Обработка событий"
import processing.parse_mission_log_line
import logging
from .players_control import PlayersController
from .ground_control import GroundController
from .missions_control import CampaignController
from .objects import Airfield


class EventsController:
    def __init__(
            self,
            objects: dict,
            players_controller: PlayersController,
            ground_controller: GroundController,
            campaign_controller: CampaignController
    ):
        """
        Контроллер обработки событий из логов
        :param objects: Справочник объектов в логах
        :param players_controller: Контроллер игроков
        :param ground_controller: Контроллер наземки
        :param campaign_controller: Контроллер кампании и миссий
        """
        self.objects = objects
        self.tik_last = 0
        self.players_controller = players_controller
        self.ground_controller = ground_controller
        self.campaign_controller = campaign_controller
        self.is_correctly_completed = False
        self.countries = dict()
        self.airfields = dict()

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
        "Точка входа обработки события"
        # TODO добавить проверку на одинаковые записи подряд
        # TODO можно либо собирать список всех записей, либо использовать очередь
        # TODO https://docs.python.org/3/library/collections.html#deque-objects
        # TODO и собирать только 5-10 последних
        if 'AType' not in line:
            logging.warning('ignored bad string: [{}]'.format(line))
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
            logging.warning('unexpected atype: [{}]'.format(line))
    
    
    def update_tik(self, tik: int) -> None:
        self.tik_last = tik

    def event_mission_start(self, tik, date, file_path, game_type_id, countries, settings, mods, preset_id):
        "AType 0 handler"
        self.update_tik(tik)
        self.campaign_controller.start_mission(
            date, file_path, game_type_id, countries, settings, mods, preset_id)

    def event_hit(self, tik, ammo, attacker_id, target_id):
        "AType 1 handler"
        self.update_tik(tik)

    def event_damage(self, tik, damage, attacker_id, target_id, pos):
        "AType 2 handler"
        self.update_tik(tik)
        # дамага может не быть из-за бага логов

    def event_kill(self, tik, attacker_id, target_id, pos):
        "AType 3 handler"
        self.update_tik(tik)
        # в логах так бывает что кто-то умер, а кто не известно :)

    def event_sortie_end(self, tik, aircraft_id, bot_id, cartridges, shells, bombs, rockets, pos):
        "AType 4 handler"
        self.update_tik(tik)
        # бывают события дубли - проверяем

    def event_takeoff(self, tik, aircraft_id, pos):
        "AType 5 handler"
        self.update_tik(tik)

    def event_landing(self, tik, aircraft_id, pos):
        "AType 6 handler"
        self.update_tik(tik)

    def event_mission_end(self, tik):
        "AType 7 handler"
        self.update_tik(tik)
        self.campaign_controller.end_mission()
        self.is_correctly_completed = True

    def event_mission_result(self, tik, object_id, coal_id, task_type_id, success, icon_type_id, pos):
        "AType 8 handler"
        self.update_tik(tik)

    def event_airfield(self, tik, airfield_id, country_id, coal_id, aircraft_id_list, pos):
        "AType 9 handler"
        self.update_tik(tik)
        if airfield_id in self.airfields.keys():
            self.airfields[airfield_id].update(country_id=country_id, coal_id=coal_id)
        else:
            airfield = Airfield(airfield_id=airfield_id, country_id=country_id, coal_id=coal_id, pos=pos)
            self.airfields[airfield_id] = airfield

    def event_player(self, tik, aircraft_id, bot_id, account_id, profile_id, name, pos, aircraft_name, country_id,
                     coal_id, airfield_id, airstart, parent_id, payload_id, fuel, skin, weapon_mods_id,
                     cartridges, shells, bombs, rockets, form):
        "AType 10 handler"
        self.players_controller.spawn_player(aircraft_id, bot_id, account_id, profile_id, name, pos, aircraft_name,
                                             country_id, coal_id, airfield_id, airstart, parent_id, payload_id, fuel,
                                             skin, weapon_mods_id, cartridges, shells, bombs, rockets, form)
        self.update_tik(tik)

    def event_group(self, tik, group_id, members_id, leader_id):
        "AType 11 handler"
        self.update_tik(tik)

    def event_game_object(self, tik, object_id, object_name, country_id, coal_id, name, parent_id):
        "AType 12 handler"
        self.update_tik(tik)

    def event_influence_area(self, tik, area_id, country_id, coal_id, enabled, in_air):
        "AType 13 handler"
        self.update_tik(tik)

    def event_influence_area_boundary(self, tik, area_id, boundary):
        "AType 14 handler"
        self.update_tik(tik)

    def event_log_version(self, tik, version):
        "AType 15 handler"
        self.update_tik(tik)

    def event_bot_deinitialization(self, tik, bot_id, pos):
        "AType 16 handler"
        self.update_tik(tik)

    def event_pos_changed(self, tik, object_id, pos):
        "AType 17 handler"
        self.update_tik(tik)

    def event_bot_eject_leave(self, tik, bot_id, parent_id, pos):
        "AType 18 handler"
        self.update_tik(tik)

    def event_round_end(self, tik):
        "AType 19 handler"
        self.update_tik(tik)

    def event_player_connected(self, tik, account_id, profile_id):
        "AType 20 handler"
        self.update_tik(tik)
        self.players_controller.connect_player(account_id=account_id, profile_id=profile_id)

    def event_player_disconnected(self, tik, account_id, profile_id):
        "AType 21 handler"
        self.update_tik(tik)
        self.players_controller.disconnect_player(account_id=account_id, profile_id=profile_id)
