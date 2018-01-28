"""Модель данных игрока"""
import constants
import log_objects


class Player:
    """Класс игрока"""
    def __init__(self, account_id: str, data: dict, bot: log_objects.BotPilot = None):
        self.account_id = account_id
        self.current_bot = bot
        self._nickname = data[constants.Player.NICKNAME] if constants.Player.NICKNAME in data else ''
        self.ban_expire_date = data[constants.Player.BAN_DATE]
        self.previous_nicknames = data[constants.Player.KNOWN_NICKNAMES]
        self.unlocks: int = data[constants.Player.UNLOCKS]
        self.online: bool = data[constants.Player.ONLINE]

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.ID: self.account_id,
            constants.Player.NICKNAME: self._nickname,
            constants.Player.BAN_DATE: self.ban_expire_date,
            constants.Player.KNOWN_NICKNAMES: self.previous_nicknames,
            constants.Player.UNLOCKS: self.unlocks,
            constants.Player.ONLINE: self.online
        }

    @staticmethod
    def initialize(account_id: str, online: bool = True) -> dict:
        """Инициализировать объект-документ для MongoDB"""
        return {
            constants.ID: account_id,
            constants.Player.NICKNAME: None,
            constants.Player.BAN_DATE: None,
            constants.Player.KNOWN_NICKNAMES: [],
            constants.Player.UNLOCKS: 1,
            constants.Player.ONLINE: online
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
