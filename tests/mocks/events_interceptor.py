"""Перехватчик сообщений в шине"""
from __future__ import annotations
from typing import List
from core import PointsGain, Spawn, Takeoff, Finish
from model import MessageAll, \
    MessageAllies, \
    MessageAxis, \
    MessagePrivate, \
    PlayerKick, \
    PlayerBanP7D, \
    PlayerBanP15M, \
    ServerInput
from services.base_event_service import BaseEventService


class EventsInterceptor(BaseEventService):
    """Перехватчик сообщений в шине"""

    def __init__(self, emitter):
        super().__init__(emitter)
        self.division_damages = []
        self.commands: List[MessageAll, MessageAllies, MessageAxis, MessagePrivate,
                            PlayerKick, PlayerBanP15M, PlayerBanP7D, ServerInput] = []
        self.points_gains: List[PointsGain] = []
        self.spawns: List[Spawn] = []
        self.takeoffs: List[Takeoff] = []
        self.deinitializations: List[Finish] = []
        self.init()

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.gameplay_division_damage.subscribe_(self.division_damages.append),
            self.emitter.gameplay_points_gain.subscribe_(self.points_gains.append),
            self.emitter.commands_rcon.subscribe_(self.commands.append),
            self.emitter.sortie_spawn.subscribe_(self.spawns.append),
            self.emitter.sortie_takeoff.subscribe_(self.takeoffs.append),
            self.emitter.sortie_deinitialize.subscribe_(self.deinitializations.append),
        ])
