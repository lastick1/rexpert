""" Обработка игроков """
import datetime

import atypes
import configs
import log_objects
import rcon
from objects_control import ObjectsController
import storage
import model


def _update_request_body(document: dict) -> dict:
    """Построить запрос обновления документа"""
    return {'$set': document}


class PlayersController:
    """Контроллер обработки событий, связанных с игроками"""
    def __init__(self, ioc):
        self._ioc = ioc
        self.player_by_bot_id: dict = None
        self.bot_id_by_aircraft_id: dict = None
        self.unlocks_taken: dict = None  # текущее количество анлоков игроков, взятое на вылет

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config
    
    @property
    def objects_controller(self) -> ObjectsController:
        """Контроллер объектов в логах миссий"""
        return self._ioc.objects_controller
    
    @property
    def storage(self) -> storage.Storage:
        """Объект для работы с БД"""
        return self._ioc.storage
    
    @property
    def rcon(self) -> rcon.DServerRcon:
        """Консоль для отправки команд в DServer.exe"""
        return self._ioc.rcon

    def _get_player(self, bot: log_objects.BotPilot) -> model.Player:
        """Получить игрока по его боту - пилоту в самолёте"""
        return self.player_by_bot_id[bot.obj_id]

    def reset(self):
        """Сбросить состояние модификаций игроков и онлайн в кампании"""
        self.storage.players.reset_mods_for_all(self.config.gameplay.unlocks_start)

    def start_mission(self):
        """Обработать начало миссии"""
        self.player_by_bot_id = dict()
        self.bot_id_by_aircraft_id = dict()
        self.unlocks_taken = dict()

    def takeoff(self, atype: atypes.Atype5):
        """Обработка взлёта"""
        player = self._get_player(self.objects_controller.get_bot(self.bot_id_by_aircraft_id[atype.aircraft_id]))
        if not self.config.main.offline_mode:
            if not self.rcon.connected:
                self.rcon.connect()
                self.rcon.auth(self.config.main.rcon_login, self.config.main.rcon_password)
            if not self.config.main.test_mode and self.unlocks_taken[player.account_id] > player.unlocks:
                self.rcon.kick(player.account_id)

    def end_mission(self):
        """Обработать конец миссии"""

    def spawn(self, atype: atypes.Atype10) -> None:
        """Обработка появления игрока"""

        player = self.storage.players.find(atype.account_id)
        player.nickname = atype.name
        self.player_by_bot_id[atype.bot_id] = player
        self.unlocks_taken[player.account_id] = len(atype.weapon_mods_id)
        self.bot_id_by_aircraft_id[atype.aircraft_id] = atype.bot_id

        if not self.config.main.offline_mode:
            if not self.rcon.connected:
                self.rcon.connect()
                self.rcon.auth(self.config.main.rcon_login, self.config.main.rcon_password)
            if self.unlocks_taken[player.account_id] > player.unlocks:
                message = f'{player.nickname} TAKEOFF is FORBIDDEN FOR YOU on this aircraft. Available unlocks {player.unlocks}'
            else:
                message = f'{player.nickname} takeoff granted! Available unlocks {player.unlocks}'
            self.rcon.private_message(player.account_id, message)

        self.storage.players.update(player)

    def finish(self, bot: log_objects.BotPilot, on_airfield=True):
        """Обработать конец вылета (деинициализация бота)"""
        player = None
        changed = False

        has_kills = len(bot.aircraft.killboard) > 0
        has_damage = len(bot.aircraft.damageboard) > 0
        ff_kills = len(bot.aircraft.friendly_fire_kills) > 0
        ff_damage = len(bot.aircraft.friendly_fire_damages) > 0
        friendly_fire = ff_damage or ff_kills

        if not friendly_fire and bot.aircraft.landed and has_kills or has_damage and on_airfield:
            changed = True
            player = self._get_player(bot)
            player.unlocks += 1

        if player and changed:
            self.storage.players.update(player)

    def connect(self, account_id: str) -> None:
        """AType 20"""

        if self.storage.players.count(account_id) == 0:
            player = model.Player(account_id, model.Player.initialize(account_id, online=True))
            self.storage.players.update(player)

        player = self.storage.players.find(account_id)
        if not self.config.main.offline_mode:
            if not self.rcon.connected:
                self.rcon.connect()
                self.rcon.auth(self.config.main.rcon_login, self.config.main.rcon_password)
            if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
                self.rcon.banuser(player.account_id)
            else:
                self.rcon.private_message(player.account_id, f'Hello {player.nickname}!')

    def disconnect(self, account_id: str) -> None:
        """AType 21"""
        player = self.storage.players.find(account_id)
        player.online = False
        self.storage.players.update(player)

    def end_sortie(self, atype: atypes.Atype4) -> None:
        """Обработать завершение вылета"""
        pass

    def influence_area(self, atype: atypes.Atype13):
        """Обработать объявление зоны влияния в логах"""
        pass

    def influence_area_boundary(self, atype: atypes.Atype14):
        """Обновить многоугольник зоны влияния"""
        pass
