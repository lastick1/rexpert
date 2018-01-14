"""Модель данных игрока"""
from log_objects import BotPilot

ID = '_id'
NICKNAME = 'nickname'
BAN_DATE = 'ban_expire_date'
KNOWN_NICKNAMES = 'known_nicknames'
UNLOCKS = 'unlocks'
ONLINE = 'online'
PLANES = 'planes'
HEAVY = 'heavy'
LIGHT = 'light'


class Player:
    """Класс игрока"""
    def __init__(self, account_id: str, data: dict, bot: BotPilot = None):
        self.account_id = account_id
        self.current_bot = bot
        self._nickname = data[NICKNAME]
        self.ban_expire_date = data[BAN_DATE]
        self.previous_nicknames = data[KNOWN_NICKNAMES]
        self.unlocks = data[UNLOCKS]
        self.online = data[ONLINE]

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            ID: self.account_id,
            NICKNAME: self._nickname,
            BAN_DATE: self.ban_expire_date,
            KNOWN_NICKNAMES: self.previous_nicknames,
            UNLOCKS: self.unlocks,
            ONLINE: self.online
        }

    @staticmethod
    def initialize(account_id: str, online: bool = True) -> dict:
        """Инициализировать объект-документ для MongoDB"""
        return {
            ID: account_id,
            NICKNAME: None,
            BAN_DATE: None,
            KNOWN_NICKNAMES: [],
            UNLOCKS: 1,
            ONLINE: online
        }

    def get_nickname(self) -> str:
        """Полчить ник"""
        return self._nickname

    def set_nickname(self, value: str) -> None:
        """Присвоить ник"""
        if not self.previous_nicknames:
            self.previous_nicknames = list()
        if self._nickname and value != self._nickname:
            self.previous_nicknames.append(self._nickname)
        self._nickname = value

    nickname = property(fget=get_nickname, fset=set_nickname, doc='Ник игрока')
