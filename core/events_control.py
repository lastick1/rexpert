"""Обработка событий"""
# pylint: disable=W0613
import logging
import datetime
import atypes
import processing
from .objects_control import ObjectsController


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
            self.event_player_disconnected, self.event_tank_travel)

    def process_line(self, line: str):
        """Точка входа обработки события"""
        # pylint: disable=W0511
        # TODO добавить проверку на одинаковые записи подряд
        # TODO можно либо собирать список всех записей, либо использовать очередь
        # TODO https://docs.python.org/3/library/collections.html#deque-objects
        # TODO и собирать только 5-10 последних

        # noinspection PyBroadException
        try:
            if 'AType' not in line:
                raise NameError(f'ignored bad string: [{line}]')

            atype = parse(line)
            atype_id = atype.pop('atype_id')
            if atype_id is 0:
                self.countries = atype['countries']
            if 'country_id' in atype.keys():
                atype['coal_id'] = self.countries[atype['country_id']]
            self.events_handlers[atype_id](**atype)

        except UnexpectedATypeWarning:
            logging.warning(f'unexpected atype: [{line}]')
        except Exception as exception:
            logging.exception(f'Error {exception} on line: {line}')

    @property
    def objects_controller(self) -> ObjectsController:
        """Контроллер объектов из логов"""
        return self._ioc.objects_controller

    @property
    def players_controller(self) -> processing.PlayersController:
        """Контроллер игроков"""
        return self._ioc.players_controller

    @property
    def campaign_controller(self) -> processing.CampaignController:
        """Контроллер кампании"""
        return self._ioc.campaign_controller

    @property
    def divisions_controller(self) -> processing.DivisionsController:
        """Контроллер дивизий"""
        return self._ioc.divisions_controller

    @property
    def warehouses_controller(self) -> processing.WarehouseController:
        """Контроллер складов"""
        return self._ioc.warehouses_controller

    @property
    def ground_controller(self) -> processing.GroundController:
        """Контроллер наземных целей"""
        return self._ioc.ground_controller

    @property
    def map_painter(self) -> processing.MapPainter:
        """Генератор изображений карт миссий"""
        return self._ioc.map_painter

    @property
    def airfields_controller(self) -> processing.AirfieldsController:
        """Контроллер аэродромов"""
        return self._ioc.airfields_controller

    def event_mission_start(self, tik: int, date: datetime.datetime, file_path: str,
                            game_type_id, countries: dict, settings, mods, preset_id) -> None:
        """AType 0 handler"""
        atype = atypes.Atype0(tik, date, file_path, game_type_id,
                              countries, settings, mods, preset_id)
        self.objects_controller.start_mission()
        self.players_controller.start_mission()
        self.campaign_controller.start_mission(atype)
        self.airfields_controller.start_mission()
        self.divisions_controller.start_mission()
        self.warehouses_controller.start_mission()
        self.ground_controller.start_mission(self.campaign_controller.mission)
        # self.map_painter.update_map()

    def event_hit(self, tik: int, ammo: str, attacker_id: int, target_id: int) -> None:
        """AType 1 handler"""
        atype = atypes.Atype1(tik, ammo, attacker_id, target_id)
        self.objects_controller.hit(atype)

    def event_damage(self, tik: int, damage: float, attacker_id: int, target_id: int, pos: dict) -> None:
        """AType 2 handler"""
        atype = atypes.Atype2(tik, damage, attacker_id, target_id, pos)
        self.objects_controller.damage(atype)
        # дамага может не быть из-за бага логов

    def event_kill(self, tik: int, attacker_id: int, target_id: int, pos: dict) -> None:
        """AType 3 handler"""
        atype = atypes.Atype3(tik, attacker_id, target_id, pos)
        self.objects_controller.kill(atype)
        self.ground_controller.kill(atype)
        # в логах так бывает что кто-то умер, а кто не известно :)

    def event_sortie_end(self, tik: int, aircraft_id: int, bot_id: int, cartridges: int,
                         shells: int, bombs: int, rockets: int, pos: dict) -> None:
        """AType 4 handler"""
        atype = atypes.Atype4(tik, aircraft_id, bot_id,
                              cartridges, shells, bombs, rockets, pos)
        self.objects_controller.end_sortie(atype)
        self.players_controller.end_sortie(atype)
        # бывают события дубли - проверяем

    def event_takeoff(self, tik: int, aircraft_id: int, pos: dict) -> None:
        """AType 5 handler"""
        atype = atypes.Atype5(tik, aircraft_id, pos)
        self.objects_controller.takeoff(atype)

    def event_landing(self, tik: int, aircraft_id: int, pos: dict) -> None:
        """AType 6 handler"""
        atype = atypes.Atype6(tik, aircraft_id, pos)
        self.objects_controller.land(atype)

    def event_mission_end(self, tik: int) -> None:
        """AType 7 handler"""
        atype = atypes.Atype7(tik)
        self.players_controller.end_mission()
        self.campaign_controller.end_mission(atype)
        self.objects_controller.end_mission()

    def event_mission_result(self, tik: int, object_id: int, coal_id: int, task_type_id: int,
                             success: int, icon_type_id: int, pos: dict) -> None:
        """AType 8 handler"""
        atype = atypes.Atype8(tik, object_id, coal_id,
                              task_type_id, success, icon_type_id, pos)
        self.ground_controller.mission_result(atype)
        self.campaign_controller.mission_result(atype)

    def event_airfield(self, tik: int, airfield_id: int, country_id: int, coal_id: int,
                       aircraft_id_list: list, pos: dict) -> None:
        """AType 9 handler"""
        atype = atypes.Atype9(tik, airfield_id, country_id,
                              coal_id, aircraft_id_list, pos)
        self.objects_controller.airfield(atype)
        self.airfields_controller.spawn_airfield(atype)

    # pylint: disable=R0914
    def event_player(self, tik: int, aircraft_id: int, bot_id: int, account_id: str,
                     profile_id: str, name: str, pos: dict, aircraft_name: str, country_id: int,
                     coal_id: int, airfield_id: int, airstart: bool, parent_id: int,
                     cartridges: int, shells: int, bombs: int, rockets: int, form: str) -> None:
        """AType 10 handler"""
        atype = atypes.Atype10(tik, aircraft_id, bot_id, account_id, profile_id, name, pos, aircraft_name, country_id,
                               coal_id, airfield_id, airstart, parent_id,
                               cartridges, shells, bombs, rockets, form)
        self.objects_controller.spawn(atype)
        self.players_controller.spawn(atype)
        tvd = self.campaign_controller.current_tvd
        if atype.airstart:
            logging.warning(f'airstart {atype}')
        self.airfields_controller.spawn_aircraft(
            tvd.name, tvd.get_country(atype.point), atype)

    def event_group(self, tik: int, group_id: int, members_id: int, leader_id: int) -> None:
        """AType 11 handler"""
        atype = atypes.Atype11(tik, group_id, members_id, leader_id)
        self.objects_controller.group(atype)

    def event_game_object(self, tik: int, object_id: int, object_name: str, country_id: int,
                          coal_id: int, name: str, parent_id: int) -> None:
        """AType 12 handler"""
        atype = atypes.Atype12(tik, object_id, object_name,
                               country_id, coal_id, name, parent_id)
        self.objects_controller.create_object(atype)

    def event_influence_area(self, tik: int, area_id: int, country_id: int, coal_id: int,
                             enabled: bool, in_air: bool) -> None:
        """AType 13 handler"""
        atype = atypes.Atype13(tik, area_id, country_id,
                               coal_id, enabled, in_air)
        self.players_controller.influence_area(atype)

    def event_influence_area_boundary(self, tik: int, area_id: int, boundary) -> None:
        """AType 14 handler"""
        atype = atypes.Atype14(tik, area_id, boundary)
        self.players_controller.influence_area_boundary(atype)

    def event_log_version(self, tik: int, version) -> None:
        """AType 15 handler"""
        atype = atypes.Atype15(tik, version)
        self.objects_controller.version(atype)
        self.warehouses_controller.notify()

    def event_bot_deinitialization(self, tik: int, bot_id: int, pos: dict) -> None:
        """AType 16 handler"""
        atype = atypes.Atype16(tik, bot_id, pos)
        bot = self._ioc.objects_controller.get_bot(atype.bot_id)
        if not bot:
            raise NameError(f'Bot not found: {atype.bot_id}')
        tvd = self.campaign_controller.current_tvd
        on_airfield = self.airfields_controller.finish(
            tvd.name, tvd.get_country(atype.point), bot)
        self.players_controller.finish(bot, on_airfield)
        self.objects_controller.deinitialize(atype)

    def event_pos_changed(self, tik: int, object_id: int, pos: dict) -> None:
        """AType 17 handler"""
        atype = atypes.Atype17(tik, object_id, pos)
        self.objects_controller.change_pos(atype)

    def event_bot_eject_leave(self, tik: int, bot_id: int, parent_id: int, pos: dict) -> None:
        """AType 18 handler"""
        atype = atypes.Atype18(tik, bot_id, parent_id, pos)
        self.objects_controller.eject_leave(atype)

    def event_round_end(self, tik: int) -> None:
        """AType 19 handler"""
        atype = atypes.Atype19(tik)
        self.airfields_controller.end_round()
        self.divisions_controller.end_round()
        self.warehouses_controller.end_round()
        self.campaign_controller.end_round(atype)

    def event_player_connected(self, tik: int, account_id: str, profile_id: str) -> None:
        """AType 20 handler"""
        if tik:
            atype = atypes.Atype20(tik, account_id, profile_id)
            self.players_controller.connect(atype.account_id)

    def event_player_disconnected(self, tik: int, account_id: str, profile_id: str) -> None:
        """AType 21 handler"""
        atype = atypes.Atype21(tik, account_id, profile_id)
        self.players_controller.disconnect(atype.account_id)

    def event_tank_travel(self, tik: int, parent_id: str, pos: dict):
        """Atype 22 handler

        Arguments:
            tik {int} -- [description]
            parent_id {str} -- [description]
            pos {dict} -- [description]
        """
        pass
