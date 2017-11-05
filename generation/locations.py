"""Классы типов локаций в текстовых базах локаций"""
from geometry import Point, Segment
from configs import LocationsConfig
from .formats import decorations_format, ground_objective_format, air_objectives_format, division_format


class AirObjectiveRecon:
    def __init__(self, string):
        self.cls = 'air_objective_recon'
        self.string = string

    def __str__(self):
        return self.string


class AirObjectiveLocation(Point):
    def __init__(self, node):
        super().__init__(x=node.x, z=node.z)
        self.loc_country = None

    def __str__(self):
        if not self.loc_country:
            raise NameError('AirObjectiveLocation must have loc_country')
        return air_objectives_format.format(
            self.x, self.z, self.loc_country
        )


class DecorationLocation(Point):
    def __init__(self, string, tvd_name, areas, frontline, objective_nodes, config: LocationsConfig):
        tmp = str(string).split(';')
        super().__init__(x=float(tmp[2].partition('= ')[-1]), z=float(tmp[4].partition('= ')[-1]))
        self.cls = 'decoration'
        self.cfg = config.cfg
        self.tvd_name = tvd_name
        self.frontline = frontline
        self.objective_nodes = objective_nodes
        self.name = str(tmp[0].partition('= ')[-1])
        self.desc = str(tmp[1].partition('= ')[-1])
        self.y = float(tmp[3].partition('= ')[-1])
        self.oy = float(tmp[5].partition('= ')[-1])
        self.length = float(tmp[6].partition('= ')[-1])
        self.width = float(tmp[7].partition('= ')[-1])
        self.types = {
            'dogfight': int(tmp[-17].partition('= ')[-1]),
            'transport': int(tmp[-16].partition('= ')[-1]),
            'train': int(tmp[-15].partition('= ')[-1]),
            'tank': int(tmp[-14].partition('= ')[-1]),
            'artillery': int(tmp[-13].partition('= ')[-1]),
            'aaa_position': int(tmp[-12].partition('= ')[-1]),
            'ship': int(tmp[-11].partition('= ')[-1]),
            'balloon': int(tmp[-10].partition('= ')[-1]),
            'windsock': int(tmp[-9].partition('= ')[-1]),
            'city_fire': int(tmp[-8].partition('= ')[-1]),
            'spotter': int(tmp[-7].partition('= ')[-1]),
            'bridge': int(tmp[-6].partition('= ')[-1]),
            'at_art_position': int(tmp[-5].partition('= ')[-1]),
            'firing_point': int(tmp[-4].partition('= ')[-1]),
            'siren': int(tmp[-3].partition('= ')[-1]),
            'parking': int(tmp[-2].partition('= ')[-1])
        }
        self.areas = areas

    @property
    def loc_country(self):
        fl_first = self.frontline[0]
        for country in self.areas:
            for area in self.areas[country]:
                if self.is_in_area(area):
                    for t in (x for x in self.types.keys() if self.types[x] == 1):
                        fl_rule = self.cfg[self.cls][self.tvd_name][str(country)]['frontline'][t]
                        on_rule = self.cfg[self.cls][self.tvd_name][str(country)]['scenario'][t]
                        if len(fl_rule) or len(on_rule):
                            if len(fl_rule) and not len(on_rule):
                                # только правило "от линии фронта"
                                closest = fl_first
                                for node in self.frontline:
                                    if self.distance_to(closest.x, closest.z) > self.distance_to(node.x, node.z):
                                        closest = node
                                if fl_rule[0] < self.distance_to(closest.x, closest.z) < fl_rule[1]:
                                    return country
                            if len(on_rule) and not len(fl_rule):
                                for node in self.objective_nodes[country]:
                                    if on_rule[0] < self.distance_to(node.x, node.z) < on_rule[1]:
                                        return country
                            if len(on_rule) and len(fl_rule):
                                on = []
                                for c in self.objective_nodes.keys():
                                    on += self.objective_nodes[c]
                                for node in on:
                                    if self.distance_to(node.x, node.z) < on_rule[1]:
                                        for fl_node in self.frontline:
                                            if self.distance_to(fl_node.x, fl_node.z) < fl_rule[0]:
                                                return
                                        return country
                            return
                        else:
                            return country
        return

    def __str__(self):
        c = '' if not self.loc_country else '\n  Country = {};'.format(self.loc_country)
        return decorations_format.format(
            self.name, self.desc, self.x, self.y, self.z, self.oy, self.length, self.width,
            c,
            self.types['dogfight'], self.types['transport'], self.types['train'], self.types['tank'],
            self.types['artillery'], self.types['aaa_position'], self.types['ship'], self.types['balloon'],
            self.types['windsock'], self.types['city_fire'], self.types['spotter'], self.types['bridge'],
            self.types['at_art_position'], self.types['firing_point'], self.types['siren'], self.types['parking']
        )


# TODO объединить классы GroundObjectiveLocation и DecorationLocation в один класс
class GroundObjectiveLocation(Point):
    def __init__(self, string, tvd_name, areas, frontline, objective_nodes, config: LocationsConfig):
        tmp = str(string).split(';')
        super().__init__(x=float(tmp[2].partition('= ')[-1]), z=float(tmp[4].partition('= ')[-1]))
        self.cls = 'ground_objective'
        self.cfg = config.cfg
        self.tvd_name = tvd_name
        self.frontline = frontline
        self.objective_nodes = objective_nodes
        self.name = str(tmp[0].partition('= ')[-1])
        self.desc = str(tmp[1].partition('= ')[-1])
        self.y = float(tmp[3].partition('= ')[-1])
        self.oy = float(tmp[5].partition('= ')[-1])
        self.length = float(tmp[6].partition('= ')[-1])
        self.width = float(tmp[7].partition('= ')[-1])
        self.types = {
            'transport': int(tmp[-15].partition('= ')[-1]),
            'armoured': int(tmp[-14].partition('= ')[-1]),
            'tank': int(tmp[-13].partition('= ')[-1]),
            'aaa_position': int(tmp[-12].partition('= ')[-1]),
            'artillery': int(tmp[-11].partition('= ')[-1]),
            'building': int(tmp[-10].partition('= ')[-1]),
            'ship': int(tmp[-9].partition('= ')[-1]),
            'train': int(tmp[-8].partition('= ')[-1]),
            'railway_station': int(tmp[-7].partition('= ')[-1]),
            'supply_dump': int(tmp[-6].partition('= ')[-1]),
            'factory': int(tmp[-5].partition('= ')[-1]),
            'airfield': int(tmp[-4].partition('= ')[-1]),
            'port': int(tmp[-3].partition('= ')[-1]),
            'recon_area': int(tmp[-2].partition('= ')[-1])
        }
        self.areas = areas
        self._loc_country = None

    @property
    def loc_country(self):
        fl_first = self.frontline[0]
        for country in self.areas:
            for area in self.areas[country]:
                if self.is_in_area(area):
                    for t in (x for x in self.types.keys() if self.types[x] == 1):
                        fl_rule = self.cfg[self.cls][self.tvd_name][str(country)]['frontline'][t]
                        on_rule = self.cfg[self.cls][self.tvd_name][str(country)]['scenario'][t]
                        if len(fl_rule) or len(on_rule):
                            if len(fl_rule) and not len(on_rule):
                                # только правило "от линии фронта"
                                closest = fl_first
                                for node in self.frontline:
                                    if self.distance_to(closest.x, closest.z) > self.distance_to(node.x, node.z):
                                        closest = node
                                if fl_rule[0] < self.distance_to(closest.x, closest.z) < fl_rule[1]:
                                    return country
                            if len(on_rule) and not len(fl_rule):
                                for node in self.objective_nodes[country]:
                                    if on_rule[0] < self.distance_to(node.x, node.z) < on_rule[1]:
                                        return country
                            if len(on_rule) and len(fl_rule):
                                on = []
                                for c in self.objective_nodes.keys():
                                    on += self.objective_nodes[c]
                                for node in on:
                                    if self.distance_to(node.x, node.z) < on_rule[1]:
                                        for fl_node in self.frontline:
                                            if self.distance_to(fl_node.x, fl_node.z) < fl_rule[0]:
                                                return
                                        return country
                            return
                        else:
                            return country
        return

    def __str__(self):
        c = '' if not self.loc_country else '\n  Country = {};'.format(self.loc_country)
        return ground_objective_format.format(
            self.name, self.desc, self.x, self.y, self.z, self.oy, self.length, self.width,
            c,
            self.types['transport'], self.types['armoured'], self.types['tank'], self.types['aaa_position'],
            self.types['artillery'], self.types['building'], self.types['ship'], self.types['train'],
            self.types['railway_station'], self.types['supply_dump'], self.types['factory'], self.types['airfield'],
            self.types['port'], self.types['recon_area']
        )


class Division(Segment):
    def __init__(self, segment_coordinates, frontline_margin_distance, depth):
        super().__init__(
            segment_coordinates[0][0],
            segment_coordinates[0][1],
            segment_coordinates[1][0],
            segment_coordinates[1][1]
        )
        self.frame = super().parallel_segments(frontline_margin_distance)
        self.depth = depth

    def __str__(self):
        return division_format.format(
            self.frame[0].center[0],
            self.frame[0].center[1],
            self.frame[0].angle,
            self.depth,
            self.frame[0].length
        ) + '\n\n' + division_format.format(
            self.frame[1].center[0],
            self.frame[1].center[1],
            self.frame[1].angle,
            self.depth,
            self.frame[1].length
        )
