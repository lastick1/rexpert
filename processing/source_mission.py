"""Модель данных исходников миссий"""
import datetime
import pathlib
DATE_FORMAT = '%d.%m.%Y'


class SourceMission:
    """Класс данных исходников миссий"""
    def __init__(self, name: str, file: pathlib.Path, date: str, guimap: str, kind: str):
        self.name = name
        self.file = file
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)
        self.guimap = guimap
        self.server_inputs = list()
        self.objectives = list()
        self.airfields = list()
        self.division_units = list()
        self.kind = kind  # тип миссии - обычная или захват
