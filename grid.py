import xml.etree.ElementTree as Et
import queue
import math
import random
import db
from cfg import MissionGenCfg


def rotate(v, b, c):
    return (b.x - v.x) * (c.z - b.z) - (b.z - v.z) * (c.x - b.x)


def get_parallel_line(line_x_y, dist):
    """Расчёт параллельного заданному (line_x_y) отрезка"""
    x1 = line_x_y[0][0]
    y1 = line_x_y[0][1]
    x2 = line_x_y[1][0]
    y2 = line_x_y[1][1]
    """Нахождение вектора нормали к исходной прямой"""
    norm = [y2 - y1, x1 - x2]
    """Длина вектора"""
    lenn = math.sqrt(math.pow(norm[0], 2) + math.pow(norm[1], 2))
    """Коэффициент перевода длины вектора нормали к заданному расстоянию"""
    kl = dist / lenn
    """Нахождение вектора нужной длины, коллинеарного нормали"""
    vect = [norm[0] * kl, norm[1] * kl]
    """Нахождение первой точки отрезка"""
    resbeg = (vect[0] + x1, vect[1] + y1)
    """Нахождение второй точки отрезка"""
    resend = (vect[0] + x2, vect[1] + y2)
    return [resbeg, resend]


class Point:
    def __init__(self, x=0.0, z=0.0, country=None):
        self.x = x
        self.z = z
        self._country = country

    def get_country(self):
        return self._country

    def set_country(self, value):
        self._country = value

    def del_country(self):
        del self._country

    country = property(get_country, set_country, del_country)

    def is_in_area(self, polygon):
        x = self.x
        y = self.z
        poly = [(x.x, x.z) for x in polygon]
        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def distance_to(self, x, z):
        return ((self.x - x) ** 2 + (self.z - z) ** 2) ** .5


class Node(Point):
    def __init__(self, key, x, z, country, is_aux, selectable, text):
        super().__init__(x=x, z=z, country=country)
        self.neighbors = set()
        self.key = key
        self.is_aux = is_aux
        self.selectable = selectable
        self.text = text

    def __str__(self):
        return '{} {} {}'.format(self.key, self.country, self.text)

    def serialize_xgml(self, c_x, c_z, tvd_name):
        """ Сериализация в формат XGML """
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
\t\t</section>""".format(
            self.key,
            self.text,
            c_z * self.z,
            - c_x * self.x,
            self.color
        )

    @property
    def color(self):
        return {0: '#00FF00', 101: '#FF0000', 201: '#0000FF'}[self.country]

    @property
    def cc(self):
        """ Компонента связности: все вершины той же страны, до которых есть путь """
        return self.bfs(ignore_country=False)[1]

    def path(self, to, ignore_country=True):
        """ Путь к указанной вершине """
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
    def __init__(self, start, end):
        """
        :type start: Node  
        :type end: Node 
        """
        self.nodes = start.path(end, ignore_country=(start.country == end.country)) + [end]


class Grid:
    def __init__(self, name):
        self.nodes = dict()  # узлы сетки
        self.name = name

    @property
    def nodes_list(self):
        """ Узлы списком """
        return list(self.nodes[x] for x in self.nodes.keys())

    @property
    def edges(self):
        """ Список всех рёбер, соединяющих вершины, в виде 2-элементных кортежей из соединяемых вершин """
        edges = []
        used = set()
        for n in self.nodes:
            if self.nodes[n] in used:
                continue
            for b in self.nodes[n].neighbors:
                if b in used:
                    continue
                edges.append((self.nodes[n], b))
            used.add(self.nodes[n])
        return edges

    def serialize_edges_xgml(self):
        string = ""
        for e in self.edges:
            string += """
\t\t<section name="edge">
\t\t\t<attribute key="source" type="int">{0}</attribute>
\t\t\t<attribute key="target" type="int">{1}</attribute>
\t\t<section name="graphics">
\t\t\t<attribute key="width" type="int">7</attribute>
\t\t\t<attribute key="fill" type="String">#000000</attribute>
\t\t</section>
\t\t</section>""".format(e[0].key, e[1].key)
        return string

    def serialize_nodes_xgml(self):
        string = ""
        c_x = MissionGenCfg.cfg[self.name]['graph_zoom_point']['y'] / MissionGenCfg.cfg[self.name]['right_top']['x']
        c_z = MissionGenCfg.cfg[self.name]['graph_zoom_point']['x'] / MissionGenCfg.cfg[self.name]['right_top']['z']
        for n in self.nodes.values():
            string += n.serialize_xgml(c_x, c_z, self.name)
        return string

    def serialize_xgml(self):
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
</section>""".format(
            self.serialize_nodes_xgml(),
            self.serialize_edges_xgml()
        )

    def connected_components(self, country):
        """ Компоненты связности указанной страны """
        ccs = []
        used = set()
        nodes = set(x for x in self.nodes_list if x.loc_country == country)
        while len(nodes - used):
            first = list(nodes - used)[0]
            cc = first.cc
            ccs.append(cc)
            used |= set(cc)
        return ccs


    def write_db(self):
        db.PGConnector.Graph.insert(
            MissionGenCfg.cfg[self.name]['tvd'],
            tuple(x.to_dict() for x in self.nodes_list),
            tuple({'node_a': x[0].key, 'node_b': x[1].key} for x in self.edges))

    def read_db(self):
        self.nodes.clear()
        nodes_rows, edges_rows = db.PGConnector.Graph.select(MissionGenCfg.cfg[self.name]['tvd'])
        for row in nodes_rows:
            self.nodes[row['key']] = Node(
                row['key'],
                row['coordinate_x'],
                row['coordinate_z'],
                row['country'],
                row['is_aux'],
                row['selectable'],
                row['text']
            )
        for row in edges_rows:
            source_id = row['node_a']
            target_id = row['node_b']
            self.nodes[source_id].neighbors.add(self.nodes[target_id])
            self.nodes[target_id].neighbors.add(self.nodes[source_id])

    def read_file(self):
        """ Считать граф из XGML файла """
        xgml_file = MissionGenCfg.xgml[self.name]
        tree = Et.parse(source=str(xgml_file.absolute()))
        root = tree.getroot()
        graph = root.find('section')
        rb_point_x = 0
        rb_point_y = 0
        for section in graph.findall("*[@name='node']"):
            tag_label = section.findall("*[@key='label']")[0]
            if tag_label.text == "rb":
                section_graphics = section.findall("*[@name='graphics']")[0]
                tag_x = section_graphics.findall("*[@key='x']")[0]
                tag_y = section_graphics.findall("*[@key='y']")[0]
                rb_point_x = float(tag_x.text)
                rb_point_y = float(tag_y.text)

        x_coefficient = MissionGenCfg.cfg[self.name]['right_top']['x'] / \
                        MissionGenCfg.cfg[self.name]['graph_zoom_point']['y']
        z_coefficient = MissionGenCfg.cfg[self.name]['right_top']['z'] / \
                        MissionGenCfg.cfg[self.name]['graph_zoom_point']['x']

        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'node':
                    tag_id = section.findall("*[@key='id']")[0]
                    tag_label = section.findall("*[@key='label']")[0]
                    section_graphics = section.findall("*[@name='graphics']")[0]
                    tag_x = section_graphics.findall("*[@key='x']")[0]
                    tag_y = section_graphics.findall("*[@key='y']")[0]
                    x = -1 * (float(tag_y.text) - rb_point_y) * x_coefficient
                    z = float(tag_x.text) * z_coefficient
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
                        self.nodes[node_id] = Node(node_id, x, z, country, is_aux, selectable, tag_label.text)

        for section in graph:
            if str(section.tag) == 'section':
                if section.attrib['name'] == 'edge':
                    source_id = int(section.findall("*[@key='source']")[0].text)
                    target_id = int(section.findall("*[@key='target']")[0].text)
                    self.nodes[source_id].neighbors.add(self.nodes[target_id])
                    self.nodes[target_id].neighbors.add(self.nodes[source_id])
        # масштабирование графа к заданному размеру (задаётся точкой right_top)
        """for n in self.nodes:
            self.nodes[n].x *= x_coefficient
            self.nodes[n].z *= z_coefficient
            """

    @property
    def neutrals(self):
        return list(x for x in self.nodes_list if x.country == 0)

    @property
    def neutral_line(self):
        """ Цепь нейтральных узлов """
        first = list(x for x in self.nodes_list if x.text == '!')[0]
        cc = list(first.cc)
        for x in cc:
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
    def areas(self):
        """ Зоны влияния
         :rtype dict """
        countries = (101, 201)
        nl = self.neutral_line
        if len(nl) < 2:
            return []
        nl_start = nl[0]
        nl_end = nl[len(nl)-1]
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
            p += nl
            if country == 201:
                p.reverse()
            areas[country].append(p)
        return self._insert_gap(areas)

    @staticmethod
    def _insert_gap(areas):
        """ Добавить зазор между зонами """
        r = {x: [] for x in areas.keys()}
        dist = -250
        for country in areas:
            for area in areas[country]:
                r[country].append([])
                i = 0
                while i < len(area):
                    if i == len(area)-1:
                        v1 = area[i]
                        v2 = area[0]
                        t = get_parallel_line(((v1.x, v1.z), (v2.x, v2.z)), dist)[0]
                        r[country][-1].append(Point(x=t[0], z=t[1], country=country))
                    else:
                        v1 = area[i]
                        v2 = area[i + 1]
                        t = get_parallel_line(((v1.x, v1.z), (v2.x, v2.z)), dist)[0]
                        r[country][-1].append(Point(x=t[0], z=t[1], country=country))
                    i += 1
        return r

    @property
    def scenarios(self):
        countries = [101, 201]
        nl = self.neutral_line[1:-2]
        first_candidates = list(nl[1:-2])
        first = nl[random.randint(0, len(first_candidates)-1)]
        second_candidates = []
        for x in first_candidates:
            if x.distance_to(first.x, first.z) > MissionGenCfg.cfg['scenario_min_distance']:
                second_candidates.append(x)
        random.shuffle(second_candidates)
        second = second_candidates.pop()
        random.shuffle(countries)
        # z = list(zip(countries, [nl[-1], nl[-2]]))
        # print('Scenarios selection in test mode')
        z = list(zip(countries, [first, second]))
        d = {x[0]: [x[1]] for x in z}
        return d

    def find(self, x, z, r=10):
        """ Найти узел по координатам (в квадрате стороной 2*r) """
        for n in self.nodes_list:
            if abs(x - n.x) < r and abs(z - n.z) < r:
                return n

    def capture(self, x, z, coal):
        """ Захват точки """
        country = coal * 100 + 1
        node = self.find(x, z)
        print('Capture {}[{}] {}'.format(node.text, node.key, country))
        if not node:
            raise NameError('Not found node to capture for [{}] coal in [x:{} z:{}]'.format(coal, x, z))
        for n in node.neighbors:
            if n.country and n.country != country:
                n.country = 0
                db.PGConnector.Graph.update_graph_node(n.key, MissionGenCfg.cfg[self.name]['tvd'], 0)
        node.country = country
        db.PGConnector.Graph.update_graph_node(node.key, MissionGenCfg.cfg[self.name]['tvd'], country)
        self._resolve(country)

    def capture_node(self, node, coal):
        """ Захват узла """
        self.capture(node.x, node.z, coal)

    def _resolve(self, priority):
        """ Красим "нейтралов" за линией фронта в цвет победившей стороны """
        resolvable = []
        for n in self.neutrals:
            is_correct = False
            for nc in list(x for x in n.neighbors if x.country):
                if nc.country and nc.country != priority:
                    is_correct = True
            if not is_correct:
                resolvable.append(n)
        for x in resolvable:
            x.country = priority
            db.PGConnector.Graph.update_graph_node(x.key, MissionGenCfg.cfg[self.name]['tvd'], priority)
