"Расчёт координат"
from math import acos, pi


class Segment:  #pylint: disable=R0902
    "Класс отрезка"
    def __init__(self, x1, y1, x2, y2):
        # http://school-collection.edu.ru/catalog/res/925c1429-c4d9-43b8-8b08-ac6d44f57906/view/
        self._center = (x1 + x2)/2, (y1 + y2)/2
        length = ((y1 - y2) ** 2 + (x2 - x1) ** 2) ** 0.5  # длина вектора нормали
        self._nx = (y1 - y2) / length  # x единичного вектора нормали отрезка
        self._ny = (x2 - x1) / length  # y единичного вектора нормали отрезка
        self._dx = self._ny   # x единичного вектора, коллинеарного отрезку
        self._dy = -self._nx  # y единичного вектора, коллинеарного отрезку
        # http://webmath.mesi.ru/MESI/JSPBaseLine/HTMLLinks/index_1.jsp
        self._length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        e_x = 0.0
        e_y = 1.0

        scalar = e_x * self._dx + e_y * self._dy

        self._cos_a = scalar / 1

    @property
    def length(self):
        """ Длина отрезка """
        return self._length

    @property
    def center(self):
        """ Центр координат отрезка """
        return self._center

    @property
    def angle(self):
        "Угол между (0.0, 1.0) вектором и параллельной отрезку прямой, проходящей через (0.0, 0.0)"
        return acos(self._cos_a) * 180 / pi

    def parallel_segments(self, distance):
        """
        :param distance:
        :return: Два параллельных отрезка такой же длины на заданной дистанции от текущего отрезка
        :rtype: (Segment, Segment)
        """
        n_vector = self._nx * distance, self._ny * distance
        seg1 = Segment(self._x1 + n_vector[0], self._y1 + n_vector[1],
                       self._x2 + n_vector[0], self._y2 + n_vector[1])
        seg2 = Segment(self._x1 - n_vector[0], self._y1 - n_vector[1],
                       self._x2 - n_vector[0], self._y2 - n_vector[1])
        return seg1, seg2


class Point:  #pylint: disable=C0103,C0111
    """ Класс точки """
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
        xinters = None

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
