"""Узел графа"""
import queue
import geometry

COLOR_MAP = {0: '#FFFFFF', 101: '#FF0000', 201: '#00CCFF'}


class Node(geometry.Point):
    """Узел графа"""
    def __init__(self, key: str, text: str, pos: dict, color: str):
        super().__init__(x=pos['x'], z=pos['z'])
        self.neighbors = set()
        self.key = key
        self._color = color
        self.text = text
        self._country = 0
        self._is_airfield = False
        if color == COLOR_MAP[101]:
            self._country = 101
            self._is_airfield = True
        if color == COLOR_MAP[201]:
            self._country = 201
            self._is_airfield = True

    @property
    def is_airfield(self):
        """Является ли вершина аэродромом (захватываемой)"""
        return self._is_airfield

    @property
    def country(self) -> int:
        """Страна вершины"""
        return self._country

    @property
    def color(self) -> str:
        """Цвет вершины"""
        return COLOR_MAP[self._country]

    @property
    def is_border(self) -> bool:
        """Лежит ли вершина между вершинами разных стран"""
        countries = set()
        for neighbor in self.neighbors:
            countries.add(neighbor.country)
        return len(countries) > 2

    @property
    def border_neighbors(self) -> set:
        """Соседи, лежащие между вершинами разных стран"""
        return set(node for node in self.neighbors if node.is_border)

    @property
    def has_border_neighbor(self) -> bool:
        """Есть ли среди соседей узлы лежащие между вершинами разных стран"""
        return bool(len(self.border_neighbors))

    @property
    def not_border_neighbors(self) -> set:
        """Соседи, не лежащие между вершинами разных стран"""
        return set(node for node in self.neighbors if not node.is_border)

    @property
    def neighbors_sorted(self) -> list:
        """Соседи, отсортированные против часовой стрелки"""
        return geometry.sort_points_clockwise(list(self.neighbors), self)

    @property
    def triangles(self) -> list:
        """Треугольники, в которые входит вершина"""
        result = list()
        used = set()
        for neighbor in self.neighbors:
            nodes = set(neighbor.neighbors) & self.neighbors
            for tmp in nodes:
                triangle = self, neighbor, tmp
                triangle_keys = int(self.key), int(neighbor.key), int(tmp.key)
                triangle_hash = ''
                for key in sorted(triangle_keys):
                    triangle_hash += '_{}'.format(key)
                if triangle_hash in used:
                    continue
                result.append(triangle)
                used.add(triangle_hash)
        return list(result)

    @property
    def related_country(self):
        """Страна соседей (все ли соседи одной страны). 0 если страны отличаются"""
        nodes = list(node for node in self.neighbors if node.country)
        if not nodes:
            return self.country
        first = nodes.pop().country
        while nodes:
            current = nodes.pop().country
            if first != current:
                return 0
        return first

    def __str__(self):
        return '{} {} {}'.format(self.key, self.country, self.text)

    def path(self, to, ignore_country=True) -> list:  # pylint: disable=C0103
        """Путь к указанной вершине"""
        bfs = self.bfs(ignore_country=ignore_country)[0]
        path = []
        i = to.key
        while i in bfs.keys():
            path.append(bfs[i])
            i = bfs[i].key
        path.reverse()
        return path

    def bfs(self, ignore_country=True) -> tuple:
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
            return path, used
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

    def to_dict(self) -> dict:
        """Сериализовать в словарь"""
        return {
            'country': self.country,
            'coordinate_x': self.x,
            'coordinate_z': self.z,
            'key': self.key,
            'text': self.text
        }

    def capture(self, country: int) -> None:
        """Захватить вершину"""
        if country == 0:
            raise NameError('Cannot capture by neutrals')  # нельзя красить в нейтралов
        if self._country == 0:
            raise NameError('Cannot capture neutrals')  # нельзя красить нейтралов
        self._country = country
