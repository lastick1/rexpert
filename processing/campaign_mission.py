"""Модель данных миссии кампании"""
import datetime
import constants


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
        self.date = datetime.datetime.strptime(date, constants.DATE_FORMAT)  # игровая дата в миссии
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
            constants.CampaignMission.DATE: self.date.strftime(constants.DATE_FORMAT),
            constants.CampaignMission.FILE: self.file,
            constants.CampaignMission.KIND: self.kind,
            constants.CampaignMission.GUIMAP: self.guimap,
            constants.CampaignMission.ADDITIONAL: self.additional,
            constants.CampaignMission.COMPLETED: self.is_correctly_completed,
            constants.CampaignMission.ROUND_ENDED: self.is_round_ended,
            constants.CampaignMission.TIK_LAST: self.tik_last,
            constants.CampaignMission.SERVER_INPUTS: self.server_inputs,
            constants.CampaignMission.OBJECTIVES: self.objectives,
            constants.CampaignMission.AIRFIELDS: self.airfields,
            constants.CampaignMission.DIVISION_UNITS: self.division_units
        }
