"""Модель данных карты кампании и логика перехода в наступление"""
import datetime

import constants

from .campaign_mission import CampaignMission
from .gameplay_actions import GameplayAction, AirfieldKill, DivisionKill, WarehouseDisable


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
        self._actions = actions  # игровые действия на карте
        self.mission = mission  # текущая миссия
        self._last_actions = {constants.Country.USSR: None, constants.Country.GERMANY: None}

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.CampaignMap.ORDER: self.order,
            constants.TVD_NAME: self.tvd_name,
            constants.CampaignMap.DATE: self.date.strftime(constants.DATE_FORMAT),
            constants.CampaignMap.MISSION_DATE: self.mission_date.strftime(constants.DATE_FORMAT),
            constants.CampaignMap.MONTHS: self.months,
            constants.CampaignMap.ACTIONS: list(x.to_dict() for x in self._actions),
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

    def register_action(self, action: GameplayAction):
        """Зарегистрировать игровое событие"""
        self._actions.append(action)
        self._last_actions[action.country] = action

    def register_capture(self):
        """Зарегистрировать захват территории"""
        self._actions.clear()

    def is_country_completed(self, country: int):
        """страна выполнила задачи для начала наступления"""
        division_kills = 0
        warehouse_kills = 0
        for action in self._actions:
            if isinstance(action, DivisionKill) and action.country == country:
                division_kills += 1
            elif isinstance(action, WarehouseDisable) and action.country == country:
                warehouse_kills += 1

        return division_kills >= 2 and warehouse_kills >= 1

    @property
    def red_completed(self) -> bool:
        """ВВС выполнили задачи для наступления"""
        return self.is_country_completed(constants.Country.USSR)

    @property
    def blue_completed(self):
        """Люфтваффе выполнили задачи для наступления"""
        return self.is_country_completed(constants.Country.GERMANY)

    def country_attacked(self) -> int:
        """Получить страну, которая перешла в наступление"""
        red_completed = self.red_completed
        blue_completed = self.blue_completed
        if red_completed and not blue_completed:
            return self._country_attacked(constants.Country.USSR)
        if blue_completed and not red_completed:
            return self._country_attacked(constants.Country.GERMANY)
        if blue_completed and red_completed:
            return self._country_attacked(self._first_completed)
        return 0

    def _country_attacked(self, country: int) -> int:
        """Страна перешла в наступление"""
        self._actions = list(x for x in self._actions if x.country != country)
        return country

    @property
    def _first_completed(self) -> int:
        """Страна, первой выполнившая необходимые игровые действия"""
        red_last_action = self._last_actions[constants.Country.USSR]
        blue_last_action = self._last_actions[constants.Country.GERMANY]
        if red_last_action.tik < blue_last_action.tik:
            return red_last_action.country
        if blue_last_action.tik < red_last_action.tik:
            return blue_last_action.country
        # это крайне маловероятное событие, что обе страны одновременно выполнят задачи для перехода в наступление
        # время берётся по тику в логах сервера
        raise NameError(f'It happened: both countries completed tasks at the same tik')

    @property
    def killed_airfields(self) -> dict:
        """Уничтоженные аэродромы"""
        return {x.country: x.airfield_name for x in self._actions if isinstance(x, AirfieldKill)}
