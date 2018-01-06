"""Настройки отрисовки карт"""
import json
import pathlib
import configparser
from .mgen import Mgen


class Draw:
    """Класс настроек отрисовки карт"""
    _instances = 0

    def __init__(self, config_path: pathlib.Path, mgen: Mgen):
        Draw._instances += 1
        if Draw._instances > 1:
            raise NameError('Too much Draw instances')
        with open('.\\configs\\draw_settings.json') as stream:
            src = json.load(stream)
        img_fld = pathlib.Path('.\\img\\').absolute()
        self.cfg = src
        self.coals = src['coals']
        self.img_folder = img_fld
        self.background = {x: str(img_fld.joinpath(src['backgrounds'][x])) for x in mgen.maps}
        self.flame = str(img_fld.joinpath(src['flames']))
        self.airfield = str(img_fld.joinpath(src['airfields']))
        self.icons = {x: {z: str(img_fld.joinpath(src[x][z]).absolute()) for z in src['coal_icons']}
                      for x in self.coals}
        src = configparser.ConfigParser()
        src.read(str(config_path.absolute()))
        self.draw_edges = True if "true" in src['PROGRAM']['draw_edges'].lower() else False
        self.draw_nodes = True if "true" in src['PROGRAM']['draw_nodes'].lower() else False
        self.draw_nodes_text = True if "true" in src['PROGRAM']['draw_nodes_text'].lower() else False
        self.draw_influences = True if "true" in src['PROGRAM']['draw_influences'].lower() else False
