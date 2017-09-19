""" Обработка игроков """
from processing.player import Player
from processing.squad import Squad
import rcon
import pymongo


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

    def spawn_player(self, aircraft_id, bot_id, account_id, profile_id, name, pos, aircraft_name,
                     country_id, coal_id, airfield_id, airstart, parent_id, payload_id, fuel, skin,
                     weapon_mods_id, cartridges, shells, bombs, rockets, form) -> None:
        "Обработка появления игрока"

        player = Player(account_id, self.__players.find_one({'_id': account_id}))
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
        pass

    def disconnect_player(self, account_id: str, profile_id: str) -> None:
        pass
