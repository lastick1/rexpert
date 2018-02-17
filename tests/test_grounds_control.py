"""Тестирование обработки наземки"""
import logging
import pathlib
import unittest

import atypes
import geometry
import model
import processing
import tests

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

IOC = tests.mocks.DependencyContainerMock(pathlib.Path('./testdata/conf.ini'))

TEST_TARGET_AIRFIELD_SERVER_INPUT = 'Verbovka'
TEST_TARGET_BTD1_SERVER_INPUT = 'BTD1'
TEST_TARGET_HP = 3
TEST_TARGET_POS_BTD1 = {'x': 156060.64, 'z': 132392.5}
TEST_TARGET_POS_BTD1_UNITS = [
    {'x': 155453.86, 'z': 130798.2},
    {'x': 156461.58, 'z': 131861.16},
    {'x': 155169.17, 'z': 133163.56},
    {'x': 155055.39, 'z': 132101.14},
    {'x': 155604.38, 'z': 131692.38},
    {'x': 156010.75, 'z': 131154.91},
    {'x': 156484.95, 'z': 133269.22},
    {'x': 156907.78, 'z': 133390.91},
    {'x': 157196.23, 'z': 134433.89},
    {'x': 157767.08, 'z': 132920.91}
]

TEST_MISSION = model.CampaignMission(
    kind='regular',
    file='result1',
    date='01.09.1941',
    tvd_name='moscow-winter',
    additional=dict(),
    server_inputs=[
        {'name': TEST_TARGET_BTD1_SERVER_INPUT, 'pos': TEST_TARGET_POS_BTD1}
    ],
    objectives=[],
    airfields=[],
    units=[
        {'name': 'REXPERT_BTD1_3', 'pos': TEST_TARGET_POS_BTD1_UNITS[0]},
        {'name': 'REXPERT_BTD1_15', 'pos': TEST_TARGET_POS_BTD1_UNITS[1]},
        {'name': 'REXPERT_BTD1_2', 'pos': TEST_TARGET_POS_BTD1_UNITS[2]},
        {'name': 'REXPERT_BTD1_10', 'pos': TEST_TARGET_POS_BTD1_UNITS[3]},
        {'name': 'REXPERT_BTD1_17', 'pos': TEST_TARGET_POS_BTD1_UNITS[4]},
        {'name': 'REXPERT_BTD1_9', 'pos': TEST_TARGET_POS_BTD1_UNITS[5]},
        {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[6]},
        {'name': 'REXPERT_BTD1_8', 'pos': TEST_TARGET_POS_BTD1_UNITS[7]},
        {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[8]},
        {'name': 'REXPERT_BTD1_20', 'pos': TEST_TARGET_POS_BTD1_UNITS[9]}
    ]
)


class TestGroundControl(unittest.TestCase):
    """Тесты контроллера наземки"""

    def setUp(self):
        """Настройка перед тестами"""

    def tearDown(self):
        """Очистка после тестов"""

    def test_kill(self):
        """Учитываются уничтоженные наземные цели"""
        controller = processing.GroundController(IOC)
        target_name = 'static_il2'
        aircraft_name = 'I-16 type 24'
        pos_target = {'x': 300.0, 'y': 100.0, 'z': 100.0}
        attacker = IOC.objects_controller.create_object(
            tests.mocks.atype_12_stub(2, aircraft_name, 201, 'Test attacker', -1)
        )
        target = IOC.objects_controller.create_object(
            tests.mocks.atype_12_stub(3, target_name, 101, 'Test ground target', -1))
        # Act
        IOC.objects_controller.kill(atypes.Atype3(4444, attacker.obj_id, target.obj_id, pos_target))
        controller.kill(atypes.Atype3(123, -1, 3, pos_target))
        # Assert
        self.assertTrue(target.killed)
        self.assertSequenceEqual([geometry.Point(x=pos_target['x'], z=pos_target['z'])], controller.ground_kills)

    def test_kill_aircraft(self):
        """Учитываются только уничтоженные наземные цели"""
        controller = processing.GroundController(IOC)
        aircraft_name = 'I-16 type 24'
        aircraft = IOC.objects_controller.create_object(
            tests.mocks.atype_12_stub(2, aircraft_name, 101, 'Test aircraft', -1))
        pos_aircraft = {'x': 200.0, 'y': 100.0, 'z': 100.0}
        # Act
        controller.kill(atypes.Atype3(123, -1, aircraft.obj_id, pos_aircraft))
        # Assert
        self.assertSequenceEqual([], controller.ground_kills)

    def test_ground_target_kill(self):
        """Обрабатывается уничтожение наземной цели"""
        controller = processing.GroundController(IOC)
        IOC.campaign_controller._mission = TEST_MISSION
        target_name = 'static_il2'
        aircraft_name = 'I-16 type 24'
        attacker = IOC.objects_controller.create_object(
            tests.mocks.atype_12_stub(2, aircraft_name, 201, 'Test attacker', -1))
        target = IOC.objects_controller.create_object(
            tests.mocks.atype_12_stub(3, target_name, 101, 'Test ground target', -1))
        controller.start_mission()
        # Act
        IOC.objects_controller.kill(atypes.Atype3(4444, attacker.obj_id, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        controller.kill(atypes.Atype3(123, -1, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        IOC.objects_controller.kill(atypes.Atype3(4444, attacker.obj_id, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        controller.kill(atypes.Atype3(123, -1, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        IOC.objects_controller.kill(atypes.Atype3(4444, attacker.obj_id, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        controller.kill(atypes.Atype3(123, -1, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        # Assert
        self.assertSequenceEqual([], IOC.console_mock.received_server_inputs)
        IOC.divisions_controller.get_division(TEST_TARGET_BTD1_SERVER_INPUT)

    def test_division_unit_kill(self):
        """Обрабатывается уничтожение подразделения дивизии"""
        controller = processing.GroundController(IOC)
        # Act
        # Assert
        self.fail('not implemented')


if __name__ == '__main__':
    unittest.main(verbosity=2)
