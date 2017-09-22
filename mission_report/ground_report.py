from cfg import Gameplay
import mission_report.mission_src

types_hp = {
    'warehouse': Gameplay.grounds['warehouse']['hp'],
    'tank': Gameplay.grounds['tanks']['hp'],
    'bridge': Gameplay.grounds['bridge']['hp'],
    'airfield': Gameplay.grounds['airfield']['hp'],
    'hq': Gameplay.grounds['hq']['hp'],
    'industrial': Gameplay.grounds['industrial']['hp'],
    'artillery': Gameplay.grounds['artillery']['hp'],
    'fort': Gameplay.grounds['fort']['hp']
}
types_radius = {
    'warehouse': Gameplay.grounds['warehouse']['radius'],
    'tank': Gameplay.grounds['tanks']['radius'],
    'bridge': Gameplay.grounds['bridge']['radius'],
    'airfield': Gameplay.grounds['airfield']['radius'],
    'hq': Gameplay.grounds['hq']['radius'],
    'industrial': Gameplay.grounds['industrial']['radius'],
    'artillery': Gameplay.grounds['artillery']['radius'],
    'fort': Gameplay.grounds['fort']['radius']
}


class Ground:
    def __init__(self, server_input):
        self.name = server_input['name']
        self.x = server_input['XPos']
        self.z = server_input['ZPos']
        self.killed_objects = set()

    def try_add_kill(self, kill):
        def distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        if distance(kill.last_pos['x'], kill.last_pos['z'], self.x, self.z) < self.radius:
            self.killed_objects.add(kill)

    @property
    def g_type(self):
        if 'warehouse' in self.name:
            return 'warehouse'
        elif 'bridge' in self.name:
            return 'bridge'
        elif 'tank' in self.name:
            return 'tank'
        elif 'hq' in self.name:
            return 'hq'
        elif 'industrial' in self.name:
            return 'industrial'
        elif 'fort' in self.name:
            return 'fort'
        elif 'arty' in self.name:
            return 'artillery'
        else:
            return 'airfield'

    @property
    def killed(self):
        if 'half' in self.name and len(self.killed_objects) > int(types_hp[self.g_type] / 2):
            return True
        if len(self.killed_objects) > types_hp[self.g_type]:
            return True
        else:
            return False

    @property
    def radius(self):
        return types_radius[self.g_type]

    def __str__(self):
        return "[{}] {}".format(self.g_type, self.name)


class GroundReport:
    def __init__(self, mission_src, mission_name):
        """ Класс, считающий уничтожение наземных целей
        :type mission_src: mission_report.mission_src.MissionSrc """
        self.src = mission_src
        self.mission_name = mission_name
        self.grounds = []
        for server_input in self.src.server_inputs:
            if server_input['name'].upper() not in ('RW', 'NW', 'BW'):
                self.grounds.append(Ground(server_input))

    def process_ground_kills(self, sorties):
        for sortie in sorties:
            for kill_list in sortie.killboard:
                for kill in sortie.killboard[kill_list]:
                    for g in self.grounds:
                        g.try_add_kill(kill)

    @property
    def killed_grounds_names(self):
        return [x.name for x in self.grounds if x.killed]

    @property
    def killed_commands(self):
        return [
            Command(
                self.mission_name,
                cmd_type=CommandType.s_input,
                subject=x.name)
            for x in self.grounds if x.killed
            ]
