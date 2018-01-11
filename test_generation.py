"""Тестирование генерации миссий и работы графа"""
# pylint: disable=C1801
import unittest
import pathlib
import random

import utils
import processing
from tests import mocks, utils


CONFIG = mocks.ConfigMock(pathlib.Path(r'./testdata/conf.ini'))
MOSCOW_FIELDS = pathlib.Path(r'./data/moscow_fields.csv')

MOSCOW = 'moscow'
STALIN = 'stalingrad'
KUBAN = 'kuban'
TEST = 'test'

TVD_DATE = '10.11.1942'


class TestGrid(unittest.TestCase):
    """Тесты графа"""
    def setUp(self):
        """Настройка тестов"""
        self.directory = pathlib.Path(r'./tmp/').absolute()
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
        self.iterations = 25

    def tearDown(self):
        """Очистка после тестов"""
        utils.clean_directory(str(self.directory))

    def test_border_test(self):
        """Упорядочиваются вершины линии фронта в тестовом графе"""
        # Arrange
        xgml = processing.Xgml(TEST, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[TEST]))
        grid = processing.Grid(TEST, xgml.nodes, xgml.edges, CONFIG.mgen)
        # Act
        frontline = grid.border_nodes
        border = grid.border
        # Assert
        self.assertEqual(len(frontline), 9)
        self.assertEqual(len(border), 9)
        self.assertEqual(border[0].text, 'L1')

    def test_border_stalin(self):
        """Упорядочиваются вершины линии фронта в сталинградском графе"""
        # Arrange
        xgml = processing.Xgml(STALIN, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[STALIN]))
        grid = processing.Grid(STALIN, xgml.nodes, xgml.edges, CONFIG.mgen)
        expected = (
            209, 94, 93, 96, 101, 100, 99, 137, 139, 138, 157,
            186, 163, 164, 165, 184, 183, 182, 194, 193, 177
        )
        # Act
        border = grid.border
        # Assert
        self.assertCountEqual(tuple(int(x.key) for x in border), expected)
        self.assertSequenceEqual(tuple(int(x.key) for x in border), expected)

    def test_grid_capturing_test(self):
        """Выполняется захват в тестовом графе"""
        xgml = processing.Xgml(TEST, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[TEST]))
        grid = processing.Grid(TEST, xgml.nodes, xgml.edges, CONFIG.mgen)
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
        xgml = processing.Xgml(TEST, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[TEST]))
        grid = processing.Grid(TEST, xgml.nodes, xgml.edges, CONFIG.mgen)
        expected = utils.get_nodes_keys([
            grid.node(18), grid.node(19), grid.node(1), grid.node(0), grid.node(21), grid.node(5),
            grid.node(24), grid.node(7), grid.node(6), grid.node(39), grid.node(8), grid.node(29),
            grid.node(12), grid.node(33), grid.node(15), grid.node(37), grid.node(14),
            grid.node(41), grid.node(13)
        ])
        # act
        result = utils.get_nodes_keys(grid.get_neighbors_of(grid.border_nodes))
        # assert
        self.assertCountEqual(result, expected)

    def _test_grid_capturing_moscow(self):
        """Выполняется захват в графе Москвы"""
        xgml = processing.Xgml(MOSCOW, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[MOSCOW]))
        grid = processing.Grid(MOSCOW, xgml.nodes, xgml.edges, CONFIG.mgen)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(MOSCOW, 0))
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        self.fail()

    def _test_grid_capturing_stalingrad(self):
        """Выполняется захват в графе Сталинграда"""
        xgml = processing.Xgml(STALIN, CONFIG.mgen)
        xgml.parse(str(CONFIG.mgen.xgml[STALIN]))
        grid = processing.Grid(STALIN, xgml.nodes, xgml.edges, CONFIG.mgen)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(STALIN, 0))
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        self.fail()


class TestNode(unittest.TestCase):
    """Тесты вершин"""

    def test_node_triangles(self):
        """Определяются смежные треугольники для вершины"""
        grid = mocks.get_test_grid(CONFIG.mgen)
        expected = utils.get_polygons_keys([
            (grid.node(30), grid.node(6), grid.node(31)),
            (grid.node(30), grid.node(31), grid.node(44)),
            (grid.node(30), grid.node(44), grid.node(43)),
            (grid.node(30), grid.node(43), grid.node(29)),
            (grid.node(30), grid.node(29), grid.node(6))
        ])
        # act
        result = utils.get_polygons_keys(grid.node(30).triangles)
        # assert
        self.assertCountEqual(result, expected)

    def test_neighbors_sorted(self):
        """Сортируются соседи по часовой стрелке"""
        grid = mocks.get_test_grid(CONFIG.mgen)
        expected = utils.get_nodes_keys([
            grid.node(5), grid.node(16), grid.node(29), grid.node(42),
            grid.node(26), grid.node(13), grid.node(27)
        ])
        # act
        result = utils.get_nodes_keys(grid.node(28).neighbors_sorted)
        # assert
        self.assertSequenceEqual(result, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
