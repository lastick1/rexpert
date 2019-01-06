"""Класс локаций и форматирование локаций"""
import geometry
from .formats import air_objectives_format, ground_objective_format, airfields_format, navigation_format
from .formats import decorations_format, reference_location_format, substrate_format, terrain_leveler_format


AIR_OBJECTIVE = 'AirObjective'
AIRFIELD = 'Airfield'
DECORATION = 'Decoration'
GROUND_OBJECTIVE = 'GroundObjective'
REFERENCE_LOCATION = 'ReferenceLocation'
SUBSTRATE = 'Substrate'
TERRAIN_LEVELER = 'TerrainLeveler'
NAVIGATION = 'Navigation'
LOCATION_TYPES = (
    AIR_OBJECTIVE, AIRFIELD, DECORATION, GROUND_OBJECTIVE, NAVIGATION, REFERENCE_LOCATION, SUBSTRATE, TERRAIN_LEVELER
)

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
GRASS_FIELD = 'grass_field'
WATER_FIELD = 'water_field'
NDB = 'ndb'
AIRFIELD_DECORATION = 'airfield_decoration'
STATIC_AIRPLANE = 'static_airplane'
STATIC_VECHICLE = 'static_vechicle'
SEARCHLIGHT = 'searchlight'
LANDING_LIGHT = 'landing_light'
LANDING_SIGN = 'landing_sign'
TEXTURE_INDEX = 'texture_index'
FILTER_TREES = 'filter_trees'
FRONT_LINE = 'front_line'
PLANE_WAYPOINT = 'plane_waypoint'
TRANSPORT_FLIGHT = 'transport_flight'
TROOPS_CONCENTRATION = 'troops_concentration'
FERRY = 'ferry'
FRONTLINE_STRONGPOINT = 'frontline_strongpoint'
FRONTLINE_EDGE = 'frontline_edge'
RAILWAY_JUNCTION = 'railway_junction'
VEHICLE = 'vehicle'


def format_air_objective(location) -> str:
    """Форматировать AirObjective локацию"""
    return air_objectives_format.format(
        location.name,  # Name
        location.desc,  # Desc
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
        1 if BALLOON in location.types else 0,  # Balloon
        1 if TRANSPORT_FLIGHT in location.types else 0  # TransportFlight
    )


def format_airfield(location) -> str:
    """Форматировать Airfield локацию"""
    return airfields_format.format(
        location.name,  # Name
        location.desc,  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.str_country,  # Country
        1 if GRASS_FIELD in location.types else 0,  # Transport
        1 if WATER_FIELD in location.types else 0  # Transport
    )


def format_ground_objective(location) -> str:
    """Форматировать GroundObjective локацию"""
    return ground_objective_format.format(
        location.name,  # Name
        location.desc,  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width,  # Width
        location.str_country,  # Country
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
        1 if RECON_AREA in location.types else 0,  # ReconArea
        1 if TROOPS_CONCENTRATION in location.types else 0,  # TroopsConcentration
        1 if FERRY in location.types else 0,  # Ferry
        1 if FRONTLINE_STRONGPOINT in location.types else 0,  # FrontlineStrongpoint
        1 if FRONTLINE_EDGE in location.types else 0,  # FrontlineEdge
        1 if RAILWAY_JUNCTION in location.types else 0,  # RailwayJunction
        1 if VEHICLE in location.types else 0  # Vehicle
    )


def format_decoration(location) -> str:
    """Форматировать Decoration локацию"""
    return decorations_format.format(
        location.name,  # Name
        location.desc,  # Desc
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
        1 if PARKING in location.types else 0,  # Parking
        1 if NDB in location.types else 0,  # NDB
        1 if AIRFIELD_DECORATION in location.types else 0,  # AirfieldDecoration
        1 if STATIC_AIRPLANE in location.types else 0,  # StaticAirplane
        1 if STATIC_VECHICLE in location.types else 0,  # StaticVechicle
        1 if SEARCHLIGHT in location.types else 0,  # Searchlight
        1 if LANDING_LIGHT in location.types else 0,  # LandingLight
        1 if LANDING_SIGN in location.types else 0  # LandingSign
    )


def format_reference_location(location) -> str:
    """Форматировать ReferenceLocation локацию"""
    return reference_location_format.format(
        location.name,  # Name
        location.desc,  # Desc
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


def format_substrate(location) -> str:
    """Форматировать ReferenceLocation локацию"""
    return substrate_format.format(
        location.name,  # Name
        location.desc,  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width,  # Width
        1 if TEXTURE_INDEX in location.types else 0,  # TextureIndex
        1 if FILTER_TREES in location.types else 0  # FilterTrees
    )


def format_terrain_leveler(location) -> str:
    """Форматировать TerrainLeveler локацию"""
    return terrain_leveler_format.format(
        location.name,  # Name
        location.desc,  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width  # Width
    )


def format_navigation(location) -> str:
    """Форматировать Navigation локацию"""
    return navigation_format.format(
        location.name,  # Name
        location.desc,  # Desc
        location.x,  # XPos
        location.y,  # YPos
        location.z,  # ZPos
        location.oy,  # OY
        location.length,  # Length
        location.width,  # Width
        1 if PLANE_WAYPOINT in location.types else 0,  # PlaneWaypoint
        1 if FRONT_LINE in location.types else 0  # FrontLine
    )


FORMATTER = {
    AIR_OBJECTIVE: format_air_objective,
    AIRFIELD: format_airfield,
    GROUND_OBJECTIVE: format_ground_objective,
    DECORATION: format_decoration,
    REFERENCE_LOCATION: format_reference_location,
    SUBSTRATE: format_substrate,
    TERRAIN_LEVELER: format_terrain_leveler,
    NAVIGATION: format_navigation
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
                 desc='',
                 country=0):
        super().__init__(x=x, z=z)
        if name not in LOCATION_TYPES:
            raise NameError(f'Incorrect location name:{name}')
        self.name = name
        self.y = y
        self.oy = oy
        self.length = length
        self.width = width
        self.desc = desc
        self.country = country
        self.types = set()

    def __str__(self):
        return FORMATTER[self.name](self)

    @property
    def str_country(self):
        return '\n  Country = {};'.format(self.country) if self.country else ''
