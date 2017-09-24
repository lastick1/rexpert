""" Обработка игроков """
import datetime
from processing.player import Player, ID, NICKNAME, BAN_DATE, KNOWN_NICKNAMES, UNLOCKS
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

    def spawn_player(self, aircraft: Aircraft, bot: BotPilot, account_id: str, profile_id: str,
                     name: str, pos: dict, aircraft_name: str, country_id: int, coal_id: int,
                     airfield_id: int, airstart: bool, parent_id: int, payload_id: int,
                     fuel: float, skin: str, weapon_mods_id: list, cartridges: int, shells: int,
                     bombs: int, rockets: int, form: str) -> None:
        "Обработка появления игрока"

        player = Player(account_id, self.__players.find_one({'_id': account_id}), aircraft, bot)
        player.nickname = name
        if self.use_rcon:
            self._commands.private_message(account_id, 'Hello {}!'.format(name))
        self.__players.update_one(
            {'_id': player.account_id}, {'$set': player.to_dict()}, upsert=True)

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
        _filter = {'_id': account_id}

        if self.__players.count(filter=_filter) == 0:
            self.__players.insert_one(self._create_document(account_id, profile_id))

        document = self.__players.find_one(filter=_filter)
        player = Player(account_id, document, None, None)
        if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
            self._commands.banuser(player.account_id)

    def _create_document(self, account_id: str, profile_id: str) -> dict:
        return {
            ID: account_id,
            NICKNAME: None,
            BAN_DATE: None,
            KNOWN_NICKNAMES: [],
            UNLOCKS: 1
        }

    def disconnect_player(self, account_id: str, profile_id: str) -> None:
        "AType 21"
        pass
