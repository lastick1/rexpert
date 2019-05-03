"""Тестирование обновления папки ТВД"""
import logging
from pathlib import Path
import shutil
import unittest

from core import EventsEmitter
from model import Tvd
from storage import Storage
from services import AirfieldsService, \
    GraphService, \
    WarehouseService, \
    TvdService
from tests.utils import clean_directory
from tests.mocks import ConfigMock

CONFIG = ConfigMock()

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

MOSCOW_FIELDS = Path('./data/moscow_fields.csv')

MOSCOW = 'moscow'
STALIN = 'stalingrad'
KUBAN = 'kuban'
TEST = 'test'

TVD_DATE = '10.11.1942'


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(CONFIG.mgen.xgml[tvd_name])


class TestTvdService(unittest.TestCase):
    """Тесты сборки ТВД"""

    def setUp(self):
        """Настройка перед тестами"""
        self._storage: Storage = Storage(CONFIG)
        self._graph_service: GraphService = GraphService(CONFIG)
        self._emitter: EventsEmitter = EventsEmitter()
        self._warehouses_service: WarehouseService = WarehouseService(
            self._emitter, CONFIG, self._storage)
        self.directory = Path('./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        Path('./tmp/data/scg/1/blocks_quickmission/airfields_red').mkdir(parents=True)
        Path('./tmp/data/scg/1/blocks_quickmission/airfields_blue').mkdir(parents=True)
        Path('./tmp/data/scg/2/blocks_quickmission/airfields_red').mkdir(parents=True)
        Path('./tmp/data/scg/2/blocks_quickmission/airfields_blue').mkdir(parents=True)

    def tearDown(self):
        """Очистка директории после теста"""
        clean_directory(str(self.directory))

    def test_influences_moscow(self):
        """Генерируются зоны влияния филдов Москвы"""
        CONFIG.mgen.icons_group_files[MOSCOW] = Path(
            './tmp/FL_icon_moscow.Group').absolute()
        self._graph_service.get_file = _get_xgml_file_mock
        builder = TvdService(
            MOSCOW,
            CONFIG,
            self._storage,
            self._graph_service,
            self._warehouses_service
        )

        def call_update():
            """Обновить иконки"""
            builder.update_icons(builder.get_tvd(TVD_DATE))

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)

    def test_influences_stalin(self):
        """Генерируются зоны влияния филдов Сталинграда"""
        CONFIG.mgen.icons_group_files[STALIN] = Path(
            './tmp/FL_icon_stalin.Group').absolute()
        self._graph_service.get_file = _get_xgml_file_mock
        builder = TvdService(
            STALIN,
            CONFIG,
            self._storage,
            self._graph_service,
            self._warehouses_service
        )

        def call_update():
            """Обновить иконки"""
            builder.update_icons(builder.get_tvd(TVD_DATE))

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)

    def test_airfields(self):
        """Генерируются координатные группы аэродромов"""
        airfields = AirfieldsService.initialize_managed_airfields(
            CONFIG.mgen.airfields_data[MOSCOW])
        builder = TvdService(
            MOSCOW,
            CONFIG,
            self._storage,
            self._graph_service,
            self._warehouses_service
        )
        grid = self._graph_service.get_grid(MOSCOW)
        tvd = Tvd(MOSCOW, 'test', TVD_DATE, {
                  'x': 281600, 'z': 281600}, dict(), grid, Path('./tmp/'))
        tvd.red_front_airfields = list(
            x for x in airfields if x.name in ('kholm', 'kalinin', 'alferevo'))
        tvd.blue_front_airfields = list(
            x for x in airfields if x.name in ('losinki', 'lotoshino', 'migalovo'))
        tvd.red_rear_airfield = list(
            x for x in airfields if x.name == 'ruza')[0]
        tvd.blue_rear_airfield = list(
            x for x in airfields if x.name == 'karpovo')[0]

        def call_update():
            """Обновить аэродромы"""
            builder.update_airfield_groups(tvd)

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)

    def test_update(self):
        """Генерируется папка ТВД"""
        shutil.copy('./data/scg/2/moscow_base.ldf', './tmp/data/scg/2/')
        airfields = AirfieldsService.initialize_managed_airfields(
            CONFIG.mgen.airfields_data[MOSCOW])
        self._graph_service.get_file = _get_xgml_file_mock
        builder = TvdService(
            MOSCOW,
            CONFIG,
            self._storage,
            self._graph_service,
            self._warehouses_service
        )

        def call_update():
            """Обновить папку"""
            builder.update(builder.get_tvd(TVD_DATE), airfields)

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)


if __name__ == '__main__':
    unittest.main(verbosity=2)
