"""Класс локаций и форматирование локаций"""
import geometry
from .formats import air_objectives_format, ground_objective_format, airfields_format
from .formats import decorations_format, reference_location_format


AIR_OBJECTIVE = 'AirObjective'
AIRFIELD = 'Airfield'
DECORATION = 'Decoration'
GROUND_OBJECTIVE = 'GroundObjective'
REFERENCE_LOCATION = 'ReferenceLocation'
LOCATION_TYPES = (AIR_OBJECTIVE, AIRFIELD, DECORATION, GROUND_OBJECTIVE, REFERENCE_LOCATION)

RECON_FLIGHT = 'recon_flight'
BOMBER_FLIGHT = 'bomber_flight'
FIGHTER_PATROL_FLIGHT = 'fighter_patrol_flight'
DUEL_OPPONENT = 'duel_opponent'
ARMOURED = 'armoured'
BUILDING = 'building'
RAILWAY_STATION = 'railway_station'
SUPPLY_DUMP = 'supply_dump'
FACTORY = 'factory'
PORT = 'port'
RECON_AREA = 'recon_area'
DOGFIGHT = 'dogfight'
TRANSPORT = 'transport'
TRAIN = 'train'
TANK = 'tank'
ARTILLERY = 'artillery'
AAA_POSITION = 'aaa_position'
SHIP = 'ship'
BALLOON = 'balloon'
WINDSOCK = 'windsock'
CITY_FIRE = 'city_fire'
SPOTTER = 'spotter'
BRIDGE = 'bridge'
AT_ART_POSITION = 'at_art_position'
FIRING_POINT = 'firing_point'
SIREN = 'siren'
PARKING = 'parking'
HW_ARTILLERY = 'hw_artillery'
AT_ARTILLERY = 'at_artillery'
RL_FIRING_POINT = 'rl_firing_point'
RL_FRONT_LINE = 'rl_front_line'


def format_air_objective(location) -> str:
    """Форматировать AirObjective локацию"""
    return air_objectives_format.format(
        '"{}"'.format(location.name),  # Name
        '"{}"'.format(location.desc),  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width,  # Width
        location.str_country,  # Country
        1 if RECON_FLIGHT in location.types else 0,  # ReconFlight
        1 if BOMBER_FLIGHT in location.types else 0,  # BomberFlight
        1 if FIGHTER_PATROL_FLIGHT in location.types else 0,  # FighterPatrolFlight
        1 if DOGFIGHT in location.types else 0,  # Dogfight
        1 if DUEL_OPPONENT in location.types else 0,  # DuelOpponent
        1 if BALLOON in location.types else 0  # Balloon
    )


def format_airfield(location) -> str:
    """Форматировать Airfield локацию"""
    return airfields_format.format(
        '"{}"'.format(location.name),  # Name
        '"{}"'.format(location.desc),  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.str_country  # Country
    )


def format_ground_objective(location) -> str:
    """Форматировать GroundObjective локацию"""
    return ground_objective_format.format(
        '"{}"'.format(location.name),  # Name
        '"{}"'.format(location.desc),  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width,  # Width
        1 if TRANSPORT in location.types else 0,  # Transport
        1 if ARMOURED in location.types else 0,  # Armoured
        1 if TANK in location.types else 0,  # Tank
        1 if AAA_POSITION in location.types else 0,  # AAAPosition
        1 if ARTILLERY in location.types else 0,  # Artillery
        1 if BUILDING in location.types else 0,  # Building
        1 if SHIP in location.types else 0,  # Ship
        1 if TRAIN in location.types else 0,  # Train
        1 if RAILWAY_STATION in location.types else 0,  # RailwayStation
        1 if SUPPLY_DUMP in location.types else 0,  # SupplyDump
        1 if FACTORY in location.types else 0,  # Factory
        1 if AIRFIELD in location.types else 0,  # Airfield
        1 if PORT in location.types else 0,  # Port
        1 if RECON_AREA in location.types else 0  # ReconArea
    )


def format_decoration(location) -> str:
    """Форматировать Decoration локацию"""
    return decorations_format.format(
        '"{}"'.format(location.name),  # Name
        '"{}"'.format(location.desc),  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width,  # Width
        location.str_country,  # Country
        1 if DOGFIGHT in location.types else 0,  # Dogfight
        1 if TRANSPORT in location.types else 0,  # Transport
        1 if TRAIN in location.types else 0,  # Train
        1 if TANK in location.types else 0,  # Tank
        1 if ARTILLERY in location.types else 0,  # Artillery
        1 if AAA_POSITION in location.types else 0,  # AAAPosition
        1 if SHIP in location.types else 0,  # Ship
        1 if BALLOON in location.types else 0,  # Balloon
        1 if WINDSOCK in location.types else 0,  # Windsock
        1 if CITY_FIRE in location.types else 0,  # CityFire
        1 if SPOTTER in location.types else 0,  # Spotter
        1 if BRIDGE in location.types else 0,  # Bridge
        1 if AT_ART_POSITION in location.types else 0,  # AtArtPosition
        1 if FIRING_POINT in location.types else 0,  # FiringPoint
        1 if SIREN in location.types else 0,  # Siren
        1 if PARKING in location.types else 0  # Parking
    )


def format_reference_location(location) -> str:
    """Форматировать ReferenceLocation локацию"""
    return reference_location_format.format(
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width,  # Width
        1 if HW_ARTILLERY in location.types else 0,  # HWArtillery
        1 if AT_ARTILLERY in location.types else 0,  # ATArtillery
        1 if RL_FIRING_POINT in location.types else 0,  # RL_FiringPoint
        1 if RL_FRONT_LINE in location.types else 0  # RL_FrontLine
    )


FORMATTER = {
    AIR_OBJECTIVE: format_air_objective,
    AIRFIELD: format_airfield,
    GROUND_OBJECTIVE: format_ground_objective,
    DECORATION: format_decoration,
    REFERENCE_LOCATION: format_reference_location
}


class Location(geometry.Point):
    """Класс локации"""
    def __init__(self,
                 name: str,
                 x: float,
                 z: float,
                 y: float,
                 oy: float,
                 length: float,
                 width: float,
                 desc=''):
        super().__init__(x=x, z=z)
        if name not in LOCATION_TYPES:
            raise NameError('Incorrect location name')
        self.name = name
        self.y = y
        self.oy = oy
        self.length = length
        self.width = width
        self.desc = desc
        self.country = 0
        self.types = set()

    def __str__(self):
        return FORMATTER[self.name](self)

    @property
    def str_country(self):
        return '\n  Country = {};'.format(self.country) if self.country else ''
