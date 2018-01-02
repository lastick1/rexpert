"""Настройки самолётов на аэродромах"""
import json


def _clean_aircraft_name(name: str) -> str:
    """Почистить имя самолёта, чтобы оно могло быть ключом в БД"""
    return name.replace('.', '').replace(' ', '')


class Planes:
    def __init__(self, path='.\\configs\\planes.json'):
        with open(path, encoding='utf-8') as stream:
            src = json.load(stream)
        self.cfg = src
        available = list(_clean_aircraft_name(name) for name in src['planes'])
        # самолёты, доступные на сервере
        self.available = available
        # стартовое кол-во
        self.default = {_clean_aircraft_name(name): src['uncommon'][name]['_default_number'] for name in src['planes']}

    @staticmethod
    def name_to_key(name: str) -> str:
        """Приведение имени самолёта к ключу БД"""
        return _clean_aircraft_name(name.lower())
