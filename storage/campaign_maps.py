from __future__ import annotations
import pymongo
import constants
from model import CampaignMap
from .collection_wrapper import CollectionWrapper, _update_request_body
from .campaign_missions import CampaignMissions



class CampaignMaps(CollectionWrapper):
    """Работа с документами карт кампании в БД"""

    @staticmethod
    def _convert_from_document(document) -> CampaignMap:
        """Конвертировать документ из БД в объект класса карты кампании"""
        return CampaignMap(
            order=document[constants.CampaignMap.ORDER],
            date=document[constants.CampaignMap.DATE],
            mission_date=document[constants.CampaignMap.MISSION_DATE],
            tvd_name=document[constants.TVD_NAME],
            months=document[constants.CampaignMap.MONTHS],
            mission=CampaignMissions.convert_from_document(
                document[constants.CampaignMap.MISSION])
        )

    def update(self, campaign_map: CampaignMap):
        """Обновить/создать документ в БД"""
        _b = _update_request_body(campaign_map.to_dict())
        self.collection.update_one(
            {constants.TVD_NAME: campaign_map.tvd_name}, _b, upsert=True)

    def count(self) -> int:
        """Посчитать количество карт в кампании"""
        return self.collection.count()

    def load_all(self):
        """Загрузить все данные по картам кампаний"""
        return list(self._convert_from_document(document)
                    for document in self.collection.find()
                    .sort(constants.CampaignMap.ORDER, pymongo.ASCENDING))

    def load_by_order(self, order: int) -> CampaignMap:
        """Загрузить карту кампании по её порядковому номеру"""
        return self._convert_from_document(self.collection.find_one({constants.CampaignMap.ORDER: order}))

    def load_by_tvd_name(self, tvd_name: str) -> CampaignMap:
        """Загрузить карту кампании по имени её ТВД (карты)"""
        return self._convert_from_document(self.collection.find_one({constants.TVD_NAME: tvd_name}))
