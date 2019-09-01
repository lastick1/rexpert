"""Заглушки и функции получения заглушек"""
from core import Atype10, Atype12
from model import Node, \
    Grid
from .configs import MgenMock


TEST_LOG1 = './testdata/logs/spawn_takeoff_landing_despawn_missionReport(2017-09-17_09-05-09)[0].txt'
TEST_LOG2 = './testdata/logs/target_bombing_crashlanded_on_af_missionReport(2017-09-23_19-31-30)[0].txt'
TEST_LOG3 = './testdata/logs/multiple_spawns_missionReport(2017-09-24_14-46-12)[0].txt'
TEST_LOG4 = './testdata/logs/gkills_with_disconnect_missionReport(2017-09-26_20-37-23)[0].txt'
TEST_LOG5 = './testdata/logs/gkill_with_altf4_disco_missionReport(2017-09-26_21-10-48)[0].txt'
TEST_LOG6 = './testdata/logs/mission_rotation_atype19.txt'
TEST_LOG7 = './tests/data/logs/short_mission_full_log.txt'

TEST_NICKNAME = '_test_nickname'
TEST_ACCOUNT_ID = '_test_id1'
TEST_PROFILE_ID = '_test_profile_id1'
# pylint: disable=unused-argument


def pass_(*args, **kwargs):
    """Заглушка функции, не выполняющая действий"""


def return_true(*args, **kwargs):
    """Заглушка, всегда возвращающая True"""
    return True


def return_false(*args, **kwargs):
    """Заглушка, всегда возвращающая False"""
    return False


def return_zero(*args, **kwargs):
    """Заглушка, всегда возвращающая 0"""
    return 0


def atype_10_stub(aircraft_id: int, bot_id: int, pos: dict, aircraft_name: str,
                  country: int, parent_id: int, nickname=TEST_NICKNAME) -> Atype10:
    """Заглушка события появления игрока"""
    return Atype10(
        123, aircraft_id, bot_id, TEST_ACCOUNT_ID, TEST_PROFILE_ID, nickname, pos, aircraft_name, country,
        int(country/100), 1234, False, parent_id, True, True, 0, 1, '', [1, 5], 200, 100, 4, 8, '')


def atype_12_stub(object_id: int, object_name: str, country: int, name: str, parent_id: int) -> Atype12:
    """Заглушка события инициализации объекта"""
    return Atype12(120, object_id, object_name, country, int(country/100), name, parent_id)


COLOR_WHITE = '#FFFFFF'
COLOR_RED = '#FF0000'
COLOR_BLUE = '#00CCFF'

TEST = 'test'
TEST_NODES_LIST = [
    Node(key='1',  text='L', pos={'x': 3, 'z': 5}, color=COLOR_WHITE),
    Node(key='2',  text='L', pos={'x': 10, 'z': 1}, color=COLOR_WHITE),
    Node(key='3',  text='L', pos={'x': 16, 'z': 1}, color=COLOR_WHITE),
    Node(key='4',  text='L', pos={'x': 23, 'z': 1}, color=COLOR_WHITE),
    Node(key='5',  text='L', pos={'x': 25, 'z': 13}, color=COLOR_WHITE),
    Node(key='6',  text='L', pos={'x': 22, 'z': 18}, color=COLOR_WHITE),
    Node(key='7',  text='L', pos={'x': 24, 'z': 29}, color=COLOR_WHITE),
    Node(key='8',  text='L', pos={'x': 21, 'z': 32}, color=COLOR_WHITE),
    Node(key='9',  text='L', pos={'x': 11, 'z': 33}, color=COLOR_WHITE),
    Node(key='10', text='L', pos={'x': 0, 'z': 28}, color=COLOR_WHITE),
    Node(key='11', text='L', pos={'x': 2, 'z': 16}, color=COLOR_WHITE),
    Node(key='12', text='28', pos={'x': 7, 'z': 5}, color=COLOR_BLUE),
    Node(key='13', text='44', pos={'x': 14, 'z': 3}, color=COLOR_BLUE),
    Node(key='14', text='43', pos={'x': 20, 'z': 2}, color=COLOR_BLUE),
    Node(key='15', text='42', pos={'x': 22, 'z': 4}, color=COLOR_BLUE),
    Node(key='16', text='46', pos={'x': 21, 'z': 14}, color=COLOR_BLUE),
    Node(key='17', text='55', pos={'x': 19, 'z': 20}, color=COLOR_BLUE),
    Node(key='18', text='L', pos={'x': 20, 'z': 23}, color=COLOR_WHITE),
    Node(key='19', text='66', pos={'x': 21, 'z': 25}, color=COLOR_RED),
    Node(key='20', text='69', pos={'x': 21, 'z': 30}, color=COLOR_RED),
    Node(key='21', text='68', pos={'x': 17, 'z': 30}, color=COLOR_RED),
    Node(key='22', text='L', pos={'x': 5, 'z': 27}, color=COLOR_WHITE),
    Node(key='23', text='50', pos={'x': 4, 'z': 28}, color=COLOR_RED),
    Node(key='24', text='27', pos={'x': 5, 'z': 11}, color=COLOR_RED),
    Node(key='25', text='L', pos={'x': 8, 'z': 9}, color=COLOR_WHITE),
    Node(key='26', text='L', pos={'x': 12, 'z': 7}, color=COLOR_WHITE),
    Node(key='27', text='L', pos={'x': 18, 'z': 5}, color=COLOR_WHITE),
    Node(key='28', text='L', pos={'x': 17, 'z': 8}, color=COLOR_WHITE),
    Node(key='29', text='L', pos={'x': 17, 'z': 12}, color=COLOR_WHITE),
    Node(key='30', text='47', pos={'x': 16, 'z': 16}, color=COLOR_BLUE),
    Node(key='31', text='L', pos={'x': 17, 'z': 18}, color=COLOR_WHITE),
    Node(key='32', text='L', pos={'x': 18, 'z': 22}, color=COLOR_WHITE),
    Node(key='33', text='67', pos={'x': 19, 'z': 25}, color=COLOR_RED),
    Node(key='34', text='L', pos={'x': 20, 'z': 27}, color=COLOR_WHITE),
    Node(key='35', text='L', pos={'x': 19, 'z': 29}, color=COLOR_WHITE),
    Node(key='36', text='L', pos={'x': 17, 'z': 25}, color=COLOR_WHITE),
    Node(key='37', text='L', pos={'x': 12, 'z': 26}, color=COLOR_WHITE),
    Node(key='38', text='53', pos={'x': 13, 'z': 24}, color=COLOR_RED),
    Node(key='39', text='L', pos={'x': 10, 'z': 23}, color=COLOR_WHITE),
    Node(key='40', text='48', pos={'x': 12, 'z': 19}, color=COLOR_RED),
    Node(key='41', text='L', pos={'x': 10, 'z': 14}, color=COLOR_WHITE),
    Node(key='42', text='45', pos={'x': 14, 'z': 11}, color=COLOR_BLUE),
    Node(key='43', text='L', pos={'x': 13, 'z': 15}, color=COLOR_WHITE),
    Node(key='44', text='L', pos={'x': 15, 'z': 18}, color=COLOR_WHITE),
    Node(key='45', text='L', pos={'x': 14, 'z': 22}, color=COLOR_WHITE),
    Node(key='46', text='L', pos={'x': 16, 'z': 23}, color=COLOR_WHITE),
    Node(key='47', text='54', pos={'x': 16, 'z': 21}, color=COLOR_RED),
    Node(key='48', text='49', pos={'x': 7, 'z': 25}, color=COLOR_RED),
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


def get_test_grid(mgen: MgenMock) -> Grid:
    """Тестовый граф"""
    nodes = {x.key: x for x in TEST_NODES_LIST}
    for edge in TEST_EDGES_LIST:
        source_id = edge[0]
        target_id = edge[1]
        nodes[source_id].neighbors.add(nodes[target_id])
        nodes[target_id].neighbors.add(nodes[source_id])
    return Grid(name=TEST, nodes=nodes, edges=TEST_EDGES_LIST, tvd=mgen.cfg[TEST]['tvd'])
