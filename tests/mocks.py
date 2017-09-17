"Заглушки, фальшивки и т.п. для тестирования"
import rcon

class CommanderMock(rcon.Commander):
    "Заглушка коммандера"
    def __init__(self):
        super().__init__(None)
