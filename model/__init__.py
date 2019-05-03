"""Модуль модели данных"""
from __future__ import annotations
from .node import Node
from .grid import Grid
from .division import Division, DIVISIONS
from .warehouse import Warehouse, WAREHOUSES
from .airfield import ManagedAirfield
from .gameplay_actions import GameplayAction, \
    AirfieldKill, \
    DivisionKill, \
    WarehouseDisable, \
    TanksCoverFail, \
    ArtilleryKill
from .campaign_map import CampaignMap, CampaignMission
from .tvd import Tvd, Boundary
from .player import Player
from .source_mission import SourceMission
from .rcon_command import Command, \
    CommandType, \
    MessageAll, \
    MessageAllies, \
    MessageAxis, \
    MessagePrivate, \
    PlayerKick, \
    PlayerBanP15M, \
    PlayerBanP7D, \
    ServerInput
