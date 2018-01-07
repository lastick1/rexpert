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
