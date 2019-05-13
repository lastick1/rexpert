"Модель сообщения в RCon"
from __future__ import annotations

from enum import Enum

class CommandType(Enum):
    "Тип команды или сообщения в RCon"
    MessageAll = 'MessageAll'
    MessageAllies = 'MessageAllies'
    MessageAxis = 'MessageAxis'
    MessagePrivate = 'MessagePrivate'
    PlayerKick = 'PlayerKick'
    PlayerBanP7D = 'PlayerBanP7D'
    PlayerBanP15M = 'PlayerBanP15M'
    ServerInput = 'ServerInput'


class Command:
    "Базовый класс команды серверу"
    def __init__(self, _type: CommandType):
        self.type: CommandType = _type


class MessageCommandBase(Command):
    "Базовый класс сообщения в чат"
    def __init__(self, message: str, _type: CommandType):
        super().__init__(_type)
        self.message: str = message


class MessageAll(MessageCommandBase):
    "Сообщение всем игрокам"
    def __init__(self, message: str):
        super().__init__(message, CommandType.MessageAll)


class MessageAllies(MessageCommandBase):
    "Сообщение союзникам"
    def __init__(self, message: str):
        super().__init__(message, CommandType.MessageAllies)


class MessageAxis(MessageCommandBase):
    "Сообщение люфтваффе"
    def __init__(self, message: str):
        super().__init__(message, CommandType.MessageAxis)


class MessagePrivate(MessageCommandBase):
    "Сообщение игроку"
    def __init__(self, message: str, account_id: str):
        super().__init__(message, CommandType.MessagePrivate)
        self.account_id = account_id


class PlayerKick(Command):
    "Команда удаления игрока с сервера"
    def __init__(self, account_id: str):
        super().__init__(CommandType.PlayerKick)
        self.account_id = account_id


class PlayerBanP7D(Command):
    "Команда бана игрока на 7 дней"
    def __init__(self, account_id: str):
        super().__init__(CommandType.PlayerBanP7D)
        self.account_id = account_id


class PlayerBanP15M(Command):
    "Команда бана игрока на 15 минут"
    def __init__(self, account_id: str):
        super().__init__(CommandType.PlayerBanP15M)
        self.account_id = account_id


class ServerInput(Command):
    "Отправка команды активации MCU ServerInput"
    def __init__(self, name: str):
        super().__init__(CommandType.ServerInput)
        self.name: str = name
