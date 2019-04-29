"""Файл с тестами чтения событий из логах"""
from __future__ import annotations
from typing import List

import unittest


from core import EventsEmitter

TEST_ATYPE_0_LINE = r'T:0 AType:0 GDate:1941.11.10 GTime:9:55:21 MFile:Multiplayer/Dogfight\result2.msnbin MID: ' + \
    r'GType:2 CNTRS:0:0,101:1,201:2 SETTS:111000000010000100000001110 MODS:0 PRESET:0 AQMID:0'
TEST_ATYPE_1_LINE = r'T:31329 AType:1 AMMO:NPC_BULLET_GER_7-92 AID:338944 TID:628737'


class TestEventsEmitter(unittest.TestCase):
    """Тесты на Rx-based парсер логов"""

    def setUp(self):
        self.emitter = EventsEmitter()

    def tearDown(self):
        self.emitter.dispose()

    def test_process_line(self):
        """Обрабатываются строчки лога"""
        processed: List = list()
        self.emitter.events_mission_start.subscribe_(processed.append)
        # Act
        self.emitter.process_line(TEST_ATYPE_0_LINE)
        self.emitter.process_line(TEST_ATYPE_1_LINE)
        # Assert
        self.assertEqual(len(processed), 1)

    def test_rx_subject(self):
        """Подписчики не получают данные от Subject, возникшие до подписки"""
        processed: List = list()
        # Act
        self.emitter.process_line(TEST_ATYPE_0_LINE)
        self.emitter.events_mission_start.subscribe_(processed.append)
        self.emitter.process_line(TEST_ATYPE_0_LINE)
        # Assert
        self.assertEqual(len(processed), 1)


if __name__ == '__main__':
    unittest.main()
