"Источник всех событий, возникающих в ходе работы приложения"
from __future__ import annotations

from rx.subjects.behaviorsubject import BehaviorSubject
from rx.subjects.subject import Subject

from .commands_emitter import CommandsEmitter


class EventsEmitter(CommandsEmitter):
    "Шина событий приложения"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._campaign_mission: BehaviorSubject = BehaviorSubject(None)
        self._current_tvd: BehaviorSubject = BehaviorSubject(None)
        self._gameplay_division_damage: Subject = Subject()
        self._gameplay_division_kill: Subject = Subject()
        self._gameplay_warehouse_damage: Subject = Subject()
        self._gameplay_warehouse_disable: Subject = Subject()
        self._gameplay_capture: Subject = Subject()
        self._player_finish: Subject = Subject()
        self._generations: Subject = Subject()

    @property
    def campaign_mission(self) -> BehaviorSubject:
        "Текущая миссия кампании"
        return self._campaign_mission

    @property
    def current_tvd(self) -> BehaviorSubject:
        "Текущий ТВД"
        return self._current_tvd

    @property
    def gameplay_division_damage(self) -> BehaviorSubject:
        "Поток игровых событий повреждений дивизий"
        return self._gameplay_division_damage

    @property
    def gameplay_division_kill(self) -> Subject:
        "Поток игровых событий уничтожений дивизий"
        return self._gameplay_division_kill

    @property
    def gameplay_warehouse_damage(self) -> Subject:
        "Поток игровых событий повреждений складов"
        return self._gameplay_warehouse_damage

    @property
    def gameplay_warehouse_disable(self) -> Subject:
        "Поток игровых событий уничтожений складов"
        return self._gameplay_warehouse_disable

    @property
    def gameplay_capture(self) -> Subject:
        "Поток игровых событий захвата территории"
        return self._gameplay_capture

    @property
    def player_finish(self) -> Subject:
        "Поток событий завершений самолётовылетов"
        return self._player_finish

    @property
    def generations(self) -> Subject:
        "Поток запусков генерации миссий"
        return self._generations
