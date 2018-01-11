"""Тестирование управления графом"""
import unittest
import pathlib
import processing
import tests

TEST_CONFIG = tests.mocks.ConfigMock(pathlib.Path('./testdata/conf.ini'))
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
        controller = processing.GridController(TEST_CONFIG)
        # Act
        controller.initialize(TEST_TVD_NAME)
        # Assert
        self.assertTrue(pathlib.Path('./tmp/current/{}/{}_0.xgml'.format(TEST_TVD_NAME, TEST_TVD_NAME)).exists())

    def test_capture(self):
        """Выполняется сохранение обновлённой версии графа после захвата"""
        pos = {'x': 144485, 'z': 136915}
        controller = processing.GridController(TEST_CONFIG)
        controller.initialize(TEST_TVD_NAME)
        # Act
        controller.capture(TEST_TVD_NAME, pos, 101)
        # Assert
        self.assertTrue(pathlib.Path('./tmp/current/{}/{}_0.xgml'.format(TEST_TVD_NAME, TEST_TVD_NAME)).exists())
        self.assertTrue(pathlib.Path('./tmp/current/{}/{}_1.xgml'.format(TEST_TVD_NAME, TEST_TVD_NAME)).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
