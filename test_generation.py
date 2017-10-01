"Тестирование генерации миссий и работы графа"
import unittest
import pathlib
import generation
from tests.mocks import MainMock, MgenMock

MAIN = MainMock(pathlib.Path(r'./testdata/conf.ini'))
MGEN = MgenMock(MAIN)

MOSCOW = 'moscow'
STALIN = 'stalingrad'

class TestGrid(unittest.TestCase):
    "Тесты графа"
    def setUp(self):
        "Настройка тестов"
        self.iterations = 25

    def test_grid_capturing_moscow(self):
        "Проверка захвата в графе"
        grid = generation.Grid(MOSCOW, MGEN.xgml[MOSCOW], MGEN)
        # Act
        for i in range(self.iterations):
            path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(MOSCOW, i))
            # grid.capture_node(grid.scenarios[101][0], 1)
            grid.save_file(path)

    def test_grid_capturing_stalingrad(self):
        "Проверка захвата в графе"
        grid = generation.Grid(STALIN, MGEN.xgml[STALIN], MGEN)
        path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(STALIN, 0))
        grid.save_file(path)
        # Act
        for i in range(1, self.iterations):
            path = pathlib.Path(r'./tmp/{}_{}.xgml'.format(STALIN, i))
            grid.capture_node(grid.scenarios[101][0], 1)
            grid.save_file(path)


class TestTvd(unittest.TestCase):
    "Тесты ТВД"
    pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
