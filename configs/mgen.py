"""Парсер конфигов генерации миссий"""
import pathlib
import json


class Mgen:
    """Класс конфига генератора"""
    def __init__(self, game_folder: pathlib.Path):
        with open('.\\configs\\missiongen.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.maps = src['maps']
        self.tvd_folders = {x: game_folder.joinpath(src[x]['tvd_folder']).absolute()
                            for x in src['maps']}
        self.af_templates_folder = pathlib.Path('.\\af_templates\\').absolute()
        self.make_ldb_folder = game_folder.joinpath('.\\bin\\missiongen\\').absolute()
        self.ldf_files = {x: self.tvd_folders[x].joinpath(src[x]['ldf_file']).absolute()
                          for x in self.maps}
        self.ldf_templates = {x: self.tvd_folders[x].joinpath(src[x]['ldf_base_file']).absolute()
                              for x in self.maps}
        self.daytime_files = {x: pathlib.Path(pathlib.Path('.\\data\\').joinpath(src[x]['daytime_csv'])).absolute()
                              for x in self.maps}
        self.af_groups_folders = {x: {z: self.tvd_folders[x].joinpath(src[x]['af_groups_folders'][z]).absolute()
                                      for z in src['sides']}
                                  for x in self.maps}
        self.subtitle_groups_folder = pathlib.Path(r'./tmp/')
        self.data_folder = pathlib.Path(r'./data/')
        self.xgml = {x: self.data_folder.joinpath(src[x]['graph_file']) for x in self.maps}
        self.icons_group_files = {x: self.tvd_folders[x].joinpath(src[x]['icons_group_file']).absolute()
                                  for x in self.maps}
        self.af_csv = {x: pathlib.Path(pathlib.Path('.\\data\\').joinpath(src[x]['airfields_csv'])).absolute()
                       for x in self.maps}


class GeneratorParamsConfig:
    """Конфиг дефолтпарамсов"""
    def __init__(self):
        with open('.\\configs\\dfpr.json') as stream:
            self.cfg = json.load(stream)
