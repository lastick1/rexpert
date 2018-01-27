"""Управление папкой ТВД"""
import datetime
import pathlib

import constants
import geometry

from .grid import Grid


class Boundary(geometry.Point):
    """Класс зоны влияния"""

    def __init__(self, x: float, z: float, polygon: list):
        super().__init__(x=x, z=z)
        self.polygon = polygon


class Tvd:
    """Настройки ТВД для генерации миссии"""
    def __init__(
            self,
            name: str,
            folder: str,
            date: str,
            right_top: dict,
            divisions: list(),
            grid: Grid,
            icons_group_file: pathlib.Path
    ):
        self.name = name  # имя твд
        self.folder = folder  # папка твд
        self.date = datetime.datetime.strptime(date, constants.DATE_FORMAT)  # дата миссии
        self.right_top = right_top  # правый верхний угол карты
        self.divisions = divisions  # дивизии с их местоположением
        self.icons_group_file = icons_group_file  # файл группы иконок
        self.confrontation_east = list()  # восточная прифронтовая зона
        self.confrontation_west = list()  # западная прифронтовая зона
        self.influences = dict()  # инфлюенсы СССР и Германии
        self.red_front_airfields = list()  # советские аэродромы в миссии
        self.red_rear_airfield = None  # советский тыловой аэродром в миссии
        self.blue_front_airfields = list()  # немецкие аэродромы в миссии
        self.blue_rear_airfield = None  # немецкий тыловой аэродром в миссии
        self._border: list = None
        self._nodes_list: list = None
        self.grid = grid  # граф этого ТВД

    @property
    def border(self) -> list:
        """упорядоченный список узлов линии фронта"""
        if not self._border:
            self._border = self.grid.border
        return self._border

    @property
    def nodes_list(self):
        """Список всех вершин графа"""
        if not self._nodes_list:
            self._nodes_list = self.grid.nodes_list
        return self._nodes_list

    def get_country(self, point: geometry.Point) -> int:
        """Определить страну, на территории которой находится точка"""
        for country in self.influences:
            for boundary in self.influences[country]:
                if point.is_in_area(boundary.polygon):
                    return country
        return 0

    def to_country_dict(self, points: list) -> dict:
        """Рассортировать точки в словарь стран"""
        result = dict()
        for point in points:
            country = self.get_country(point)
            if country not in result:
                result[country] = list()
            result[country].append(point)
        return result

    def to_country_dict_rear(self, points: list) -> dict:
        """Рассортировать тыловые точки в словарь стран"""
        front_areas = {101: self.confrontation_east, 201: self.confrontation_west}
        result = dict()
        for point in points:
            country = self.get_country(point)
            if country not in result:
                result[country] = list()
            if not point.is_in_area(front_areas[country]):
                result[country].append(point)
        return result

    def to_country_dict_front(self, points: list) -> dict:
        """Рассортировать фронтовые точки в словарь стран"""
        front_areas = {101: self.confrontation_east, 201: self.confrontation_west}
        result = dict()
        for point in points:
            country = self.get_country(point)
            if country not in result:
                result[country] = list()
            if point.is_in_area(front_areas[country]):
                result[country].append(point)
        return result
