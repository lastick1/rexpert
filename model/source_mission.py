"""Модель данных исходников миссий"""
from datetime import datetime
from pathlib import Path
DATE_FORMAT = '%d.%m.%Y'


class SourceMission:
    """Класс данных исходников миссий"""
    def __init__(self, name: str, file: Path, date: str, guimap: str):
        self.name = name
        self.file = file
        self.date = datetime.strptime(date, DATE_FORMAT)
        self.guimap = guimap
        self.server_inputs = list()
        self.objectives = list()
        self.airfields = list()
        self.units = list()  # юниты(таймеры) дивизий и складов в исходниках
