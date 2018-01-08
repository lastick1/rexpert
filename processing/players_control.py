""" Обработка игроков """
import datetime
import configs
from processing.player import Player
from .storage import Storage
import rcon
from .objects import BotPilot


def _update_request_body(document: dict) -> dict:
    """Построить запрос обновления документа"""
    return {'$set': document}


class PlayersController:
    """Контроллер обработки событий, связанных с игроками"""
    def __init__(
            self,
            main: configs.Main,
            commands: rcon.DServerRcon
    ):
        self.main = main
        self.player_by_bot_id = dict()
        self._commands = commands
        self.storage = Storage(main)

    def spawn(self, bot: BotPilot, account_id: str, name: str) -> None:
        """Обработка появления игрока"""
        player = self.storage.players.find(account_id)
        player.nickname = name
        if not self.main.offline_mode:
            if not self._commands.connected:
                self._commands.connect()
                self._commands.auth(self.main.rcon_login, self.main.rcon_password)
            self._commands.private_message(account_id, 'Hello {}!'.format(name))

        self.storage.players.update(player)
        self.player_by_bot_id[bot.obj_id] = player

    def finish(self, bot: BotPilot):
        """Обработать конец вылета (деинициализация бота)"""
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

        if bot.aircraft.damaged_by_enemy and not bot.aircraft.is_safe:
            changed = True
            player = self._get_player(bot)
            player.planes[bot.aircraft.type] -= 1

        if player and changed:
            self.storage.players.update(player)

    def _get_player(self, bot: BotPilot) -> Player:
        """Получить игрока по его боту - пилоту в самолёте"""
        return self.player_by_bot_id[bot.obj_id]

    def connect(self, account_id: str) -> None:
        """AType 20"""

        if self.storage.players.count(account_id) == 0:
            player = Player(account_id, Player.initialize(account_id, online=True))
            self.storage.players.update(player)

        player = self.storage.players.find(account_id)

        if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
            self._commands.banuser(player.account_id)

    def disconnect(self, account_id: str) -> None:
        """AType 21"""
        player = self.storage.players.find(account_id)
        player.online = False
        self.storage.players.update(player)
