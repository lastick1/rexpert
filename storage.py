"""Работа с БД"""
from __future__ import annotations
import datetime

import pymongo

import configs
import constants
import model


def _update_request_body(document: dict) -> dict:
    """Построить запрос обновления документа"""
    return {'$set': document}


class CollectionWrapper:
    """Класс работы с коллекцией"""
    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection

    def update_one(self, _filter, document):
        """Обновить документ в коллекции"""
        self.collection.update_one(_filter, document, upsert=True)


class CampaignMaps(CollectionWrapper):
    """Работа с документами карт кампании в БД"""

    @staticmethod
    def _convert_from_document(document) -> model.CampaignMap:
        """Конвертировать документ из БД в объект класса карты кампании"""
        return model.CampaignMap(
            order=document[constants.CampaignMap.ORDER],
            date=document[constants.CampaignMap.DATE],
            mission_date=document[constants.CampaignMap.MISSION_DATE],
            tvd_name=document[constants.TVD_NAME],
            months=document[constants.CampaignMap.MONTHS],
            mission=CampaignMissions.convert_from_document(document[constants.CampaignMap.MISSION])
        )

    def update(self, campaign_map: model.CampaignMap):
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

    def load_by_order(self, order: int) -> model.CampaignMap:
        """Загрузить карту кампании по её порядковому номеру"""
        return self._convert_from_document(self.collection.find_one({constants.CampaignMap.ORDER: order}))

    def load_by_tvd_name(self, tvd_name: str) -> model.CampaignMap:
        """Загрузить карту кампании по имени её ТВД (карты)"""
        return self._convert_from_document(self.collection.find_one({constants.TVD_NAME: tvd_name}))


class CampaignMissions(CollectionWrapper):
    """Работа с документами миссий в БД"""

    @staticmethod
    def _convert_actions(actions: list) -> list:
        """Конвертировать игровые действия из документа"""
        result = list()
        for action in actions:
            if action[constants.GameplayAction.KIND] == model.DivisionKill.__name__:
                act = model.DivisionKill(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
            elif action[constants.GameplayAction.KIND] == model.WarehouseDisable.__name__:
                act = model.WarehouseDisable(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
            elif action[constants.GameplayAction.KIND] == model.AirfieldKill.__name__:
                act = model.AirfieldKill(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
            elif action[constants.GameplayAction.KIND] == model.TanksCoverFail.__name__:
                act = model.TanksCoverFail(
                    action[constants.GameplayAction.TIK],
                    action[constants.COUNTRY],
                    action[constants.GameplayAction.OBJECT_NAME]
                )
                act.date = datetime.datetime.strptime(action[constants.GameplayAction.DATE], constants.DATE_FORMAT)
                result.append(act)
        return result

    @staticmethod
    def convert_from_document(document) -> model.CampaignMission:
        """Конвертировать документ из БД в объект класса миссии"""
        if document:
            return model.CampaignMission(
                file=document[constants.CampaignMission.FILE],
                date=document['date'],
                tvd_name=document[constants.TVD_NAME],
                additional=document[constants.CampaignMission.ADDITIONAL],
                server_inputs=document[constants.CampaignMission.SERVER_INPUTS],
                objectives=document[constants.CampaignMission.OBJECTIVES],
                airfields=document[constants.CampaignMission.AIRFIELDS],
                units=document[constants.CampaignMission.DIVISION_UNITS],
                actions=CampaignMissions._convert_actions(document[constants.CampaignMission.ACTIONS])
            )

    def update(self, mission: model.CampaignMission):
        """Обновить/создать документ в БД"""
        self.update_one({'date': mission.date.strftime(constants.DATE_FORMAT)}, _update_request_body(mission.to_dict()))

    def load_by_date(self, date: str) -> model.CampaignMission:
        """Загрузить миссию по её игровой дате"""
        return self.convert_from_document(self.collection.find_one({'date': date}))

    def load_all_by_guimap(self, tvd_name) -> list:
        """Загрузить все миссии указанного ТВД"""
        result = list()
        for each in self.collection.find({'guimap': tvd_name}):
            result.append(self.convert_from_document(each))
        return result


class Divisions(CollectionWrapper):
    """Работа с документами дивизий в БД"""

    @staticmethod
    def _make_filter(tvd_name: str, division_name: str) -> dict:
        """Построить фильтр для поиска документа дивизии в БД"""
        return {constants.TVD_NAME: tvd_name, constants.NAME: division_name}

    @staticmethod
    def _convert_from_document(document) -> model.Division:
        """Конвертировать документ из БД в объект класса дивизии"""
        return model.Division(
            tvd_name=document[constants.TVD_NAME],
            name=document[constants.NAME],
            units=document[constants.Division.UNITS],
            pos=document[constants.POS]
        )

    def update(self, division: model.Division):
        """Обновить/создать документ в БД"""
        self.update_one(self._make_filter(division.tvd_name, division.name), _update_request_body(division.to_dict()))

    def load_by_name(self, tvd_name: str, division_name: str) -> model.Division:
        """Загрузить данные дивизии по её имени"""
        return self._convert_from_document(self.collection.find_one(self._make_filter(tvd_name, division_name)))

    def load_by_tvd(self, tvd_name: str) -> tuple:
        """Загрузить дивизии указанного ТВД"""
        result = list()
        for document in self.collection.find({constants.TVD_NAME: tvd_name}):
            result.append(self._convert_from_document(document))
        return tuple(result)


class Warehouses(CollectionWrapper):
    """Работа с документами складов в БД"""

    @staticmethod
    def _make_filter(tvd_name: str, name: str) -> dict:
        """Построить фильтр для поиска документа склада в БД"""
        return {constants.TVD_NAME: tvd_name, constants.NAME: name}

    @staticmethod
    def _convert_from_document(document) -> model.Warehouse:
        """Конвертировать документ из БД в объект класса склада"""
        return model.Warehouse(
            name=document[constants.NAME],
            tvd_name=document[constants.TVD_NAME],
            health=document[constants.Warehouse.HEALTH],
            deaths=document[constants.Warehouse.DEATHS],
            country=document[constants.COUNTRY],
            pos=document[constants.POS]
        )

    def update(self, warehouse: model.Warehouse) -> None:
        """Обновить/создать документ в БД"""
        self.update_one(
            self._make_filter(warehouse.tvd_name, warehouse.name), _update_request_body(warehouse.to_dict()))

    def load_by_name(self, tvd_name: str, name: str) -> model.Warehouse:
        """Загрузить данные склада по его имени"""
        document = self.collection.find_one(self._make_filter(tvd_name, name))
        if not document:
            raise NameError(f'not found warehouse:{tvd_name} {name}')
        return self._convert_from_document(document)

    def load_by_tvd(self, tvd_name: str) -> list:
        """Загрузить склады указанного ТВД"""
        result = list()
        for document in self.collection.find({constants.TVD_NAME: tvd_name}):
            result.append(self._convert_from_document(document))
        return result


class Players(CollectionWrapper):
    """Работа с документами игроков в БД"""
    def count(self, account_id) -> int:
        """Посчитать документы игрока в БД"""
        return self.collection.count({constants.ID: account_id})

    def find(self, account_id) -> model.Player:
        """Найти документ игрока в БД"""
        document = self.collection.find_one({constants.ID: account_id})
        return model.Player(account_id, document)

    def update(self, player: model.Player):
        """Обновить/создать игрока в БД"""
        document = _update_request_body(player.to_dict())
        self.collection.update_one({constants.ID: player.account_id}, document, upsert=True)

    def reset_mods_for_all(self, value: int):
        """Сбросить количество модификаций всем игрокам"""
        self.collection.update_many({}, {'$set': {constants.Player.UNLOCKS: value}})


class Airfields(CollectionWrapper):
    """Работа с документами аэродромов в БД"""

    def update_airfield(self, managed_airfield: model.ManagedAirfield):
        """Обновить аэродром"""
        update = _update_request_body(managed_airfield.to_dict())
        self.update_one({constants.ID: managed_airfield.id}, update)

    def update_airfields(self, managed_airfields: list):
        """Обновить аэродромы"""
        for managed_airfield in managed_airfields:
            self.update_airfield(managed_airfield)

    @staticmethod
    def _convert_from_document(document) -> model.ManagedAirfield:
        """Конвертировать документ из БД в объект класса управляемого аэродрома"""
        return model.ManagedAirfield(
            name=document[constants.NAME],
            tvd_name=document[constants.TVD_NAME],
            x=float(document[constants.POS]['x']),
            z=float(document[constants.POS]['z']),
            planes=document[constants.Airfield.PLANES]
        )

    def load_by_id(self, airfield_id) -> model.ManagedAirfield:
        """Загрузить аэродром по его идентификатору из базы данных"""
        document = self.collection.find_one({constants.ID: airfield_id})
        if document:
            return self._convert_from_document(document)
        raise NameError(f'аэродром с airfield_id:{airfield_id} не найден')

    def load_by_tvd(self, tvd_name: str) -> list:
        """Загрузить аэродромы для ТВД из базы данных"""
        return list(self._convert_from_document(document)
                    for document in self.collection.find({constants.TVD_NAME: tvd_name}))

    def load_by_name(self, tvd_name: str, airfield_name: str) -> model.ManagedAirfield:
        """Загрузить аэродром указанного ТВД по его имени"""
        return self._convert_from_document(
            self.collection.find_one({constants.TVD_NAME: tvd_name, 'name': airfield_name}))


class Storage:
    """Класс работы с БД"""
    def __init__(self, main: configs.Main):
        if not main:
            print('main: {}'.format(main))
        self._main = main
        self._mongo = pymongo.MongoClient(self._main.mongo_host, self._main.mongo_port)
        self._database = self._mongo[main.mongo_database]
        self.airfields = Airfields(self._database[Airfields.__name__])
        self.players = Players(self._database[Players.__name__])
        self.campaign_maps = CampaignMaps(self._database[CampaignMaps.__name__])
        self.campaign_missions = CampaignMissions(self._database[CampaignMissions.__name__])
        self.divisions = Divisions(self._database[Divisions.__name__])
        self.warehouses = Warehouses(self._database[Warehouses.__name__])

    def drop_database(self):
        """Удалить базу данных (использовать только в тестах)"""
        self._mongo.drop_database(self._main.mongo_database)
