"Сервис обработки действий игроков из логов"
from __future__ import annotations
from typing import Dict

import datetime
import logging

from core import EventsEmitter, \
    Atype0, \
    Atype4, \
    Atype5, \
    Atype10, \
    Atype13, \
    Atype14, \
    Atype20, \
    Atype21, \
    Spawn, \
    Takeoff, \
    Finish
from configs import Config
from storage import Storage
from log_objects import BotPilot
from model import Player, \
    MessagePrivate, \
    PlayerKick, \
    PlayerBanP15M

from .base_event_service import BaseEventService
from .objects_service import ObjectsService


class PlayersService(BaseEventService):
    "Сервис обработки действий игроков из логов"

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config,
            storage: Storage,
            objects_service: ObjectsService
    ):
        super().__init__(emitter)
        self._config: Config = config
        self._storage: Storage = storage
        self._objects_service: ObjectsService = objects_service
        self.player_by_bot_id: Dict[int, Player] = dict()
        self.bot_id_by_aircraft_id: Dict[int, int] = dict()
        self.unlocks_taken: Dict[str, int] = dict()

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.events_mission_start.subscribe_(self._start_mission),
            self.emitter.events_sortie_end.subscribe_(self._end_sortie),
            self.emitter.events_player_connected.subscribe_(self._connect),
            self.emitter.events_player_disconnected.subscribe_(self._disconnect),

            self.emitter.sortie_spawn.subscribe_(self._spawn),
            self.emitter.sortie_takeoff.subscribe_(self._takeoff),
            self.emitter.sortie_deinitialize.subscribe_(self._finish),
        ])

    def _get_player(self, bot: BotPilot) -> Player:
        """Получить игрока по его боту - пилоту в самолёте"""
        return self.player_by_bot_id[bot.obj_id]

    def reset(self):
        """Сбросить состояние модификаций игроков и онлайн в кампании"""
        self._storage.players.reset_mods_for_all(
            self._config.gameplay.unlocks_start)

    def _start_mission(self, atype: Atype0):
        """Обработать начало миссии"""
        self.player_by_bot_id.clear()
        self.bot_id_by_aircraft_id.clear()
        self.unlocks_taken.clear()

    def _takeoff(self, takeoff: Takeoff):
        """Обработка взлёта"""
        player = self._storage.players.find(takeoff.account_id)
        if takeoff.unlocks > player.unlocks:
            self.emitter.commands_rcon.on_next(PlayerKick(player.account_id))

    def _end_mission(self):
        """Обработать конец миссии"""

    def _spawn(self, spawn: Spawn) -> None:
        """Обработка появления игрока"""
        player = self._storage.players.find(spawn.account_id)
        player.nickname = spawn.name

        if spawn.unlocks > player.unlocks:
            message = f'{player.nickname} TAKEOFF is FORBIDDEN FOR YOU on this aircraft. ' + \
                f'Available modifications {player.unlocks}'
        else:
            message = f'{player.nickname} takeoff granted! Available modifications {player.unlocks}'

        self.emitter.commands_rcon.on_next(MessagePrivate(message, spawn.account_id))

        self._storage.players.update(player)

    def _finish(self, finish: Finish):
        """Обработать конец вылета (деинициализация бота)"""
        if finish.gain_unlocks:
            try:
                player = self._get_player(self._objects_service.get_bot(self.bot_id_by_aircraft_id[finish.aircraft_id]))
                player.unlocks += 1
                self._storage.players.update(player)
            except Exception as exception:
                logging.exception(exception)

    def _connect(self, atype: Atype20) -> None:
        """AType 20"""

        if self._storage.players.count(atype.account_id) == 0:
            player = Player(atype.account_id, Player.initialize(
                atype.account_id, online=True))
            self._storage.players.update(player)

        player = self._storage.players.find(atype.account_id)
        if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
            self.emitter.commands_rcon.on_next(
                PlayerBanP15M(player.account_id))
        else:
            self.emitter.commands_rcon.on_next(MessagePrivate(
                f'Hello {player.nickname}!', player.account_id))

    def _disconnect(self, atype: Atype21) -> None:
        """AType 21"""
        player = self._storage.players.find(atype.account_id)
        player.online = False
        self._storage.players.update(player)

    def _end_sortie(self, atype: Atype4) -> None:
        """Обработать завершение вылета"""

    def _influence_area(self, atype: Atype13):
        """Обработать объявление зоны влияния в логах"""

    def _influence_area_boundary(self, atype: Atype14):
        """Обновить многоугольник зоны влияния"""
