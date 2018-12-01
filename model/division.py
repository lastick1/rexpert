"""Модель данных дивизии"""
import constants
import geometry

DIVISIONS = {
    'BTD1': 12,
    'RTD1': 12,
    'BAD1': 12,
    'RAD1': 12,
    'BID1': 12,
    'RID1': 12
}
RED_NAMES = tuple(x for x in DIVISIONS if 'R' in x)
BLUE_NAMES = tuple(x for x in DIVISIONS if 'B' in x)
TANK_NAMES = tuple(x for x in DIVISIONS if 'T' in x)
ARTY_NAMES = tuple(x for x in DIVISIONS if 'A' in x)
INF_NAMES = tuple(x for x in DIVISIONS if 'I' in x)


class Division:
    """Войсковая дивизия"""
    def __init__(self, tvd_name: str, name: str, units: float, pos: dict):
        self.units = units
        self.name = name
        self.tvd_name = tvd_name
        self.pos = pos

    @property
    def point(self) -> geometry.Point:
        """Точка аэродрома"""
        return geometry.Point(x=self.pos['x'], z=self.pos['z'])

    @property
    def country(self) -> int:
        """Страна дивизии"""
        for name in RED_NAMES:
            if name in self.name:
                return 101
        for name in BLUE_NAMES:
            if name in self.name:
                return 201
        raise NameError('Некорректное имя дивизии')

    @property
    def type_of_army(self) -> str:
        """Тип дивизии - танковая, артиллерийская, общая"""
        for name in TANK_NAMES:
            if name in self.name:
                return 'tank'
        for name in ARTY_NAMES:
            if name in self.name:
                return 'artillery'
        for name in INF_NAMES:
            if name in self.name:
                return 'infantry'
        raise NameError('Некорректное имя дивизии')

    def to_dict(self) -> dict:
        """Сериализация в словарь для MongoDB"""
        return {
            constants.ID: '{}_{}'.format(self.tvd_name, self.name),
            constants.Division.UNITS: self.units,
            constants.TVD_NAME: self.tvd_name,
            constants.POS: self.pos
        }
