"""Узел графа"""
import queue
import geometry


class Node(geometry.Point):
    color_map = {0: '#FFFFFF', 101: '#FF0000', 201: '#00CCFF'}

    """Узел графа"""
    def __init__(self, key: str, text: str, pos: dict, color: str):
        super().__init__(x=pos['x'], z=pos['z'])
        self.neighbors = set()
        self.key = key
        self._color = color
        self.text = text
        self._country = 0
        self._is_airfield = False
        if color == '#FF0000':
            self._country = 101
            self._is_airfield = True
        if color == '#00CCFF':
            self._country = 201
            self._is_airfield = True

    @property
    def country(self) -> int:
        """Страна вершины"""
        return self._country

    @property
    def color(self) -> str:
        """Цвет вершины"""
        return Node.color_map[self._country]

    @property
    def is_border(self) -> bool:
        """Лежит ли вершина между вершинами разных стран"""
        countries = set()
        for neighbor in self.neighbors:
            countries.add(neighbor.country)
        return len(countries) > 2

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
