"""Тесты сборки аэродромов"""
import unittest
import generation


class TestAirfield(unittest.TestCase):
    """Тестирование форматирования MCU аэродрома"""
    def test_airfield_ctor(self):
        """Создаётся класс MCU аэродрома"""
        airfield = generation.Airfield(0, 0, 0, [], 0)
        self.fail()



class TestAirfieldsBuilder(unittest.TestCase):
    """Тестирование сборщика аэродромов"""


if __name__ == '__main__':
    unittest.main(verbosity=2)
