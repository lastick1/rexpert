"Мок коллекции аэродромов в БД"
from storage import Airfields
from .stubs import pass_


class AirfieldsMock(Airfields):
    "Мок коллекции аэродромов в БД"

    def __init__(self):
        super().__init__(None)
        self.load_by_id = pass_
        self.load_by_name = pass_
        self.load_by_tvd = pass_
        self.update_airfield = pass_
        self.update_airfields = pass_
        self.update_one = pass_
