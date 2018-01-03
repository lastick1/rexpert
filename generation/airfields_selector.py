"""Выбор аэродромов для миссии"""
import random
import configs
import processing
import utils


def _rear_airfields_comparator(airfield1: processing.ManagedAirfield, airfield2: processing.ManagedAirfield):
    """Сравнение тыловых аэродромов при выборе"""
    first_planes = sum(airfield1.planes[name] for name in airfield1.planes)
    second_planes = sum(airfield2.planes[name] for name in airfield2.planes)
    if first_planes < second_planes:
        return -1
    if first_planes > second_planes:
        return 1
    return 0


class AirfieldsSelector:
    """Класс, отвечающий за выбор аэродромов в зависимости от их состояния"""
    def __init__(self, main: configs.Main):
        self._main = main

    @staticmethod
    def calc_power(airfield: processing.ManagedAirfield) -> float:
        """Рассчитать силу аэродрома в зависимости от его состояния"""
        result = airfield.supplies
        for name in airfield.planes:
            result += airfield.planes[name]
        return result

    @staticmethod
    def select_rear(influence: list, front_area: list, airfields: list) -> processing.ManagedAirfield:
        """Выбрать тыловой аэродром"""
        result = list()
        for airfield in airfields:
            if airfield.is_in_area(influence) and not airfield.is_in_area(front_area):
                result.append(airfield)
        result.sort(key=utils.cmp_to_key(_rear_airfields_comparator))
        result = result[-3:]
        random.shuffle(result)
        return result.pop()
