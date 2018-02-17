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
            tvd_name: str,
            additional: dict,
            server_inputs: list,
            objectives: list,
            airfields: list,
            units: list
    ):
        self.kind = kind  # тип миссии - противостояние или захват
        self.file = file  # имя файла миссии - result1 или result2
        self.date = datetime.datetime.strptime(date, constants.DATE_FORMAT)  # игровая дата в миссии
        self.tvd_name = tvd_name  # имя карты из логов
        self.additional = additional  # дополнительная информация о миссии из логов
        self.is_correctly_completed = False  # признак корректного завершения миссии (есть atype7)
        self.is_round_ended = False  # признак завершённости раунда (есть atype19)
        self.tik_last = 0  # последний тик в миссии
        self.server_inputs = server_inputs  # сервер инпуты в исходнике миссии
        self.objectives = objectives  # все обжективы в исходнике миссии
        self.airfields = airfields  # все аэродромы в исходнике миссии
        self.units = units  # все юниты дивизий и складов в исходнике миссии

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.CampaignMission.DATE: self.date.strftime(constants.DATE_FORMAT),
            constants.CampaignMission.FILE: self.file,
            constants.CampaignMission.KIND: self.kind,
            constants.TVD_NAME: self.tvd_name,
            constants.CampaignMission.ADDITIONAL: self.additional,
            constants.CampaignMission.COMPLETED: self.is_correctly_completed,
            constants.CampaignMission.ROUND_ENDED: self.is_round_ended,
            constants.CampaignMission.TIK_LAST: self.tik_last,
            constants.CampaignMission.SERVER_INPUTS: self.server_inputs,
            constants.CampaignMission.OBJECTIVES: self.objectives,
            constants.CampaignMission.AIRFIELDS: self.airfields,
            constants.CampaignMission.DIVISION_UNITS: self.units
        }

    @property
    def map_icons(self) -> dict:
        """Иконки целей для изображения карты и планнера"""
        icons = {
            '1': {
                'flames': [],
                'trucks': [],
                'tanks': [],
                'arts': [],
                'warehouses': [],
                'hqs': [],
                'airfields': [],
                'forts': []
            },
            '2': {
                'flames': [],
                'trucks': [],
                'tanks': [],
                'arts': [],
                'warehouses': [],
                'hqs': [],
                'airfields': [],
                'forts': []
            }
        }
        for server_input in self.server_inputs:
            if 'R' in server_input['name']:
                coal = '1'
            elif 'B' in server_input['name']:
                coal = '2'
            else:
                continue
            if 'TD' in server_input['name']:
                icons[coal]['tanks'].append(server_input['pos'])
            elif 'AD' in server_input['name']:
                icons[coal]['arts'].append(server_input['pos'])
            elif 'ID' in server_input['name']:
                icons[coal]['forts'].append(server_input['pos'])
        for airfield in self.airfields:
            coal = str(int(airfield['country']/100))
            result = airfield['pos'].copy()
            result.update({'name': airfield['name']})
            icons[coal]['airfields'].append(result)
        return icons
