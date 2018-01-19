"""Модель данных миссии кампании"""
import datetime

DATE_FORMAT = '%d.%m.%Y'
ID = '_id'
KIND = 'kind'
FILE = 'file'
DATE = 'date'
GUIMAP = 'guimap'
ADDITIONAL = 'additional'
COMPLETED = 'completed'
ROUND_ENDED = 'round_ended'
TIK_LAST = 'tik_last'
SERVER_INPUTS = 'server_inputs'
OBJECTIVES = 'objectives'
AIRFIELDS = 'airfields'
DIVISION_UNITS = 'division_units'


class CampaignMission:
    """Класс текущей миссии кампании"""
    def __init__(
            self,
            kind: str,
            file: str,
            date: str,
            guimap: str,
            additional: dict,
            server_inputs: list,
            objectives: list,
            airfields: list,
            division_units: list
    ):
        self.kind = kind  # тип миссии - противостояние или захват
        self.file = file  # имя файла миссии - result1 или result2
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)  # игровая дата в миссии
        self.guimap = guimap  # имя карты из логов
        self.additional = additional  # дополнительная информация о миссии из логов
        self.is_correctly_completed = False  # признак корректного завершения миссии (есть atype7)
        self.is_round_ended = False  # признак завершённости раунда (есть atype19)
        self.tik_last = 0  # последний тик в миссии
        self.server_inputs = server_inputs  # сервер инпуты в исходнике миссии
        self.objectives = objectives  # все обжективы в исходнике миссии
        self.airfields = airfields  # все аэродромы в исходнике миссии
        self.division_units = division_units  # все юниты дивизий в исходнике миссии

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            # ID: self.date.strftime(DATE_FORMAT),
            DATE: self.date.strftime(DATE_FORMAT),
            FILE: self.file,
            KIND: self.kind,
            GUIMAP: self.guimap,
            ADDITIONAL: self.additional,
            COMPLETED: self.is_correctly_completed,
            ROUND_ENDED: self.is_round_ended,
            TIK_LAST: self.tik_last,
            SERVER_INPUTS: self.server_inputs,
            OBJECTIVES: self.objectives,
            AIRFIELDS: self.airfields,
            DIVISION_UNITS: self.division_units
        }
