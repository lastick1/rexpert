"""Тестирование управления графом"""
from __future__ import annotations
import pathlib
import unittest

from core import EventsEmitter
from services import GraphService
from tests.mocks import ConfigMock
from tests.utils import clean_directory

CONFIG = ConfigMock()
TEST_TVD_NAME = 'moscow'


class TestGridControl(unittest.TestCase):
    """Тестовый класс"""

    def setUp(self):
        """Настройка перед тестом"""
        self.emitter: EventsEmitter = EventsEmitter()
        self.directory = pathlib.Path('./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        pathlib.Path('./tmp/current/').absolute().mkdir(parents=True)

    def tearDown(self):
        """Очистка после тестов"""
        clean_directory(str(self.directory))

    def test_initialize(self):
        """Выполняется инициализация графа кампании"""
        service = GraphService(self.emitter, CONFIG)
        service.init()
        # Act
        service.initialize(TEST_TVD_NAME)
        # Assert
        self.assertTrue(pathlib.Path(
            './tmp/current/{0}/{0}_0.xgml'.format(TEST_TVD_NAME)).exists())

    def test_reset(self):
        """Выполняется сброс графа кампании"""
        service = GraphService(self.emitter, CONFIG)
        service.init()
        service.initialize(TEST_TVD_NAME)
        # Act
        service.reset(TEST_TVD_NAME)
        # Assert
        xgml_files = list(pathlib.Path(
            './tmp/current/{}/'.format(TEST_TVD_NAME)).glob('*.xgml'))
        self.assertEqual(len(xgml_files), 0)

    def test_capture(self):
        """Выполняется сохранение обновлённой версии графа после захвата"""
        pos = {'x': 144485, 'z': 136915}
        service = GraphService(self.emitter, CONFIG)
        service.init()
        service.initialize(TEST_TVD_NAME)
        # Act
        service.capture(TEST_TVD_NAME, pos, 101)
        # Assert
        self.assertTrue(pathlib.Path(
            './tmp/current/{0}/{0}_0.xgml'.format(TEST_TVD_NAME)).exists())
        self.assertTrue(pathlib.Path(
            './tmp/current/{0}/{0}_1.xgml'.format(TEST_TVD_NAME)).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
