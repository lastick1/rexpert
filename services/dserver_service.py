"Управление игровым сервером"
from __future__ import annotations
from typing import Dict, Any


from configs import Config
from core import EventsEmitter
from rcon import DServerRcon
from model import Command, \
    CommandType, \
    MessageAll, \
    MessageAllies, \
    MessageAxis, \
    MessagePrivate, \
    PlayerKick, \
    PlayerBanP15M, \
    PlayerBanP7D, \
    ServerInput

from .base_event_service import BaseEventService


class DServerService(BaseEventService):
    "Сервис управления DServer через Rcon"

    def __init__(self, emitter: EventsEmitter, config: Config, rcon: DServerRcon):
        super().__init__(emitter)
        self._config: Config = config
        self._rcon: DServerRcon = rcon
        self._bindings: Dict[str, Any] = {
            str(CommandType.MessageAll): self.message_all,
            str(CommandType.MessageAllies): self.message_allies,
            str(CommandType.MessageAxis): self.message_axis,
            str(CommandType.MessagePrivate): self.message_private,
            str(CommandType.PlayerKick): self.kick,
            str(CommandType.PlayerBanP15M): self.ban_short,
            str(CommandType.PlayerBanP7D): self.ban_long,
            str(CommandType.ServerInput): self.server_input,
        }

    def init(self) -> None:
        self.register_subscription(
            self.emitter.commands_rcon.subscribe_(self.on_command))

    def on_command(self, command: Command) -> None:
        "Обработать команду в RCon"
        if not self._config.main.offline_mode:
            self._bindings[str(command.type)](command)

    def message_all(self, command: MessageAll) -> None:
        "Отправить сообщение всем игрокам"
        self._rcon.info_message(command.message)

    def message_allies(self, command: MessageAllies) -> None:
        "Отправить сообщение союзникам"
        self._rcon.allies_message(command.message)

    def message_axis(self, command: MessageAxis) -> None:
        "Отправить сообщение люфтваффе"
        self._rcon.axis_message(command.message)

    def message_private(self, command: MessagePrivate) -> None:
        "Отправить сообщение игроку"
        self._rcon.private_message(command.account_id, command.message)

    def kick(self, command: PlayerKick) -> None:
        "Выбросить игрока с сервера"
        self._rcon.kick(command.account_id)

    def ban_short(self, command: PlayerBanP15M) -> None:
        "Забанить игрока на 15 минут"
        self._rcon.banuser(command.account_id)

    def ban_long(self, command: PlayerBanP7D) -> None:
        "Забанить игрока на 7 дней"
        self._rcon.ban(command.account_id)

    def server_input(self, command: ServerInput) -> None:
        "Активировать MCU ServerInput"
        self._rcon.server_input(command.name)
