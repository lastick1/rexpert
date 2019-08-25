"""Мок коллекции складов в БД"""

from storage import Warehouses
from .stubs import pass_


class WarehousesMock(Warehouses):
    """Мок коллекции складов в БД"""

    def __init__(self):
        super().__init__(None)
        self.load_by_name = pass_
        self.load_by_tvd = pass_
        self.update = pass_
        self.update_one = pass_
        self.update_request_body = pass_
