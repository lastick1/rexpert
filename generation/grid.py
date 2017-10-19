"Работа с графом"
import codecs
import xml.etree.ElementTree as Et
import queue
import random
import pathlib
import geometry
import configs

class Node(geometry.Point):
    "Узел графа"
    def __init__(self, key: str, text: str, pos: dict, color: str):
        super().__init__(x=pos['x'], z=pos['z'])
        self.neighbors = set()
        self.key = key
        self.color = color
        self.text = text
        self._country = 0
        self._is_airfield = False
        if color == '#FF0000':
            self._country = 101
            self._is_airfield = True
        if color == '#00CCFF':
            self._country = 201
            self._is_airfield = True

    def get_country(self) -> int:
        "Получить страну"
        return self._country

    country = property(fget=get_country, doc='Страна')

    def __str__(self):
        return '{} {} {}'.format(self.key, self.country, self.text)

    def serialize_xgml(self, c_x, c_z, offset):
        "Сериализовать в формат XGML"
        return """\t\t<section name="node">
\t\t\t<attribute key="id" type="int">{0}</attribute>
\t\t\t<attribute key="label" type="String">{1}</attribute>
\t\t\t<section name="graphics">
\t\t\t\t<attribute key="x" type="double">{2}</attribute>
\t\t\t\t<attribute key="y" type="double">{3}</attribute>
\t\t\t\t<attribute key="w" type="double">45.0</attribute>
\t\t\t\t<attribute key="h" type="double">45.0</attribute>
\t\t\t\t<attribute key="type" type="String">ellipse</attribute>
\t\t\t\t<attribute key="raisedBorder" type="boolean">false</attribute>
\t\t\t\t<attribute key="fill" type="String">{4}</attribute>
\t\t\t\t<attribute key="outline" type="String">#000000</attribute>
\t\t\t\t<attribute key="outlineWidth" type="int">7</attribute>
\t\t\t</section>
\t\t\t<section name="LabelGraphics">
\t\t\t\t<attribute key="text" type="String">{1}</attribute>
\t\t\t\t<attribute key="fontSize" type="int">12</attribute>
\t\t\t\t<attribute key="fontName" type="String">Dialog</attribute>
\t\t\t\t<attribute key="anchor" type="String">c</attribute>
\t\t\t</section>
\t\t</section>""".format(self.key, self.text, c_z * self.z, offset - c_x * self.x, self.color)

    @property
    def color(self):
        "Цвет вершины"
        return {0: '#00FF00', 101: '#FF0000', 201: '#0000FF'}[self.country]

    @property
    def cc(self):  # pylint: disable=C0103
        "Компонента связности: все вершины той же страны, до которых есть путь"
        return self.bfs(ignore_country=False)[1]

    def path(self, to, ignore_country=True):  # pylint: disable=C0103
        "Путь к указанной вершине"
        bfs = self.bfs(ignore_country=ignore_country)[0]
        path = []
        i = to.key
        while i in bfs.keys():
            path.append(bfs[i])
            i = bfs[i].key
        path.reverse()
        return path

    def bfs(self, ignore_country=True):
        """ Обход в ширину от вершины
        :param ignore_country: Обходить всё подряд или только той же страны
        :rtype: tuple[dict, set]
        :returns: Словарь маршрута обхода в ширину [0], использованные вершины [1]
        """
        # pylint: disable=C0103
        v = self
        q = queue.Queue()  # очередь для добавления вершин при обходе в ширину
        path = dict()
        used = set()
        if v in used:
            return
        q.put(v)  # начинаем обход из вершины v
        used.add(v)
        while not q.empty():  # пока в очереди есть хотя бы одна вершина
            v = q.get()  # извлекаем вершину из очереди
            neighbors = v.neighbors if ignore_country else set(x for x in v.neighbors if x.country == self.country)  # pylint: disable=C0301
            for w in neighbors:  # запускаем обход из всех вершин, смежных с вершиной v
                if w in used:  # если вершина уже была посещена, то пропускаем ее
                    continue
                q.put(w)  # добавляем вершину в очередь обхода
                used.add(w)  # помечаем вершину как пройденную
                path[w.key] = v
        return path, used

    def to_dict(self):
        "Сериализовать в словарь"
        return {
            'country': self.country,
            'coordinate_x': self.x,
            'coordinate_z': self.z,
            'key': self.key,
            'text': self.text
        }


class Grid:
    "Граф (сетка)"
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
        "Узлы списком"
        return list(self.nodes[x] for x in self.nodes)

    @property
    def edges(self) -> list:
        "Все рёбра графа, в виде 2-элементных кортежей из соединяемых вершин"
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
        """ Кортеж всех рёбер в виде 2-элементных кортежей координат точек вершин ребра """
        edges = self.edges
        return tuple(((x[0].x, x[0].z), (x[1].x, x[1].z)) for x in edges)

    def serialize_edges_xgml(self) -> str:
        "Сериализация рёбер"
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

    def serialize_nodes_xgml(self) -> str:
        "Сериализовать узлы графа"
        string = ""
        for node in self.nodes.values():
            string += node.serialize_xgml(
                self.x_coefficient_serialization,
                self.z_coefficient_serialization,
                self.graph_zoom_x)
        return string

    def serialize_xgml(self) -> str:
        "Сериализовать граф"
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
</section>""".format(self.serialize_nodes_xgml(), self.serialize_edges_xgml())

    def save_file(self, path: pathlib.Path):
        "Записать граф в XGML файл"
        with codecs.open(str(path), "w", encoding="cp1251") as stream:
            stream.write(self.serialize_xgml())
            stream.close()

    def read_file(self, xgml_file: pathlib.Path):
        "Считать граф из XGML файла"
        # pylint: disable=C0103
        tree = Et.parse(source=str(xgml_file.absolute()))
        root = tree.getroot()
        graph = root.find('section')

        self._read_nodes(graph)
        self._read_edges(graph)

    def _read_nodes(self, graph):
        "Считать узлы графа"
        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'node':
                    node_id = int(section.findall("*[@key='id']")[0].text)
                    text = section.findall("*[@key='label']")[0].text
                    graphics = section.findall("*[@name='graphics']")[0]
                    coords = self._get_coordinates(graphics)
                    color = graphics.findall("*[@key='fill']")[0].text.upper()
                    self.nodes[node_id] = Node(node_id, text, coords, color)

    def _get_coordinates(self, section) -> tuple:
        'Получить координаты из секции графики'
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
        "Узлы, где страна ==0"
        return list(x for x in self.nodes_list if x.country == 0)

    @property
    def neutral_line(self) -> list:
        "Цепь нейтральных узлов"
        first = list(x for x in self.nodes_list if x.text == '!')[0]
        connected_component = list(first.cc)
        for node in connected_component:
            if node == first:
                continue
            r_prot = False
            b_prot = False
            for neighbor in node.neighbors:
                if neighbor.country == 101 and 'prot' in neighbor.text:
                    r_prot = True
                if neighbor.country == 201 and 'prot' in neighbor.text:
                    b_prot = True
            if r_prot and b_prot:
                return first.path(node, ignore_country=False) + [node]
        raise NameError('WTF')

    def find(self, x, z, side: float = 10) -> Node:  # pylint: disable=C0103
        "Найти узел по координатам (в квадрате стороной 2*r)"
        for node in self.nodes_list:
            if abs(x - node.x) < side and abs(z - node.z) < side:
                return node

    def capture(self, x, z, coal):  # pylint: disable=C0103
        "Захват точки"
        country = coal * 100 + 1
        node = self.find(x, z)
        print('Capture {}[{}] {}'.format(node.text, node.key, country))
        if not node:
            raise NameError('Not found node to capture for [{}] coal in [x:{} z:{}]'.format(
                coal, x, z))
        for neighbor in node.neighbors:
            if neighbor.country and neighbor.country != country:
                neighbor.country = 0
        node.country = country

    def capture_node(self, node: Node, coal: int):
        "Захват узла"
        self.capture(node.x, node.z, coal)
