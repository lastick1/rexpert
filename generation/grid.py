"""Работа с графом"""
import codecs
import xml.etree.ElementTree as Et
import pathlib
from .node import Node
import configs


class Grid:
    """Граф (сетка)"""
    def __init__(self, name: str, xgml: pathlib.Path, config: configs.Mgen):
        self.nodes = dict()  # узлы сетки
        self.tvd = config.cfg[name]['tvd']
        self.scenario_min_distance = config.cfg['scenario_min_distance']
        self.graph_zoom_x = config.cfg[name]['graph_zoom_point']['y']
        self.graph_zoom_z = config.cfg[name]['graph_zoom_point']['x']
        self.x_coefficient_serialization = self.graph_zoom_x / config.cfg[name]['right_top']['x']
        self.z_coefficient_serialization = self.graph_zoom_z / config.cfg[name]['right_top']['z']
        self.x_coefficient_deserialization = config.cfg[name]['right_top']['x'] / self.graph_zoom_x
        self.z_coefficient_deserialization = config.cfg[name]['right_top']['z'] / self.graph_zoom_z
        self.read_file(xgml)

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

    def serialize_edges_xgml(self) -> str:
        """Сериализация рёбер"""
        string = ""
        for edge in self.edges:
            string += """
\t\t<section name="edge">
\t\t\t<attribute key="source" type="int">{0}</attribute>
\t\t\t<attribute key="target" type="int">{1}</attribute>
\t\t<section name="graphics">
\t\t\t<attribute key="width" type="int">7</attribute>
\t\t\t<attribute key="fill" type="String">#000000</attribute>
\t\t</section>
\t\t</section>""".format(edge[0].key, edge[1].key)
        return string

    @property
    def serialize_nodes_xgml(self) -> str:
        """Сериализовать узлы графа"""
        string = ""
        for node in self.nodes.values():
            string += node.serialize_xgml(
                self.x_coefficient_serialization,
                self.z_coefficient_serialization,
                self.graph_zoom_x)
        return string

    def serialize_xgml(self) -> str:
        """Сериализовать граф"""
        return """<?xml version="1.0" encoding="Cp1251"?>
<section name="xgml">
\t<attribute key="Creator" type="String">yFiles</attribute>
\t<attribute key="Version" type="String">2.14</attribute>
\t<section name="graph">
\t\t<attribute key="hierarchic" type="int">1</attribute>
\t\t<attribute key="label" type="String"></attribute>
\t\t<attribute key="directed" type="int">1</attribute>
{0}{1}
\t</section>
</section>""".format(self.serialize_nodes_xgml, self.serialize_edges_xgml())

    def save_file(self, path: pathlib.Path):
        """Записать граф в XGML файл"""
        with codecs.open(str(path), "w", encoding="cp1251") as stream:
            stream.write(self.serialize_xgml())
            stream.close()

    def read_file(self, xgml_file: pathlib.Path):
        """Считать граф из XGML файла"""
        # pylint: disable=C0103
        tree = Et.parse(source=str(xgml_file.absolute()))
        root = tree.getroot()
        graph = root.find('section')

        self._read_nodes(graph)
        self._read_edges(graph)

    def _read_nodes(self, graph):
        """Считать узлы графа"""
        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'node':
                    node_id = section.findall("*[@key='id']")[0].text
                    text = section.findall("*[@key='label']")[0].text
                    graphics = section.findall("*[@name='graphics']")[0]
                    coordinates = self._get_coordinates(graphics)
                    color = graphics.findall("*[@key='fill']")[0].text.upper()
                    self.nodes[node_id] = Node(node_id, text, coordinates, color)

    def _get_coordinates(self, section) -> dict:
        """Получить координаты из секции графики"""
        tag_x = section.findall("*[@key='x']")[0]
        tag_y = section.findall("*[@key='y']")[0]
        return {
            'x': -1 * (float(tag_y.text) - self.graph_zoom_x) * self.x_coefficient_deserialization,
            'z': float(tag_x.text) * self.z_coefficient_deserialization
        }

    def _read_edges(self, graph):
        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'edge':
                    source_id = int(section.findall("*[@key='source']")[0].text)
                    target_id = int(section.findall("*[@key='target']")[0].text)
                    self.nodes[source_id].neighbors.add(self.nodes[target_id])
                    self.nodes[target_id].neighbors.add(self.nodes[source_id])

    @property
    def neutrals(self) -> list:
        """Узлы, где страна ==0"""
        return list(node for node in self.nodes_list if node.country == 0)

    @property
    def neutral_line(self) -> list:
        """Цепь нейтральных узлов"""

        raise NameError('WTF')

    def find(self, x, z, side: float = 10) -> Node:  # pylint: disable=C0103
        """Найти узел по координатам (в квадрате стороной 2*r)"""
        for node in self.nodes_list:
            if abs(x - node.x) < side and abs(z - node.z) < side:
                return node

    def capture(self, x, z, country: int):  # pylint: disable=C0103
        """Захват вершины"""
        node = self.find(x, z)
        print('Capture {}[{}] {}'.format(node.text, node.key, country))
        if not node:
            raise NameError('Not found node to capture for [{}] country in [x:{} z:{}]'.format(
                country, x, z))
        for neighbor in node.neighbors:
            if neighbor.country and neighbor.country != country:
                neighbor.country = 0
        node.capture(country)

    def capture_node(self, node: Node, coal: int):
        """Захват узла"""
        self.capture(node.x, node.z, coal)
