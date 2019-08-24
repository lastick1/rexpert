from __future__ import annotations
from typing import List
import datetime
import constants
from model import CampaignMission, \
    DivisionKill, \
    WarehouseDisable, \
    AirfieldKill, \
    TanksCoverFail

from .collection_wrapper import CollectionWrapper

class CampaignMissions(CollectionWrapper):
    """Работа с документами миссий в БД"""

    @staticmethod
    def _convert_actions(actions: list) -> list:
        """Конвертировать игровые действия из документа"""
        result = list()
        for action in actions:
            if action[constants.GameplayAction.KIND] == DivisionKill.__name__:
                act = DivisionKill(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(
                    action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
            elif action[constants.GameplayAction.KIND] == WarehouseDisable.__name__:
                act = WarehouseDisable(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(
                    action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
            elif action[constants.GameplayAction.KIND] == AirfieldKill.__name__:
                act = AirfieldKill(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(
                    action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
            elif action[constants.GameplayAction.KIND] == TanksCoverFail.__name__:
                act = TanksCoverFail(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(
                    action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
        return result

    @staticmethod
    def convert_from_document(document) -> CampaignMission:
        """Конвертировать документ из БД в объект класса миссии"""
        if document:
            return CampaignMission(
                file=document[constants.CampaignMission.FILE],
                date=document['date'],
                tvd_name=document[constants.TVD_NAME],
                additional=document[constants.CampaignMission.ADDITIONAL],
                server_inputs=document[constants.CampaignMission.SERVER_INPUTS],
                objectives=document[constants.CampaignMission.OBJECTIVES],
                airfields=document[constants.CampaignMission.AIRFIELDS],
                units=document[constants.CampaignMission.DIVISION_UNITS],
                actions=CampaignMissions._convert_actions(
                    document[constants.CampaignMission.ACTIONS])
            )

    def update(self, mission: CampaignMission):
        """Обновить/создать документ в БД"""
        self.update_one({'date': mission.date.strftime(
            constants.DATE_FORMAT)}, CollectionWrapper.update_request_body(mission.to_dict()))

    def load_by_date(self, date: str) -> CampaignMission:
        """Загрузить миссию по её игровой дате"""
        return self.convert_from_document(self.collection.find_one({'date': date}))

    def load_all_by_guimap(self, tvd_name) -> List[CampaignMission]:
        """Загрузить все миссии указанного ТВД"""
        result = list()
        for each in self.collection.find({'guimap': tvd_name}):
            result.append(self.convert_from_document(each))
        return result
