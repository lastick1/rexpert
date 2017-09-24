""" Обработка игроков """
import datetime
from processing.player import Player, ID
from processing.squad import Squad
import rcon
import pymongo
from .objects import Aircraft, BotPilot, Airfield


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
        self._commands = commands
        self.__players = players
        self.__squads = squads

    def _filter_by_account_id(self, account_id: str) -> dict:
        "Получить фильтр документов по ИД игрока"
        return {ID: account_id}

    def _update_request_body(self, document: dict) -> dict:
        "Построить запрос обновления документа"
        return {'$set': document}

    def _count(self, account_id) -> int:
        "Посчитать документы игрока в БД"
        _filter = self._filter_by_account_id(account_id)
        return self.__players.count(_filter)

    def _find(self, account_id) -> dict:
        "Найти документ игрока в БД"
        _filter = self._filter_by_account_id(account_id)
        return self.__players.find_one(_filter)

    def _update(self, player: Player):
        "Обновить/создать игрока в БД"
        _filter = self._filter_by_account_id(player.account_id)
        document = self._update_request_body(player.to_dict())
        self.__players.update_one(_filter, document, upsert=True)

    def spawn_player(self, aircraft: Aircraft, bot: BotPilot, account_id: str, profile_id: str,
                     name: str, pos: dict, aircraft_name: str, country_id: int, coal_id: int,
                     airfield_id: int, airstart: bool, parent_id: int, payload_id: int,
                     fuel: float, skin: str, weapon_mods_id: list, cartridges: int, shells: int,
                     bombs: int, rockets: int, form: str) -> None:
        "Обработка появления игрока"

        document = self._find(account_id)
        player = Player(account_id, document, aircraft, bot)
        player.nickname = name
        if self.use_rcon:
            self._commands.private_message(account_id, 'Hello {}!'.format(name))

        self._update(player)

    def bot_deinitialization(self, bot_id, pos):
        "AType 16"
        pass

    def bot_eject_leave(self, bot_id, parent_id, pos):
        pass

    def influence_area(self, area_id, country_id, coal_id, enabled, in_air):
        pass

    def influence_area_boundary(self, area_id, boundary):
        pass

    def connect_player(self, account_id: str, profile_id: str) -> None:
        "AType 20"

        if self._count(account_id) == 0:
            document = Player.create_document(account_id, online=True)
            player = Player(account_id, document)
            self._update(player)

        document = self._find(account_id)
        player = Player(account_id, document)
        if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
            self._commands.banuser(player.account_id)

    def disconnect_player(self, account_id: str, profile_id: str) -> None:
        "AType 21"
        _filter = self._filter_by_account_id(account_id)
        document = self.__players.find_one(_filter)
        player = Player(account_id, document)
        player.online = False
        self._update(player)
