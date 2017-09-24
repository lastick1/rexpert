""" Обработка игроков """
import datetime
from processing.player import Player, ID
from processing.squad import Squad
import rcon
import pymongo
from .objects import BotPilot, Object


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
        self.players_aircrafts = dict()
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

    def spawn_player(self, bot: BotPilot, account_id: str, name: str) -> None:
        "Обработка появления игрока"

        document = self._find(account_id)
        player = Player(account_id, document, bot)
        player.nickname = name
        if self.use_rcon:
            self._commands.private_message(account_id, 'Hello {}!'.format(name))

        self._update(player)
        self.players_aircrafts[bot.aircraft.obj_id] = player

    def damage(self, attacker: Object, damage: float, target: Object, pos: dict):
        "Обработать килл"
        if attacker and attacker.cls_base == 'aircraft':
            pass

    def kill(self, attacker: Object, target: Object, pos: dict):
        "Обработать килл"
        if attacker and attacker.cls_base == 'aircraft':
            pass

    def bot_deinitialization(self, bot: BotPilot):
        "Обработать конец вылета"
        player = self._get_player_by_bot(bot)
        has_kills = len(player.current_bot.aircraft.killboard) > 0
        has_damage = len(player.current_bot.aircraft.damageboard) > 0
        if has_kills or has_damage:
            player.unlocks += 1
            self._update(player)

    def _get_player_by_bot(self, bot: BotPilot) -> Player:
        return self.players_aircrafts[bot.aircraft.obj_id]

    def connect_player(self, account_id: str) -> None:
        "AType 20"

        if self._count(account_id) == 0:
            document = Player.create_document(account_id, online=True)
            player = Player(account_id, document)
            self._update(player)

        document = self._find(account_id)
        player = Player(account_id, document)
        if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
            self._commands.banuser(player.account_id)

    def disconnect_player(self, account_id: str) -> None:
        "AType 21"
        document = self._find(account_id)
        player = Player(account_id, document)
        player.online = False
        self._update(player)
