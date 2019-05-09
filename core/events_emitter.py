"Источник всех событий, возникающих в ходе работы приложения"
from __future__ import annotations

from rx.subjects.behaviorsubject import BehaviorSubject
from rx.subjects.subject import Subject

from .gameplay_emitter import GameplayEmitter


class EventsEmitter(GameplayEmitter):
    "Шина событий приложения"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._campaign_mission: Subject = Subject()
        self._current_tvd: BehaviorSubject = BehaviorSubject(None)
        self._player_finish: Subject = Subject()
        self._generations: Subject = Subject()

    @property
    def campaign_mission(self) -> Subject:
        "Текущая миссия кампании"
        return self._campaign_mission

    @property
    def current_tvd(self) -> BehaviorSubject:
        "Текущий ТВД"
        return self._current_tvd

    @property
    def player_finish(self) -> Subject:
        "Поток событий завершений самолётовылетов"
        return self._player_finish

    @property
    def generations(self) -> Subject:
        "Поток запусков генерации миссий"
        return self._generations
