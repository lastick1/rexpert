"""Тестирование обработки наземных целей"""
from __future__ import annotations
import logging
import unittest

from configs import Objects
from core import EventsEmitter, Atype3
from geometry import Point
from services import GroundTargetsService, ObjectsService
from model import CampaignMission

from tests.mocks import EventsInterceptor, \
    ConfigMock, \
    atype_12_stub

CONFIG = ConfigMock()

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)


TEST_DATE = '01.09.1941'
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

TEST_MISSION = CampaignMission(
    file='result1',
    date=TEST_DATE,
    tvd_name='moscow',
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
    ],
    actions=list()
)


class TestGroundControl(unittest.TestCase):
    """Тесты контроллера наземных целей"""

    def setUp(self):
        """Настройка перед тестами"""
        self._events_emitter = EventsEmitter()
        self._interceptor = EventsInterceptor(self._events_emitter)
        self._interceptor.init()
        self._objects_service = ObjectsService(
            self._events_emitter, CONFIG, Objects())

    def tearDown(self):
        """Очистка после тестов"""
        self._interceptor.dispose()

    def test_kill(self):
        """Учитываются уничтоженные наземные цели"""
        service = GroundTargetsService(self._events_emitter,
                                       CONFIG,
                                       self._objects_service)
        target_name = 'static_il2'
        aircraft_name = 'I-16 type 24'
        pos_target = {'x': 300.0, 'y': 100.0, 'z': 100.0}
        attacker = self._objects_service._create_object(
            atype_12_stub(2, aircraft_name, 201, 'Test attacker', -1)
        )
        target = self._objects_service._create_object(
            atype_12_stub(3, target_name, 101, 'Test ground target', -1))
        # Act
        self._objects_service._kill(
            Atype3(4444, attacker.obj_id, target.obj_id, pos_target))
        service._kill(Atype3(123, -1, 3, pos_target))
        # Assert
        self.assertTrue(target.killed)
        self.assertSequenceEqual(
            [Point(x=pos_target['x'], z=pos_target['z'])], service.ground_kills)

    def test_kill_aircraft(self):
        """Учитываются только уничтоженные наземные цели"""
        service = GroundTargetsService(self._events_emitter,
                                       CONFIG,
                                       self._objects_service)
        aircraft_name = 'I-16 type 24'
        aircraft = self._objects_service._create_object(
            atype_12_stub(2, aircraft_name, 101, 'Test aircraft', -1))
        pos_aircraft = {'x': 200.0, 'y': 100.0, 'z': 100.0}
        # Act
        service._kill(Atype3(123, -1, aircraft.obj_id, pos_aircraft))
        # Assert
        self.assertSequenceEqual([], service.ground_kills)

    def test_division_unit_kill(self):
        """Обрабатывается уничтожение подразделения дивизии"""
        service = GroundTargetsService(self._events_emitter,
                                       CONFIG,
                                       self._objects_service)
        service.init()
        self._events_emitter.campaign_mission.on_next(TEST_MISSION)
        target_name = 'static_il2'
        aircraft_name = 'I-16 type 24'
        attacker = self._objects_service._create_object(
            atype_12_stub(2, aircraft_name, 201, 'Test attacker', -1))
        target = self._objects_service._create_object(
            atype_12_stub(3, target_name, 101, 'Test ground target', -1))
        service._mission_start(None)
        # Act
        self._objects_service._kill(
            Atype3(4444, attacker.obj_id, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        service._kill(Atype3(123, -1, target.obj_id,
                             TEST_TARGET_POS_BTD1_UNITS[0]))
        self._objects_service._kill(
            Atype3(4444, attacker.obj_id, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        service._kill(Atype3(123, -1, target.obj_id,
                             TEST_TARGET_POS_BTD1_UNITS[0]))
        self._objects_service._kill(
            Atype3(4444, attacker.obj_id, target.obj_id, TEST_TARGET_POS_BTD1_UNITS[0]))
        service._kill(Atype3(123, -1, target.obj_id,
                             TEST_TARGET_POS_BTD1_UNITS[0]))
        # Assert
        self.assertTrue(self._interceptor.division_damages)

    @unittest.skip('Перенести тест в сервис управления дивизиями')
    def test_division_kill(self):
        """Обрабатывается уничтожение дивизии"""
        service = GroundTargetsService(self._events_emitter,
                                       CONFIG,
                                       self._objects_service)
        service.init()
        self._events_emitter.campaign_mission.on_next(TEST_MISSION)
        target_name = 'static_il2'
        aircraft_name = 'I-16 type 24'
        attacker = self._objects_service._create_object(
            atype_12_stub(2, aircraft_name, 201, 'Test attacker', -1))
        target = self._objects_service._create_object(
            atype_12_stub(3, target_name, 101, 'Test ground target', -1))
        service._mission_start(None)
        # Act
        for pos in TEST_TARGET_POS_BTD1_UNITS:
            for i in range(20):
                self._objects_service._kill(
                    Atype3(4444, attacker.obj_id, target.obj_id, pos))
                service._kill(Atype3(123, -1, target.obj_id, pos))
        # Assert
        self.assertTrue(self._interceptor.division_kills)


if __name__ == '__main__':
    unittest.main(verbosity=2)