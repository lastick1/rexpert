"Полезные функции"
import math


# http://www.ariel.com.au/a/python-point-int-poly.html
#pylint: disable=C0103
def point_in_polygon(point, polygon):
    "Проверка вхождения точки в многоугольник"
    x, y = point['x'], point['z']
    n = len(polygon)
    inside = False
    p1x, _, p1y = polygon[0]
    for i in range(n + 1):
        p2x, _, p2y = polygon[i % n]
        if min(p1y, p2y) < y <= max(p1y, p2y) and x <= max(p1x, p2x):
            if p1y != p2y:
                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if p1x == p2x or x <= xinters:
                inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def distance(point1: dict, point2: dict) -> float:
    "Расстояние между точками"
    return math.hypot(point2['x'] - point1['x'], point2['z'] - point1['z'])


def is_pos_correct(pos: dict) -> bool:
    "Коррекная ли позиция"
    if not pos or pos == {'x': 0.0, 'y': 0.0, 'z': 0.0}:
        return False
    return True
