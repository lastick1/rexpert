from processing.player import *
from processing.squad import *
import rcon
import pymongo


class PlayersController:
    """ Контроллер обработки событий, связанных с игроками """
    def __init__(self, commands: rcon.Commander, players: pymongo.collection.Collection):
        self._commands = commands
        self.__players = players
        pass

    def spawn_player(self, aircraft_id, bot_id, account_id, profile_id, name, pos, aircraft_name, country_id,
                     coal_id, airfield_id, airstart, parent_id, payload_id, fuel, skin, weapon_mods_id,
                     cartridges, shells, bombs, rockets, form) -> None:

        p = Player(account_id, self.__players.find_one({'_id': account_id}))
        p.nickname = name
        # self._commands.message(account_id, 'Hello {}!'.format(name))
        self.__players.update_one({'_id': p.account_id}, {'$set': p.to_dict()}, upsert=True)

    def connect_player(self, account_id: str, profile_id: str) -> None:
        pass

    def disconnect_player(self, account_id: str, profile_id: str) -> None:
        pass
