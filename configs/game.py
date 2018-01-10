"""Настройки игрового процесса"""
import json
import pathlib


class Gameplay:
    """Класс настроек игрового процесса"""
    def __init__(self):
        with open('.\\configs\\gameplay.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.supply_csv = {tvd_name: pathlib.Path(r'./').joinpath(src['supply_schedule'][tvd_name])
                           for tvd_name in src['maps']}
        self.transfer_amount = src['transfer_amount']
        self.airfield_min_planes = src['airfield_min_planes']
        self.rear_max_power = src['rear_max_power']
        self.front_min_supply = src['front_min_supply']
        self.front_max_planes = src['front_max_planes']
        self.front_start_planes = src['front_start_planes']
        self.front_init_planes = {tvd_name: src['initial_front_supply'][tvd_name] for tvd_name in src['maps']}
        self.initial_priority = {tvd_name: src['initial_priority_supply'][tvd_name] for tvd_name in src['maps']}
