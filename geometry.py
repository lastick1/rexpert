"""Расчёт координат"""
import math
import utils


def rotate(v, b, c):  # pylint: disable=C0103
    """Полезная функция, с помощью которой можно определить положение точки относительно отрезка
    положительное возвращаемое значение соответствует левой стороне, отрицательное — правой"""
    return (b.x - v.x) * (c.z - b.z) - (b.z - v.z) * (c.x - b.x)


def get_parallel_line(line_x_y, dist):
    """Расчёт параллельного заданному (line_x_y) отрезка"""
    x_1 = line_x_y[0][0]
    y_1 = line_x_y[0][1]
    x_2 = line_x_y[1][0]
    y_2 = line_x_y[1][1]
    # Нахождение вектора нормали к исходной прямой
    norm = [y_2 - y_1, x_1 - x_2]
    # Длина вектора
    lenn = math.sqrt(math.pow(norm[0], 2) + math.pow(norm[1], 2))
    # Коэффициент перевода длины вектора нормали к заданному расстоянию
    koef = dist / lenn
    # Нахождение вектора нужной длины, коллинеарного нормали
    vect = [norm[0] * koef, norm[1] * koef]
    # Нахождение первой точки отрезка
    resbeg = (vect[0] + x_1, vect[1] + y_1)
    # Нахождение второй точки отрезка
    resend = (vect[0] + x_2, vect[1] + y_2)
    return [resbeg, resend]


class Segment:  # pylint: disable=R0902
    """Класс отрезка"""

    def __init__(self, x1, y1, x2, y2):
        # http://school-collection.edu.ru/catalog/res/925c1429-c4d9-43b8-8b08-ac6d44f57906/view/
        self._center = (x1 + x2) / 2, (y1 + y2) / 2
        length = ((y1 - y2) ** 2 + (x2 - x1) ** 2) ** 0.5  # длина вектора нормали
        self._nx = (y1 - y2) / length  # x единичного вектора нормали отрезка
        self._ny = (x2 - x1) / length  # y единичного вектора нормали отрезка
        self._dx = self._ny  # x единичного вектора, коллинеарного отрезку
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
        """Угол между (0.0, 1.0) вектором и параллельной отрезку прямой, проходящей через (0.0, 0.0)"""
        return math.acos(self._cos_a) * 180 / math.pi

    def parallel_segments(self, gap):
        """
        :param gap: расстояние между отрезками
        :return: Два параллельных отрезка такой же длины на заданной дистанции от текущего отрезка
        :rtype: (Segment, Segment)
        """
        n_vector = self._nx * gap, self._ny * gap
        seg1 = Segment(self._x1 + n_vector[0], self._y1 + n_vector[1],
                       self._x2 + n_vector[0], self._y2 + n_vector[1])
        seg2 = Segment(self._x1 - n_vector[0], self._y1 - n_vector[1],
                       self._x2 - n_vector[0], self._y2 - n_vector[1])
        return seg1, seg2


class Point:  # pylint: disable=C0103,C0111
    """ Класс точки """

    def __init__(self, x=0.0, z=0.0):
        self.x = x
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.z))

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {'x': self.x, 'z': self.z}

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

    def get_closest(self, points):
        closest: Point = points[0]
        for point in points:
            if self.distance_to(point.x, point.z) < self.distance_to(closest.x, closest.z):
                closest = point
        return closest

    def is_in_vertices_of_area(self, points, radius):
        for point in points:
            if self.distance_to(point.x, point.z) < radius:
                return True
        return False

    def is_related_to_area(self, polygon):
        return self.is_in_area(polygon) or self.is_in_vertices_of_area(polygon, 1000)

    def distance_to(self, x: float, z: float):
        return ((self.x - x) ** 2 + (self.z - z) ** 2) ** .5


def distance(point1: dict, point2: dict) -> float:
    """Расстояние между точками"""
    return math.hypot(point2['x'] - point1['x'], point2['z'] - point1['z'])


def sort_points_clockwise(points, middle_point) -> list:
    """Сортировка точек по часовой стрелке вокруг центра"""
    def comparator(lhs, rhs):
        """Сравнить углы"""
        lhs_angle = math.atan2(lhs.z - average_z, lhs.x - average_x)
        rhs_angle = math.atan2(rhs.z - average_z, rhs.x - average_x)
        if lhs_angle < rhs_angle:
            return -1
        if lhs_angle > rhs_angle:
            return 1
        return 0

    average_x = middle_point.x
    average_z = middle_point.z
    return sorted(points, key=utils.cmp_to_key(comparator))


def remove_too_close(src: list, check_points: list, radius: float) -> list:
    """Убрать из списка точки, которые слишком близко к точкам второго списка"""
    result = list()
    for point in src:
        close = False
        for check in check_points:
            if point.distance_to(check.x, check.z) < radius:
                close = True
                break
        if not close:
            result.append(point)
    return result

def remove_too_far(src: list, check_points: list, radius: float) -> list:
    """Убрать из списка точки, которые слишком далеко от точек второго списка"""
    result = list()
    for point in src:
        for check in check_points:
            if point.distance_to(check.x, check.z) < radius:
                result.append(point)
                break
    return result

def jarvis_march(array: list) -> list:
    """Находит минимальную выпуклую оболочку в массиве точек"""
    # pylint: disable=C0103
    # https://habrahabr.ru/post/144921/
    n = len(array)
    p = list(range(n))
    # start point
    for i in range(1, n):
        if array[p[i]].x < array[p[0]].x:
            p[i], p[0] = p[0], p[i]
    h = [p[0]]
    del p[0]
    p.append(h[0])
    while True:
        right = 0
        for i in range(1, len(p)):
            if rotate(array[h[-1]], array[p[right]], array[p[i]]) < 0:
                right = i
        if p[right] == h[0]:
            break
        else:
            h.append(p[right])
            del p[right]
    return [array[x] for x in h]


def is_pos_correct(pos: dict) -> bool:
    """Корректная ли позиция"""
    if not pos or pos == {'x': 0.0, 'y': 0.0, 'z': 0.0}:
        return False
    return True
