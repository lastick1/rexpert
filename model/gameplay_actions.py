"""События в игровом процессе"""
import datetime
import re
import abc
import constants

DIVISION_TYPE_RE = re.compile(r'^[RB](?P<type>.)D\d$')

class GameplayAction:
    """Игровое действие"""

    def __init__(self, tik: int, country: int, kind: str, object_name: str):
        self.date: datetime.datetime = None  # дата кампании, когда возникло событие
        self.tik = tik  # тик в миссии, в котором возникло событие
        self.country = country  # сторона, которая выполнила действие
        self.kind = kind  # тип события
        self.object_name = object_name  # имя объекта, с которым связано событие

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.GameplayAction.DATE: self.date.strftime(constants.DATE_FORMAT),
            constants.GameplayAction.TIK: self.tik,
            constants.GameplayAction.KIND: self.kind,
            constants.GameplayAction.OBJECT_NAME: self.object_name,
            constants.COUNTRY: self.country
        }

    @abc.abstractmethod
    def __str__(self):
        return None


class AirfieldKill(GameplayAction):
    """Уничтожение аэродрома"""

    def __init__(self, tik: int, country: int, airfield_name: str):
        super().__init__(tik, country, self.__class__.__name__, airfield_name)

    @property
    def airfield_name(self):
        """Уничтоженный аэродром"""
        return self.object_name

    def __str__(self):
        return f"{self.airfield_name} airfield destruction"


class DivisionKill(GameplayAction):
    """Уничтожение дивизии"""

    def __init__(self, tik: int, country: int, division_name: str):
        super().__init__(tik, country, self.__class__.__name__, division_name)

    @property
    def division_name(self):
        """Уничтоженная дивизия"""
        return self.object_name

    def __str__(self):
        types = {
            'A': 'artillery',
            'T': 'tanks',
            'I': 'vehicles',
        }
        match = DIVISION_TYPE_RE.match(self.division_name)
        return f'fortified area ({types[match.group(1)]}) destruction'


class ArtilleryKill(GameplayAction):
    """Уничтожение артиллерии"""

    def __init__(self, tik: int, country: int, name: str = 'artillery'):
        super().__init__(tik, country, self.__class__.__name__, name)

    def __str__(self):
        return 'artillery position destruction'


class WarehouseDisable(GameplayAction):
    """Подавление склада (<40%)"""

    def __init__(self, tik: int, country: int, warehouse_name: str):
        super().__init__(tik, country, self.__class__.__name__, warehouse_name)

    @property
    def warehouse_name(self) -> str:
        """Подавленный склад"""
        return self.object_name

    def __str__(self):
        return 'warehouse disable'

class TanksCoverFail(GameplayAction):
    """Уничтожены наступающие танки"""

    def __init__(self, tik: int, country: int, name: str = 'tanks'):
        super().__init__(tik, country, self.__class__.__name__, name)

    def __str__(self):
        return 'lost of attacking tanks'
