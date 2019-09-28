"""Тестирование событий, связанных с игроками"""
import datetime
import logging
import unittest

from core import EventsEmitter, \
    Atype20, \
    Atype21, \
    Spawn, \
    Takeoff, \
    Finish
from configs import Objects
from services import ObjectsService, \
    PlayersService
import constants
from model import Player, PlayerBanP15M, MessagePrivate
from tests.mocks import ConfigMock, \
    EventsInterceptor, \
    StorageMock, \
    PlayersMock, \
    TEST_NICKNAME, \
    TEST_ACCOUNT_ID, \
    TEST_PROFILE_ID, \
    return_zero

CONFIG = ConfigMock()
OBJECTS = Objects()

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)


class TestPlayersController(unittest.TestCase):
    """Тесты событий с обработкой данных игроков"""

    def setUp(self):
        self._storage: StorageMock = StorageMock(CONFIG.main)
        self._emitter: EventsEmitter = EventsEmitter()
        self._objects_service: ObjectsService = ObjectsService(self._emitter, CONFIG, OBJECTS)
        self._objects_service.init()
        self._interceptor: EventsInterceptor = EventsInterceptor(self._emitter)
        self._player_dict = Player.initialize(TEST_ACCOUNT_ID)
        self._player = Player(TEST_ACCOUNT_ID, self._player_dict)

        self.update_calls = []
        self.reset_mods_for_all_calls = []
        self.players_mock.update = self._update
        self.players_mock.find = self._find
        self.players_mock.reset_mods_for_all = self._reset_mods_for_all

    @property
    def players_mock(self) -> PlayersMock:
        "Мок коллекции игроков"
        return self._storage.players

    def _update(self, player: Player) -> None:
        self.update_calls.append(player)

    def _find(self, account_id) -> Player:
        return Player(account_id, self._player_dict)

    def _reset_mods_for_all(self, unlocks: int) -> None:
        self.reset_mods_for_all_calls.append(unlocks)

    def _init_new_service_instance(self) -> PlayersService:
        controller = PlayersService(
            self._emitter,
            CONFIG,
            self._storage,
            self._objects_service
        )
        controller.init()
        return controller

    def test_connect_player(self):
        """Отправляется приветственное сообщение игроку на подключении"""
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        self._init_new_service_instance()
        # Act
        self._emitter.events_player_connected.on_next(Atype20(150, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertTrue(self._interceptor.commands)
        command: MessagePrivate = self._interceptor.commands[0]
        self.assertTupleEqual((TEST_ACCOUNT_ID, 'Hello {}!'.format(TEST_NICKNAME)),
                              (command.account_id, command.message))

    def test_connect_player_check_ban(self):
        """Отправляется команда бана заблокированного пользователя через консоль"""
        self._init_new_service_instance()
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self._player_dict[constants.Player.BAN_DATE] = date
        # Act
        self._emitter.events_player_connected.on_next(Atype20(150, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertTrue(self._interceptor.commands)
        command: PlayerBanP15M = self._interceptor.commands[0]
        self.assertEqual(TEST_ACCOUNT_ID, command.account_id)

    def test_connect_player_init(self):
        """Инициализируется игрок на первом входе на сервер"""
        self.players_mock.count = return_zero
        self._init_new_service_instance()
        # Act
        self._emitter.events_player_connected.on_next(Atype20(150, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertNotEqual(len(self.update_calls), 0)

    def test_disconnect_player(self):
        """Ставится статус offline при выходе игрока с сервера"""
        self._init_new_service_instance()
        # Act
        self._emitter.events_player_disconnected.on_next(Atype21(1500, TEST_ACCOUNT_ID, TEST_PROFILE_ID))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertEqual(False, self.update_calls[0].online)

    def test_do_not_give_unlock_for_not_success(self):
        """Не даётся модификация за провальный вылет"""
        self._init_new_service_instance()
        # Act
        self._emitter.sortie_deinitialize.on_next(Finish(1, True, False, None, None))
        # Assert
        self.assertFalse(self.update_calls)

    def test_msg_restricted_takeoff(self):
        """Отправляется предупреждение о запрете взлёта"""
        self._player_dict[constants.Player.UNLOCKS] = 0
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        self._init_new_service_instance()
        # Act
        self._emitter.sortie_spawn.on_next(Spawn(TEST_ACCOUNT_ID, TEST_NICKNAME, 1, None, None))
        # Assert
        self.assertTrue(self._interceptor.commands)
        self.assertEqual(
            self._interceptor.commands[0].message,
            f'{TEST_NICKNAME} TAKEOFF is FORBIDDEN FOR YOU on this aircraft. Available modifications 0')

    def test_msg_granted_takeoff(self):
        """Отправляется разрешение на взлёт"""
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        self._init_new_service_instance()
        # Act
        self._emitter.sortie_spawn.on_next(Spawn(TEST_ACCOUNT_ID, TEST_NICKNAME, 1, None, None))
        # Assert
        self.assertTrue(self._interceptor.commands)
        self.assertEqual(
            self._interceptor.commands[0].message,
            f'{TEST_NICKNAME} takeoff granted! Available modifications 1')

    def test_kick_restricted_takeoff(self):
        """Отправляется команда кика при запрещённом взлёте"""
        self._player_dict[constants.Player.UNLOCKS] = 0
        self._init_new_service_instance()
        # Act
        self._emitter.sortie_spawn.on_next(Spawn(TEST_ACCOUNT_ID, TEST_NICKNAME, 1, None, None))
        self._emitter.sortie_takeoff.on_next(Takeoff(TEST_ACCOUNT_ID, 1))
        # Assert
        # приветствие + предупреждение
        self.assertTrue(self._interceptor.commands)
        welcome: MessagePrivate = self._interceptor.commands[0]
        warning: MessagePrivate = self._interceptor.commands[1]
        self.assertEqual(TEST_ACCOUNT_ID, welcome.account_id)
        self.assertEqual(TEST_ACCOUNT_ID, warning.account_id)

    def test_multiple_spawn_new_nick(self):
        """Пополняются известные ники при появлении с новым ником"""
        new_nickname = 'new_nickname'
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        self._init_new_service_instance()
        # Act
        self._emitter.sortie_spawn.on_next(Spawn(TEST_ACCOUNT_ID, new_nickname, 0, None, None))
        # Assert
        self.assertListEqual(self.update_calls[0].previous_nicknames, [TEST_NICKNAME])

    def test_multiple_spawn_nickname(self):
        """Не добавляется лишний известный ник при неоднократном появлении"""
        self._player_dict[constants.Player.NICKNAME] = TEST_NICKNAME
        self._init_new_service_instance()
        # Act
        self._emitter.sortie_spawn.on_next(Spawn(TEST_ACCOUNT_ID, TEST_NICKNAME, 0, None, None))
        # Assert
        self.assertTrue(self.update_calls)
        self.assertFalse(self.update_calls[0].previous_nicknames)

    def test_player_initialization(self):
        """Обновляется ник игрока на появлении"""
        self._init_new_service_instance()
        # Act
        self._emitter.sortie_spawn.on_next(Spawn(TEST_ACCOUNT_ID, TEST_NICKNAME, 0, None, None))
        # Assert
        self.assertTrue(self.update_calls)

    def test_reset(self):
        """Сбрасывается состояние игроков в кампании"""
        self._player_dict[constants.Player.UNLOCKS] = 4
        controller = self._init_new_service_instance()
        # Act
        controller.reset()
        # Assert
        self.assertTrue(self.reset_mods_for_all_calls)


if __name__ == '__main__':
    unittest.main(verbosity=2)
