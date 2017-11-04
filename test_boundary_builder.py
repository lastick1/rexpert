"""Тестирование построения многоугольников зон влияния"""
import unittest
import generation
import geometry


class TestGrid(unittest.TestCase):
    """Тестовый класс"""

    def test_boundary_builder_build_east(self):
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
        nodes = []
        key = 0
        for point in points:
            nodes.append(generation.Node(key=key, text=key, pos=point.to_dict(), color='#FFFFFF'))
            key += 1
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

    def test_boundary_builder_build_west(self):
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
        nodes = []
        key = 0
        for point in points:
            nodes.append(generation.Node(key=key, text=key, pos=point.to_dict(), color='#FFFFFF'))
            key += 1
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
