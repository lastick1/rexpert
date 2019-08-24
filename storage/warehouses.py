from __future__ import annotations
from typing import List
import constants
from model import Warehouse
from .collection_wrapper import CollectionWrapper, _update_request_body


class Warehouses(CollectionWrapper):
    """Работа с документами складов в БД"""

    @staticmethod
    def _make_filter(tvd_name: str, name: str) -> dict:
        """Построить фильтр для поиска документа склада в БД"""
        return {constants.TVD_NAME: tvd_name, constants.NAME: name}

    @staticmethod
    def _convert_from_document(document) -> Warehouse:
        """Конвертировать документ из БД в объект класса склада"""
        return Warehouse(
            name=document[constants.NAME],
            tvd_name=document[constants.TVD_NAME],
            health=document[constants.Warehouse.HEALTH],
            deaths=document[constants.Warehouse.DEATHS],
            country=document[constants.COUNTRY],
            pos=document[constants.POS]
        )

    def update(self, warehouse: Warehouse) -> None:
        """Обновить/создать документ в БД"""
        self.update_one(
            self._make_filter(warehouse.tvd_name, warehouse.name), _update_request_body(warehouse.to_dict()))

    def load_by_name(self, tvd_name: str, name: str) -> Warehouse:
        """Загрузить данные склада по его имени"""
        document = self.collection.find_one(self._make_filter(tvd_name, name))
        if not document:
            raise NameError(f'not found warehouse:{tvd_name} {name}')
        return self._convert_from_document(document)

    def load_by_tvd(self, tvd_name: str) -> List[Warehouse]:
        """Загрузить склады указанного ТВД"""
        result = list()
        for document in self.collection.find({constants.TVD_NAME: tvd_name}):
            result.append(self._convert_from_document(document))
        return result
