"""Выбор аэродромов для миссии
В миссии у сторон по 3 фронтовых филда и по 4 тыловых.

Фронтовые (по 3) выбираются по алгоритму:
* Все аэродромы фильтруются по нахождению в прифронтовой зоне
* Полученный список сортируется по общему количеству самолётов
* Из списка берутся первый, последний и случайный аэродром

Тыловые (по 4) выбираются по алгоритму:
* Все аэродромы фильтруются по нахождению вне прифронтовой зоны
* Список делится на 2 по дистанции до ближайшего склада
* Из списка аэродромов каждого склада выбираются: наиболее заполненный и случайный"""

from random import choice, shuffle
from geometry import remove_too_close
from configs import Main
from model import ManagedAirfield
from utils import compare_float, cmp_to_key


def _front_airfields_comparator(airfield1: ManagedAirfield, airfield2: ManagedAirfield):
    """Сравнение фронтовых аэродромов при выборе"""
    return compare_float(airfield1.power, airfield2.power)


def _rear_airfields_comparator(airfield1: ManagedAirfield, airfield2: ManagedAirfield):
    """Сравнение тыловых аэродромов при выборе"""
    return compare_float(airfield1.planes_count, airfield2.planes_count)


class AirfieldsSelector:
    """Класс, отвечающий за выбор аэродромов в зависимости от их состояния"""

    def __init__(self, main: Main):
        self._main = main

    def select_rear(self, influence: list, front_area: list, airfields: list, warehouses: list) -> list:
        """Выбрать тыловой аэродром"""
        country_warehouses = list()
        for warehouse in warehouses:
            if warehouse.is_in_area(influence):
                country_warehouses.append(warehouse)

        rear_airfields = list(x for x in airfields if not x.is_related_to_area(front_area) and x.is_in_area(influence))
        if not rear_airfields:
            raise NameError('Невозможно выбрать тыловой аэродром')

        warehouse_airfields = dict()
        for airfield in rear_airfields:
            key = airfield.get_closest(country_warehouses).name
            if key not in warehouse_airfields:
                warehouse_airfields[key] = list()
            warehouse_airfields[key].append(airfield)
        result = list()
        for key in warehouse_airfields:
            warehouse_airfields[key].sort(
                key=cmp_to_key(_rear_airfields_comparator))
            result.append(warehouse_airfields[key].pop())
            shuffle(warehouse_airfields[key])
            result.append(warehouse_airfields[key].pop())
        return result

    def select_front(self, divisions: list, influence: list, front_area: list, airfields: list) -> list:
        """Выбрать фронтовые аэродромы"""
        # TODO придумать, как сделать выбор аэродромов в зависимости от дивизий
        if airfields:
            front = list(x for x in airfields if x.is_related_to_area(front_area) and x.is_in_area(influence))
            # d = {x.name: x.to_dict() for x in front}
            if front:
                result = list()
                front.sort(key=cmp_to_key(_front_airfields_comparator))
                result.append(front.pop())
                front.reverse()
                result.append(front.pop())
                # чем ближе 2 первых друг к другу, тем дальше от них третий
                distance = 1000000000 / \
                    result[0].distance_to(result[1].x, result[1].z) + 10000
                front = remove_too_close(front, result, distance)
                result.append(choice(front))
                return result
            raise NameError('Невозможно выбрать фронтовые аэродромы')
        raise ValueError()
