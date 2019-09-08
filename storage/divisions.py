"""Работа с документами дивизий в БД"""
from __future__ import annotations
from typing import Tuple
import constants
from model import Division
from .collection_wrapper import CollectionWrapper


class Divisions(CollectionWrapper):
    """Работа с документами дивизий в БД"""

    @staticmethod
    def _make_filter(tvd_name: str, division_name: str) -> dict:
        """Построить фильтр для поиска документа дивизии в БД"""
        return {constants.TVD_NAME: tvd_name, constants.NAME: division_name}

    @staticmethod
    def _convert_from_document(document) -> Division:
        """Конвертировать документ из БД в объект класса дивизии"""
        return Division(
            tvd_name=document[constants.TVD_NAME],
            name=document[constants.NAME],
            units=document[constants.Division.UNITS],
            pos=document[constants.POS]
        )

    def update(self, division: Division):
        """Обновить/создать документ в БД"""
        self.update_one(self._make_filter(
            division.tvd_name, division.name), CollectionWrapper.update_request_body(division.to_dict()))

    def load_by_name(self, tvd_name: str, division_name: str) -> Division:
        """Загрузить данные дивизии по её имени"""
        return self._convert_from_document(self.collection.find_one(self._make_filter(tvd_name, division_name)))

    def load_by_tvd(self, tvd_name: str) -> Tuple[Division]:
        """Загрузить дивизии указанного ТВД"""
        result = list()
        for document in self.collection.find({constants.TVD_NAME: tvd_name}):
            result.append(self._convert_from_document(document))
        return tuple(result)
