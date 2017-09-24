"Заглушки, фальшивки и т.п. для тестирования"
# pylint: disable=all
import pathlib
import rcon
import configs
import generation

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
        self.recieved_private_messages = []
        self.banned = []

    def private_message(self, account_id: str, message: str):
        self.recieved_private_messages.append((account_id, message))

    def banuser(self, name):
        self.banned.append(name)

class GeneratorMock(generation.Generator):
    "Заглушка генератора миссий"
    def __init__(self, main: MainMock, mgen: MgenMock):
        super().__init__(main, mgen)
        self.generations = []

    def make_mission(self, file_name: str, tvd_name: str):
        self.generations.append((file_name, tvd_name))
