"""Парсер конфигов генерации миссий"""
from pathlib import Path
import json
from .main import Main


class Mgen:
    """Класс конфига генератора"""
    def __init__(self, main: Main):
        with open('.\\configs\\missiongen.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.maps = src['maps']
        self.tvd_folders = {x: main.game_folder.joinpath(src[x]['tvd_folder']).absolute()
                            for x in src['maps']}
        self.af_templates_folder = Path('.\\af_templates\\').absolute()
        self.make_ldb_folder = main.game_folder.joinpath('.\\bin\\missiongen\\').absolute()
        self.ldf_files = {x: self.tvd_folders[x].joinpath(src[x]['ldf_file']).absolute()
                          for x in self.maps}
        self.ldf_templates = {x: self.tvd_folders[x].joinpath(src[x]['ldf_base_file']).absolute()
                              for x in self.maps}
        self.daytime_files = {x: Path(Path('.\\data\\').joinpath(src[x]['daytime_csv'])).absolute()
                              for x in self.maps}
        self.af_groups_folders = {x: {z: self.tvd_folders[x].joinpath(src[x]['af_groups_folders'][z]).absolute()
                                      for z in src['sides']}
                                  for x in self.maps}
        self.subtitle_groups_folder = Path('r./tmp')
        self.xgml = {x: main.configs_folder.joinpath(src[x]['graph_file']) for x in self.maps}
        self.icons_group_files = {x: self.tvd_folders[x].joinpath(src[x]['icons_group_file']).absolute()
                                  for x in self.maps}
        self.af_csv = {x: Path(Path('.\\data\\').joinpath(src[x]['airfields_csv'])).absolute()
                       for x in self.maps}


class LocationsConfig:
    """Конфиг генерации базы локаций"""
    def __init__(self):
        with open('.\\configs\\loc_cfg.json') as stream:
            self.cfg = json.load(stream)


class GeneratorParamsConfig:
    """Конфиг дефолтпарамсов"""
    def __init__(self):
        with open('.\\configs\\dfpr.json') as stream:
            self.cfg = json.load(stream)
