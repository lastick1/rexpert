"""Источник событий самолётовылетов"""
from __future__ import annotations

from rx.subjects.subject import Subject

from .gameplay_emitter import GameplayEmitter

class SortieEmitter(GameplayEmitter):
    """Шина событий вылетов самолётов"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._spawn: Subject = Subject()
        self._takeoff: Subject = Subject()
        self._deinitialize: Subject = Subject()

    @property
    def sortie_spawn(self) -> Subject:
        """Поток событий появлений самолётов"""
        return self._spawn

    @property
    def sortie_takeoff(self) -> Subject:
        """Поток событий взлётов"""
        return self._takeoff

    @property
    def sortie_deinitialize(self) -> Subject:
        """Поток событий деинициализации ботов и завершения вылетов"""
        return self._deinitialize
