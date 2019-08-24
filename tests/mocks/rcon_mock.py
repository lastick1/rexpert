"Заглушка коннектора консоли DServer"
from configs import Config
from rcon import DServerRcon
from .stubs import pass_


class RConMock(DServerRcon):
    "Заглушка коннектора консоли DServer"
    def __init__(self, config: Config, buffer_size=1024):
        super().__init__(config.main.rcon_ip, config.main.rcon_port, buffer_size=buffer_size)
        self.private_messages = []
        self.connect = pass_
        self.auth = pass_

    def private_message(self, account_id, message):
        self.private_messages.append((account_id, message))
