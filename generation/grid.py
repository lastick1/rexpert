"""Работа с графом"""
import pathlib
import configs
import geometry
from .node import Node


class Grid:
    """Граф (сетка)"""
    def __init__(self, name: str, nodes: dict, edges: list, config: configs.Mgen):
        self.nodes = nodes  # узлы сетки
        self.edges_ids = edges  # рёбра графа в виде пар (ключ_вершины, ключ_вершины)
        self.tvd = config.cfg[name]['tvd']
        self.scenario_min_distance = config.cfg['scenario_min_distance']

    @property
    def nodes_list(self) -> list:
        """Узлы списком"""
        return list(self.nodes[x] for x in self.nodes)

    @property
    def edges(self) -> list:
        """Все рёбра графа, в виде 2-элементных кортежей из соединяемых вершин"""
        edges = []
        used = set()
        for node in self.nodes:
            if self.nodes[node] in used:
                continue
            for neighbors in self.nodes[node].neighbors:
                if neighbors in used:
                    continue
                edges.append((self.nodes[node], neighbors))
            used.add(self.nodes[node])
        return edges

    @property
    def edges_raw(self) -> tuple:
        """Кортеж всех рёбер в виде 2-элементных кортежей координат точек вершин ребра"""
        edges = self.edges
        return tuple(((x[0].x, x[0].z), (x[1].x, x[1].z)) for x in edges)

    def save_file(self, path: pathlib.Path):
        """Записать граф в XGML файл"""

    @property
    def neutrals(self) -> list:
        """Узлы, где страна ==0"""
        return list(node for node in self.nodes_list if node.country == 0)

    @property
    def border_nodes(self) -> set:
        """Вершины линии фронта"""
        return set(node for node in self.neutrals if node.is_border)

    @property
    def border(self) -> list:
        """Линия фронта (упорядоченные с юга на север)"""
        def _is_reversed(a: Node, b: Node) -> bool:
            """Прямой или обратный порядок построения ЛФ"""
            # pylint: disable=C0103
            # 1. получаем цветные вершины треугольников со стороной - отрезком лф
            colored = set(a.neighbors) & set(b.neighbors)
            # 2. проверяем, какая из них слева от отрезка лф
            for c in colored:
                rotation = geometry.rotate(a, b, c)
                if rotation < 0 and c.country == 101:
                    return True
            return False

        nodes = list(self.border_nodes)
        first = nodes.pop()
        result = [first]
        while len(nodes):
            # пока список не опустеет, повторяем
            # вытаскиваем вершину с головы списка, добавляем её к концу или к началу результата
            # либо в конец списка
            node = nodes.pop(0)
            if node in result[-1].neighbors:
                result.append(node)
            elif node in result[0].neighbors:
                result.insert(0, node)
            else:
                nodes.append(node)

        # переворачиваем результат, если слева от линии оказались красные вершины
        if _is_reversed(result[0], result[1]):
            result.reverse()
        return result

    def node(self, key) -> Node:
        """Получить узел"""
        return self.nodes[str(key)]

    def find(self, x, z, side: float = 10) -> Node:  # pylint: disable=C0103
        """Найти узел по координатам (в квадрате стороной 2*r)"""
        for node in self.nodes_list:
            if abs(x - node.x) < side and abs(z - node.z) < side:
                return node

    def capture(self, x, z, country: int) -> None:  # pylint: disable=C0103
        """Захват вершины"""
        node = self.find(x, z)
        print('Capture {}[{}] {}'.format(node.text, node.key, country))
        if not node:
            raise NameError('Not found node to capture for [{}] country in [x:{} z:{}]'.format(
                country, x, z))
        node.capture(country)

    def capture_node(self, node: Node, country: int) -> None:
        """Захват узла"""
        self.capture(node.x, node.z, country)

    @staticmethod
    def get_neighbors_of(nodes: set) -> list:
        """Получить все узлы, соседствующие с хотя бы одним из списка"""
        result = set()
        for node in nodes:
            result |= node.neighbors - nodes
        return list(result)
