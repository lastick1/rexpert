"""Тестирование обработки событий"""
from __future__ import annotations
from typing import Dict
from pathlib import Path
import logging
import shutil
import unittest

from configs import Objects
from storage import Storage
from services import ObjectsService, \
    GraphService, \
    CampaignService, \
    PlayersService, \
    WarehouseService, \
    AirfieldsService, \
    AircraftVendorService, \
    DivisionsService, \
    TvdService, \
    GroundTargetsService
from core import EventsEmitter
from processing import SourceParser
from model import SourceMission, CampaignMap
from tests.utils import clean_directory
from tests.mocks import ConfigMock, GeneratorMock

CONFIG = ConfigMock()
OBJECTS = Objects()

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

TEST_LOG1 = './testdata/logs/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'
TEST_LOG2 = './testdata/logs/target_bombing_crashlanded_on_af_missionReport(2017-09-23_19-31-30)[0].txt'
TEST_LOG3 = './testdata/logs/multiple_spawns_missionReport(2017-09-24_14-46-12)[0].txt'
TEST_LOG4 = './testdata/logs/gkills_with_disconnect_missionReport(2017-09-26_20-37-23)[0].txt'
TEST_LOG5 = './testdata/logs/gkill_with_altf4_disco_missionReport(2017-09-26_21-10-48)[0].txt'
TEST_LOG6 = './testdata/logs/mission_rotation_atype19.txt'
DB_NAME = 'test_rexpert'


TEST_TVD_NAME = 'moscow'
TEST_TVD_DATE = '01.01.1941'
TEST_FIELDS = Path('./data/moscow_fields.csv')


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(CONFIG.mgen.xgml[tvd_name])


def _load_all_campaign_maps():
    """Фальшивый метод загрузки карт кампании"""
    return [CampaignMap(1, TEST_TVD_DATE, TEST_TVD_DATE, TEST_TVD_NAME, list(), list())]


def _parse_mock(name: str) -> SourceMission:
    """Фальшивый метод парсинга исходников"""
    return SourceMission(name=name, file=Path(), date=TEST_TVD_DATE, guimap=TEST_TVD_NAME)


def _make_dirs(dirs: list):
    for directory in dirs:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def setUp(self):
        """Настройка базы перед тестом"""
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
        self._campaign_service: CampaignService = CampaignService(
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
        self._ground_targets_service: GroundTargetsService = GroundTargetsService(
            self._emitter, CONFIG, self._objects_service)
        self.directory = Path(r'./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        _make_dirs([
            './tmp/data/scg/1/blocks_quickmission/airfields_red',
            './tmp/data/scg/1/blocks_quickmission/airfields_blue',
            './tmp/data/scg/2/blocks_quickmission/airfields_red',
            './tmp/data/scg/2/blocks_quickmission/airfields_blue',
            './tmp/data/scg/1/blocks_quickmission/icons',
            './tmp/data/scg/2/blocks_quickmission/icons',
            './tmp/red/',
            './tmp/blue/'
        ])
        self._generator.generations.clear()

    def tearDown(self):
        """Удаление базы после теста"""
        clean_directory(str(self.directory))
        self._storage.drop_database()

    def test_processing_with_atype_7(self):
        """Завершается корректно миссия с AType:7 в логе"""
        for tvd_name in CONFIG.mgen.maps:
            self._graph_service.get_file = _get_xgml_file_mock
            self._campaign_service.initialize_map(tvd_name)
        # Act
        for line in Path(TEST_LOG1).read_text().split('\n'):
            self._emitter.process_line(line)
        # Assert
        self.assertEqual(
            True, self._campaign_service.mission.is_correctly_completed)

    def test_bombing(self):
        """Учитываются наземные цели"""
        self._source_parser.parse_in_dogfight = _parse_mock
        for tvd_name in CONFIG.mgen.maps:
            self._graph_service.get_file = _get_xgml_file_mock
            self._campaign_service.initialize_map(tvd_name)
        # Act
        for line in Path(TEST_LOG2).read_text().split('\n'):
            self._emitter.process_line(line)
        # Assert
        self.assertGreater(len(self._ground_targets_service.ground_kills), 1)

    def test_end_round(self):
        """Перераспределяются самолёты по аэродромам в конце миссии"""
        shutil.copy('./data/scg/1/stalin-base.ldf', './tmp/data/scg/1/')
        shutil.copy('./data/scg/2/moscow_base.ldf', './tmp/data/scg/2/')
        self._source_parser.parse_in_dogfight = _parse_mock
        for tvd_name in CONFIG.mgen.maps:
            self._graph_service.get_file = _get_xgml_file_mock
            self._campaign_service.initialize_map(tvd_name)
        # Act
        for line in Path(TEST_LOG6).read_text().split('\n'):
            self._emitter.process_line(line)
        # Assert
        airfield = self._airfields_service.get_airfield_in_radius(
            TEST_TVD_NAME, 21649, 108703, 50)
        self.assertGreater(airfield.planes_count, 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)
