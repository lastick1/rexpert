"""Настройки самолётов на аэродромах"""
from __future__ import annotations
from json import load


def _clean_aircraft_name(name: str) -> str:
    """Почистить имя самолёта, чтобы оно могло быть ключом в БД"""
    return name.replace('.', '').replace(' ', '')


class Planes:
    """Настройки самолётов на аэродромах"""
    def __init__(self, path='./configs/planes.json'):
        with open(path, encoding='utf-8') as stream:
            src = load(stream)
        self.cfg = src

    @staticmethod
    def name_to_key(name: str) -> str:
        """Приведение имени самолёта к ключу БД"""
        return _clean_aircraft_name(name.lower())
