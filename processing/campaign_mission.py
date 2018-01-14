"""Модель данных миссии кампании"""
import datetime

DATE_FORMAT = '%d.%m.%Y'
KIND = 'kind'
FILE = 'file'
DATE = 'date'


class CampaignMission:
    """Класс текущей миссии кампании"""
    def __init__(self, kind: str, file: str, date: str):
        self.kind = kind  # тип миссии - противостояние или захват
        self.file = file  # файл миссии - result1 или result2
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)  # игровая дата в миссии

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            DATE: self.date.strftime(DATE_FORMAT),
            FILE: self.file,
            KIND: self.kind
        }
