from __future__ import annotations
from typing import List
import constants
from model import ManagedAirfield


from .collection_wrapper import CollectionWrapper


class Airfields(CollectionWrapper):
    """Работа с документами аэродромов в БД"""

    def update_airfield(self, managed_airfield: ManagedAirfield):
        """Обновить аэродром"""
        update = CollectionWrapper.update_request_body(managed_airfield.to_dict())
        self.update_one({constants.ID: managed_airfield.id}, update)

    def update_airfields(self, managed_airfields: List[ManagedAirfield]):
        """Обновить аэродромы"""
        for managed_airfield in managed_airfields:
            self.update_airfield(managed_airfield)

    @staticmethod
    def _convert_from_document(document) -> ManagedAirfield:
        """Конвертировать документ из БД в объект класса управляемого аэродрома"""
        return ManagedAirfield(
            name=document[constants.NAME],
            tvd_name=document[constants.TVD_NAME],
            x=float(document[constants.POS]['x']),
            z=float(document[constants.POS]['z']),
            planes=document[constants.Airfield.PLANES]
        )

    def load_by_id(self, airfield_id) -> ManagedAirfield:
        """Загрузить аэродром по его идентификатору из базы данных"""
        document = self.collection.find_one({constants.ID: airfield_id})
        if document:
            return self._convert_from_document(document)
        raise NameError(f'аэродром с airfield_id:{airfield_id} не найден')

    def load_by_tvd(self, tvd_name: str) -> List[ManagedAirfield]:
        """Загрузить аэродромы для ТВД из базы данных"""
        return list(self._convert_from_document(document)
                    for document in self.collection.find({constants.TVD_NAME: tvd_name}))

    def load_by_name(self, tvd_name: str, airfield_name: str) -> ManagedAirfield:
        """Загрузить аэродром указанного ТВД по его имени"""
        return self._convert_from_document(
            self.collection.find_one({constants.TVD_NAME: tvd_name, 'name': airfield_name}))
