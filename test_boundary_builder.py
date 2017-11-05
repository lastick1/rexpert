"""Тестирование построения многоугольников зон влияния"""
import unittest
import generation
import geometry


class TestBoundaryBuilder(unittest.TestCase):
    """Тестовый класс"""

    @staticmethod
    def _get_nodes(points: list) -> list:
        """Получить узлы из точек (нейтральные)"""
        nodes = []
        key = 0
        for point in points:
            nodes.append(generation.Node(key=key, text=key, pos=point.to_dict(), color='#FFFFFF'))
            key += 1
        return nodes

    def test_build_east(self):
        """Создаётся корректный многоугольник восточной InfluenceArea"""
        north, east, south, west = 10, 10, 0, 0
        builder = generation.BoundaryBuilder(north, east, south, west)
        points = [
            geometry.Point(x=1, z=6),
            geometry.Point(x=4, z=3),
            geometry.Point(x=5, z=6),
            geometry.Point(x=7, z=4),
            geometry.Point(x=9, z=6)
        ]
        nodes = self._get_nodes(points)
        expected = points + [
            geometry.Point(x=north, z=6),
            geometry.Point(x=north, z=east),
            geometry.Point(x=south, z=east),
            geometry.Point(x=south, z=6)
        ]
        # Act
        result = builder.build_east(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_build_west(self):
        """Создаётся корректный многоугольник западной InfluenceArea"""
        north, east, south, west = 10, 10, 0, 0
        builder = generation.BoundaryBuilder(north, east, south, west)
        points = [
            geometry.Point(x=1, z=6),
            geometry.Point(x=4, z=3),
            geometry.Point(x=5, z=6),
            geometry.Point(x=7, z=4),
            geometry.Point(x=9, z=6)
        ]
        nodes = self._get_nodes(points)
        points.reverse()
        expected = [
            geometry.Point(x=south, z=6),
            geometry.Point(x=south, z=west),
            geometry.Point(x=north, z=west),
            geometry.Point(x=north, z=6)
        ] + points
        # Act
        result = builder.build_west(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_build_west_complex(self):
        """Создаётся корректный многоугольник для 'сложной' линии фронта"""
        north, east, south, west = 10, 10, 0, 0
        builder = generation.BoundaryBuilder(north, east, south, west)
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
        nodes = self._get_nodes(points)
        points.reverse()
        expected = [
            geometry.Point(x=south, z=1),
            geometry.Point(x=south, z=west),
            geometry.Point(x=north, z=west),
            geometry.Point(x=north, z=1)
        ] + points

        # Act
        result = builder.build_west(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
