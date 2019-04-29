"Тесты на сервис управления объектами из логов"
from __future__ import annotations

import unittest
import pathlib

from configs import Config, Objects
from core import EventsEmitter
from services import ObjectsService

from tests import mocks


class TestObjectsService(unittest.TestCase):
    "Тесты на сервис управления объектами из логов"

    def setUp(self):
        self.emitter = EventsEmitter()

    def tearDown(self):
        self.emitter.dispose()

    def test_creates_objects(self):
        "Создаются объекты, обнаруженные в логах до завершения раунда"
        service = ObjectsService(self.emitter, Config(
            pathlib.Path('./testdata/main.json')), Objects())
        # Act
        service.init()
        with open(mocks.TEST_LOG7) as stream:
            lines = stream.readlines()
            for line in lines:
                if 'AType:7' not in line:
                    self.emitter.process_line(line)
        self.assertEqual(len(service.get_all()), 29)

    def test_cleans_objects_after_mission_end(self):
        "Удаляются объекты, созданные до завершения раунда"
        service = ObjectsService(self.emitter, Config(
            pathlib.Path('./testdata/main.json')), Objects())
        # Act
        service.init()
        with open(mocks.TEST_LOG7) as stream:
            lines = stream.readlines()
            for line in lines:
                self.emitter.process_line(line)
        self.assertEqual(len(service.get_all()), 0)


if __name__ == '__main__':
    unittest.main()
