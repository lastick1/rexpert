"""Настройки игрового процесса"""
from __future__ import annotations
import json
import pathlib


class Gameplay:
    """Класс настроек игрового процесса"""
    def __init__(self):
        with open('./configs/gameplay.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.supply_csv = {tvd_name: pathlib.Path(r'./').joinpath(src['supply_schedule'][tvd_name])
                           for tvd_name in src['maps']}
        self.airfield_radius = src['airfield_radius']
        self.airfield_min_planes = src['airfield_min_planes']
        self.transfer_amount = src['transfer_amount']
        self.front_max_planes = src['front_max_planes']
        self.front_init_planes = {tvd_name: src['initial_front_supply'][tvd_name] for tvd_name in src['maps']}
        self.initial_priority = {tvd_name: src['initial_priority_supply'][tvd_name] for tvd_name in src['maps']}
        self.division_death = src['division_death']
        self.division_repair = src['division_repair']
        self.division_margin = src['division_margin']
        self.division_unit_radius = src['division_unit_radius']
        self.warehouse_unit_radius = src['warehouse_unit_radius']
        self.unlocks_start = src['unlocks_start']
        self.unlocks_min = src['unlocks_min']
        self.unlocks_max = src['unlocks_max']
        self.rear_max_power = 100
