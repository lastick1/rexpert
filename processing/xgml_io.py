"""Чтение-запись графа из/в xmgl-файлы"""
import codecs
import xml.etree.ElementTree as Et
import configs
import model
from .grid_io import GridIO

FILE_FORMAT = """<?xml version="1.0" encoding="Cp1251"?>
<section name="xgml">
\t<attribute key="Creator" type="String">yFiles</attribute>
\t<attribute key="Version" type="String">2.14</attribute>
\t<section name="graph">
\t\t<attribute key="hierarchic" type="int">1</attribute>
\t\t<attribute key="label" type="String"></attribute>
\t\t<attribute key="directed" type="int">1</attribute>
{0}{1}
\t</section>
</section>"""

NODE_FORMAT = """\t\t<section name="node">
\t\t\t<attribute key="id" type="int">{0}</attribute>
\t\t\t<attribute key="label" type="String">{1}</attribute>
\t\t\t<section name="graphics">
\t\t\t\t<attribute key="x" type="double">{2}</attribute>
\t\t\t\t<attribute key="y" type="double">{3}</attribute>
\t\t\t\t<attribute key="w" type="double">15.0</attribute>
\t\t\t\t<attribute key="h" type="double">15.0</attribute>
\t\t\t\t<attribute key="type" type="String">ellipse</attribute>
\t\t\t\t<attribute key="raisedBorder" type="boolean">false</attribute>
\t\t\t\t<attribute key="fill" type="String">{4}</attribute>
\t\t\t\t<attribute key="outline" type="String">#000000</attribute>
\t\t\t\t<attribute key="outlineWidth" type="int">1</attribute>
\t\t\t</section>
\t\t\t<section name="LabelGraphics">
\t\t\t\t<attribute key="text" type="String">{1}</attribute>
\t\t\t\t<attribute key="fontSize" type="int">12</attribute>
\t\t\t\t<attribute key="fontName" type="String">Dialog</attribute>
\t\t\t\t<attribute key="anchor" type="String">c</attribute>
\t\t\t</section>
\t\t</section>"""

EDGE_FORMAT = """
\t\t<section name="edge">
\t\t\t<attribute key="source" type="int">{0}</attribute>
\t\t\t<attribute key="target" type="int">{1}</attribute>
\t\t<section name="graphics">
\t\t\t<attribute key="width" type="int">1</attribute>
\t\t\t<attribute key="fill" type="String">#000000</attribute>
\t\t</section>
\t\t</section>"""


class Xgml(GridIO):  # pylint: disable=R0902
    """Класс ввода-вывода графа в xgml формате"""
    def __init__(self, name: str, config: configs.Mgen):
        self._nodes, self._edges, self.name = None, None, name
        self.graph_zoom_x = config.cfg[name]['graph_zoom_point']['y']
        self.graph_zoom_z = config.cfg[name]['graph_zoom_point']['x']
        self.x_coefficient_serialization = self.graph_zoom_x / config.cfg[name]['right_top']['x']
        self.z_coefficient_serialization = self.graph_zoom_z / config.cfg[name]['right_top']['z']
        self.x_coefficient_deserialization = config.cfg[name]['right_top']['x'] / self.graph_zoom_x
        self.z_coefficient_deserialization = config.cfg[name]['right_top']['z'] / self.graph_zoom_z

    def parse(self, file: str) -> None:
        tree = Et.parse(source=file)
        root = tree.getroot()
        graph = root.find('section')

        self._nodes, self._edges = self._read_edges(graph, self._read_nodes(graph))

    def save_file(self, path: str, nodes: dict, edges: list) -> None:
        with codecs.open(str(path), "w", encoding="cp1251") as stream:
            stream.write(self.serialize(nodes, edges))
            stream.close()

    @property
    def edges(self) -> list:
        if self._edges:
            return list(self._edges).copy()

    @property
    def nodes(self) -> dict:
        if self._nodes:
            return dict(self._nodes).copy()

    def _read_nodes(self, graph) -> dict:
        """Считать узлы графа"""
        nodes = dict()
        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'node':
                    node_id = section.findall("*[@key='id']")[0].text
                    text = section.findall("*[@key='label']")[0].text
                    graphics = section.findall("*[@name='graphics']")[0]
                    coordinates = self._get_coordinates(graphics)
                    color = graphics.findall("*[@key='fill']")[0].text.upper()
                    nodes[node_id] = model.Node(node_id, text, coordinates, color)
        return nodes

    def _get_coordinates(self, section) -> dict:
        """Получить координаты из секции графики"""
        tag_x = section.findall("*[@key='x']")[0]
        tag_y = section.findall("*[@key='y']")[0]
        return {
            'x': -1 * (float(tag_y.text) - self.graph_zoom_x) * self.x_coefficient_deserialization,
            'z': float(tag_x.text) * self.z_coefficient_deserialization
        }

    @staticmethod
    def _read_edges(graph, nodes: dict) -> tuple:
        edges = []
        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'edge':
                    source_id = section.findall("*[@key='source']")[0].text
                    target_id = section.findall("*[@key='target']")[0].text
                    nodes[source_id].neighbors.add(nodes[target_id])
                    nodes[target_id].neighbors.add(nodes[source_id])
                    edges.append((source_id, target_id))
        return nodes, edges

    @staticmethod
    def serialize_node_xgml(c_x, c_z, offset, node: model.Node) -> str:
        """Сериализовать в формат XGML"""
        return NODE_FORMAT.format(node.key, node.text + ' ' + node.key, c_z * node.z, offset - c_x * node.x, node.color)
    # TODO не забыть убрать запись ключа в текст узла тут ^

    @staticmethod
    def serialize_edges_xgml(edges: list) -> str:
        """Сериализация рёбер"""
        string = ""
        for edge in edges:
            string += EDGE_FORMAT.format(edge[0].key, edge[1].key)
        return string

    def serialize_nodes_xgml(self, nodes: dict) -> str:
        """Сериализовать узлы графа"""
        string = ""
        for node in nodes.values():
            string += self.serialize_node_xgml(
                self.x_coefficient_serialization,
                self.z_coefficient_serialization,
                self.graph_zoom_x, node)
        return string

    def serialize(self, nodes: dict, edges: list) -> str:
        return FILE_FORMAT.format(self.serialize_nodes_xgml(nodes), self.serialize_edges_xgml(edges))
