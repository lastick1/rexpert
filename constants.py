"""Константы"""
# pylint: disable=R0903


ID = '_id'
TVD_NAME = 'tvd_name'
POS = 'pos'
DATE_FORMAT = '%d.%m.%Y'
NAME = 'name'
COUNTRY = 'country'
VICTORY = {101: 'VICTORY_RED', 201: 'VICTORY_BLUD'}


class Mongo:
    """Константы базы данных"""
    SET = '$set'


class Player:
    """Константы модели данных игроков"""
    NICKNAME = 'nickname'
    BAN_DATE = 'ban_expire_date'
    KNOWN_NICKNAMES = 'known_nicknames'
    UNLOCKS = 'unlocks'
    ONLINE = 'online'
    PLANES = 'planes'
    HEAVY = 'heavy'
    LIGHT = 'light'


class Country:
    """Коды стран"""
    USSR = 101
    GERMANY = 201


class Airfield:
    """Константы модели данных аэродромов"""
    PLANES = 'planes'
    SUPPLIES = 'supplies'


class CampaignMap:
    """Константы модели данных карты кампании"""
    ORDER = 'order'
    DATE = 'current_date'
    MISSION_DATE = 'mission_date'
    MONTHS = 'months'
    MISSION = 'mission'


class TvdNames:
    """Имена ТВД"""
    MOSCOW = 'moscow'
    STALIN = 'stalingrad'
    KUBAN = 'kuban'


class GameplayAction:
    """Константы модели данных игровых событий"""
    DATE = 'date'
    TIK = 'tik'
    KIND = 'kind'
    OBJECT_NAME = 'object_name'


class CampaignMission:
    """Константы модели данных миссии кампании"""
    KIND = 'kind'
    FILE = 'file'
    DATE = 'date'
    GUIMAP = 'guimap'
    ADDITIONAL = 'additional'
    COMPLETED = 'completed'
    ROUND_ENDED = 'round_ended'
    TIK_LAST = 'tik_last'
    SERVER_INPUTS = 'server_inputs'
    OBJECTIVES = 'objectives'
    AIRFIELDS = 'airfields'
    DIVISION_UNITS = 'division_units'
    ACTIONS = 'actions'


class Division:
    """Константы модели данных дивизии"""
    UNITS = 'units'


class Warehouse:
    """Константы модели данных склада"""
    HEALTH = 'health'
    DEATHS = 'deaths'
