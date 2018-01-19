""" Обработка игроков """
import datetime
import atypes

import log_objects

from processing.player import Player


def _update_request_body(document: dict) -> dict:
    """Построить запрос обновления документа"""
    return {'$set': document}


class PlayersController:
    """Контроллер обработки событий, связанных с игроками"""
    def __init__(self, ioc):
        self._ioc = ioc
        self.player_by_bot_id = dict()

    def spawn(self, atype: atypes.Atype10) -> None:
        """Обработка появления игрока"""
        player = self._ioc.storage.players.find(atype.account_id)
        player.nickname = atype.name
        if not self._ioc.config.main.offline_mode:
            if not self._ioc.rcon.connected:
                self._ioc.rcon.connect()
                self._ioc.rcon.auth(self._ioc.config.main.rcon_login, self._ioc.config.main.rcon_password)
            self._ioc.rcon.private_message(atype.account_id, 'Hello {}!'.format(atype.name))

        self._ioc.storage.players.update(player)
        self.player_by_bot_id[atype.bot_id] = player

    def finish(self, atype: atypes.Atype16):
        """Обработать конец вылета (деинициализация бота)"""
        bot = self._ioc.objects_controller.get_bot(atype.bot_id)
        player = None
        changed = False

        has_kills = len(bot.aircraft.killboard) > 0
        has_damage = len(bot.aircraft.damageboard) > 0
        ff_kills = len(bot.aircraft.friendly_fire_kills) > 0
        ff_damage = len(bot.aircraft.friendly_fire_damages) > 0
        friendly_fire = ff_damage or ff_kills

        if not friendly_fire and bot.aircraft.landed and has_kills or has_damage:
            changed = True
            player = self._get_player(bot)
            player.unlocks += 1

        if player and changed:
            self._ioc.storage.players.update(player)

    def _get_player(self, bot: log_objects.BotPilot) -> Player:
        """Получить игрока по его боту - пилоту в самолёте"""
        return self.player_by_bot_id[bot.obj_id]

    def connect(self, account_id: str) -> None:
        """AType 20"""

        if self._ioc.storage.players.count(account_id) == 0:
            player = Player(account_id, Player.initialize(account_id, online=True))
            self._ioc.storage.players.update(player)

        player = self._ioc.storage.players.find(account_id)

        if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
            self._ioc.rcon.banuser(player.account_id)

    def disconnect(self, account_id: str) -> None:
        """AType 21"""
        player = self._ioc.storage.players.find(account_id)
        player.online = False
        self._ioc.storage.players.update(player)
