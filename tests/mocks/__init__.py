"Модуль с заглушками для тестов"
from .stubs import *
from .configs import ConfigMock, MainMock, MgenMock, PlanesMock
from .events_interceptor import EventsInterceptor
from .objects_service_mock import ObjectsServiceMock
from .generator_mock import GeneratorMock
from .painter_mock import PainterMock
from .rcon_mock import RConMock
from .tvd_mock import TvdMock
from .airfields_mock import AirfieldsMock
from .campaign_maps_mock import CampaignMapsMock
from .campaign_missions_mock import CampaignMissionsMock
from .divisions_mock import DivisionsMock
from .players_mock import PlayersMock
from .warehouses_mock import WarehousesMock
from .storage_mock import StorageMock
from .airfields_service_mock import AirfieldsServiceMock
