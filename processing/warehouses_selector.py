"""Выбор складов для миссии

В миссии у сторон по 2 склада
"""
from __future__ import annotations
import logging
import random

import geometry
import model


class WarehousesSelector:
    """Класс, реализующий выбор"""

    def __init__(self, warehouses: list, current: list):
        self._warehouses = warehouses
        self._current = current

    def _get_max_deaths(self, country: int):
        if self._warehouses:
            return max(x.deaths for x in self._warehouses if x.country == country) + 1
        return 0

    def select(self, tvd: model.Tvd) -> list:
        """Выбрать склады для ТВД"""
        result = self._next_warehouses(101, tvd) + self._next_warehouses(201, tvd)
        param_names = {
            101: ['RWH1', 'RWH2'],
            201: ['BWH1', 'BWH2']
        }
        for warehouse in result:
            warehouse.server_input = param_names[warehouse.country].pop()
        return result

    def _next_warehouses(self, country: int, tvd: model.Tvd) -> list:
        """Склады для следующей миссии для указанной стороны и указанного ТВД"""
        # выбираются те склады, которые убивались меньшее количество раз, текущие склады в приоритете
        airfields = tvd.airfields[country]
        max_deaths = self._get_max_deaths(country)
        warehouses = list(x for x in geometry.remove_too_close(self._warehouses, airfields, 30000)
                          if x.deaths < max_deaths
                          and x.country == country
                          and tvd.is_rear(x, country))
        if not warehouses:
            logging.warning(f'No warehouses selected {country}')
            return list()
        result = list(x for x in self._current
                      if x.deaths < max_deaths
                      and x.country == country
                      and tvd.is_rear(x, country))
        while len(result) < 2:
            random.shuffle(warehouses)
            result.append(warehouses.pop())
        return result
