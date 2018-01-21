"""Сборка базы локаций"""
import re
import processing
from .locations import Location, AIR_OBJECTIVE, AIRFIELD, DECORATION, GROUND_OBJECTIVE, REFERENCE_LOCATION, NAVIGATION
from .locations import LOCATION_TYPES, PLANE_WAYPOINT, FRONT_LINE
from .locations import SUBSTRATE, TERRAIN_LEVELER, GRASS_FIELD, WATER_FIELD, LANDING_SIGN, FILTER_TREES, TEXTURE_INDEX
from .locations import RECON_FLIGHT, BOMBER_FLIGHT, FIGHTER_PATROL_FLIGHT, DUEL_OPPONENT, ARMOURED, BUILDING
from .locations import RAILWAY_STATION, SUPPLY_DUMP, FACTORY, PORT, RECON_AREA, DOGFIGHT, TRANSPORT, TRAIN, TANK
from .locations import ARTILLERY, AAA_POSITION, SHIP, BALLOON, WINDSOCK, CITY_FIRE, SPOTTER, BRIDGE, AT_ART_POSITION
from .locations import FIRING_POINT, SIREN, PARKING, HW_ARTILLERY, AT_ARTILLERY, RL_FIRING_POINT, RL_FRONT_LINE
from .locations import NDB, AIRFIELD_DECORATION, STATIC_AIRPLANE, STATIC_VECHICLE, SEARCHLIGHT, LANDING_LIGHT


def _parse_location(name: str, _list: list) -> Location:
    """Считать основную информацию о локации"""
    xpos = float(_list[2].partition('= ')[-1])
    ypos = float(_list[3].partition('= ')[-1])
    zpos = float(_list[4].partition('= ')[-1])
    oy = float(_list[5].partition('= ')[-1])
    length = float(_list[6].partition('= ')[-1])
    width = float(_list[7].partition('= ')[-1])
    return Location(name=name, x=xpos, z=zpos, y=ypos, oy=oy, length=length, width=width)


def parse_air_objective(text: str) -> Location:
    """Считать AirObjective локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(name=AIR_OBJECTIVE, _list=tmp)
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
    result = _parse_location(name=AIRFIELD, _list=tmp)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(WATER_FIELD)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(GRASS_FIELD)
    return result


def parse_ground_objective(text: str) -> Location:
    """Считать GroundObjective локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(name=GROUND_OBJECTIVE, _list=tmp)
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
    result = _parse_location(name=DECORATION, _list=tmp)
    try:
        if int(tmp[-24].partition('= ')[-1]):
            result.types.add(DOGFIGHT)
        if int(tmp[-23].partition('= ')[-1]):
            result.types.add(TRANSPORT)
        if int(tmp[-22].partition('= ')[-1]):
            result.types.add(TRAIN)
        if int(tmp[-21].partition('= ')[-1]):
            result.types.add(TANK)
        if int(tmp[-20].partition('= ')[-1]):
            result.types.add(ARTILLERY)
        if int(tmp[-19].partition('= ')[-1]):
            result.types.add(AAA_POSITION)
        if int(tmp[-18].partition('= ')[-1]):
            result.types.add(SHIP)
        if int(tmp[-17].partition('= ')[-1]):
            result.types.add(BALLOON)
        if int(tmp[-16].partition('= ')[-1]):
            result.types.add(WINDSOCK)
        if int(tmp[-15].partition('= ')[-1]):
            result.types.add(CITY_FIRE)
        if int(tmp[-14].partition('= ')[-1]):
            result.types.add(SPOTTER)
        if int(tmp[-13].partition('= ')[-1]):
            result.types.add(BRIDGE)
        if int(tmp[-12].partition('= ')[-1]):
            result.types.add(AT_ART_POSITION)
        if int(tmp[-11].partition('= ')[-1]):
            result.types.add(FIRING_POINT)
        if int(tmp[-10].partition('= ')[-1]):
            result.types.add(SIREN)
        if int(tmp[-9].partition('= ')[-1]):
            result.types.add(PARKING)
        if int(tmp[-8].partition('= ')[-1]):
            result.types.add(NDB)
        if int(tmp[-7].partition('= ')[-1]):
            result.types.add(AIRFIELD_DECORATION)
        if int(tmp[-6].partition('= ')[-1]):
            result.types.add(STATIC_AIRPLANE)
        if int(tmp[-5].partition('= ')[-1]):
            result.types.add(STATIC_VECHICLE)
        if int(tmp[-4].partition('= ')[-1]):
            result.types.add(SEARCHLIGHT)
        if int(tmp[-3].partition('= ')[-1]):
            result.types.add(LANDING_LIGHT)
        if int(tmp[-2].partition('= ')[-1]):
            result.types.add(LANDING_SIGN)
    except ValueError as error:
        print(error)
    return result


def parse_reference_location(text: str) -> Location:
    """Считать Airfield локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(name=REFERENCE_LOCATION, _list=tmp)
    if int(tmp[-5].partition('= ')[-1]):
        result.types.add(HW_ARTILLERY)
    if int(tmp[-4].partition('= ')[-1]):
        result.types.add(AT_ARTILLERY)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(RL_FIRING_POINT)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(RL_FRONT_LINE)
    return result


def parse_substrate(text: str) -> Location:
    """Считать Substrate локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(name=SUBSTRATE, _list=tmp)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(TEXTURE_INDEX)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(FILTER_TREES)
    return result


def parse_terrain_leveler(text: str) -> Location:
    """Считать TerrainLeveler локацию из текста"""
    tmp = str(text).split(';')
    result = _parse_location(name=TERRAIN_LEVELER, _list=tmp)
    return result


def parse_navigation(text: str) -> Location:
    tmp = str(text).split(';')
    result = _parse_location(name=NAVIGATION, _list=tmp)
    if int(tmp[-3].partition('= ')[-1]):
        result.types.add(PLANE_WAYPOINT)
    if int(tmp[-2].partition('= ')[-1]):
        result.types.add(FRONT_LINE)
    return result


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
substrate_raw_re = re.compile(
    '\nSubstrate\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
terrain_leveler_raw_re = re.compile(
    '\nTerrainLeveler\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
navigation_raw_re = re.compile(
    '\nNavigation\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)


class LocationsBuilder:
    """Сборщик баз локаций"""
    def __init__(self, ldf_base=''):
        self.locations = {
            AIR_OBJECTIVE: [],
            AIRFIELD: [],
            DECORATION: [],
            GROUND_OBJECTIVE: [],
            REFERENCE_LOCATION: [],
            SUBSTRATE: [],
            TERRAIN_LEVELER: [],
            NAVIGATION: []
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
            for match in substrate_raw_re.findall(ldf_base):
                self.locations[SUBSTRATE].append(parse_substrate(match))
            for match in terrain_leveler_raw_re.findall(ldf_base):
                self.locations[TERRAIN_LEVELER].append(parse_terrain_leveler(match))
            for match in navigation_raw_re.findall(ldf_base):
                self.locations[NAVIGATION].append(parse_navigation(match))

    def add(self, name: str, x: float, z: float, country: int, y=0.0, oy=0.0, length=100, width=100):
        """Добавить локацию"""
        if name not in self.locations:
            raise NameError('Incorrect location name')
        location = Location(name=name, x=x, z=z, y=y, oy=oy, length=length, width=width)
        location.country = country
        self.locations[name].append(location)

    def make_text(self) -> str:
        """Собрать файл базы локаций (*.ldf)"""
        result = '#1CGS Location Database file'
        for location_type in LOCATION_TYPES:
            result += self._serialize_locations(self.locations[location_type])
        result += '\n\n#end of file'
        return result

    def _serialize_locations(self, locations: list) -> str:
        """Сериализовать локации"""
        result = ''
        for location in locations:
            result += '\n\n' + self._serialize_location(location)
        return result

    @staticmethod
    def _serialize_location(location: Location) -> str:
        """Сериализовать локацию"""
        return str(location)

    @staticmethod
    def _is_in_influences(point, influences) -> bool:
        """Находится ли точка в инфлюенсах страны"""
        for boundary in influences:
            if point.is_in_area(boundary.polygon):
                return True
        return False

    def _is_rear(self, confrontation_area, influences, point):
        """Расположена ли точка вне фронтовой зоны но на территории инфлюенса"""
        return self._is_in_influences(point, influences) and not point.is_in_area(confrontation_area)

    def apply_tvd_setup(self, tvd: processing.Tvd):
        """Покраска локаций в соответствии с их расположением в зоне влияния"""
        front_airfields = {101: tvd.red_front_airfields, 201: tvd.blue_front_airfields}
        confrontations = {101: tvd.confrontation_east, 201: tvd.confrontation_west}
        all_airfields = [tvd.red_rear_airfield, tvd.blue_rear_airfield] + \
                        tvd.blue_front_airfields + tvd.red_front_airfields
        for location in self.locations[DECORATION]:
            if PARKING in location.types:
                for country in front_airfields:
                    for airfield in front_airfields[country]:
                        if location.distance_to(airfield.x, airfield.z) < 10:
                            location.country = country
                continue
            if {ARTILLERY}.intersection(location.types):
                for country in confrontations:
                    if location.is_in_area(confrontations[country]):
                        location.country = country
                        break
                continue
            if {TRANSPORT, FACTORY}.intersection(location.types):
                for country in confrontations:
                    if self._is_rear(confrontations[country], tvd.influences[country], location):
                        location.country = country
                        break
                continue
            for country in confrontations:
                if location.is_in_area(confrontations[country]):
                    location.country = country
                    break

        for location in self.locations[GROUND_OBJECTIVE]:
            if {FACTORY}.intersection(location.types):
                for country in confrontations:
                    if self._is_rear(confrontations[country], tvd.influences[country], location):
                        location.country = country
                        break
                continue
            if {TANK}.intersection(location.types):
                for country in confrontations:
                    if location.is_in_area(confrontations[country]):
                        close = False
                        for airfield in all_airfields:
                            if location.distance_to(airfield.x, airfield.z) < 30000:
                                close = True
                                break

                        far = True
                        for airfield in tvd.red_front_airfields + tvd.blue_front_airfields:
                            if location.distance_to(airfield.x, airfield.z) < 60000:
                                far = False
                                break

                        if not close and not far:
                            location.country = country
                            break

        red_rear_af = Location(
            name=AIRFIELD, x=tvd.red_rear_airfield.x, z=tvd.red_rear_airfield.z, y=0, oy=0, length=10, width=10)
        red_rear_af.country = 101
        red_rear_af.types.add(GRASS_FIELD)

        blue_rear_af = Location(
            name=AIRFIELD, x=tvd.blue_rear_airfield.x, z=tvd.blue_rear_airfield.z, y=0, oy=0, length=10, width=10)
        blue_rear_af.country = 201
        blue_rear_af.types.add(GRASS_FIELD)

        self.locations[AIRFIELD].append(red_rear_af)
        self.locations[AIRFIELD].append(blue_rear_af)
