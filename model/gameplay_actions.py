"""События в игровом процессе"""
import constants
import datetime


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
            constants.GameplayAction.OBJECT_NAME: self.object_name
        }


class DivisionKill(GameplayAction):
    """Уничтожение дивизии"""

    def __init__(self, tik: int, country: int, division_name: str):
        super().__init__(tik, country, self.__class__.__name__, division_name)

    @property
    def division_name(self):
        """Уничтоженная дивизия"""
        return self.object_name


class WarehouseDisable(GameplayAction):
    """Подавление склада (<40%)"""

    def __init__(self, tik: int, country: int, warehouse_name: str):
        super().__init__(tik, country, self.__class__.__name__, warehouse_name)

    @property
    def warehouse_name(self):
        """Подавленный склад"""
        return self.object_name
