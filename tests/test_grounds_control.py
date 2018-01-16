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
        self.controller = processing.GroundController(IOC)

    def test_kill(self):
        """Учитываются уничтоженные наземные цели"""
        pos_target = {'x': 300.0, 'y': 100.0, 'z': 100.0}
        target = log_objects.Ground(3, IOC.objects['static_il2'], 101, 1, 'Test ground target', pos_target)
        # Act
        self.controller.kill(target, atype=atypes.Atype3(123, -1, 3, pos_target))
        # Assert
        self.assertTrue(target.killed)

    def test_kill_aircraft(self):
        """Учитываются только уничтоженные наземные цели"""
        pos_aircraft = {'x': 200.0, 'y': 100.0, 'z': 100.0}
        aircraft = log_objects.Aircraft(2, IOC.objects['I-16 type 24'], 101, 1, 'Test aircraft', pos_aircraft)

        def test_func():
            # Act
            # noinspection PyTypeChecker
            self.controller.kill(aircraft, atype=atypes.Atype3(123, -1, 3, pos_aircraft))
        # Assert
        self.assertRaises(TypeError, test_func)


if __name__ == '__main__':
    unittest.main(verbosity=2)
