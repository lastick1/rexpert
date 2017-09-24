"Тестирование обработки наземки"
import unittest
from processing.ground_control import GroundController
from processing.objects import Ground, Aircraft
from configs.objects import Objects

OBJECTS = Objects()

class TestGroundControl(unittest.TestCase):
    "Тесты контроллера наземки"
    def setUp(self):
        self.controller = GroundController(OBJECTS)

    def test_count_only_grounds(self):
        "Учитываются только наземные цели"
        # Arrange
        pos_attacker = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        pos_aircraft = {'x': 200.0, 'y': 100.0, 'z': 100.0}
        pos_target = {'x': 300.0, 'y': 100.0, 'z': 100.0}
        attacker = Aircraft(1, OBJECTS['Bf 109 E-7'], 201, 2, 'Test attacker', pos_attacker)
        aircraft = Aircraft(2, OBJECTS['I-16 type 24'], 101, 1, 'Test aircraft', pos_aircraft)
        target = Ground(3, OBJECTS['static_il2'], 101, 1, 'Test ground target', pos_target)
        # Act
        self.controller.damage(attacker, 10.0, target, pos_target)
        self.controller.kill(attacker, target, pos_target)
        self.controller.damage(attacker, 12.0, aircraft, pos_aircraft)
        # Assert
        self.assertIn(target, self.controller.grounds.values())
        self.assertNotIn(aircraft, self.controller.grounds.values())

if __name__ == '__main__':
    unittest.main(verbosity=2)
