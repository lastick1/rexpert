"""Настройки самолётов на аэродромах"""
import json


class Planes:
    def __init__(self, path='.\\configs\\planes.json'):
        with open(path) as stream:
            src = json.load(stream)
        self.cfg = src
