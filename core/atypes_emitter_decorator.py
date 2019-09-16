"Потоки событый из логов"
# pylint: disable=too-many-public-methods
from __future__ import annotations
from rx.subject import Subject
from .atypes_emitter import AtypesEmitter


class AtypesEmitterDecorator(AtypesEmitter):
    "Декоратор с потоками сообщений из логов"

    @property
    def events_mission_start(self) -> Subject:
        "Observable старта миссии"
        return self._atypes[0]

    @property
    def events_hit(self) -> Subject:
        "Observable попаданий"
        return self._atypes[1]

    @property
    def events_damage(self) -> Subject:
        "Observable урона"
        return self._atypes[2]

    @property
    def events_kill(self) -> Subject:
        "Observable убийств"
        return self._atypes[3]

    @property
    def events_sortie_end(self) -> Subject:
        "Observable завершений вылета"
        return self._atypes[4]

    @property
    def events_takeoff(self) -> Subject:
        "Observable взлётов"
        return self._atypes[5]

    @property
    def events_landing(self) -> Subject:
        "Observable посадок самолётов"
        return self._atypes[6]

    @property
    def events_mission_end(self) -> Subject:
        "Observable завершений миссии"
        return self._atypes[7]

    @property
    def events_mission_result(self) -> Subject:
        "Observable целей миссии (mission objective)"
        return self._atypes[8]

    @property
    def events_airfield(self) -> Subject:
        "Observable инициализаций аэродромов"
        return self._atypes[9]

    @property
    def events_player_spawn(self) -> Subject:
        "Observable инициализаций игроков"
        return self._atypes[10]

    @property
    def events_group(self) -> Subject:
        "Observable инициализаций групп"
        return self._atypes[11]

    @property
    def events_game_object(self) -> Subject:
        "Observable инициализаций игровых объектов"
        return self._atypes[12]

    @property
    def events_influence_area(self) -> Subject:
        "Observable инициализаций зоны влияния"
        return self._atypes[13]

    @property
    def events_influence_area_boundary(self) -> Subject:
        "Observable многоугольников зон влияния"
        return self._atypes[14]

    @property
    def events_log_version(self) -> Subject:
        "Observable версий логов"
        return self._atypes[15]

    @property
    def events_bot_deinitialization(self) -> Subject:
        "Observable де-инициализаций игроков"
        return self._atypes[16]

    @property
    def events_pos_changed(self) -> Subject:
        "Observable изменений позиции"
        return self._atypes[17]

    @property
    def events_bot_eject_leave(self) -> Subject:
        "Observable прыжков с парашютом"
        return self._atypes[18]

    @property
    def events_round_end(self) -> Subject:
        "Observable завершений раундов"
        return self._atypes[19]

    @property
    def events_player_connected(self) -> Subject:
        "Observable подключений игроков"
        return self._atypes[20]

    @property
    def events_player_disconnected(self) -> Subject:
        "Observable отключений игроков"
        return self._atypes[21]

    @property
    def events_tank_travel(self) -> Subject:
        "Observable движений танков"
        return self._atypes[22]
