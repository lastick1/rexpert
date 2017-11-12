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
    def get_confrontation_nodes(grid: Grid, country: int) -> set:
        """Получить все узлы, входящие в прифронтовую полосу, кроме узлов линии фронта"""
        border_nodes = grid.border_nodes
        return set(
            {x for x in grid.get_neighbors_of(border_nodes) if x.country == country or x.related_country == country}
        )

    def confrontation_west(self, grid: Grid) -> list:
        """Построить вершины для западной прифронтовой зоны"""
        confrontation_nodes = self.get_confrontation_nodes(grid, 201)
        border = grid.border
        start = _to_node(border[0])
        end = _to_node(border[-1])
        result = []

        while start not in end.neighbors:
            nodes = list(end.neighbors & confrontation_nodes)
            if len(nodes):
                nodes.sort(key=lambda x: len(x.not_border_neighbors - confrontation_nodes))
                end = nodes.pop()
                result.append(end)
                confrontation_nodes.remove(end)
            else:
                break

        result = border + result
        result.reverse()
        return result

    def confrontation_east(self, grid: Grid) -> list:
        """Построить вершины для западной прифронтовой зоны"""
        confrontation_nodes = self.get_confrontation_nodes(grid, 101)
        border = grid.border
        start = _to_node(border[-1])
        end = _to_node(border[0])
        result = []

        while start not in end.neighbors:
            nodes = list(end.neighbors & confrontation_nodes)
            if len(nodes):
                nodes.sort(key=lambda x: len(x.not_border_neighbors - confrontation_nodes))
                end = nodes.pop()
                result.append(end)
                confrontation_nodes.remove(end)
            else:
                break

        result.reverse()
        result = result + border
        return result
