"Модель данных игрока"
from .objects import Aircraft, BotPilot

ID = '_id'
NICKNAME = 'nickname'
BAN_DATE = 'ban_expire_date'
KNOWN_NICKNAMES = 'known_nicknames'
UNLOCKS = 'unlocks'


class Player:
    "Класс игрока"
    def __init__(self, account_id: str, data: dict, aircraft: Aircraft, bot: BotPilot):
        self.account_id = account_id
        self.current_aircraft = aircraft
        self.current_bot = bot
        self._nickname = data[NICKNAME]
        self.ban_expire_date = data[BAN_DATE]
        self.previous_nicknames = data[KNOWN_NICKNAMES]
        self.unlocks = data[UNLOCKS]

    def to_dict(self):
        "Сериализация в словарь для MongoDB"
        return {
            ID: self.account_id,
            NICKNAME: self._nickname,
            BAN_DATE: self.ban_expire_date,
            KNOWN_NICKNAMES: self.previous_nicknames,
            UNLOCKS: self.unlocks
        }

    def get_nickname(self):
        "Полчить ник"
        return self._nickname

    def set_nickname(self, value):
        "Присвоить ник"
        if not self.previous_nicknames:
            self.previous_nicknames = list()
        if self._nickname and value != self._nickname:
            self.previous_nicknames.append(self._nickname)
        self._nickname = value

    nickname = property(fget=get_nickname, fset=set_nickname, doc='Ник игрока')
