"""Выбор аэродромов для миссии"""
import random
import configs
import utils

from processing import ManagedAirfield


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
    def _rear_airfields_comparator(airfield1: ManagedAirfield, airfield2: ManagedAirfield):
        """Сравнение тыловых аэродромов при выборе"""
        return _compare(airfield1.planes_count, airfield2.planes_count)

    @staticmethod
    def _front_airfields_comparator(airfield1: ManagedAirfield, airfield2: ManagedAirfield):
        """Сравнение фронтовых аэродромов при выборе"""
        return _compare(airfield1.power, airfield2.power)

    def select_rear(self, influence: list, front_area: list, airfields: list) -> ManagedAirfield:
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
                if airfield.is_in_area(front_area):
                    front.append(airfield)
            if front:
                result = list()
                front.sort(key=utils.cmp_to_key(self._front_airfields_comparator))
                result.append(front.pop())
                front.reverse()
                result.append(front.pop())
                random.shuffle(front)
                result.append(front.pop())
                return result
            else:
                raise NameError('Невозможно выбрать фронтовые аэродромы')
        else:
            raise ValueError
