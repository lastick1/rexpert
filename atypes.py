"""Классы атайпов логов"""
import datetime

import geometry


class Atype:
    """Базовый класс всех атайпов"""

    def __init__(self, tik: int):
        self.tik = tik


class Atype0(Atype):
    """Старт миссии"""

    def __init__(self, tik: int, date: datetime.datetime, file_path: str,
                 game_type_id, countries: dict, settings, mods, preset_id):
        super().__init__(tik)
        self.date = date
        self.file_path = file_path
        self.game_type_id = game_type_id
        self.countries = countries
        self.settings = settings
        self.mods = mods
        self.preset_id = preset_id


class Atype1(Atype):
    """Попадание"""

    def __init__(self, tik: int, ammo: str, attacker_id: int, target_id: int):
        super().__init__(tik)
        self.ammo = ammo
        self.attacker_id = attacker_id
        self.target_id = target_id


class Atype2(Atype):
    """Повреждение"""

    def __init__(self, tik: int, damage: float, attacker_id: int, target_id: int, pos: dict):
        super().__init__(tik)
        self.damage = damage
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.pos = pos


class Atype3(Atype):
    """Kill"""

    def __init__(self, tik: int, attacker_id: int, target_id: int, pos):
        super().__init__(tik)
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.pos = pos


class Atype4(Atype):
    """Завершение вылета"""

    def __init__(self, tik: int, aircraft_id: int, bot_id: int, cartridges: int,
                 shells: int, bombs: int, rockets: int, pos: dict):
        super().__init__(tik)
        self.aircraft_id = aircraft_id
        self.bot_id = bot_id
        self.cartridges = cartridges
        self.shells = shells
        self.bombs = bombs
        self.rockets = rockets
        self.pos = pos


class Atype5(Atype):
    """Взлёт"""

    def __init__(self, tik: int, aircraft_id: int, pos: dict):
        super().__init__(tik)
        self.aircraft_id = aircraft_id
        self.pos = pos


class Atype6(Atype):
    """Посадка"""

    def __init__(self, tik: int, aircraft_id: int, pos: dict):
        super().__init__(tik)
        self.aircraft_id = aircraft_id
        self.pos = pos


class Atype7(Atype):
    """Завершение миссии"""

    def __init__(self, tik: int):
        super().__init__(tik)


class Atype8(Atype):
    """Mission Objective"""

    def __init__(self, tik: int, object_id: int, coal_id: int, task_type_id: int,
                 success: int, icon_type_id: int, pos: dict):
        super().__init__(tik)
        self.object_id = object_id
        self.coal_id = coal_id
        self.task_type_id = task_type_id
        self.success = success
        self.icon_type_id = icon_type_id
        self.pos = pos


class Atype9(Atype):
    """Аэродром"""

    def __init__(self, tik: int, airfield_id: int, country_id: int, coal_id: int,
                 aircraft_id_list: list, pos: dict):
        super().__init__(tik)
        self.airfield_id = airfield_id
        self.country_id = country_id
        self.coal_id = coal_id
        self.aircraft_id_list = aircraft_id_list
        self.pos = pos

    @property
    def point(self) -> geometry.Point:
        return geometry.Point(x=self.pos['x'], z=self.pos['z'])


class Atype10(Atype):
    """Спаун игрока"""

    def __init__(self, tik: int, aircraft_id: int, bot_id: int, account_id: str,
                 profile_id: str, name: str, pos: dict, aircraft_name: str, country_id: int,
                 coal_id: int, airfield_id: int, airstart: bool, parent_id: int,
                 payload_id: int, fuel: float, skin: str, weapon_mods_id: list,
                 cartridges: int, shells: int, bombs: int, rockets: int, form: str):
        super().__init__(tik)
        self.aircraft_id = aircraft_id
        self.bot_id = bot_id
        self.account_id = account_id
        self.profile_id = profile_id
        self.name = name
        self.pos = pos
        self.aircraft_name = aircraft_name
        self.country_id = country_id
        self.coal_id = coal_id
        self.airfield_id = airfield_id
        self.airstart = airstart
        self.parent_id = parent_id
        self.payload_id = payload_id
        self.fuel = fuel
        self.skin = skin
        self.weapon_mods_id = weapon_mods_id
        self.cartridges = cartridges
        self.shells = shells
        self.bombs = bombs
        self.rockets = rockets
        self.form = form

    @property
    def point(self) -> geometry.Point:
        return geometry.Point(x=self.pos['x'], z=self.pos['z'])


class Atype11(Atype):
    """Группа"""

    def __init__(self, tik: int, group_id: int, members_id: int, leader_id: int):
        super().__init__(tik)
        self.group_id = group_id
        self.members_id = members_id
        self.leader_id = leader_id


class Atype12(Atype):
    """Инициализация игрового объекта"""

    def __init__(self, tik: int, object_id: int, object_name: str, country_id: int,
                 coal_id: int, name: str, parent_id: int):
        super().__init__(tik)
        self.object_id = object_id
        self.object_name = object_name
        self.country_id = country_id
        self.coal_id = coal_id
        self.name = name
        self.parent_id = parent_id


class Atype13(Atype):
    """Influence Area"""

    def __init__(self, tik: int, area_id: int, country_id: int, coal_id: int,
                 enabled: bool, in_air: bool):
        super().__init__(tik)
        self.area_id = area_id
        self.country_id = country_id
        self.coal_id = coal_id
        self.enabled = enabled
        self.in_air = in_air


class Atype14(Atype):
    """Influence Area boundary"""

    def __init__(self, tik: int, area_id: int, boundary):
        super().__init__(tik)
        self.area_id = area_id
        self.boundary = boundary


class Atype15(Atype):
    """Версия логов"""

    def __init__(self, tik: int, version):
        super().__init__(tik)
        self.version = version


class Atype16(Atype):
    """Деинициализация бота игрока"""

    def __init__(self, tik: int, bot_id: int, pos: dict):
        super().__init__(tik)
        self.bot_id = bot_id
        self.pos = pos

    @property
    def point(self) -> geometry.Point:
        return geometry.Point(x=self.pos['x'], z=self.pos['z'])


class Atype17(Atype):
    """Изменение позиции объекта"""

    def __init__(self, tik: int, object_id: int, pos: dict):
        super().__init__(tik)
        self.object_id = object_id
        self.pos = pos


class Atype18(Atype):
    """Прыжок с парашютом"""

    def __init__(self, tik: int, bot_id: int, parent_id: int, pos: dict):
        super().__init__(tik)
        self.bot_id = bot_id
        self.parent_id = parent_id
        self.pos = pos


class Atype19(Atype):
    """Конец раунда"""

    def __init__(self, tik: int):
        super().__init__(tik)


class Atype20(Atype):
    """Подключение пользователя к серверу"""

    def __init__(self, tik: int, account_id: str, profile_id: str):
        super().__init__(tik)
        self.account_id = account_id
        self.profile_id = profile_id


class Atype21(Atype):
    """Отключение пользователя от сервера"""

    def __init__(self, tik: int, account_id: str, profile_id: str):
        super().__init__(tik)
        self.account_id = account_id
        self.profile_id = profile_id


class Atype22(Atype):
    """Неизвестный атайп"""

    def __init__(self, tik: int):
        super().__init__(tik)
