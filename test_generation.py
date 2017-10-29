"""Тестирование генерации миссий и работы графа"""
import unittest
import pathlib
import generation
from tests.mocks import MainMock, MgenMock

MAIN = MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = MgenMock(MAIN)

MOSCOW = 'moscow'
STALIN = 'stalingrad'
KUBAN = 'kuban'
TEST = 'test'


class TestGrid(unittest.TestCase):
    """Тесты графа"""
    def setUp(self):
        """Настройка тестов"""
        self.iterations = 25

    def test_neutrals_property(self):
        """Проверка выбора вершин линии фронта"""
        # Arrange
        grid = generation.Grid(TEST, MGEN.xgml[TEST], MGEN)
        # Act
        neutrals = grid.neutrals
        # Assert
        self.fail()

    def test_grid_capturing_moscow(self):
        """Проверка захвата в графе Москвы"""
        grid = generation.Grid(MOSCOW, MGEN.xgml[MOSCOW], MGEN)
        # Act
        self.fail()

    def test_grid_capturing_stalingrad(self):
        """Проверка захвата в графе Сталинграда"""
        grid = generation.Grid(STALIN, MGEN.xgml[STALIN], MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(STALIN, 0))
        grid.save_file(path)
        # Act
        self.fail()

    def test_grid_capturing_kuban(self):
        """Проверка захвата в графе Кубани"""
        grid = generation.Grid(STALIN, MGEN.xgml[KUBAN], MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(KUBAN, 0))
        grid.save_file(path)
        # Act
        self.fail()


class TestTvd(unittest.TestCase):
    """Тесты ТВД"""
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
