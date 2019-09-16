"Источник всех событий, возникающих в ходе работы приложения"
from __future__ import annotations

from rx.subject.behaviorsubject import BehaviorSubject
from rx.subject.subject import Subject

from .sortie_emitter import SortieEmitter


class EventsEmitter(SortieEmitter):
    "Шина событий приложения"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._campaign_mission: Subject = Subject()
        self._current_tvd: BehaviorSubject = BehaviorSubject(None)
        self._mission_victory: BehaviorSubject = BehaviorSubject(0)
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
    def mission_victory(self) -> BehaviorSubject:
        "Победа страны в миссии"
        return self._mission_victory

    @property
    def generations(self) -> Subject:
        "Поток запусков генерации миссий"
        return self._generations
