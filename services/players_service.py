"Сервис обработки действий игроков из логов"
from __future__ import annotations
from typing import Dict

import datetime

from core import EventsEmitter, Atype0, Atype4, Atype5, Atype10, Atype13, Atype14, Atype20, Atype21, Finish
from configs import Config
from rcon import DServerRcon
from storage import Storage
from log_objects import BotPilot
from model import Player

from .base_event_service import BaseEventService
from .objects_service import ObjectsService


class PlayersService(BaseEventService):
    "Сервис обработки действий игроков из логов"

    def __init__(self,
                 emitter: EventsEmitter,
                 config: Config,
                 rcon: DServerRcon,
                 storage: Storage,
                 objects_service: ObjectsService):
        super().__init__(emitter)
        self._config: Config = config
        self._rcon: DServerRcon = rcon
        self._storage: Storage = storage
        self._objects_service: ObjectsService = objects_service
        self.player_by_bot_id: Dict[int, Player]
        self.bot_id_by_aircraft_id: Dict[int, int]
        self.unlocks_taken: Dict[str, int]

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.events_mission_start.subscribe_(self._start_mission),
            self.emitter.events_sortie_end.subscribe_(self._end_sortie),
            self.emitter.events_takeoff.subscribe_(self._takeoff),
            self.emitter.events_player_spawn.subscribe_(self._spawn),
            self.emitter.events_player_connected.subscribe_(self._connect),
            self.emitter.events_player_disconnected.subscribe_(self._disconnect),

            self.emitter.player_finish.subscribe_(self._finish),
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
        self.player_by_bot_id = dict()
        self.bot_id_by_aircraft_id = dict()
        self.unlocks_taken = dict()

    def _takeoff(self, atype: Atype5):
        """Обработка взлёта"""
        player = self._get_player(self._objects_service.get_bot(
            self.bot_id_by_aircraft_id[atype.aircraft_id]))
        if not self._config.main.offline_mode:
            if not self._rcon.connected:
                self._rcon.connect()
                self._rcon.auth(self._config.main.rcon_login,
                                self._config.main.rcon_password)
            if not self._config.main.test_mode and self.unlocks_taken[player.account_id] > player.unlocks:
                self._rcon.kick(player.account_id)

    def _end_mission(self):
        """Обработать конец миссии"""

    def _spawn(self, atype: Atype10) -> None:
        """Обработка появления игрока"""

        player = self._storage.players.find(atype.account_id)
        player.nickname = atype.name
        self.player_by_bot_id[atype.bot_id] = player
        self.unlocks_taken[player.account_id] = len(atype.weapon_mods_id)
        self.bot_id_by_aircraft_id[atype.aircraft_id] = atype.bot_id

        if not self._config.main.offline_mode:
            if not self._rcon.connected:
                self._rcon.connect()
                self._rcon.auth(self._config.main.rcon_login,
                                self._config.main.rcon_password)
            if self.unlocks_taken[player.account_id] > player.unlocks:
                message = f'{player.nickname} TAKEOFF is FORBIDDEN FOR YOU on this aircraft. Available unlocks {player.unlocks}'
            else:
                message = f'{player.nickname} takeoff granted! Available unlocks {player.unlocks}'
            self._rcon.private_message(player.account_id, message)

        self._storage.players.update(player)

    def _finish(self, finish: Finish):
        """Обработать конец вылета (деинициализация бота)"""
        bot: BotPilot = self._objects_service.get_bot(finish.atype.bot_id)
        player = None
        changed = False

        has_kills = len(bot.aircraft.killboard) > 0
        has_damage = len(bot.aircraft.damageboard) > 0
        ff_kills = len(bot.aircraft.friendly_fire_kills) > 0
        ff_damage = len(bot.aircraft.friendly_fire_damages) > 0
        friendly_fire = ff_damage or ff_kills

        if not friendly_fire and bot.aircraft.landed and has_kills or has_damage and finish.on_airfield:
            changed = True
            player = self._get_player(bot)
            player.unlocks += 1

        if player and changed:
            self._storage.players.update(player)

    def _connect(self, atype: Atype20) -> None:
        """AType 20"""

        if self._storage.players.count(atype.account_id) == 0:
            player = Player(atype.account_id, Player.initialize(
                atype.account_id, online=True))
            self._storage.players.update(player)

        player = self._storage.players.find(atype.account_id)
        if not self._config.main.offline_mode:
            if not self._rcon.connected:
                self._rcon.connect()
                self._rcon.auth(self._config.main.rcon_login,
                                self._config.main.rcon_password)
            if player.ban_expire_date and player.ban_expire_date > datetime.datetime.now():
                self._rcon.banuser(player.account_id)
            else:
                self._rcon.private_message(
                    player.account_id, f'Hello {player.nickname}!')

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
