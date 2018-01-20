"""Обработка событий"""
# pylint: disable=W0613
import logging
import datetime
import atypes

from .parse_mission_log_line import parse, UnexpectedATypeWarning


class EventsController:  # pylint: disable=R0902,R0904,R0913
    """Контроллер обработки событий из логов"""
    def __init__(self, _ioc):
        self._ioc = _ioc
        self.countries = dict()

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
            atype = parse(line)
            atype_id = atype.pop('atype_id')
            if atype_id is 0:
                self.countries = atype['countries']
            if 'country_id' in atype.keys():
                atype['coal_id'] = self.countries[atype['country_id']]
            self.events_handlers[atype_id](**atype)

        except UnexpectedATypeWarning:
            logging.warning('unexpected atype: [%s]', line)

    def event_mission_start(self, tik: int, date: datetime.datetime, file_path: str,
                            game_type_id, countries: dict, settings, mods, preset_id) -> None:
        """AType 0 handler"""
        atype = atypes.Atype0(tik, date, file_path, game_type_id, countries, settings, mods, preset_id)
        self._ioc.objects_controller.start_mission()
        self._ioc.players_controller.start_mission()
        self._ioc.campaign_controller.start_mission(atype)
        self._ioc.ground_controller.start_mission()

    def event_hit(self, tik: int, ammo: str, attacker_id: int, target_id: int) -> None:
        """AType 1 handler"""
        atype = atypes.Atype1(tik, ammo, attacker_id, target_id)

    def event_damage(self, tik: int, damage: float, attacker_id: int, target_id: int, pos: dict) -> None:
        """AType 2 handler"""
        atype = atypes.Atype2(tik, damage, attacker_id, target_id, pos)
        self._ioc.objects_controller.damage(atype)
        # дамага может не быть из-за бага логов

    def event_kill(self, tik: int, attacker_id: int, target_id: int, pos: dict) -> None:
        """AType 3 handler"""
        atype = atypes.Atype3(tik, attacker_id, target_id, pos)
        self._ioc.objects_controller.kill(atype)
        self._ioc.ground_controller.kill(atype)
        # в логах так бывает что кто-то умер, а кто не известно :)

    def event_sortie_end(self, tik: int, aircraft_id: int, bot_id: int, cartridges: int,
                         shells: int, bombs: int, rockets: int, pos: dict) -> None:
        """AType 4 handler"""
        atype = atypes.Atype4(tik, aircraft_id, bot_id, cartridges, shells, bombs, rockets, pos)
        # бывают события дубли - проверяем

    def event_takeoff(self, tik: int, aircraft_id: int, pos: dict) -> None:
        """AType 5 handler"""
        atype = atypes.Atype5(tik, aircraft_id, pos)
        self._ioc.objects_controller.takeoff(atype)

    def event_landing(self, tik: int, aircraft_id: int, pos: dict) -> None:
        """AType 6 handler"""
        atype = atypes.Atype6(tik, aircraft_id, pos)
        self._ioc.objects_controller.land(atype)

    def event_mission_end(self, tik: int) -> None:
        """AType 7 handler"""
        atype = atypes.Atype7(tik)
        self._ioc.players_controller.end_mission()
        self._ioc.campaign_controller.end_mission(atype)
        self._ioc.objects_controller.end_mission()

    def event_mission_result(self, tik: int, object_id: int, coal_id: int, task_type_id: int,
                             success: int, icon_type_id: int, pos: dict) -> None:
        """AType 8 handler"""
        atype = atypes.Atype8(tik, object_id, coal_id, task_type_id, success, icon_type_id, pos)

    def event_airfield(self, tik: int, airfield_id: int, country_id: int, coal_id: int,
                       aircraft_id_list: list, pos: dict) -> None:
        """AType 9 handler"""
        atype = atypes.Atype9(tik, airfield_id, country_id, coal_id, aircraft_id_list, pos)
        self._ioc.objects_controller.airfield(atype)

    # pylint: disable=R0914
    def event_player(self, tik: int, aircraft_id: int, bot_id: int, account_id: str,
                     profile_id: str, name: str, pos: dict, aircraft_name: str, country_id: int,
                     coal_id: int, airfield_id: int, airstart: bool, parent_id: int,
                     payload_id: int, fuel: float, skin: str, weapon_mods_id: list,
                     cartridges: int, shells: int, bombs: int, rockets: int, form: str) -> None:
        """AType 10 handler"""
        atype = atypes.Atype10(tik, aircraft_id, bot_id, account_id, profile_id, name, pos, aircraft_name, country_id,
                               coal_id, airfield_id, airstart, parent_id, payload_id, fuel, skin, weapon_mods_id,
                               cartridges, shells, bombs, rockets, form)
        self._ioc.objects_controller.spawn(atype)
        self._ioc.players_controller.spawn(atype)
        self._ioc.airfields_controller.spawn_aircraft(self._ioc.campaign_controller.current_tvd, atype)

    def event_group(self, tik: int, group_id: int, members_id: int, leader_id: int) -> None:
        """AType 11 handler"""
        atype = atypes.Atype11(tik, group_id, members_id, leader_id)

    def event_game_object(self, tik: int, object_id: int, object_name: str, country_id: int,
                          coal_id: int, name: str, parent_id: int) -> None:
        """AType 12 handler"""
        atype = atypes.Atype12(tik, object_id, object_name, country_id, coal_id, name, parent_id)
        self._ioc.objects_controller.create_object(atype)

    def event_influence_area(self, tik: int, area_id: int, country_id: int, coal_id: int,
                             enabled: bool, in_air: bool) -> None:
        """AType 13 handler"""
        atype = atypes.Atype13(tik, area_id, country_id, coal_id, enabled, in_air)

    def event_influence_area_boundary(self, tik: int, area_id: int, boundary) -> None:
        """AType 14 handler"""
        atype = atypes.Atype14(tik, area_id, boundary)

    def event_log_version(self, tik: int, version) -> None:
        """AType 15 handler"""
        atype = atypes.Atype15(tik, version)

    def event_bot_deinitialization(self, tik: int, bot_id: int, pos: dict) -> None:
        """AType 16 handler"""
        atype = atypes.Atype16(tik, bot_id, pos)
        bot = self._ioc.objects_controller.get_bot(atype.bot_id)
        self._ioc.players_controller.finish(atype)
        # TODO оптимизировать, т.к. расчёт текущего ТВД - ресурсоёмкий процесс
        self._ioc.airfields_controller.finish(self._ioc.campaign_controller.current_tvd, bot)
        self._ioc.objects_controller.deinitialize(atype)

    def event_pos_changed(self, tik: int, object_id: int, pos: dict) -> None:
        """AType 17 handler"""
        atype = atypes.Atype17(tik, object_id, pos)
        self._ioc.objects_controller.change_pos(atype)

    def event_bot_eject_leave(self, tik: int, bot_id: int, parent_id: int, pos: dict) -> None:
        """AType 18 handler"""
        atype = atypes.Atype18(tik, bot_id, parent_id, pos)
        self._ioc.objects_controller.eject_leave(atype)

    def event_round_end(self, tik: int) -> None:
        """AType 19 handler"""
        atype = atypes.Atype19(tik)
        self._ioc.campaign_controller.end_round(atype)

    def event_player_connected(self, tik: int, account_id: str, profile_id: str) -> None:
        """AType 20 handler"""
        if tik:
            atype = atypes.Atype20(tik, account_id, profile_id)
            self._ioc.players_controller.connect(atype.account_id)

    def event_player_disconnected(self, tik: int, account_id: str, profile_id: str) -> None:
        """AType 21 handler"""
        atype = atypes.Atype21(tik, account_id, profile_id)
        self._ioc.players_controller.disconnect(atype.account_id)
