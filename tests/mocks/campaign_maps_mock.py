"""Мок коллекции карт кампании в БД"""

from storage import CampaignMaps
from .stubs import pass_


class CampaignMapsMock(CampaignMaps):
    """Мок коллекции карт кампании в БД"""

    def __init__(self):
        super().__init__(None)
        self.count = pass_
        self.load_all = pass_
        self.load_by_order = pass_
        self.load_by_tvd_name = pass_
        self.update = pass_
        self.update_one = pass_
        self.update_request_body = pass_
