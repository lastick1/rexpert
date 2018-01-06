"""Тестирование построения многоугольников зон влияния"""
import unittest
import pathlib
import geometry
import processing

from tests import mocks, utils

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = mocks.MgenMock(MAIN)

STALIN = 'stalingrad'


class TestBoundaryBuilder(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        self.north, self.east, self.south, self.west = 10, 10, 0, 0

    def test_build_east(self):
        """Создаётся корректный многоугольник восточной InfluenceArea"""
        builder = processing.BoundaryBuilder(self.north, self.east, self.south, self.west)
        points = [
            geometry.Point(x=1, z=6),
            geometry.Point(x=4, z=3),
            geometry.Point(x=5, z=6),
            geometry.Point(x=7, z=4),
            geometry.Point(x=9, z=6)
        ]
        nodes = utils.get_nodes(points)
        expected = points + [
            geometry.Point(x=self.north, z=6),
            geometry.Point(x=self.north, z=self.east),
            geometry.Point(x=self.south, z=self.east),
            geometry.Point(x=self.south, z=6)
        ]
        # Act
        result = builder.influence_east(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_build_west(self):
        """Создаётся корректный многоугольник западной InfluenceArea"""
        builder = processing.BoundaryBuilder(self.north, self.east, self.south, self.west)
        points = [
            geometry.Point(x=1, z=6),
            geometry.Point(x=4, z=3),
            geometry.Point(x=5, z=6),
            geometry.Point(x=7, z=4),
            geometry.Point(x=9, z=6)
        ]
        nodes = utils.get_nodes(points)
        points.reverse()
        expected = [
            geometry.Point(x=self.south, z=6),
            geometry.Point(x=self.south, z=self.west),
            geometry.Point(x=self.north, z=self.west),
            geometry.Point(x=self.north, z=6)
        ] + points
        # Act
        result = builder.influence_west(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_build_west_complex(self):
        """Создаётся корректный многоугольник для 'сложной' линии фронта"""
        builder = processing.BoundaryBuilder(self.north, self.east, self.south, self.west)
        points = [
            geometry.Point(x=1, z=1),
            geometry.Point(x=1, z=9),
            geometry.Point(x=9, z=9),
            geometry.Point(x=7, z=4),
            geometry.Point(x=5, z=4),
            geometry.Point(x=4, z=1),
            geometry.Point(x=8, z=3),
            geometry.Point(x=8, z=1),
        ]
        nodes = utils.get_nodes(points)
        points.reverse()
        expected = [
            geometry.Point(x=self.south, z=1),
            geometry.Point(x=self.south, z=self.west),
            geometry.Point(x=self.north, z=self.west),
            geometry.Point(x=self.north, z=1)
        ] + points

        # Act
        result = builder.influence_west(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_get_confrontation_nodes(self):
        """Определяются вершины, входящие в прифронтовую полосу"""
        expected_keys = {
            101: ('24', '11', '40', '45', '47', '46', '36', '35', '33', '34', '19', '7'),
            201: ('2', '12', '26', '42', '29', '16', '30', '17', '5')
        }
        countries = (101, 201)
        builder = processing.BoundaryBuilder(self.north, self.east, self.south, self.west)
        grid = mocks.get_test_grid(MGEN)
        for country in countries:
            # Act
            result = utils.get_nodes_keys(list(builder.get_confrontation_nodes(grid, country)))
            # Assert
            self.assertCountEqual(expected_keys[country], result, msg=country)

    def test_confrontation_area_west(self):
        """Создаётся многоугольник западной прифронтовой полосы"""
        expected_keys = (2, 26, 42, 29, 16, 5, 6, 18, 32, 31, 44, 43, 41, 25, 1)
        builder = processing.BoundaryBuilder(self.north, self.east, self.south, self.west)
        grid = mocks.get_test_grid(MGEN)
        # Act
        result = builder.confrontation_west(grid)
        # Assert
        self.assertSequenceEqual(tuple(int(x.key) for x in result), expected_keys)

    def test_confrontation_area_east(self):
        """Создаётся многоугольник восточной прифронтовой полосы"""
        expected_keys = (7, 34, 35, 36, 46, 45, 40, 11, 1, 25, 41, 43, 44, 31, 32, 18, 6)
        builder = processing.BoundaryBuilder(self.north, self.east, self.south, self.west)
        grid = mocks.get_test_grid(MGEN)
        # Act
        result = builder.confrontation_east(grid)
        # Assert
        self.assertSequenceEqual(tuple(int(x.key) for x in result), expected_keys)

    def test_confrontation_area_stalingrad_east(self):
        """Создаётся многоугольник восточной прифронтовой полосы"""
        xgml = processing.Xgml(STALIN, MGEN)
        xgml.parse()
        expected_keys = (
            192, 57, 196, 197, 185, 188, 187, 48, 110, 25, 102, 19, 95, 3, 191, 209, 94, 93, 96,
            101, 100, 99, 137, 139, 138, 157, 186, 163, 164, 165, 184, 183, 182, 194, 193, 177
        )
        builder = processing.BoundaryBuilder(self.north, self.east, self.south, self.west)
        grid = processing.Grid(STALIN, xgml.nodes, xgml.edges, MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(STALIN, 0))
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        result = builder.confrontation_east(grid)
        # Assert
        self.assertSequenceEqual(tuple(int(x.key) for x in result), expected_keys)

    def _test_confrontation_area_complex(self):
        """Создаётся многоугольник западной прифронтовой полосы с длинным выступом"""
        self.fail()


if __name__ == '__main__':
    unittest.main(verbosity=2)
