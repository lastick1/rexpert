"""Тестирование управления графом"""
import pathlib
import unittest

import processing
import tests

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))
IOC.config.main = tests.mocks.MainMock(pathlib.Path('./testdata/conf.ini'))
IOC.config.mgen = tests.mocks.MgenMock(IOC.config.main.game_folder)
TEST_TVD_NAME = 'moscow'


class TestGridControl(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        """Настройка перед тестом"""
        self.directory = pathlib.Path('./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        pathlib.Path('./tmp/current/').absolute().mkdir(parents=True)

    def tearDown(self):
        """Очистка после тестов"""
        tests.utils.clean_directory(str(self.directory))

    def test_initialize(self):
        """Выполняется инициализация графа кампании"""
        controller = processing.GridController(IOC.config)
        # Act
        controller.initialize(TEST_TVD_NAME)
        # Assert
        self.assertTrue(pathlib.Path('./tmp/current/{}/{}_0.xgml'.format(TEST_TVD_NAME, TEST_TVD_NAME)).exists())

    def test_reset(self):
        """Выполняется сброс графа кампании"""
        controller = processing.GridController(IOC.config)
        controller.initialize(TEST_TVD_NAME)
        # Act
        controller.reset(TEST_TVD_NAME)
        # Assert
        xgml_files = list(pathlib.Path('./tmp/current/{}/'.format(TEST_TVD_NAME)).glob('*.xgml'))
        self.assertEqual(len(xgml_files), 0)

    def test_capture(self):
        """Выполняется сохранение обновлённой версии графа после захвата"""
        pos = {'x': 144485, 'z': 136915}
        controller = processing.GridController(IOC.config)
        controller.initialize(TEST_TVD_NAME)
        # Act
        controller.capture(TEST_TVD_NAME, pos, 101)
        # Assert
        self.assertTrue(pathlib.Path('./tmp/current/{}/{}_0.xgml'.format(TEST_TVD_NAME, TEST_TVD_NAME)).exists())
        self.assertTrue(pathlib.Path('./tmp/current/{}/{}_1.xgml'.format(TEST_TVD_NAME, TEST_TVD_NAME)).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
