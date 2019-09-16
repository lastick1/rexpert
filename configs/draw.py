"""Настройки отрисовки карт"""
from __future__ import annotations
import json
import pathlib
from .mgen import Mgen


class Draw:
    """Класс настроек отрисовки карт"""
    _instances = 0

    def __init__(self, mgen: Mgen):
        with open('./configs/draw_settings.json') as stream:
            src = json.load(stream)
        project_fld = pathlib.Path('.\\').absolute()
        self.cfg = src
        self.coals = src['coals']
        self.img_folder = project_fld
        self.background = {x: str(project_fld.joinpath(src['backgrounds'][x])) for x in mgen.maps}
        self.flame = str(project_fld.joinpath(src['flames']))
        self.airfield = str(project_fld.joinpath(src['airfields']))
        self.icons = {x: {z: str(project_fld.joinpath(src[x][z]).absolute()) for z in src['coal_icons']}
                      for x in self.coals}
        self.draw_edges = False
        self.draw_nodes = False
        self.draw_nodes_text = False
        self.draw_influences = False
