"""Классы объектов миссии"""

from geometry import Point
from .formats import icon_text, influence_text


class FrontLineIcon(Point):
    def __init__(self, _id, point, target=None):
        """
        Класс иконки, из которых состоит линия фронта
        :param _id: ИД объекта MCU_Icon
        :param point: узел, иконки
        :param target: ИД следующей иконки в цепочке
        """
        super().__init__(x=point.x, z=point.z)
        self.target = target
        self.id = _id
        self.lc_name = _id * 2 - 1
        self.lc_desc = _id * 2

    def __str__(self):
        if self.target is not None:
            return icon_text.format(self.id, self.target, self.x, self.z, self.lc_name, self.lc_desc)
        else:
            return icon_text.format(self.id, '', self.x, self.z, self.lc_name, self.lc_desc)


class InfluenceArea(Point):
    def __init__(self, x: float, z: float, _id: int, boundary: list, country: int):
        """Класс зоны влияния, которая определяет принадлежность территории к какой-то стране
        :param _id: ИД объекта MCU_TR_InfluenceArea
        :param boundary: список вершин многоугольника зоны (по часовой стрелке)
        :param country: страна, к которой относится территория зоны
        """
        super().__init__(x=x, z=z)
        self.id = _id
        self.boundary = boundary
        self.country = country

    def __str__(self):
        boundary_text = ''
        for point in self.boundary:
            boundary_text += '    {:.2f}, {:.2f};\n'.format(point.x, point.z)
        return influence_text.format(self.id, float(self.x), float(self.z), self.country, boundary_text)

