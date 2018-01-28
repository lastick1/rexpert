"""Заглушки, фальшивки и т.п. для тестирования"""
# pylint: disable=all
import pathlib

import atypes
import model
import rcon
import configs
import processing
import dependency_container

COLOR_WHITE = '#FFFFFF'
COLOR_RED = '#FF0000'
COLOR_BLUE = '#00CCFF'


class MainMock(configs.Main):
    """Заглушка конфига"""
    def __init__(self, path: pathlib.Path):
        super().__init__(path=path)
        self.current_grid_folder = pathlib.Path('./tmp/current/')


class MgenMock(configs.Mgen):
    """Заглушка конфига генерации миссий"""

    def __init__(self, game_folder: pathlib.Path):
        super().__init__(game_folder)
        self.xgml = {
            'stalingrad': pathlib.Path('./testdata/stalingrad.xgml').absolute(),
            'moscow': pathlib.Path('./testdata/moscow.xgml').absolute(),
            'kuban': pathlib.Path('./testdata/kuban.xgml').absolute(),
            'test': pathlib.Path('./testdata/test_w4f.xgml').absolute()
        }
        folders = {'red': pathlib.Path('./tmp/red/'), 'blue': pathlib.Path('./tmp/blue/')}
        self.af_groups_folders = {
            'moscow': folders,
            'stalingrad': folders
        }


class PlanesMock(configs.Planes):
    """Заглушка конфига самолётов"""
    def __init__(self):
        super().__init__(path='.\\testdata\\planes.json')


class TvdMock(processing.Tvd):
    def __init__(self, name: str):
        super().__init__(name, '', '10.11.1941', {'x': 281600, 'z': 281600}, dict(), pathlib.Path())
        self.country = 201

    def get_country(self, point):
        return self.country


class ConsoleMock(rcon.DServerRcon):
    """Заглушка коммандера"""

    def __init__(self):
        super().__init__('127.0.0.1', '8991')
        self.received_private_messages = []
        self.banned = []
        self.kicks = []
        self.received_server_inputs = []

    def private_message(self, account_id: str, message: str):
        self.received_private_messages.append((account_id, message))

    def banuser(self, name):
        self.banned.append(name)

    def kick(self, name):
        self.kicks.append(name)

    def server_input(self, server_input):
        self.received_server_inputs.append(server_input)


class GeneratorMock(processing.Generator):
    """Заглушка генератора миссий"""

    def __init__(self, config: configs.Config):
        super().__init__(config)
        self.generations = []

    def make_mission(self, file_name: str, tvd_name: str):
        self.generations.append((file_name, tvd_name))

    def make_ldb(self, tvd_name: str):
        pass


TEST = 'test'
TEST_NODES_LIST = [
    model.Node(key='1',  text='L', pos={'x': 3, 'z': 5}, color=COLOR_WHITE),
    model.Node(key='2',  text='L', pos={'x': 10, 'z': 1}, color=COLOR_WHITE),
    model.Node(key='3',  text='L', pos={'x': 16, 'z': 1}, color=COLOR_WHITE),
    model.Node(key='4',  text='L', pos={'x': 23, 'z': 1}, color=COLOR_WHITE),
    model.Node(key='5',  text='L', pos={'x': 25, 'z': 13}, color=COLOR_WHITE),
    model.Node(key='6',  text='L', pos={'x': 22, 'z': 18}, color=COLOR_WHITE),
    model.Node(key='7',  text='L', pos={'x': 24, 'z': 29}, color=COLOR_WHITE),
    model.Node(key='8',  text='L', pos={'x': 21, 'z': 32}, color=COLOR_WHITE),
    model.Node(key='9',  text='L', pos={'x': 11, 'z': 33}, color=COLOR_WHITE),
    model.Node(key='10', text='L', pos={'x': 0, 'z': 28}, color=COLOR_WHITE),
    model.Node(key='11', text='L', pos={'x': 2, 'z': 16}, color=COLOR_WHITE),
    model.Node(key='12', text='28', pos={'x': 7, 'z': 5}, color=COLOR_BLUE),
    model.Node(key='13', text='44', pos={'x': 14, 'z': 3}, color=COLOR_BLUE),
    model.Node(key='14', text='43', pos={'x': 20, 'z': 2}, color=COLOR_BLUE),
    model.Node(key='15', text='42', pos={'x': 22, 'z': 4}, color=COLOR_BLUE),
    model.Node(key='16', text='46', pos={'x': 21, 'z': 14}, color=COLOR_BLUE),
    model.Node(key='17', text='55', pos={'x': 19, 'z': 20}, color=COLOR_BLUE),
    model.Node(key='18', text='L', pos={'x': 20, 'z': 23}, color=COLOR_WHITE),
    model.Node(key='19', text='66', pos={'x': 21, 'z': 25}, color=COLOR_RED),
    model.Node(key='20', text='69', pos={'x': 21, 'z': 30}, color=COLOR_RED),
    model.Node(key='21', text='68', pos={'x': 17, 'z': 30}, color=COLOR_RED),
    model.Node(key='22', text='L', pos={'x': 5, 'z': 27}, color=COLOR_WHITE),
    model.Node(key='23', text='50', pos={'x': 4, 'z': 28}, color=COLOR_RED),
    model.Node(key='24', text='27', pos={'x': 5, 'z': 11}, color=COLOR_RED),
    model.Node(key='25', text='L', pos={'x': 8, 'z': 9}, color=COLOR_WHITE),
    model.Node(key='26', text='L', pos={'x': 12, 'z': 7}, color=COLOR_WHITE),
    model.Node(key='27', text='L', pos={'x': 18, 'z': 5}, color=COLOR_WHITE),
    model.Node(key='28', text='L', pos={'x': 17, 'z': 8}, color=COLOR_WHITE),
    model.Node(key='29', text='L', pos={'x': 17, 'z': 12}, color=COLOR_WHITE),
    model.Node(key='30', text='47', pos={'x': 16, 'z': 16}, color=COLOR_BLUE),
    model.Node(key='31', text='L', pos={'x': 17, 'z': 18}, color=COLOR_WHITE),
    model.Node(key='32', text='L', pos={'x': 18, 'z': 22}, color=COLOR_WHITE),
    model.Node(key='33', text='67', pos={'x': 19, 'z': 25}, color=COLOR_RED),
    model.Node(key='34', text='L', pos={'x': 20, 'z': 27}, color=COLOR_WHITE),
    model.Node(key='35', text='L', pos={'x': 19, 'z': 29}, color=COLOR_WHITE),
    model.Node(key='36', text='L', pos={'x': 17, 'z': 25}, color=COLOR_WHITE),
    model.Node(key='37', text='L', pos={'x': 12, 'z': 26}, color=COLOR_WHITE),
    model.Node(key='38', text='53', pos={'x': 13, 'z': 24}, color=COLOR_RED),
    model.Node(key='39', text='L', pos={'x': 10, 'z': 23}, color=COLOR_WHITE),
    model.Node(key='40', text='48', pos={'x': 12, 'z': 19}, color=COLOR_RED),
    model.Node(key='41', text='L', pos={'x': 10, 'z': 14}, color=COLOR_WHITE),
    model.Node(key='42', text='45', pos={'x': 14, 'z': 11}, color=COLOR_BLUE),
    model.Node(key='43', text='L', pos={'x': 13, 'z': 15}, color=COLOR_WHITE),
    model.Node(key='44', text='L', pos={'x': 15, 'z': 18}, color=COLOR_WHITE),
    model.Node(key='45', text='L', pos={'x': 14, 'z': 22}, color=COLOR_WHITE),
    model.Node(key='46', text='L', pos={'x': 16, 'z': 23}, color=COLOR_WHITE),
    model.Node(key='47', text='54', pos={'x': 16, 'z': 21}, color=COLOR_RED),
    model.Node(key='48', text='49', pos={'x': 7, 'z': 25}, color=COLOR_RED),
]
TEST_EDGES_LIST = [
    ('1', '2'), ('2', '3'), ('3', '4'), ('4', '5'), ('5', '6'), ('6', '7'), ('7', '8'), ('8', '9'), ('9', '10'),
    ('10', '11'), ('11', '1'), ('1', '12'), ('2', '12'), ('2', '26'), ('2', '13'), ('3', '13'), ('3', '27'),
    ('3', '14'), ('4', '14'), ('4', '27'), ('4', '15'), ('5', '15'), ('5', '27'), ('5', '28'), ('5', '16'),
    ('6', '16'), ('6', '29'), ('6', '30'), ('6', '31'), ('6', '17'), ('6', '18'), ('6', '19'), ('7', '19'),
    ('7', '34'), ('7', '20'), ('8', '20'), ('8', '35'), ('8', '21'), ('9', '21'), ('9', '37'), ('9', '48'),
    ('9', '22'), ('9', '23'), ('10', '23'), ('10', '22'), ('10', '48'), ('11', '48'), ('11', '39'),
    ('11', '40'), ('11', '41'), ('11', '24'), ('1', '24'), ('1', '25'), ('12', '25'), ('12', '26'),
    ('13', '26'), ('13', '28'), ('13', '27'), ('27', '15'), ('27', '28'), ('28', '26'), ('28', '42'),
    ('28', '29'), ('28', '16'), ('42', '29'), ('42', '26'), ('42', '25'), ('42', '41'), ('42', '43'),
    ('29', '43'), ('29', '30'), ('25', '24'), ('25', '41'), ('24', '41'), ('41', '40'), ('41', '43'),
    ('43', '40'), ('43', '44'), ('43', '30'), ('30', '44'), ('30', '31'), ('31', '17'), ('31', '32'),
    ('31', '47'), ('31', '44'), ('44', '40'), ('40', '39'), ('40', '45'), ('44', '47'), ('45', '44'),
    ('45', '47'), ('45', '46'), ('45', '38'), ('45', '39'), ('47', '32'), ('47', '46'), ('46', '38'),
    ('46', '36'), ('46', '32'), ('32', '36'), ('32', '33'), ('32', '18'), ('32', '17'), ('18', '17'),
    ('18', '33'), ('18', '34'), ('18', '19'), ('19', '34'), ('34', '33'), ('34', '20'), ('34', '35'),
    ('35', '33'), ('35', '36'), ('35', '21'), ('21', '36'), ('21', '37'), ('36', '37'), ('36', '38'),
    ('38', '37'), ('38', '39'), ('39', '48'), ('39', '37'), ('37', '48'), ('48', '22'), ('22', '23'),
    ('14', '27'), ('26', '25'), ('32', '35'), ('16', '29'), ('20', '35')
]


def get_test_grid(mgen: MgenMock) -> processing.Grid:
    """Тестовый граф"""
    nodes = {x.key: x for x in TEST_NODES_LIST}
    for edge in TEST_EDGES_LIST:
        source_id = edge[0]
        target_id = edge[1]
        nodes[source_id].neighbors.add(nodes[target_id])
        nodes[target_id].neighbors.add(nodes[source_id])
    return processing.Grid(name=TEST, nodes=nodes, edges=TEST_EDGES_LIST, config=mgen)


class AirfieldsControllerMock(processing.AirfieldsController):
    # noinspection PyTypeChecker
    def __init__(self, config: configs.Config):
        super().__init__(config)

    def spawn(self, tvd, aircraft_name: str, xpos: float, zpos: float):
        pass

    def finish(self, tvd, bot):
        pass


class DependencyContainerMock(dependency_container.DependencyContainer):
    def __init__(self, path: pathlib.Path):
        super().__init__()
        self._config = configs.Config(path)
        self._generator = GeneratorMock(self._config)
        self.generator_mock = self._generator
        self._rcon = ConsoleMock()
        self.console_mock = self._rcon
        self._map_painter = PainterMock()


def atype_12_stub(object_id: int, object_name: str, country: int, name: str, parent_id: int) -> atypes.Atype12:
    """Заглушка события инициализации объекта"""
    return atypes.Atype12(120, object_id, object_name, country, int(country/100), name, parent_id)


class PainterMock(processing.MapPainter):
    def __init__(self):
        super().__init__(None)

    def update_map(self):
        pass
