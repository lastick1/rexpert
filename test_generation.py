"""Тестирование генерации миссий и работы графа"""
import unittest
import pathlib
import random
import generation
from tests import mocks, utils

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)

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
        """Упорядочиваются вершины линии фронта"""
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
        """Выполняется захват в тестовом графе"""
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

    def test_get_neighbors_of(self):
        """Находятся все соседи узлов из списка"""
        xgml = generation.Xgml(TEST, MGEN)
        xgml.parse()
        grid = generation.Grid(TEST, xgml.nodes, xgml.edges, MGEN)
        expected = utils.get_nodes_keys([
            grid.nodes['18'], grid.nodes['19'], grid.nodes['1'], grid.nodes['0'], grid.nodes['21'], grid.nodes['5'],
            grid.nodes['24'], grid.nodes['7'], grid.nodes['6'], grid.nodes['39'], grid.nodes['8'], grid.nodes['29'],
            grid.nodes['12'], grid.nodes['33'], grid.nodes['15'], grid.nodes['37'], grid.nodes['14'], grid.nodes['41'],
            grid.nodes['13']
        ])
        # act
        result = utils.get_nodes_keys(grid.get_neighbors_of(grid.border_nodes))
        # assert
        self.assertCountEqual(result, expected)

    def _test_grid_capturing_moscow(self):
        """Выполняется захват в графе Москвы"""
        xgml = generation.Xgml(MOSCOW, MGEN)
        xgml.parse()
        grid = generation.Grid(MOSCOW, xgml.nodes, xgml.edges, MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(MOSCOW, 0))
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        self.fail()

    def _test_grid_capturing_stalingrad(self):
        """Выполняется захват в графе Сталинграда"""
        xgml = generation.Xgml(STALIN, MGEN)
        xgml.parse()
        grid = generation.Grid(STALIN, xgml.nodes, xgml.edges, MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(STALIN, 0))
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        self.fail()


class TestNode(unittest.TestCase):
    """Тесты вершин"""

    def test_node_triangles(self):
        """Определяются смежные треугольники для вершины"""
        xgml = generation.Xgml(TEST, MGEN)
        xgml.parse()
        grid = mocks.get_test_grid(MGEN)
        nodes = grid.nodes
        expected = utils.get_polygons_keys([
            (nodes['30'], nodes['6'], nodes['31']),
            (nodes['30'], nodes['31'], nodes['44']),
            (nodes['30'], nodes['44'], nodes['43']),
            (nodes['30'], nodes['43'], nodes['29']),
            (nodes['30'], nodes['29'], nodes['6'])
        ])
        # act
        result = utils.get_polygons_keys(grid.node('30').triangles)
        # assert
        self.assertCountEqual(result, expected)

    def test_neighbors_sorted(self):
        """Сортируются соседи по часовой стрелке"""

        # act
        # assert
        self.fail()


class TestTvd(unittest.TestCase):
    """Тесты ТВД"""


if __name__ == '__main__':
    unittest.main(verbosity=2)
