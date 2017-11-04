"""Тестирование генерации миссий и работы графа"""
import unittest
import pathlib
import random
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

    def test_neutral_line_property(self):
        """Проверка выбора вершин линии фронта"""
        # Arrange
        xgml = generation.Xgml(TEST, MGEN)
        xgml.parse()
        grid = generation.Grid(TEST, xgml.nodes, xgml.edges, MGEN)
        # Act
        frontline = grid.border_nodes
        border = grid.border
        # Assert
        self.assertEqual(len(frontline), 9)
        self.assertEqual(len(border), 9)
        self.assertEqual(border[0].text, 'L1')

    def test_grid_capturing_test(self):
        """Проверка захвата в тестовом графе"""
        xgml = generation.Xgml(TEST, MGEN)
        xgml.parse()
        grid = generation.Grid(TEST, xgml.nodes, xgml.edges, MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(TEST, 0))
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        for i in range(1, self.iterations):
            nodes = list(grid.border_nodes)
            if len(nodes) == 0:
                break
            random.shuffle(nodes)
            for node in nodes.pop().neighbors:
                if node.country == 201:
                    node.capture(101)
                    break
            path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(TEST, i))
            xgml.save_file(str(path), grid.nodes, grid.edges)

    def test_grid_capturing_moscow(self):
        """Проверка захвата в графе Москвы"""
        grid = generation.Grid(MOSCOW, MGEN.xgml[MOSCOW], MGEN)
        # Act
        self.fail()

    def test_grid_capturing_stalingrad(self):
        """Проверка захвата в графе Сталинграда"""
        xgml = generation.Xgml(STALIN, MGEN)
        xgml.parse()
        grid = generation.Grid(STALIN, xgml.nodes, xgml.edges, MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(STALIN, 0))
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        self.fail()


class TestTvd(unittest.TestCase):
    """Тесты ТВД"""
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
