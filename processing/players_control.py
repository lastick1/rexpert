""" Обработка игроков """
import datetime
from processing.player import Player, ID
from processing.squad import Squad
import rcon
import pymongo
from .objects import BotPilot


def _filter_by_account_id(account_id: str) -> dict:
    "Получить фильтр документов по ИД игрока"
    return {ID: account_id}


def _update_request_body(document: dict) -> dict:
    "Построить запрос обновления документа"
    return {'$set': document}


class PlayersController:
    """ Контроллер обработки событий, связанных с игроками """
    def __init__(
            self,
            offline_mode: bool,
            commands: rcon.DServerRcon,
            players: pymongo.collection.Collection,
            squads: pymongo.collection.Collection
    ):
        self.use_rcon = not offline_mode
        self.player_by_bot_id = dict()
        self._commands = commands
        self.__players = players
        self.__squads = squads

    def _count(self, account_id) -> int:
        "Посчитать документы игрока в БД"
        _filter = _filter_by_account_id(account_id)
        return self.__players.count(_filter)

    def _find(self, account_id) -> dict:
        "Найти документ игрока в БД"
        _filter = _filter_by_account_id(account_id)
        return self.__players.find_one(_filter)

    def _update(self, player: Player):
        "Обновить/создать игрока в БД"
        _filter = _filter_by_account_id(player.account_id)
        document = _update_request_body(player.to_dict())
        self.__players.update_one(_filter, document, upsert=True)

    def spawn(self, bot: BotPilot, account_id: str, name: str) -> None:
        "Обработка появления игрока"

        document = self._find(account_id)
        player = Player(account_id, document, bot)
        player.nickname = name
        if self.use_rcon:
            self._commands.private_message(account_id, 'Hello {}!'.format(name))

        self._update(player)
        self.player_by_bot_id[bot.obj_id] = player

    def finish(self, bot: BotPilot):
        "Обработать конец вылета (деинициализация бота)"
        has_kills = len(bot.aircraft.killboard) > 0
        has_damage = len(bot.aircraft.damageboard) > 0
        ff_kills = len(bot.aircraft.friendly_fire_kills) > 0
        ff_damage = len(bot.aircraft.friendly_fire_damages) > 0
        friendly_fire = ff_damage or ff_kills
        if not friendly_fire and bot.aircraft.landed and has_kills or has_damage:
            player = self._get_player(bot)
            player.unlocks += 1
            self._update(player)

    def _get_player(self, bot: BotPilot) -> Player:
        "Получить игрока по его боту - пилоту в самолёте"
        return self.player_by_bot_id[bot.obj_id]

    def connect(self, account_id: str) -> None:
        "AType 20"

        if self._count(account_id) == 0:
            document = Player.create_document(account_id, online=True)
            player = Player(account_id, document)
            self._update(player)

        document = self._find(account_id)
        player = Player(account_id, document)
        if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
            self._commands.banuser(player.account_id)

    def disconnect(self, account_id: str) -> None:
        "AType 21"
        document = self._find(account_id)
        player = Player(account_id, document)
        player.online = False
        self._update(player)
