"""Объекты, встречаемые в логах"""
from __future__ import annotations
import codecs


class Object:
    """Класс объекта из логов"""
    # pylint: disable=R0913,R0903
    def __init__(self, cls_name: str, log_name: str, playable: str, name: str, name_ru: str):
        self.cls = cls_name
        self.log_name = log_name
        self.playable = bool(int(playable))
        self.name = name
        self.name_ru = name_ru.replace('\n', '').replace('\r', '')


class Objects(dict):
    """Словарь объектов"""
    def __init__(self):
        with codecs.open(r'./configs/objects.csv', encoding='utf-8') as stream:
            lines = stream.readlines()
        tmp = list(Object(*x.split(',')) for x in lines[1:])
        data = list((x.log_name, x) for x in tmp)
        super().__init__(data)
