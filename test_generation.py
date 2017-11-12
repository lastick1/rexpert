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
            grid.node(18), grid.node(19), grid.node(1), grid.node(0), grid.node(21), grid.node(5), grid.node(24),
            grid.node(7), grid.node(6), grid.node(39), grid.node(8), grid.node(29), grid.node(12), grid.node(33),
            grid.node(15), grid.node(37), grid.node(14), grid.node(41), grid.node(13)
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
        grid = mocks.get_test_grid(MGEN)
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
        grid = mocks.get_test_grid(MGEN)
        expected = utils.get_nodes_keys([
            grid.node(5), grid.node(16), grid.node(29), grid.node(42), grid.node(26), grid.node(13), grid.node(27)
        ])
        # act
        result = utils.get_nodes_keys(grid.node(28).neighbors_sorted)
        # assert
        self.assertSequenceEqual(result, expected)


class TestTvd(unittest.TestCase):
    """Тесты ТВД"""

    def test_influences_moscow(self):
        """Генерируются зоны влияния филдов"""
        xgml = generation.Xgml(MOSCOW, MGEN)
        xgml.parse()
        MGEN.icons_group_files[MOSCOW] = pathlib.Path('./tmp/FL_icon_moscow.Group').absolute()
        tvd = generation.Tvd(MOSCOW, '10.11.1942', MGEN, MAIN, None, None)
        tvd.update_icons()

    def test_influences_stalin(self):
        """Генерируются зоны влияния филдов"""
        xgml = generation.Xgml(STALIN, MGEN)
        xgml.parse()
        MGEN.icons_group_files[STALIN] = pathlib.Path('./tmp/FL_icon_stalin.Group').absolute()
        tvd = generation.Tvd(STALIN, '10.11.1942', MGEN, MAIN, None, None)
        tvd.update_icons()

if __name__ == '__main__':
    unittest.main(verbosity=2)
