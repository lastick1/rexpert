"""Тестирование построения многоугольников зон влияния"""
import unittest
import pathlib
import generation
import geometry

from tests import mocks

MAIN = mocks.MainMock(pathlib.Path(r'.\testdata\conf.ini'))
MGEN = mocks.MgenMock(MAIN)

TEST = 'test'
COLOR_WHITE = '#FFFFFF'
COLOR_RED = '#FF0000'
COLOR_BLUE = '#00CCFF'


class TestBoundaryBuilder(unittest.TestCase):
    """Тестовый класс"""
    def setUp(self):
        self.north, self.east, self.south, self.west = 10, 10, 0, 0

    @staticmethod
    def _get_grid() -> generation.Grid:
        """Тестовый граф"""
        nodes_list = [
            generation.Node(key='1',  text='L', pos={'x': 3, 'z': 5}, color=COLOR_WHITE),
            generation.Node(key='2',  text='L', pos={'x': 10, 'z': 1}, color=COLOR_WHITE),
            generation.Node(key='3',  text='L', pos={'x': 16, 'z': 1}, color=COLOR_WHITE),
            generation.Node(key='4',  text='L', pos={'x': 23, 'z': 1}, color=COLOR_WHITE),
            generation.Node(key='5',  text='L', pos={'x': 25, 'z': 13}, color=COLOR_WHITE),
            generation.Node(key='6',  text='L', pos={'x': 22, 'z': 18}, color=COLOR_WHITE),
            generation.Node(key='7',  text='L', pos={'x': 24, 'z': 29}, color=COLOR_WHITE),
            generation.Node(key='8',  text='L', pos={'x': 21, 'z': 32}, color=COLOR_WHITE),
            generation.Node(key='9',  text='L', pos={'x': 11, 'z': 33}, color=COLOR_WHITE),
            generation.Node(key='10', text='L', pos={'x': 0, 'z': 28}, color=COLOR_WHITE),
            generation.Node(key='11', text='L', pos={'x': 2, 'z': 16}, color=COLOR_WHITE),
            generation.Node(key='12', text='28', pos={'x': 7, 'z': 5}, color=COLOR_BLUE),
            generation.Node(key='13', text='44', pos={'x': 14, 'z': 3}, color=COLOR_BLUE),
            generation.Node(key='14', text='43', pos={'x': 20, 'z': 2}, color=COLOR_BLUE),
            generation.Node(key='15', text='42', pos={'x': 22, 'z': 4}, color=COLOR_BLUE),
            generation.Node(key='16', text='46', pos={'x': 21, 'z': 14}, color=COLOR_BLUE),
            generation.Node(key='17', text='55', pos={'x': 19, 'z': 20}, color=COLOR_BLUE),
            generation.Node(key='18', text='L', pos={'x': 20, 'z': 23}, color=COLOR_WHITE),
            generation.Node(key='19', text='66', pos={'x': 21, 'z': 25}, color=COLOR_RED),
            generation.Node(key='20', text='69', pos={'x': 21, 'z': 30}, color=COLOR_RED),
            generation.Node(key='21', text='68', pos={'x': 17, 'z': 30}, color=COLOR_RED),
            generation.Node(key='22', text='L', pos={'x': 5, 'z': 27}, color=COLOR_WHITE),
            generation.Node(key='23', text='50', pos={'x': 4, 'z': 28}, color=COLOR_RED),
            generation.Node(key='24', text='27', pos={'x': 5, 'z': 11}, color=COLOR_RED),
            generation.Node(key='25', text='L', pos={'x': 8, 'z': 9}, color=COLOR_WHITE),
            generation.Node(key='26', text='L', pos={'x': 12, 'z': 7}, color=COLOR_WHITE),
            generation.Node(key='27', text='L', pos={'x': 18, 'z': 5}, color=COLOR_WHITE),
            generation.Node(key='28', text='L', pos={'x': 17, 'z': 8}, color=COLOR_WHITE),
            generation.Node(key='29', text='L', pos={'x': 17, 'z': 12}, color=COLOR_WHITE),
            generation.Node(key='30', text='47', pos={'x': 16, 'z': 16}, color=COLOR_BLUE),
            generation.Node(key='31', text='L', pos={'x': 17, 'z': 18}, color=COLOR_WHITE),
            generation.Node(key='32', text='L', pos={'x': 18, 'z': 22}, color=COLOR_WHITE),
            generation.Node(key='33', text='67', pos={'x': 19, 'z': 25}, color=COLOR_WHITE),
            generation.Node(key='34', text='L', pos={'x': 20, 'z': 27}, color=COLOR_WHITE),
            generation.Node(key='35', text='L', pos={'x': 19, 'z': 29}, color=COLOR_WHITE),
            generation.Node(key='36', text='L', pos={'x': 17, 'z': 25}, color=COLOR_WHITE),
            generation.Node(key='37', text='L', pos={'x': 12, 'z': 26}, color=COLOR_WHITE),
            generation.Node(key='38', text='53', pos={'x': 13, 'z': 24}, color=COLOR_RED),
            generation.Node(key='39', text='L', pos={'x': 10, 'z': 23}, color=COLOR_WHITE),
            generation.Node(key='40', text='48', pos={'x': 12, 'z': 19}, color=COLOR_RED),
            generation.Node(key='41', text='L', pos={'x': 10, 'z': 14}, color=COLOR_WHITE),
            generation.Node(key='42', text='45', pos={'x': 14, 'z': 11}, color=COLOR_BLUE),
            generation.Node(key='43', text='L', pos={'x': 13, 'z': 15}, color=COLOR_WHITE),
            generation.Node(key='44', text='L', pos={'x': 15, 'z': 18}, color=COLOR_WHITE),
            generation.Node(key='45', text='L', pos={'x': 14, 'z': 22}, color=COLOR_WHITE),
            generation.Node(key='46', text='L', pos={'x': 16, 'z': 23}, color=COLOR_WHITE),
            generation.Node(key='47', text='54', pos={'x': 16, 'z': 21}, color=COLOR_RED),
            generation.Node(key='48', text='49', pos={'x': 7, 'z': 25}, color=COLOR_RED),
        ]
        edges = [
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
        nodes = {x.key: x for x in nodes_list}
        for edge in edges:
            source_id = edge[0]
            target_id = edge[1]
            nodes[source_id].neighbors.add(nodes[target_id])
            nodes[target_id].neighbors.add(nodes[source_id])
        return generation.Grid(name=TEST, nodes=nodes, edges=edges, config=MGEN)

    @staticmethod
    def _get_nodes(points: list) -> list:
        """Получить узлы из точек (нейтральные)"""
        nodes = []
        key = 0
        for point in points:
            nodes.append(generation.Node(key=key, text=key, pos=point.to_dict(), color='#FFFFFF'))
            key += 1
        return nodes

    def test_build_east(self):
        """Создаётся корректный многоугольник восточной InfluenceArea"""
        builder = generation.BoundaryBuilder(self.north, self.east, self.south, self.west)
        points = [
            geometry.Point(x=1, z=6),
            geometry.Point(x=4, z=3),
            geometry.Point(x=5, z=6),
            geometry.Point(x=7, z=4),
            geometry.Point(x=9, z=6)
        ]
        nodes = self._get_nodes(points)
        expected = points + [
            geometry.Point(x=self.north, z=6),
            geometry.Point(x=self.north, z=self.east),
            geometry.Point(x=self.south, z=self.east),
            geometry.Point(x=self.south, z=6)
        ]
        # Act
        result = builder.influence_east(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_build_west(self):
        """Создаётся корректный многоугольник западной InfluenceArea"""
        builder = generation.BoundaryBuilder(self.north, self.east, self.south, self.west)
        points = [
            geometry.Point(x=1, z=6),
            geometry.Point(x=4, z=3),
            geometry.Point(x=5, z=6),
            geometry.Point(x=7, z=4),
            geometry.Point(x=9, z=6)
        ]
        nodes = self._get_nodes(points)
        points.reverse()
        expected = [
            geometry.Point(x=self.south, z=6),
            geometry.Point(x=self.south, z=self.west),
            geometry.Point(x=self.north, z=self.west),
            geometry.Point(x=self.north, z=6)
        ] + points
        # Act
        result = builder.influence_west(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_build_west_complex(self):
        """Создаётся корректный многоугольник для 'сложной' линии фронта"""
        builder = generation.BoundaryBuilder(self.north, self.east, self.south, self.west)
        points = [
            geometry.Point(x=1, z=1),
            geometry.Point(x=1, z=9),
            geometry.Point(x=9, z=9),
            geometry.Point(x=7, z=4),
            geometry.Point(x=5, z=4),
            geometry.Point(x=4, z=1),
            geometry.Point(x=8, z=3),
            geometry.Point(x=8, z=1),
        ]
        nodes = self._get_nodes(points)
        points.reverse()
        expected = [
            geometry.Point(x=self.south, z=1),
            geometry.Point(x=self.south, z=self.west),
            geometry.Point(x=self.north, z=self.west),
            geometry.Point(x=self.north, z=1)
        ] + points

        # Act
        result = builder.influence_west(nodes)
        # Assert
        self.assertSequenceEqual(result, expected)

    def test_confrontation_area_west(self):
        """Создаётся многоугольник западно прифронтовой полосы"""
        expected_keys = (1, 25, 41, 43, 44, 31, 32, 18, 6, 5, 16, 29, 42, 26, 12, 2, 1)
        xgml = generation.Xgml(TEST, MGEN)
        builder = generation.BoundaryBuilder(self.north, self.east, self.south, self.west)
        xgml.z_coefficient_serialization = 15
        xgml.x_coefficient_serialization = 15
        grid = self._get_grid()
        nodes = grid.nodes
        # expected_nodes = list(x for x in nodes if int(x.key) in expected_keys)
        path = pathlib.Path(r'./tmp/tmp.xgml')
        xgml.save_file(str(path), grid.nodes, grid.edges)
        # Act
        result = builder.confrontation_west(grid)
        # Assert
        self.assertCountEqual(tuple(int(x.key) for x in result), expected_keys)


if __name__ == '__main__':
    unittest.main(verbosity=2)
