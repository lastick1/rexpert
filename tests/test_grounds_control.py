"""Тестирование обработки наземки"""
import unittest
import pathlib

import atypes
import log_objects
import processing
import tests

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))


class TestGroundControl(unittest.TestCase):
    """Тесты контроллера наземки"""
    def setUp(self):
        """Настройка перед тестами"""

    def tearDown(self):
        """Очистка после тестов"""

    def test_kill(self):
        """Учитываются уничтоженные наземные цели"""
        controller = processing.GroundController(IOC)
        pos_target = {'x': 300.0, 'y': 100.0, 'z': 100.0}
        target = log_objects.Ground(3, IOC.objects['static_il2'], 101, 1, 'Test ground target', pos_target)
        # Act
        controller.kill(atypes.Atype3(123, -1, 3, pos_target))
        # Assert
        self.assertTrue(target.killed)

    def test_kill_aircraft(self):
        """Учитываются только уничтоженные наземные цели"""
        controller = processing.GroundController(IOC)
        aircraft_name = 'I-16 type 24'
        aircraft = IOC.objects_controller.create_object(
            tests.mocks.atype_12_stub(2, aircraft_name, 101, 'Test aircraft', -1))
        pos_aircraft = {'x': 200.0, 'y': 100.0, 'z': 100.0}

        def test_func():
            # Act
            controller.kill(atypes.Atype3(123, -1, 3, pos_aircraft))
        # Assert
        self.assertRaises(TypeError, test_func)

    def test_ground_target_kill(self):
        """Обрабатывается уничтожение наземной цели"""
        self.fail('not implemented')


if __name__ == '__main__':
    unittest.main(verbosity=2)
