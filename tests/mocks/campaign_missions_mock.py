"""Мок коллекции миссий кампании"""

from storage import CampaignMissions
from .stubs import pass_


class CampaignMissionsMock(CampaignMissions):
    """Мок коллекции миссий кампании"""

    def __init__(self):
        super().__init__(None)
        self.convert_from_document = pass_
        self.load_all_by_guimap = pass_
        self.load_by_date = pass_
        self.update_airfield = pass_
        self.update_airfields = pass_
        self.update_one = pass_
