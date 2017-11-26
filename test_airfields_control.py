"""Тестирование управления аэродромами"""
import unittest
from processing import AirfieldsController


class TestAirfieldsController(unittest.TestCase):
    """Тестовый класс контроллера"""
    def test_get_airfield_by_coords(self):
        """Определяется аэродром по координатам"""
        controller = AirfieldsController()
        result = controller.get_airfield_by_coords(x=20115, z=14146, radius=1000)
        self.assertEqual(result.name, 'bolshoe vergovo')


if __name__ == '__main__':
    unittest.main(verbosity=2)
