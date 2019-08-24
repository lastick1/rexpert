"""Мок коллекции игроков в БД"""

from storage import Players
from .stubs import pass_


class PlayersMock(Players):
    """Мок коллекции игроков в БД"""

    def __init__(self):
        super().__init__()
        self.count = pass_
        self.find = pass_
        self.reset_mods_for_all = pass_
        self.update = pass_
        self.update_airfield = pass_
        self.update_airfields = pass_
        self.update_one = pass_
        self.update_request_body = pass_
