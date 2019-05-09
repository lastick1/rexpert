"Шина событий игрового процесса"

from rx.subjects.subject import Subject
from .commands_emitter import CommandsEmitter


class GameplayEmitter(CommandsEmitter):
    "Шина событий игрового процесса"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gameplay_division_damage: Subject = Subject()
        self._gameplay_warehouse_damage: Subject = Subject()
        self._gameplay_points_gain: Subject = Subject()
        self._gameplay_capture: Subject = Subject()

    @property
    def gameplay_division_damage(self) -> Subject:
        "Поток игровых событий повреждений дивизий"
        return self._gameplay_division_damage

    @property
    def gameplay_warehouse_damage(self) -> Subject:
        "Поток игровых событий повреждений складов"
        return self._gameplay_warehouse_damage

    @property
    def gameplay_points_gain(self) -> Subject:
        "Поток игровых событий получения очков захвата"
        return self._gameplay_points_gain

    @property
    def gameplay_capture(self) -> Subject:
        "Поток игровых событий захвата территории"
        return self._gameplay_capture
