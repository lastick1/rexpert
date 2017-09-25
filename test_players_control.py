"Тестирование событий, связанных с игроками"
import unittest
import datetime
import pathlib
import pymongo
from processing import PlayersController, Player
from processing.player import ID, NICKNAME, KNOWN_NICKNAMES, ONLINE, BAN_DATE, UNLOCKS
from processing.objects import Aircraft, BotPilot, Ground
from configs.objects import Objects
from tests import mocks
from tests import ConsoleMock

MAIN = mocks.MainMock(pathlib.Path(r'.\testdata\conf.ini'))
DB_NAME = 'test_rexpert'
TEST_NICKNAME = '_test_nickname'
TEST_ACCOUNT_ID = '_test_id1'
TEST_PROFILE_ID = '_test_profile_id1'
TEST_PLAYER = Player.create_document(TEST_ACCOUNT_ID)
FILTER = {ID: TEST_ACCOUNT_ID}
OBJECTS = Objects()

class TestPlayersController(unittest.TestCase):
    "Тесты событий с обработкой данных игроков"
    def setUp(self):
        self.mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
        rexpert = self.mongo[DB_NAME]
        self.players = rexpert['Players']
        self.squads = rexpert['Squads']
        self.console_mock = ConsoleMock()
        self.controller = PlayersController(False, self.console_mock, self.players, self.squads)

    def tearDown(self):
        self.console_mock.socket.close()
        self.mongo.drop_database(DB_NAME)
        self.mongo.close()

    def _create(self, _filter: dict, _player: dict):
        self.players.update_one(_filter, {'$set': _player}, upsert=True)

    def test_connect_player_init(self):
        "Инициализируется игрок на первом входе на сервер"
        # Act
        self.controller.connect_player(TEST_ACCOUNT_ID)
        document = self.players.find_one(FILTER)
        # Assert
        self.assertNotEqual(None, document)

    def test_connect_player_check_ban(self):
        "Отправляется команда бана забаненого пользователя через консоль"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.players.update_one(FILTER, update={'$set': {BAN_DATE: date}})
        # Act
        self.controller.connect_player(TEST_ACCOUNT_ID)
        # Assert
        self.assertIn(TEST_ACCOUNT_ID, self.console_mock.banned)

    def test_player_initialization(self):
        "Обновляется ник игрока на спауне"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        # Assert
        player = self.players.find_one(FILTER)
        self.assertEqual(TEST_NICKNAME, player[NICKNAME])

    def test_spawn_player(self):
        "Отправляется приветственное сообщение игроку на спауне"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        # Assert
        self.assertIn(
            (TEST_ACCOUNT_ID, 'Hello {}!'.format(TEST_NICKNAME)),
            self.console_mock.recieved_private_messages)

    def test_multiple_spawn_nickname(self):
        "Не добавляетcя лишний известный ник при неоднократном спауне"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual([], document[KNOWN_NICKNAMES])

    def test_multiple_spawn_new_nick(self):
        "Пополняются известные ники при спауне с новым ником"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        aircraft = Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        # Act
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, 'new_nickname')
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual([TEST_NICKNAME], document[KNOWN_NICKNAMES])

    def test_disconnect_player(self):
        "Ставится статус offline при дисконнекте игрока"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        # Act
        self.controller.disconnect_player(TEST_ACCOUNT_ID)
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual(False, document[ONLINE])

    def test_give_unlock_for_damage(self):
        "Даётся модификация за вылет с уроном"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        damage = 80.0
        aircraft = Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        target = Ground(3, OBJECTS['static_il2'], 101, 1, 'Test target', pos)
        expect = TEST_PLAYER[UNLOCKS] + 1
        # Act
        self.controller.connect_player(TEST_ACCOUNT_ID)
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        aircraft.add_damage(target, damage)
        self.controller.damage(aircraft, damage, target, pos)
        self.controller.bot_deinitialization(bot)
        self.controller.disconnect_player(TEST_ACCOUNT_ID)
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_give_unlock_for_kill(self):
        "Даётся модификация за вылет с килом"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        aircraft = Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        target = Ground(3, OBJECTS['static_il2'], 101, 1, 'Test target', pos)
        expect = TEST_PLAYER[UNLOCKS] + 1
        # Act
        self.controller.connect_player(TEST_ACCOUNT_ID)
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        aircraft.add_kill(target)
        self.controller.kill(aircraft, target, pos)
        self.controller.bot_deinitialization(bot)
        self.controller.disconnect_player(TEST_ACCOUNT_ID)
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_dont_give_for_disco(self):
        "Не даётся модификация за вылет с килом и диско"
        # Arrange
        self._create(FILTER, TEST_PLAYER)
        pos = {'x': 100.0, 'y': 100.0, 'z': 100.0}
        aircraft = Aircraft(1, OBJECTS['I-16 type 24'], 201, 2, 'Test I-16')
        bot = BotPilot(2, OBJECTS['BotPilot'], aircraft, 201, 2, 'Test pilot')
        target = Ground(3, OBJECTS['static_il2'], 101, 1, 'Test target', pos)
        expect = TEST_PLAYER[UNLOCKS]
        # Act
        self.controller.connect_player(TEST_ACCOUNT_ID)
        self.controller.spawn_player(bot, TEST_ACCOUNT_ID, TEST_NICKNAME)
        aircraft.add_kill(target)
        self.controller.kill(aircraft, target, pos)
        self.controller.bot_deinitialization(bot)
        self.controller.disconnect_player(TEST_ACCOUNT_ID)
        # Assert
        document = self.players.find_one(FILTER)
        self.assertEqual(expect, document[UNLOCKS])

    def test_dont_give_for_friendly(self):
        "Не даётся модификация за вылет со стрельбой по своим"
        self.fail("Дописать тест")

if __name__ == '__main__':
    unittest.main(verbosity=2)
