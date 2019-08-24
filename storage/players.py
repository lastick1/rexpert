from __future__ import annotations
import constants
from model import Player
from .collection_wrapper import CollectionWrapper, _update_request_body


class Players(CollectionWrapper):
    """Работа с документами игроков в БД"""

    def count(self, account_id) -> int:
        """Посчитать документы игрока в БД"""
        return self.collection.count({constants.ID: account_id})

    def find(self, account_id) -> Player:
        """Найти документ игрока в БД"""
        document = self.collection.find_one({constants.ID: account_id})
        return Player(account_id, document)

    def update(self, player: Player):
        """Обновить/создать игрока в БД"""
        document = _update_request_body(player.to_dict())
        self.collection.update_one(
            {constants.ID: player.account_id}, document, upsert=True)

    def reset_mods_for_all(self, value: int):
        """Сбросить количество модификаций всем игрокам"""
        self.collection.update_many(
            {}, {'$set': {constants.Player.UNLOCKS: value}})
