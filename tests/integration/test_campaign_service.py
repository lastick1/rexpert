"""Тестирование управления кампанией"""
from __future__ import annotations
from typing import Dict
import logging
import datetime
import shutil
import unittest
from pathlib import Path

from core import EventsEmitter, \
    Atype0, \
    Atype19
from configs import Objects
from storage import Storage

from model import SourceMission
from processing import SourceParser
from services import ObjectsService, \
    GraphService, \
    CampaignService, \
    PlayersService, \
    WarehouseService, \
    AirfieldsService, \
    AircraftVendorService, \
    DivisionsService, \
    TvdService
from tests.utils import clean_directory
from tests.mocks import ConfigMock, \
    GeneratorMock

CONFIG = ConfigMock()

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

DATE_FORMAT = '%d.%m.%Y'

TEMP_DIRECTORY = Path('./tmp/').absolute()

MOSCOW = 'moscow'
STALIN = 'stalingrad'

TEST_TVD_DATE = '01.09.1941'
TEST_TVD_NAME = MOSCOW


def _parse_mock(name: str) -> SourceMission:
    """Фальшивый метод парсинга исходников"""
    return SourceMission(name=name, file=Path(), date=TEST_TVD_DATE, guimap=TEST_TVD_NAME)


class TestCampaignService(unittest.TestCase):
    """Тесты бизнес-логики хода кампании"""

    def setUp(self):
        """Настройка перед тестом"""
        self._storage: Storage = Storage(CONFIG)
        self._graph_service: GraphService = GraphService(CONFIG)
        self._generator: GeneratorMock = GeneratorMock(CONFIG)
        self._source_parser: SourceParser = SourceParser(CONFIG)
        self._emitter: EventsEmitter = EventsEmitter()
        self._objects_service: ObjectsService = ObjectsService(
            self._emitter, CONFIG, Objects())
        self._players_service: PlayersService = PlayersService(
            self._emitter, CONFIG, self._storage, self._objects_service)
        self._warehouse_service: WarehouseService = WarehouseService(
            self._emitter, CONFIG, self._storage)
        self._airfields_service: AirfieldsService = AirfieldsService(
            self._emitter, CONFIG, self._storage, self._objects_service, AircraftVendorService(CONFIG))
        self._divisions_service: DivisionsService = DivisionsService(
            self._emitter, CONFIG, self._storage)
        self._tvd_services: Dict[str, TvdService] = {tvd_name: TvdService(tvd_name,
                                                                          CONFIG,
                                                                          self._storage,
                                                                          self._graph_service,
                                                                          self._warehouse_service)
                                                     for tvd_name in CONFIG.mgen.maps}
        self.get_xgml_file_calls = 0
        if not TEMP_DIRECTORY.exists():
            TEMP_DIRECTORY.mkdir(parents=True)
        Path('./tmp/data/scg/1/blocks_quickmission/airfields_red').mkdir(parents=True)
        Path('./tmp/data/scg/1/blocks_quickmission/airfields_blue').mkdir(parents=True)
        Path('./tmp/data/scg/2/blocks_quickmission/airfields_red').mkdir(parents=True)
        Path('./tmp/data/scg/2/blocks_quickmission/airfields_blue').mkdir(parents=True)
        Path('./tmp/data/scg/1/blocks_quickmission/icons').mkdir(parents=True)
        Path('./tmp/data/scg/2/blocks_quickmission/icons').mkdir(parents=True)
        Path('./tmp/red/').mkdir(parents=True)
        Path('./tmp/blue/').mkdir(parents=True)

    def tearDown(self):
        """Удаление базы и очистка временной папки после теста"""
        self._storage.drop_database()
        clean_directory(str(TEMP_DIRECTORY))
        self._generator.generations.clear()

    def _get_xgml_file_mock(self, tvd_name: str) -> str:
        """Подделка метода получения файла графа"""
        self.get_xgml_file_calls = 0
        return str(CONFIG.mgen.xgml[tvd_name])

    def test_next_mission_bin_name(self):
        """Отличается имя следующей миссии от имени текущей"""
        campaign = CampaignService(
            self._emitter,
            CONFIG,
            self._storage,
            self._players_service,
            self._graph_service,
            self._warehouse_service,
            self._airfields_service,
            self._divisions_service,
            self._tvd_services,
            self._source_parser,
            self._generator
        )
        self._source_parser.parse_in_dogfight = _parse_mock
        for tvd_name in CONFIG.mgen.maps:
            self._graph_service.get_file = self._get_xgml_file_mock
            campaign.initialize_map(tvd_name)
        atype = Atype0(
            tik=0,
            date=datetime.datetime.strptime('01.10.1941', DATE_FORMAT),
            file_path=r'Multiplayer/Dogfight\result2.msnbin',
            game_type_id=2,
            countries=dict(),
            settings=(0, 0),
            mods=False,
            preset_id=0
        )
        # Act
        campaign._start_mission(atype)
        # Assert
        self.assertEqual(campaign.next_name, 'result1')

    def test_reset(self):
        """Сбрасывается состояние кампании"""
        campaign = CampaignService(
            self._emitter,
            CONFIG,
            self._storage,
            self._players_service,
            self._graph_service,
            self._warehouse_service,
            self._airfields_service,
            self._divisions_service,
            self._tvd_services,
            self._source_parser,
            self._generator
        )
        for tvd_name in CONFIG.mgen.maps:
            self._graph_service.get_file = self._get_xgml_file_mock
            campaign.initialize_map(tvd_name)
        # Act
        campaign.reset()
        # Assert
        self.assertEqual(self._storage.campaign_maps.count(), 0)
        self.assertEqual(self._storage.airfields.collection.count(), 0)

    def test_generate(self):
        """Генерируется указанная миссия"""
        shutil.copy('./data/scg/1/stalin-base.ldf', './tmp/data/scg/1/')
        shutil.copy('./data/scg/2/moscow_base.ldf', './tmp/data/scg/2/')
        campaign = CampaignService(
            self._emitter,
            CONFIG,
            self._storage,
            self._players_service,
            self._graph_service,
            self._warehouse_service,
            self._airfields_service,
            self._divisions_service,
            self._tvd_services,
            self._source_parser,
            self._generator
        )
        self._graph_service.get_file = self._get_xgml_file_mock
        campaign.initialize()
        campaign_map = self._storage.campaign_maps.load_by_tvd_name(MOSCOW)
        campaign_map.set_date(CONFIG.mgen.cfg[MOSCOW]['start_date'])
        self._storage.campaign_maps.update(campaign_map)
        campaign._campaign_map = campaign_map
        # Act
        campaign.generate('result2', MOSCOW, '03.09.1941')
        # Assert
        self.assertIn(('result2', MOSCOW), self._generator.generations)

    def test_generate_next_with_atype_19(self):
        """Генерируется следующая миссия с AType:19 в логе"""
        campaign = CampaignService(
            self._emitter,
            CONFIG,
            self._storage,
            self._players_service,
            self._graph_service,
            self._warehouse_service,
            self._airfields_service,
            self._divisions_service,
            self._tvd_services,
            self._source_parser,
            self._generator
        )
        shutil.copy('./data/scg/2/moscow_base.ldf',
                    './tmp/data/scg/2/moscow_base.ldf')
        self._graph_service.get_file = self._get_xgml_file_mock
        self._source_parser.parse_in_dogfight = _parse_mock
        campaign.initialize_map(MOSCOW)
        atype0 = Atype0(
            tik=0,
            date=datetime.datetime.strptime('01.10.1941', DATE_FORMAT),
            file_path=r'Multiplayer/Dogfight\result1.msnbin',
            game_type_id=2,
            countries=dict(),
            settings=(0, 0),
            mods=False,
            preset_id=0
        )

        # Act
        campaign._start_mission(atype0)
        campaign._end_round(Atype19(1312))

        # Assert
        self.assertIn(('result2', MOSCOW), self._generator.generations)

    def test_initialize_map(self):
        """Инициализируется карта кампании"""
        order = 1
        campaign = CampaignService(
            self._emitter,
            CONFIG,
            self._storage,
            self._players_service,
            self._graph_service,
            self._warehouse_service,
            self._airfields_service,
            self._divisions_service,
            self._tvd_services,
            self._source_parser,
            self._generator
        )
        self._graph_service.get_file = self._get_xgml_file_mock
        # Act
        campaign.initialize_map(TEST_TVD_NAME)
        # Assert
        campaign_map = self._storage.campaign_maps.load_by_order(order)
        self.assertSequenceEqual(campaign_map.months, [
                                 campaign_map.date.strftime(DATE_FORMAT)])

    def test_initialize(self):
        """Инициализируется кампания"""
        shutil.copy('./data/scg/1/stalin-base.ldf', './tmp/data/scg/1/')
        shutil.copy('./data/scg/2/moscow_base.ldf', './tmp/data/scg/2/')
        campaign = CampaignService(
            self._emitter,
            CONFIG,
            self._storage,
            self._players_service,
            self._graph_service,
            self._warehouse_service,
            self._airfields_service,
            self._divisions_service,
            self._tvd_services,
            self._source_parser,
            self._generator
        )
        self._graph_service.get_file = self._get_xgml_file_mock
        # Act
        campaign.initialize()
        # Assert
        self.assertIn(('result1', MOSCOW), self._generator.generations)


if __name__ == '__main__':
    unittest.main(verbosity=2)
