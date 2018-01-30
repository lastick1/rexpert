"""Работа с БД"""
import pymongo

import configs
import constants
import model


def _filter_by_id(_id: str) -> dict:
    """Получить фильтр документов по идентификатору"""
    return {constants.ID: _id}


def _filter_by_tvd(tvd_name: str) -> dict:
    """Получить фильтр документов по театру военных действий (ТВД)"""
    return {constants.TVD_NAME: tvd_name}


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
    def convert_from_document(document) -> model.CampaignMission:
        """Конвертировать документ из БД в объект класса миссии"""
        if document:
            return model.CampaignMission(
                kind=document['kind'],
                file=document['file'],
                date=document['date'],
                guimap=document['guimap'],
                additional=document['additional'],
                server_inputs=document['server_inputs'],
                objectives=document['objectives'],
                airfields=document['airfields'],
                division_units=document['division_units']
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
        return {constants.TVD_NAME: tvd_name, constants.Division.NAME: division_name}

    @staticmethod
    def _convert_from_document(document) -> model.Division:
        """Конвертировать документ из БД в объект класса дивизии"""
        return model.Division(
            tvd_name=document[constants.TVD_NAME],
            name=document[constants.Division.NAME],
            units=document[constants.Division.UNITS],
            pos=document[constants.POS]
        )

    def update(self, division: model.Division):
        """Обновить/создать документ в БД"""
        self.update_one(self._make_filter(division.tvd_name, division.name), _update_request_body(division.to_dict()))

    def load_by_name(self, tvd_name: str, division_name: str) -> model.Division:
        """Загрузить данные дивизии по её имени"""
        return self._convert_from_document(self.collection.find_one(self._make_filter(tvd_name, division_name)))

    def load_by_tvd(self, tvd_name: str) -> list:
        """Загрузить дивизии указанного ТВД"""
        result = list()
        for document in self.collection.find({constants.TVD_NAME: tvd_name}):
            result.append(self._convert_from_document(document))
        return result


class Players(CollectionWrapper):
    """Работа с документами игроков в БД"""
    def count(self, account_id) -> int:
        """Посчитать документы игрока в БД"""
        _filter = _filter_by_id(account_id)
        return self.collection.count(_filter)

    def find(self, account_id) -> model.Player:
        """Найти документ игрока в БД"""
        _filter = _filter_by_id(account_id)
        document = self.collection.find_one(_filter)
        return model.Player(account_id, document)

    def update(self, player: model.Player):
        """Обновить/создать игрока в БД"""
        _filter = _filter_by_id(player.account_id)
        document = _update_request_body(player.to_dict())
        self.collection.update_one(_filter, document, upsert=True)

    def reset_mods_for_all(self, value: int):
        """Сбросить количество модификаций всем игрокам"""
        self.collection.update_many({}, {'$set': {constants.Player.UNLOCKS: value}})


class Airfields(CollectionWrapper):
    """Работа с документами аэродромов в БД"""
    @staticmethod
    def _filter_by_tvd(tvd_name: str) -> dict:
        """Получить фильтр по театру военных действий"""
        return {constants.TVD_NAME: tvd_name}

    def update_airfield(self, managed_airfield: model.ManagedAirfield):
        """Обновить аэродром"""
        _filter = _filter_by_id(managed_airfield.id)
        update = _update_request_body(managed_airfield.to_dict())
        self.update_one(_filter, update)

    def update_airfields(self, managed_airfields: list):
        """Обновить аэродромы"""
        for managed_airfield in managed_airfields:
            self.update_airfield(managed_airfield)

    @staticmethod
    def _convert_from_document(document) -> model.ManagedAirfield:
        """Конвертировать документ из БД в объект класса управляемого аэродрома"""
        return model.ManagedAirfield(
            name=document[constants.Airfield.NAME],
            tvd_name=document[constants.TVD_NAME],
            x=float(document[constants.POS]['x']),
            z=float(document[constants.POS]['z']),
            planes=document[constants.Airfield.PLANES]
        )

    def load_by_id(self, airfield_id) -> model.ManagedAirfield:
        """Загрузить аэродром по его идентификатору из базы данных"""
        document = self.collection.find_one(_filter_by_id(_id=airfield_id))
        if document:
            return self._convert_from_document(document)
        raise NameError(f'аэродром с airfield_id:{airfield_id} не найден')

    def load_by_tvd(self, tvd_name: str) -> list:
        """Загрузить аэродромы для ТВД из базы данных"""
        return list(self._convert_from_document(document)
                    for document in self.collection.find(_filter_by_tvd(tvd_name=tvd_name)))

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
        self.airfields = Airfields(self._database['Airfields'])
        self.players = Players(self._database['Players'])
        self.campaign_maps = CampaignMaps(self._database['CampaignMaps'])
        self.campaign_missions = CampaignMissions(self._database['CampaignMissions'])
        self.divisions = Divisions(self._database['Divisions'])

    def drop_database(self):
        """Удалить базу данных (использовать только в тестах)"""
        self._mongo.drop_database(self._main.mongo_database)
