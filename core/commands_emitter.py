"Источник событий управления сервером (DServer)"
from __future__ import annotations

from rx.subject.subject import Subject

from .atypes_emitter_decorator import AtypesEmitterDecorator


class CommandsEmitter(AtypesEmitterDecorator):
    "Контейнер потоков команд"
    def __init__(self):
        super().__init__()
        self._commands_rcon: Subject = Subject()

    @property
    def commands_rcon(self) -> Subject:
        "Поток команд в консоль сервера (Rcon)"
        return self._commands_rcon
