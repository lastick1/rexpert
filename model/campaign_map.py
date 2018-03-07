"""Модель данных карты кампании"""
import datetime

import constants

from .campaign_mission import CampaignMission


class CampaignMap:
    """Класс кампании, хранящий текущее состояние игрового процесса на карте"""
    def __init__(
            self,
            order: int,
            date: str,
            mission_date: str,
            tvd_name: str,
            months: list,
            actions: list,
            mission: CampaignMission = None
    ):
        self.order = order  # порядковый номер карты кампании
        self.date = datetime.datetime.strptime(date, constants.DATE_FORMAT)  # дата последней завершённой миссии
        self.mission_date = datetime.datetime.strptime(mission_date, constants.DATE_FORMAT)  # дата текущей миссии
        self.tvd_name = tvd_name  # имя твд
        self.months = months  # завершённые месяцы
        self.actions = actions  # игровые действия на карте
        self.mission = mission

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.CampaignMap.ORDER: self.order,
            constants.TVD_NAME: self.tvd_name,
            constants.CampaignMap.DATE: self.date.strftime(constants.DATE_FORMAT),
            constants.CampaignMap.MISSION_DATE: self.mission_date.strftime(constants.DATE_FORMAT),
            constants.CampaignMap.MONTHS: self.months,
            constants.CampaignMap.ACTIONS: list(x.to_dict() for x in self.actions),
            constants.CampaignMap.MISSION: self.mission.to_dict() if self.mission else None
        }

    @property
    def current_month(self) -> str:
        """Текущий месяц карты кампании"""
        return self.date.strftime('01.%m.%Y')

    def is_ended(self, end_date: str):
        """Закончена ли карта по дате"""
        end = datetime.datetime.strptime(end_date, constants.DATE_FORMAT)
        return self.date >= end

    def set_date(self, date: str):
        """Установить текущую дату карты"""
        self.date = datetime.datetime.strptime(date, constants.DATE_FORMAT)
