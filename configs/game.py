"Настройки игрового процесса"
import json

class Gameplay:
    "Класс настроек игрового процесса"
    _instances = 0
    def __init__(self):
        Gameplay._instances += 1
        if Gameplay._instances > 1:
            raise NameError('Too much Gameplay instances')
        with open('.\\configs\\gameplay.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.penalties = src['penalties']
        self.aircraft_lost = src['aircraft_lost']
        self.grounds = src['grounds']
        supply = src['supply']
        self.free_plane_hours = supply['free_plane_hours']
        self.renew_minutes = supply['renew_minutes']
        self.aircraft_multipliers = {
            'light': supply['aircraft_multipliers']['light'],
            'medium': supply['aircraft_multipliers']['medium'],
            'heavy': supply['aircraft_multipliers']['heavy'],
            'transport': supply['aircraft_multipliers']['transport']
        }
