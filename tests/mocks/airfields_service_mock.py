"""Заглушка сервиса аэродромов"""
from configs import Config
from services import AirfieldsService

class AirfieldsServiceMock(AirfieldsService):
    """Заглушка сервиса аэродромов"""
    def __init__(self, config: Config):
        super().__init__(config)

    def spawn(self, tvd, aircraft_name: str, xpos: float, zpos: float):
        pass

    def finish(self, tvd_name: str, airfield_country: int, bot):
        pass
