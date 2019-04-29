"""Парсер конфигов генерации миссий"""
from __future__ import annotations
import pathlib
import json


class Mgen:
    """Класс конфига генератора"""

    def __init__(self, game_folder: pathlib.Path):
        with open('./configs/mgen.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.maps = src['maps']
        self.tvd_folders = {x: game_folder.joinpath(src[x]['tvd_folder']).absolute()
                            for x in src['maps']}
        self.af_templates_folder = pathlib.Path('./af_templates/').absolute()
        self.make_ldb_folder = game_folder.joinpath('./bin/missiongen/').absolute()
        self.ldf_files = {x: self.tvd_folders[x].joinpath(src[x]['ldf_file']).absolute()
                          for x in self.maps}
        self.lgb_files = {x: self.tvd_folders[x].joinpath(src[x]['lgb_file']).absolute()
                          for x in self.maps}
        self.lgb_bin_files = {x: self.tvd_folders[x].joinpath(src[x]['lgb_file']+'.lgb').absolute()
                              for x in self.maps}
        self.ldf_templates = {x: list(self.tvd_folders[x].joinpath(z).absolute() for z in src[x]['ldf_base_files'])
                              for x in self.maps}
        self.daytime_files = {x: pathlib.Path(pathlib.Path('./data/').joinpath(src[x]['daytime_csv'])).absolute()
                              for x in self.maps}
        self.af_groups_folders = {x: {z: self.tvd_folders[x].joinpath(src[x]['af_groups_folders'][z]).absolute()
                                      for z in src['sides']}
                                  for x in self.maps}
        self.subtitle_groups_folder = pathlib.Path('./tmp/')
        self.data_folder = pathlib.Path('./data/')
        self.xgml = {x: pathlib.Path(self.data_folder.joinpath(src[x]['graph_file'])).absolute() for x in self.maps}
        self.icons_group_files = {x: self.tvd_folders[x].joinpath(src[x]['icons_group_file']).absolute()
                                  for x in self.maps}
        self._af_csv = {x: pathlib.Path(pathlib.Path('./data/').joinpath(src[x]['airfields_csv'])).absolute()
                        for x in self.maps}
        self._warehouses_csv = {x: pathlib.Path(pathlib.Path('./data/').joinpath(src[x]['warehouses_csv'])).absolute()
                                for x in self.maps}
        self._airfields_data = dict()
        self._warehouses_data = dict()

    @property
    def airfields_data(self) -> dict:
        """Аэродромы из файлов"""
        if not self._airfields_data:
            for tvd_name in self.maps:
                self._airfields_data[tvd_name] = list()
                with self._af_csv[tvd_name].open() as stream:
                    for line in stream.readlines():
                        string = line.split(sep=';')
                        self._airfields_data[tvd_name].append({
                            'name': string[0],
                            'x': float(string[1]),
                            'z': float(string[2]),
                            'tvd_name': tvd_name
                        })
        return self._airfields_data

    @property
    def warehouses_data(self) -> dict:
        """Склады из файлов"""
        if not self._warehouses_data:
            for tvd_name in self.maps:
                self._warehouses_data[tvd_name] = list()
                with self._warehouses_csv[tvd_name].open() as stream:
                    for line in stream.readlines():
                        string = line.split(sep=';')
                        self._warehouses_data[tvd_name].append({
                            'name': string[0],
                            'x': float(string[1]),
                            'z': float(string[2]),
                            'country': int(str(string[3]).rstrip('\n')),
                            'tvd_name': tvd_name
                        })
        return self._warehouses_data


class GeneratorParamsConfig:
    """Конфиг дефолтпарамсов"""
    def __init__(self):
        with open('.\\configs\\dfpr.json') as stream:
            self.cfg = json.load(stream)
