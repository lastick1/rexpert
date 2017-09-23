"Работа с графом"
import xml.etree.ElementTree as Et
import queue
import random
import geometry
import configs
import pathlib

class Node(geometry.Point):
    "Узел графа"
    def __init__(self, key, x, z, country, is_aux: bool, selectable: bool, text: str):
        super().__init__(x=x, z=z, country=country)
        self.neighbors = set()
        self.key = key
        self.is_aux = is_aux
        self.selectable = selectable
        self.text = text

    def __str__(self):
        return '{} {} {}'.format(self.key, self.country, self.text)

    def serialize_xgml(self, c_x, c_z):
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
\t\t</section>""".format(self.key, self.text, c_z * self.z, - c_x * self.x, self.color)

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
            neighbors = v.neighbors if ignore_country else set(x for x in v.neighbors if x.country == self.country)
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
            'selectable': self.selectable,
            'text': self.text,
            'is_aux': self.is_aux
        }


class Chain:
    """ Цепочка узлов от начального до конечного """
    def __init__(self, start: Node, end: Node):
        self.nodes = start.path(end, ignore_country=(start.country == end.country)) + [end]


class Grid:
    "Граф (сетка)"
    def __init__(self, name: str, xgml: pathlib.Path, config: configs.Mgen):
        self.nodes = dict()  # узлы сетки
        self.tvd = config.cfg[name]['tvd']
        self.xgml_file = xgml
        self.scenario_min_distance = config.cfg['scenario_min_distance']
        self.graph_zoom_x = config.cfg[name]['graph_zoom_point']['y']
        self.graph_zoom_z = config.cfg[name]['graph_zoom_point']['x']
        self.x_coefficient_serialization = self.graph_zoom_x / config.cfg[name]['right_top']['x']
        self.z_coefficient_serialization = self.graph_zoom_z / config.cfg[name]['right_top']['z']
        self.x_coefficient_deserialization = config.cfg[name]['right_top']['x'] / self.graph_zoom_x
        self.z_coefficient_deserialization = config.cfg[name]['right_top']['z'] / self.graph_zoom_z
        self.read_file()

    @property
    def nodes_list(self) -> list:
        "Узлы списком"
        return list(self.nodes[x] for x in self.nodes.keys())

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
        for nodes in self.nodes.values():
            string += nodes.serialize_xgml(
                self.x_coefficient_serialization, self.z_coefficient_serialization)
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

    def connected_components(self, country) -> list:
        "Компоненты связности указанной страны"
        ccs = []
        used = set()
        nodes = set(x for x in self.nodes_list if x.loc_country == country)
        while len(nodes - used):
            first = list(nodes - used)[0]
            connected_component = first.cc
            ccs.append(connected_component)
            used |= set(connected_component)
        return ccs

    def read_file(self):
        "Считать граф из XGML файла"
        tree = Et.parse(source=str(self.xgml_file.absolute()))
        root = tree.getroot()
        graph = root.find('section')

        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'node':
                    tag_id = section.findall("*[@key='id']")[0]
                    tag_label = section.findall("*[@key='label']")[0]
                    section_graphics = section.findall("*[@name='graphics']")[0]
                    tag_x = section_graphics.findall("*[@key='x']")[0]
                    tag_y = section_graphics.findall("*[@key='y']")[0]
                    x = -1 * (float(tag_y.text) - self.graph_zoom_x) * self.x_coefficient_deserialization
                    z = float(tag_x.text) * self.z_coefficient_deserialization
                    tag_fill = section_graphics.findall("*[@key='fill']")[0]
                    country = None
                    if tag_fill.text.upper() == '#FF0000':
                        country = 101
                    if tag_fill.text.upper() == '#0000FF':
                        country = 201
                    if tag_fill.text.upper() == '#00FF00':
                        country = 0
                    node_id = int(tag_id.text)
                    selectable = False if '.' in tag_label.text else True
                    is_aux = True if 'prot' in tag_label.text.lower() else False
                    if tag_label.text not in ('rb', 'zero'):
                        self.nodes[node_id] = Node(
                            node_id, x, z, country, is_aux, selectable, tag_label.text)

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
        for x in connected_component:
            if x == first:
                continue
            r_prot = False
            b_prot = False
            for n in x.neighbors:
                if n.country == 101 and 'prot' in n.text:
                    r_prot = True
                if n.country == 201 and 'prot' in n.text:
                    b_prot = True
            if r_prot and b_prot:
                return first.path(x, ignore_country=False) + [x]

    @property
    def areas(self) -> dict:
        "Зоны влияния"
        countries = (101, 201)
        neutral_line = self.neutral_line
        if len(neutral_line) < 2:
            return []
        nl_start = neutral_line[0]
        nl_end = neutral_line[len(neutral_line)-1]
        areas = {x: [] for x in countries}
        for country in countries:
            cc_end_prot = None
            cc_start_prot = None
            for n in list(x for x in nl_start.neighbors if 'prot' in x.text):
                if n.country == country:
                    cc_end_prot = n
                    break
            for n in list(x for x in nl_end.neighbors if 'prot' in x.text):
                if n.country == country:
                    cc_start_prot = n
                    break
            p = cc_start_prot.path(cc_end_prot) + [cc_end_prot]
            p += neutral_line
            if country == 201:
                p.reverse()
            areas[country].append(p)
        return self._insert_gap(areas)

    @staticmethod
    def _insert_gap(areas):
        "Добавить зазор между зонами"
        result = {x: [] for x in areas.keys()}
        dist = -250
        for country in areas:
            for area in areas[country]:
                result[country].append([])
                i = 0
                while i < len(area):
                    if i == len(area)-1:
                        v_1 = area[i]
                        v_2 = area[0]
                        tmp = geometry.get_parallel_line(((v_1.x, v_1.z), (v_2.x, v_2.z)), dist)[0]
                        result[country][-1].append(
                            geometry.Point(x=tmp[0], z=tmp[1], country=country))
                    else:
                        v_1 = area[i]
                        v_2 = area[i + 1]
                        tmp = geometry.get_parallel_line(((v_1.x, v_1.z), (v_2.x, v_2.z)), dist)[0]
                        result[country][-1].append(
                            geometry.Point(x=tmp[0], z=tmp[1], country=country))
                    i += 1
        return result

    @property
    def scenarios(self) -> dict:
        "Выьрать точки сценариев, за которые будут вестись бои"
        countries = [101, 201]
        neutral_line = self.neutral_line[1:-2]
        first_candidates = list(neutral_line[1:-2])
        first = neutral_line[random.randint(0, len(first_candidates)-1)]
        second_candidates = []
        for candidate in first_candidates:
            if candidate.distance_to(first.x, first.z) > self.scenario_min_distance:
                second_candidates.append(candidate)
        random.shuffle(second_candidates)
        second = second_candidates.pop()
        random.shuffle(countries)
        zipped = list(zip(countries, [first, second]))
        result = {candidate[0]: [candidate[1]] for candidate in zipped}
        return result

    def find(self, x, z, r=10) -> Node:
        "Найти узел по координатам (в квадрате стороной 2*r)"
        for node in self.nodes_list:
            if abs(x - node.x) < r and abs(z - node.z) < r:
                return node

    def capture(self, x, z, coal):
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
        self._resolve(country)

    def capture_node(self, node, coal):
        "Захват узла"
        self.capture(node.x, node.z, coal)

    def _resolve(self, priority):
        "Красим 'нейтралов' за линией фронта в цвет победившей стороны"
        resolvable = []
        for neutral in self.neutrals:
            is_correct = False
            for node in list(x for x in neutral.neighbors if x.country):
                if node.country and node.country != priority:
                    is_correct = True
            if not is_correct:
                resolvable.append(neutral)
        for x in resolvable:
            x.country = priority
