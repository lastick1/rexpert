"""Формирование списков вершин для InfluenceArea"""
import geometry

from .grid import Grid

class BoundaryBuilder:
    def __init__(self, north: float, east: float, south: float, west: float):
        self._north, self._east, self._south, self._west = north, east, south, west

    def influence_east(self, border: list) -> list:
        """Построить вершины для восточной InfluenceArea"""
        start = border[0]
        end = border[-1]
        result = [geometry.Point(node.x, node.z) for node in border] + [
            geometry.Point(x=self._north, z=end.z),
            geometry.Point(x=self._north, z=self._east),
            geometry.Point(x=self._south, z=self._east),
            geometry.Point(x=self._south, z=start.z)
        ]
        return result

    def influence_west(self, border: list) -> list:
        """Построить вершины для западной InfluenceArea"""
        start = border[0]
        end = border[-1]
        result = [geometry.Point(node.x, node.z) for node in border] + [
            geometry.Point(x=self._north, z=end.z),
            geometry.Point(x=self._north, z=self._west),
            geometry.Point(x=self._south, z=self._west),
            geometry.Point(x=self._south, z=start.z)
        ]
        result.reverse()
        return result

    def confrontation_west(self, grid: Grid) -> list:
        """Построить вершины для западной прифронтовой зоны"""
        border = grid.border
        nodes = grid.nodes_list

        return []

    def confrontation_east(self, nodes):
        """Построить вершины для западной прифронтовой зоны"""
