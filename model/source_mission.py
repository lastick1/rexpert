"""Модель данных исходников миссий"""
import datetime
import pathlib
DATE_FORMAT = '%d.%m.%Y'


class SourceMission:
    """Класс данных исходников миссий"""
    def __init__(self, name: str, file: pathlib.Path, date: str, guimap: str):
        self.name = name
        self.file = file
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)
        self.guimap = guimap
        self.server_inputs = list()
        self.objectives = list()
        self.airfields = list()
        self.units = list()  # юниты(таймеры) дивизий и складов в исходниках
        self.kind: str = None  # тип миссии - обычная или захват
