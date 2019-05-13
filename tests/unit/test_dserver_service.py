"Тестирование сервиса управления RCon"
import unittest

from core import EventsEmitter
from services import DServerService
from tests.mocks import ConfigMock, RConMock
from model import MessagePrivate


class TestDServerService(unittest.TestCase):
    "Тесты"

    def setUp(self):
        "Настройка перед тестом"
        self.emitter = EventsEmitter()
        self.config = ConfigMock()
        self.rcon = RConMock(self.config)

    def test_send_private_message(self):
        "Отправляется приватное сообщение"
        service = DServerService(self.emitter, self.config)
        service._rcon = self.rcon
        service.init()
        # Act
        self.emitter.commands_rcon.on_next(MessagePrivate('test_account_id', 'test_private_message'))
        # Assert
        self.assertIn(('test_private_message', 'test_account_id'), self.rcon.private_messages)
