"""Сборка базы локаций"""
import re
from .locations import Location, AIR_OBJECTIVE, AIRFIELD, DECORATION, GROUND_OBJECTIVE, REFERENCE_LOCATION
from .locations import RECON_FLIGHT, BOMBER_FLIGHT, FIGHTER_PATROL_FLIGHT, DUEL_OPPONENT, ARMOURED, BUILDING
from .locations import RAILWAY_STATION, SUPPLY_DUMP, FACTORY, PORT, RECON_AREA, DOGFIGHT, TRANSPORT, TRAIN, TANK
from .locations import ARTILLERY, AAA_POSITION, SHIP, BALLOON, WINDSOCK, CITY_FIRE, SPOTTER, BRIDGE, AT_ART_POSITION
from .locations import FIRING_POINT, SIREN, PARKING, HW_ARTILLERY, AT_ARTILLERY, RL_FIRING_POINT, RL_FRONT_LINE

airfields_raw_re = re.compile(
    '\nAirfield\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
decorations_raw_re = re.compile(
    '\nDecoration\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
ground_objective_raw_re = re.compile(
    '\nGroundObjective\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
air_objective_raw_re = re.compile(
    '\nAirObjective\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
reference_location_raw_re = re.compile(
    '\nReferenceLocation\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)


def _parse_location(_list: list) -> Location:
    """Считать основную информацию о локации"""
    xpos = float(_list[2].partition('= ')[-1])
    ypos = float(_list[3].partition('= ')[-1])
    zpos = float(_list[4].partition('= ')[-1])
    oy = float(_list[5].partition('= ')[-1])
    length = float(_list[6].partition('= ')[-1])
    width = float(_list[7].partition('= ')[-1])
    return Location(name=DECORATION, x=xpos, z=zpos, y=ypos, oy=oy, length=length, width=width)


def parse_air_objective(text: str) -> Location:
    """Считать AirObjective локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(_list=tmp)
    if int(tmp[-7].partition('= ')[-1]):
        result.types.add(RECON_FLIGHT)
    if int(tmp[-6].partition('= ')[-1]):
        result.types.add(BOMBER_FLIGHT)
    if int(tmp[-5].partition('= ')[-1]):
        result.types.add(FIGHTER_PATROL_FLIGHT)
    if int(tmp[-4].partition('= ')[-1]):
        result.types.add(DOGFIGHT)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(DUEL_OPPONENT)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(BALLOON)
    return result


def parse_airfield(text: str) -> Location:
    """Считать Airfield локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(_list=tmp)
    return result


def parse_ground_objective(text: str) -> Location:
    """Считать GroundObjective локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(_list=tmp)
    if int(tmp[-15].partition('= ')[-1]):
        result.types.add(TRANSPORT)
    if int(tmp[-14].partition('= ')[-1]):
        result.types.add(ARMOURED)
    if int(tmp[-13].partition('= ')[-1]):
        result.types.add(TANK)
    if int(tmp[-12].partition('= ')[-1]):
        result.types.add(AAA_POSITION)
    if int(tmp[-11].partition('= ')[-1]):
        result.types.add(ARTILLERY)
    if int(tmp[-10].partition('= ')[-1]):
        result.types.add(BUILDING)
    if int(tmp[-9].partition('= ')[-1]):
        result.types.add(SHIP)
    if int(tmp[-8].partition('= ')[-1]):
        result.types.add(TRAIN)
    if int(tmp[-7].partition('= ')[-1]):
        result.types.add(RAILWAY_STATION)
    if int(tmp[-6].partition('= ')[-1]):
        result.types.add(SUPPLY_DUMP)
    if int(tmp[-5].partition('= ')[-1]):
        result.types.add(FACTORY)
    if int(tmp[-4].partition('= ')[-1]):
        result.types.add(AIRFIELD)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(PORT)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(RECON_AREA)
    return result


def parse_decoration(text: str) -> Location:
    """Считать Decoration локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(_list=tmp)
    if int(tmp[-17].partition('= ')[-1]):
        result.types.add(DOGFIGHT)
    if int(tmp[-16].partition('= ')[-1]):
        result.types.add(TRANSPORT)
    if int(tmp[-15].partition('= ')[-1]):
        result.types.add(TRAIN)
    if int(tmp[-14].partition('= ')[-1]):
        result.types.add(TANK)
    if int(tmp[-13].partition('= ')[-1]):
        result.types.add(ARTILLERY)
    if int(tmp[-12].partition('= ')[-1]):
        result.types.add(AAA_POSITION)
    if int(tmp[-11].partition('= ')[-1]):
        result.types.add(SHIP)
    if int(tmp[-10].partition('= ')[-1]):
        result.types.add(BALLOON)
    if int(tmp[-9].partition('= ')[-1]):
        result.types.add(WINDSOCK)
    if int(tmp[-8].partition('= ')[-1]):
        result.types.add(CITY_FIRE)
    if int(tmp[-7].partition('= ')[-1]):
        result.types.add(SPOTTER)
    if int(tmp[-6].partition('= ')[-1]):
        result.types.add(BRIDGE)
    if int(tmp[-5].partition('= ')[-1]):
        result.types.add(AT_ART_POSITION)
    if int(tmp[-4].partition('= ')[-1]):
        result.types.add(FIRING_POINT)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(SIREN)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(PARKING)
    return result


def parse_reference_location(text: str) -> Location:
    """Считать Airfield локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(_list=tmp)
    if int(tmp[-5].partition('= ')[-1]):
        result.types.add(HW_ARTILLERY)
    if int(tmp[-4].partition('= ')[-1]):
        result.types.add(AT_ARTILLERY)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(RL_FIRING_POINT)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(RL_FRONT_LINE)
    return result


class LocationsBuilder:
    """Сборщик баз локаций"""
    def __init__(self, ldf_base=''):
        self.locations = {
            AIR_OBJECTIVE: [],
            AIRFIELD: [],
            DECORATION: [],
            GROUND_OBJECTIVE: [],
            REFERENCE_LOCATION: []
        }

        if ldf_base:
            for match in air_objective_raw_re.findall(ldf_base):
                self.locations[AIR_OBJECTIVE].append(parse_air_objective(match))
            for match in airfields_raw_re.findall(ldf_base):
                self.locations[AIRFIELD].append(parse_airfield(match))
            for match in ground_objective_raw_re.findall(ldf_base):
                self.locations[GROUND_OBJECTIVE].append(parse_ground_objective(match))
            for match in decorations_raw_re.findall(ldf_base):
                self.locations[DECORATION].append(parse_decoration(match))
            for match in reference_location_raw_re.findall(ldf_base):
                self.locations[REFERENCE_LOCATION].append(parse_reference_location(match))

    def add(self, name: str, x: float, z: float, country: int, y=0.0, oy=0.0, length=100, width=100):
        """Добавить локацию"""
        if name not in self.locations:
            raise NameError('Incorrect location name')
        location = Location(name=name, x=x, z=z, y=y, oy=oy, length=length, width=width)
        location.country = country
        self.locations[name].append(location)
