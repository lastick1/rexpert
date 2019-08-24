import pymongo


class CollectionWrapper:
    """Класс работы с коллекцией"""

    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection

    def update_one(self, _filter, document):
        """Обновить документ в коллекции"""
        self.collection.update_one(_filter, document, upsert=True)

    @staticmethod
    def update_request_body(document: dict) -> dict:
        """Построить запрос обновления документа"""
        return {'$set': document}
