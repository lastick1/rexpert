"""Выбор аэродромов для миссии"""
import random
import configs
import processing
import utils


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
    def _rear_airfields_comparator(airfield1: processing.ManagedAirfield, airfield2: processing.ManagedAirfield):
        """Сравнение тыловых аэродромов при выборе"""
        first_planes = sum(airfield1.planes[name] for name in airfield1.planes)
        second_planes = sum(airfield2.planes[name] for name in airfield2.planes)
        return _compare(first_planes, second_planes)

    def _front_airfields_comparator(self, airfield1: processing.ManagedAirfield, airfield2: processing.ManagedAirfield):
        """Сравнение фронтовых аэродромов при выборе"""
        return _compare(self.calc_power(airfield1), self.calc_power(airfield2))

    @staticmethod
    def calc_power(airfield: processing.ManagedAirfield) -> float:
        """Рассчитать силу аэродрома в зависимости от его состояния"""
        result = airfield.supplies
        for name in airfield.planes:
            result += airfield.planes[name]
        return result

    def select_rear(self, influence: list, front_area: list, airfields: list) -> processing.ManagedAirfield:
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
