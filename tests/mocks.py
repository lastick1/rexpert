"Заглушки, фальшивки и т.п. для тестирования"
import pathlib
import rcon
import db
import gen
import configs

class MainMock(configs.Main):
    "Заглушка конфига"
    def __init__(self, path: pathlib.Path):
        super().__init__(path=path)

class MgenMock(configs.Mgen):
    "Заглушка конфига генерации миссий"
    pass

class ConsoleMock(rcon.DServerRcon):
    "Заглушка коммандера"
    def __init__(self):
        super().__init__('127.0.0.1', '8991')
        self.recieved_private_messages = 0

    def private_message(self, account_id: str, message: str):
        self.recieved_private_messages += 1

class PGConnectorMock(db.PGConnector):
    "Заглушка коннектора к postgresql"
    @staticmethod
    def get_objects_dict():
        return {}

class GeneratorMock(gen.Generator):
    "Заглушка генератора миссий"
    @staticmethod
    def make_mission(file_name: str, tvd_name: str, main: configs.Main, mgen: configs.Mgen):
        pass
