"""Модель данных карты кампании"""
import datetime

from .campaign_mission import CampaignMission

DATE_FORMAT = '%d.%m.%Y'

ORDER = 'order'
DATE = 'current_date'
MISSION_DATE = 'mission_date'
TVD_NAME = 'tvd_name'
MONTHS = 'months'
MISSION = 'mission'


class CampaignMap:
    """Класс кампании, хранящий текущее состояние игрового процесса на карте"""
    def __init__(
            self,
            order: int,
            date: str,
            mission_date: str,
            tvd_name: str,
            months: list,
            mission: CampaignMission = None
    ):
        self.order = order  # порядковый номер карты кампании
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)  # дата кампании (дата последней завершённой миссии)
        self.mission_date = datetime.datetime.strptime(mission_date, DATE_FORMAT)  # дата текущей миссии
        self.tvd_name = tvd_name  # имя твд
        self.months = months  # завершённые месяцы
        self.mission = mission

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            ORDER: self.order,
            TVD_NAME: self.tvd_name,
            DATE: self.date.strftime(DATE_FORMAT),
            MISSION_DATE: self.mission_date.strftime(DATE_FORMAT),
            MONTHS: self.months,
            MISSION: self.mission
        }

    @property
    def current_month(self) -> str:
        """Текущий месяц карты кампании"""
        return self.date.strftime('01.%m.%Y')

    def is_ended(self, end_date: str):
        """Закончена ли карта по дате"""
        end = datetime.datetime.strptime(end_date, DATE_FORMAT)
        return self.date >= end

    def set_date(self, date: str):
        """Установить текущую дату карты"""
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)