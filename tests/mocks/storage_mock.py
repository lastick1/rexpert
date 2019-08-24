"""Заглушка работы с БД"""


from storage import Storage
from .configs import MainMock
from .airfields_mock import AirfieldsMock
from .campaign_maps_mock import CampaignMapsMock
from .campaign_missions_mock import CampaignMissionsMock
from .players_mock import PlayersMock
from .divisions_mock import DivisionsMock
from .warehouses_mock import WarehousesMock


class StorageMock(Storage):
    """Заглушка работы с БД"""

    def __init__(self, main: MainMock):
        super().__init__(main)
        self._airfields = AirfieldsMock()
        self._campaign_maps = CampaignMapsMock()
        self._campaign_missions = CampaignMissionsMock()
        self._players = PlayersMock()
        self._divisions = DivisionsMock()
        self._warehouses = WarehousesMock()
