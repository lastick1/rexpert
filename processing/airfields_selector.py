"""Выбор аэродромов для миссии
В миссии у сторон по 3 фронтовых филда и 1 тыловой.

Фронтовые выбираются по алгоритму:
* Все аэродромы фильтруются по нахождению в прифронтовой зоне
* Полученный список сортируется по общему количеству самолётов
* Из списка берутся первый, последний и случайный аэродром"""
import random
import configs
import geometry
import utils
import model


def _compare(left: float, right: float) -> int:
    """Функция сравнения"""
    if left < right:
        return -1
    if left > right:
        return 1
    return 0


class AirfieldsSelector:
    """Класс, отвечающий за выбор аэродромов в зависимости от их состояния"""
    def __init__(self, main: configs.Main):
        self._main = main

    @staticmethod
    def _rear_airfields_comparator(airfield1: model.ManagedAirfield, airfield2: model.ManagedAirfield):
        """Сравнение тыловых аэродромов при выборе"""
        return _compare(airfield1.planes_count, airfield2.planes_count)

    @staticmethod
    def _front_airfields_comparator(airfield1: model.ManagedAirfield, airfield2: model.ManagedAirfield):
        """Сравнение фронтовых аэродромов при выборе"""
        return _compare(airfield1.power, airfield2.power)

    def select_rear(self, influence: list, front_area: list, airfields: list) -> model.ManagedAirfield:
        """Выбрать тыловой аэродром"""
        result = list()
        added = False
        for airfield in airfields:
            if airfield.is_in_area(influence) and not airfield.is_in_area(front_area):
                result.append(airfield)
                added = True
        if added:
            result.sort(key=utils.cmp_to_key(self._rear_airfields_comparator))
            result = result[-3:]
            random.shuffle(result)
            return result.pop()
        else:
            raise NameError('Невозможно выбрать тыловой аэродром')

    def select_front(self, front_area: list, airfields: list) -> list:
        """Выбрать фронтовые аэродромы"""
        if airfields:
            front = list()
            for airfield in airfields:
                if airfield.is_in_area(front_area) or airfield.is_in_vertices_of_area(front_area, 1000):
                    front.append(airfield)
            # d = {x.name: x.to_dict() for x in front}
            if front:
                result = list()
                front.sort(key=utils.cmp_to_key(self._front_airfields_comparator))
                result.append(front.pop())
                front = geometry.remove_too_close(front, result, 15000)
                front.reverse()
                result.append(front.pop())
                distance = 1000000000 / result[0].distance_to(result[1].x, result[1].z) + 10000
                front = geometry.remove_too_close(front, result, distance)
                result.append(random.choice(front))
                return result
            else:
                raise NameError('Невозможно выбрать фронтовые аэродромы')
        else:
            raise ValueError
