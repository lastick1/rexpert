from math import acos, pi
# import math


class Segment:
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
        return self._length

    @property
    def center(self):
        """ Центр координат отрезка """
        return self._center

    @property
    def angle(self):
        """ Угол между (0.0, 1.0) вектором и параллельной отрезку прямой, проходящей через (0.0, 0.0) """
        return acos(self._cos_a) * 180 / pi

    def parallel_segments(self, distance):
        """
        :param distance:
        :return: Два параллельных отрезка такой же длины на заданной дистанции от отрезка
        :rtype: (Segment, Segment)
        """
        n_vector = self._nx * distance, self._ny * distance
        s1 = Segment(self._x1 + n_vector[0], self._y1 + n_vector[1], self._x2 + n_vector[0], self._y2 + n_vector[1])
        s2 = Segment(self._x1 - n_vector[0], self._y1 - n_vector[1], self._x2 - n_vector[0], self._y2 - n_vector[1])
        return s1, s2
