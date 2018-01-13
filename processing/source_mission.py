"""Класс данных исходников миссий"""
import datetime
DATE_FORMAT = '%d.%m.%Y'


class SourceMission:
    def __init__(self, name: str, date: str, guimap: str):
        self.name = name
        self.guimap = guimap
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)
        self.server_inputs = list()
