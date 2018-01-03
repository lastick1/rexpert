"""Тестирование выбора аэродромов на миссию"""
import unittest
import pathlib
import generation
from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'./testdata/conf.ini'))


class TestAirfieldsSelector(unittest.TestCase):
    """Тестовый класс"""
    def test_calc_airfield_priority(self):
        """Рассчитывается показатель приоритета аэродрома"""
        selector = generation.AirfieldsSelector(MAIN)
        # Act
        # Assert
