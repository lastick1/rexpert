"Узел графа"
import queue
import geometry


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

