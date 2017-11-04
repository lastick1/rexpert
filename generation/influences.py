"""Формирование списков вершин для InfluenceArea"""
import geometry


class BoundaryBuilder:
    def __init__(self, north: float, east: float, south: float, west: float):
        self.north, self.east, self.south, self.west = north, east, south, west

    def build_east(self, border: list) -> list:
        """Построить вершины для восточной InfluenceArea"""
        start = border[0]
        end = border[-1]
        result = [geometry.Point(node.x, node.z) for node in border] + [
            geometry.Point(x=self.north, z=end.z),
            geometry.Point(x=self.north, z=self.east),
            geometry.Point(x=self.south, z=self.east),
            geometry.Point(x=self.south, z=start.z)
        ]
        return result

    def build_west(self, border: list) -> list:
        """Построить вершины для западной InfluenceArea"""
        start = border[0]
        end = border[-1]
        result = [geometry.Point(node.x, node.z) for node in border] + [
            geometry.Point(x=self.north, z=end.z),
            geometry.Point(x=self.north, z=self.west),
            geometry.Point(x=self.south, z=self.west),
            geometry.Point(x=self.south, z=start.z)
        ]
        result.reverse()
        return result
