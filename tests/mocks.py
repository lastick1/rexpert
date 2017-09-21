"Заглушки, фальшивки и т.п. для тестирования"
import rcon
import db

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
