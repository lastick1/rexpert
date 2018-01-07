"""Настройки игрового процесса"""
import json
import pathlib


class Gameplay:
    """Класс настроек игрового процесса"""
    _instances = 0

    def __init__(self):
        Gameplay._instances += 1
        if Gameplay._instances > 1:
            raise NameError('Too much Gameplay instances')
        with open('.\\configs\\gameplay.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.supply_csv = {tvd_name: pathlib.Path(r'./').joinpath(src['supply_schedule'][tvd_name])
                           for tvd_name in src['maps']}
        self.transfer_percent = src['transfer_percent']
        self.rear_max_power = src['rear_max_power']
        self.front_min_power = src['front_min_power']
        self.front_max_power = src['front_max_power']
        self.front_start_power = src['front_start_power']
