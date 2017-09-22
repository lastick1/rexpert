"Парсер конфигов генерации миссий"
from pathlib import Path
import json
from .main import Main

class Mgen:
    "Класс конфига генератора"
    _instances = 0

    def __init__(self, main: Main):
        Mgen._instances += 1
        if Mgen._instances > 1:
            raise NameError('Too much Mgen instances')
        with open('.\\configs\\missiongen.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.maps = src['maps']
        self.tvd_folders = {x: main.game_folder.joinpath(src[x]['tvd_folder']).absolute()
                            for x in src['maps']}
        self.af_tf = Path('.\\af_templates\\').absolute()
        self.make_ldb_folder = main.game_folder.joinpath('.\\bin\\missiongen\\').absolute()
        self.ldf_files = {x: self.tvd_folders[x].joinpath(src[x]['ldf_file']).absolute()
                          for x in self.maps}
        self.ldf_templates = {x: self.tvd_folders[x].joinpath(src[x]['ldf_base_file']).absolute()
                              for x in self.maps}
        self.daytime_files = {x: Path(Path('.\\configs\\').joinpath(src[x]['daytime_csv'])).absolute()
                          for x in self.maps}
        self.af_groups_folders = {x: {z: self.tvd_folders[x].joinpath(src[x]['af_groups_folders'][z]).absolute()
                                      for z in src['sides']}
                                  for x in self.maps}
        self.stages = {x: src[x]['stages'] for x in self.maps}
        self.default_stages = {x: {z: self.af_tf.joinpath(src[x]['default_templates'][z]).absolute()
                                   for z in src['sides']}
                               for x in self.maps}
        self.xgml = {x: main.configs_folder.joinpath(src[x]['graph_file']) for x in self.maps}
        self.icons_group_files = {x: self.tvd_folders[x].joinpath(src[x]['icons_group_file']).absolute()
                                  for x in self.maps}

class LocationsConfig:
    "Конфиг генерации базы локаций"
    def __init__(self):
        self.cfg = json.load(open('.\\configs\\loc_cfg.json'))

class GeneratorParamsConfig:
    "Конфиг дефолтпарамсов"
    def __init__(self):
        self.cfg = json.load(open('.\\configs\\dfpr.json'))
