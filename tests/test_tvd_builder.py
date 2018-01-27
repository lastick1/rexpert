"""Тестирование обновления папки ТВД"""
import unittest
import pathlib
import shutil

import processing
import tests

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
MOSCOW_FIELDS = pathlib.Path('./data/moscow_fields.csv')

MOSCOW = 'moscow'
STALIN = 'stalingrad'
KUBAN = 'kuban'
TEST = 'test'

TVD_DATE = '10.11.1942'


def _get_xgml_file_mock(tvd_name: str) -> str:
    """Подделка метода получения файла графа"""
    return str(IOC.config.mgen.xgml[tvd_name])


class TestTvdBuilder(unittest.TestCase):
    """Тесты сборки ТВД"""
    def setUp(self):
        """Настройка перед тестами"""
        self.directory = pathlib.Path('./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/airfields_red').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/1/blocks_quickmission/airfields_blue').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/airfields_red').mkdir(parents=True)
        pathlib.Path('./tmp/data/scg/2/blocks_quickmission/airfields_blue').mkdir(parents=True)

    def tearDown(self):
        """Очистка директории после теста"""
        tests.utils.clean_directory(str(self.directory))

    def test_influences_moscow(self):
        """Генерируются зоны влияния филдов Москвы"""
        IOC.config.mgen.icons_group_files[MOSCOW] = pathlib.Path('./tmp/FL_icon_moscow.Group').absolute()
        IOC.grid_controller.get_file = _get_xgml_file_mock
        builder = processing.TvdBuilder(MOSCOW, IOC)

        def call_update():
            """Обновить иконки"""
            builder.update_icons(builder.get_tvd(TVD_DATE))

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)

    def test_influences_stalin(self):
        """Генерируются зоны влияния филдов Сталинграда"""
        IOC.config.mgen.icons_group_files[STALIN] = pathlib.Path('./tmp/FL_icon_stalin.Group').absolute()
        IOC.grid_controller.get_file = _get_xgml_file_mock
        builder = processing.TvdBuilder(STALIN, IOC)

        def call_update():
            """Обновить иконки"""
            builder.update_icons(builder.get_tvd(TVD_DATE))

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)

    def test_airfields(self):
        """Генерируются координатные группы аэродромов"""
        airfields = processing.AirfieldsController.initialize_managed_airfields(IOC.config.mgen.airfields_data[MOSCOW])
        builder = processing.TvdBuilder(MOSCOW, IOC)
        grid = IOC.grid_controller.get_grid(MOSCOW)
        tvd = processing.Tvd(MOSCOW, 'test', TVD_DATE, {'x': 281600, 'z': 281600}, dict(), grid, pathlib.Path('./tmp/'))
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
        shutil.copy('./data/scg/2/moscow-base_v2.ldf', './tmp/data/scg/2/')
        airfields = processing.AirfieldsController.initialize_managed_airfields(IOC.config.mgen.airfields_data[MOSCOW])
        IOC.grid_controller.get_file = _get_xgml_file_mock
        builder = processing.TvdBuilder(MOSCOW, IOC)

        def call_update():
            """Обновить папку"""
            builder.update(builder.get_tvd(TVD_DATE), airfields)

        try:
            call_update()
        except Exception as exception:  # pylint: disable=W0703
            self.fail(exception)


if __name__ == '__main__':
    unittest.main(verbosity=2)
