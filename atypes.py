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

    def __str__(self):
        return f'T:{self.tik} AType:0 GDate:1943.1.1 GTime:9:15:0 MFile:{self.file_path} MID: GType:2 ' \
               f'CNTRS:0:0,101:1,201:2 SETTS:111000000010000100000001110 MODS:0 PRESET:0 AQMID:0'


class Atype1(Atype):
    """Попадание"""

    def __init__(self, tik: int, ammo: str, attacker_id: int, target_id: int):
        super().__init__(tik)
        self.ammo = ammo
        self.attacker_id = attacker_id
        self.target_id = target_id

    def __str__(self):
        return f'T:{self.tik} AType:1 AMMO:{self.ammo} AID:{self.attacker_id} TID:{self.target_id}'


class Atype2(Atype):
    """Повреждение"""

    def __init__(self, tik: int, damage: float, attacker_id: int, target_id: int, pos: dict):
        super().__init__(tik)
        self.damage = damage
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.pos = pos

    def __str__(self):
        return f'T:{self.tik} AType:2 DMG:{self.damage} AID:{self.attacker_id} TID:{self.target_id} POS({self.pos})'


class Atype3(Atype):
    """Kill"""

    def __init__(self, tik: int, attacker_id: int, target_id: int, pos):
        super().__init__(tik)
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.pos = pos

    @property
    def point(self) -> geometry.Point:
        """Координаты события"""
        return geometry.Point(x=self.pos['x'], z=self.pos['z'])

    def __str__(self):
        return f'T:{self.tik} AType:3 AID:{self.attacker_id} TID:{self.target_id} POS({self.pos})'


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

    def __str__(self):
        return f'T:{self.tik} AType:4 PLID:{self.aircraft_id} PID:{self.bot_id} BUL:{self.cartridges} ' \
               f'SH:{self.shells} BOMB:{self.bombs} RCT:{self.rockets} ({self.pos})'


class Atype5(Atype):
    """Взлёт"""

    def __init__(self, tik: int, aircraft_id: int, pos: dict):
        super().__init__(tik)
        self.aircraft_id = aircraft_id
        self.pos = pos

    def __str__(self):
        return f'T:{self.tik} AType:5 PID:{self.aircraft_id} POS({self.pos})'


class Atype6(Atype):
    """Посадка"""

    def __init__(self, tik: int, aircraft_id: int, pos: dict):
        super().__init__(tik)
        self.aircraft_id = aircraft_id
        self.pos = pos

    def __str__(self):
        return f'T:{self.tik} AType:6 PID:{self.aircraft_id} POS({self.pos})'


class Atype7(Atype):
    """Завершение миссии"""

    def __init__(self, tik: int):
        super().__init__(tik)

    def __str__(self):
        return f'T:{self.tik} AType:7'


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

    def __str__(self):
        return f'T:{self.tik} AType:8 OBJID:{self.object_id} POS({self.pos}) COAL:{self.coal_id} ' \
               f'TYPE:{self.task_type_id} RES:{self.success} ICTYPE:{self.icon_type_id}'


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

    def __str__(self):
        return f'T:{self.tik} AType:9 AID:{self.airfield_id} COUNTRY:{self.country_id} POS({self.pos}) IDS()'

# T:10 AType:9 AID:13312 COUNTRY:501 POS(30178.900, 66.126, 25254.000) IDS()
# T:10 AType:9 AID:150527 COUNTRY:201 POS(144322.453, 82.669, 259528.047) IDS(-1,-1,-1)


class Atype10(Atype):
    """Спаун игрока"""

    def __init__(self, tik: int, aircraft_id: int, bot_id: int, account_id: str,
                 profile_id: str, name: str, pos: dict, aircraft_name: str, country_id: int,
                 coal_id: int, airfield_id: int, airstart: bool, parent_id: int,
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
        self.payload_id = 1  # payload_id
        self.fuel = 1  # fuel
        self.skin = ''  # skin
        self.weapon_mods_id = list()  # weapon_mods_id
        self.cartridges = cartridges
        self.shells = shells
        self.bombs = bombs
        self.rockets = rockets
        self.form = form

    @property
    def point(self) -> geometry.Point:
        return geometry.Point(x=self.pos['x'], z=self.pos['z'])

    def __str__(self):
        return f'T:{self.tik} AType:10 PLID:{self.aircraft_id} PID:{self.bot_id} BUL:{self.cartridges} ' \
               f'SH:{self.shells} BOMB:{self.bombs} RCT:{self.rockets} ({self.pos})  IDS:{self.profile_id} ' \
               f'LOGIN:{self.account_id} NAME:{self.name} TYPE:{self.aircraft_name} COUNTRY:{self.country_id} ' \
               f'FORM:{self.form} FIELD:{self.airfield_id} INAIR:{self.airstart} PARENT:{self.parent_id} ' \
               f'PAYLOAD:{self.payload_id} FUEL:{self.fuel} SKIN:{self.skin} WM:{self.weapon_mods_id}'


class Atype11(Atype):
    """Группа"""

    def __init__(self, tik: int, group_id: int, members_id: int, leader_id: int):
        super().__init__(tik)
        self.group_id = group_id
        self.members_id = members_id
        self.leader_id = leader_id

    def __str__(self):
        return f'T:{self.tik} AType:11 GID:{self.group_id} IDS:17407,26623,35839 LID:{self.leader_id}'


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

    def __str__(self):
        return f'T:{self.tik} AType:12 ID:{self.object_id} TYPE:{self.object_name} COUNTRY:{self.country_id} ' \
               f'NAME:{self.name} PID:{self.parent_id}'

# T:53 AType:12 ID:61440 TYPE:bridge_big_1[265,1] COUNTRY:201 NAME:Bridge PID:-1
# T:48738 AType:12 ID:649216 TYPE:static_zis[-1,-1] COUNTRY:101 NAME:Block PID:-1
# T:171760 AType:12 ID:1266700 TYPE:CParachute_1266700 COUNTRY:101 NAME:CParachute_1266700 PID:-1


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

    def __str__(self):
        return f'T:{self.tik} AType:13 AID:{self.area_id} COUNTRY:{self.country_id} ENABLED:{self.enabled} ' \
               f'BC({self.in_air})'


class Atype14(Atype):
    """Influence Area boundary"""

    def __init__(self, tik: int, area_id: int, boundary):
        super().__init__(tik)
        self.area_id = area_id
        self.boundary = boundary

    def __str__(self):
        return f'T:{self.tik} AType:14 AID:{self.area_id} BP((26968.0,74.3,22949.0),(30848.0,74.3,23891.0),' \
               f'(35717.0,74.3,23876.0),(55007.0,74.3,15026.0),(55001.0,74.3,55020.0),(-5018.0,74.3,55042.0),' \
               f'(-4991.0,74.3,34620.0),(2552.0,74.3,34401.0),(8185.0,74.3,29341.0),(17968.0,74.3,26690.0),' \
               f'(21055.0,74.3,27434.0),(22561.0,74.3,24669.0),(25287.6,74.3,24965.3))'


class Atype15(Atype):
    """Версия логов"""

    def __init__(self, tik: int, version):
        super().__init__(tik)
        self.version = version

    def __str__(self):
        return f'T:{self.tik} AType:15 VER:{self.version}'


class Atype16(Atype):
    """Деинициализация бота игрока"""

    def __init__(self, tik: int, bot_id: int, pos: dict):
        super().__init__(tik)
        self.bot_id = bot_id
        self.pos = pos

    @property
    def point(self) -> geometry.Point:
        return geometry.Point(x=self.pos['x'], z=self.pos['z'])

    def __str__(self):
        return f'T:{self.tik} AType:16 BOTID:{self.bot_id} POS({self.pos})'


class Atype17(Atype):
    """Изменение позиции объекта"""

    def __init__(self, tik: int, object_id: int, pos: dict):
        super().__init__(tik)
        self.object_id = object_id
        self.pos = pos

    def __str__(self):
        return f'T:{self.tik} AType:17 ID:{self.object_id} POS({self.pos})'


class Atype18(Atype):
    """Прыжок с парашютом"""

    def __init__(self, tik: int, bot_id: int, parent_id: int, pos: dict):
        super().__init__(tik)
        self.bot_id = bot_id
        self.parent_id = parent_id
        self.pos = pos

    def __str__(self):
        return f'T:{self.tik} AType:18 BOTID:{self.bot_id} PARENTID:{self.parent_id} POS({self.pos})'


class Atype19(Atype):
    """Конец раунда"""

    def __init__(self, tik: int):
        super().__init__(tik)

    def __str__(self):
        return f'T:{self.tik} AType:19'


class Atype20(Atype):
    """Подключение пользователя к серверу"""

    def __init__(self, tik: int, account_id: str, profile_id: str):
        super().__init__(tik)
        self.account_id = account_id
        self.profile_id = profile_id

    def __str__(self):
        return f'T:{self.tik} AType:20 USERID:{self.account_id} USERNICKID:{self.profile_id}'


class Atype21(Atype):
    """Отключение пользователя от сервера"""

    def __init__(self, tik: int, account_id: str, profile_id: str):
        super().__init__(tik)
        self.account_id = account_id
        self.profile_id = profile_id

    def __str__(self):
        return f'T:{self.tik} AType:21 USERID:{self.account_id} USERNICKID:{self.profile_id}'


class Atype22(Atype):
    """Неизвестный атайп"""

    def __init__(self, tik: int):
        super().__init__(tik)
