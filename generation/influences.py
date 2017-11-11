"""Формирование списков вершин для InfluenceArea"""
import geometry

from .grid import Grid, Node


def _to_node(obj) -> Node:
    """Приведение типа к узлу"""
    return obj


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

    @staticmethod
    def get_second_line_nodes(grid: Grid, country: int) -> set:
        """Получить все узлы, ограничивающие прифронтовую полосу"""
        # TODO решить проблему... может быть более одного ребра от вершины из ограничения до линии фронта
        result = set()
        border_nodes = grid.border_nodes
        nodes = tuple(x for x in grid.get_neighbors_of(border_nodes)
                      if x.country == country or x.related_country == country)
        for node in nodes:
            if len(node.neighbors & border_nodes) != 2:
                result.add(node)
        return result

    def confrontation_west(self, grid: Grid) -> list:
        """Построить вершины для западной прифронтовой зоны"""
        second_line_nodes = self.get_second_line_nodes(grid)
        result = []

        cursor = _to_node(grid.border[0])
        while len(second_line_nodes):
            nodes = cursor.neighbors & second_line_nodes
            neutrals = list(x for x in nodes if x.country == 0)
            airfields = list(x for x in nodes if x.country != 0)
            if len(neutrals) == 1:
                cursor = neutrals[0]
                result.append(cursor)
                second_line_nodes.remove(cursor)
            elif len(airfields) >= 1:
                cursor = airfields[0]
                result.append(cursor)
                second_line_nodes.remove(cursor)

        return result

    def confrontation_east(self, nodes):
        """Построить вершины для западной прифронтовой зоны"""
