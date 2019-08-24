"""Заглушки конфигов"""
from pathlib import Path
from configs import Config, Main, Mgen, Planes


class MainMock(Main):
    """Заглушка конфига"""

    def __init__(self, path: Path):
        super().__init__(path=path)
        self.current_grid_folder = Path('./tmp/current/')


class MgenMock(Mgen):
    """Заглушка конфига генерации миссий"""

    def __init__(self, game_folder: Path):
        super().__init__(game_folder)
        self.xgml = {
            'stalingrad': Path('./tests/data/xgml/stalingrad.xgml').absolute(),
            'moscow': Path('./tests/data/xgml/moscow.xgml').absolute(),
            'kuban': Path('./tests/data/xgml/kuban.xgml').absolute(),
            'test': Path('./tests/data/xgml/test_w4f.xgml').absolute()
        }
        folders = {'red': Path('./tmp/red/'), 'blue': Path('./tmp/blue/')}
        self.af_groups_folders = {
            'moscow': folders,
            'stalingrad': folders
        }


class PlanesMock(Planes):
    """Заглушка конфига самолётов"""

    def __init__(self):
        super().__init__(path='./tests/data/config/planes.json')


class ConfigMock(Config):
    """Заглушка главного конфига"""
    def __init__(self):
        path = Path('./tests/data/config/main.json')
        super().__init__(path)
        self.main = MainMock(path)
        self.mgen = MgenMock(self.main.game_folder)
        self.planes = PlanesMock()
