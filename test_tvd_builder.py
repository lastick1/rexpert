import unittest
import pathlib
import shutil

import processing
from tests import mocks, utils

CONFIG = mocks.ConfigMock(pathlib.Path(r'./testdata/conf.ini'))
MOSCOW_FIELDS = pathlib.Path(r'./data/moscow_fields.csv')

MOSCOW = 'moscow'
STALIN = 'stalingrad'
KUBAN = 'kuban'
TEST = 'test'

TVD_DATE = '10.11.1942'


class TestTvdBuilder(unittest.TestCase):
    """Тесты сборки ТВД"""
    def setUp(self):
        """Настройка перед тестами"""
        self.directory = pathlib.Path(r'./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        pathlib.Path('./tmp/red/').mkdir(parents=True)
        pathlib.Path('./tmp/blue/').mkdir(parents=True)

    def tearDown(self):
        """Очистка директории после теста"""
        utils.clean_directory(str(self.directory))

    def test_influences_moscow(self):
        """Генерируются зоны влияния филдов Москвы"""
        xgml = processing.Xgml(MOSCOW, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[MOSCOW]))
        CONFIG.mgen.icons_group_files[MOSCOW] = pathlib.Path('./tmp/FL_icon_moscow.Group').absolute()
        builder = processing.TvdBuilder(MOSCOW, CONFIG)
        builder.update_icons(builder.get_tvd(TVD_DATE))
        self.assertEqual(True, True)

    def test_influences_stalin(self):
        """Генерируются зоны влияния филдов Сталинграда"""
        xgml = processing.Xgml(STALIN, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[STALIN]))
        CONFIG.mgen.icons_group_files[STALIN] = pathlib.Path('./tmp/FL_icon_stalin.Group').absolute()
        builder = processing.TvdBuilder(STALIN, CONFIG)

        def call_update():
            """Обновить иконки"""
            builder.update_icons(builder.get_tvd(TVD_DATE))

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)

    def test_airfields(self):
        """Генерируются координатные группы аэродромов"""
        airfields = processing.AirfieldsController.initialize_managed_airfields(CONFIG.mgen.airfields_data[MOSCOW])
        builder = processing.TvdBuilder(MOSCOW, CONFIG)
        tvd = processing.Tvd(MOSCOW, 'test', TVD_DATE, {'x': 281600, 'z': 281600}, pathlib.Path(r'./tmp/'))
        tvd.red_front_airfields = list(x for x in airfields if x.name in ('kholm', 'kalinin', 'alferevo'))
        tvd.blue_front_airfields = list(x for x in airfields if x.name in ('losinki', 'lotoshino', 'migalovo'))
        tvd.red_rear_airfield = list(x for x in airfields if x.name == 'ruza')[0]
        tvd.blue_rear_airfield = list(x for x in airfields if x.name == 'karpovo')[0]

        def call_update():
            """Обновить аэродромы"""
            builder.update_airfields(tvd)

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)

    def test_update(self):
        """Генерируется папка ТВД"""
        pathlib.Path('./tmp/data/scg/1/').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/').mkdir(parents=True)
        shutil.copy('./data/scg/2/moscow-base_v2.ldf', './tmp/data/scg/2/')
        airfields = processing.AirfieldsController.initialize_managed_airfields(CONFIG.mgen.airfields_data[MOSCOW])
        builder = processing.TvdBuilder(MOSCOW, CONFIG)

        def call_update():
            """Обновить папку"""
            builder.update(builder.get_tvd(TVD_DATE), airfields)

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)


if __name__ == '__main__':
    unittest.main(verbosity=2)
