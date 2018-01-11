"""Управление графом"""
import os
import pathlib
import shutil

import configs

from .xgml_io import Xgml
from .grid import Grid


class GridController:
    """Класс, выполняющий управление графами в кампании"""
    def __init__(self, config: configs.Config):
        self.config = config

    def _xgml_folder(self, tvd_name: str) -> pathlib.Path:
        """Получить путь к папке с историей графа"""
        return pathlib.Path(self.config.main.current_grid_folder.joinpath(tvd_name))

    def initialize(self, tvd_name: str):
        """Инициализировать граф указанного ТВД в кампании"""
        xgml_file = str(self.config.mgen.xgml[tvd_name])
        tvd_dir = self._xgml_folder(tvd_name)
        if not tvd_dir.exists():
            tvd_dir.mkdir(parents=True)
        dest_file = str(tvd_dir.joinpath('{}_0.xgml'.format(tvd_name)))
        shutil.copy(xgml_file, dest_file)

    def get_file(self, tvd_name: str) -> pathlib.Path:
        """Получить последний файл графа для ТВД кампании"""
        files = pathlib.Path(self._xgml_folder(tvd_name)).glob('*.xgml')
        return list(sorted(list(str(x) for x in files), key=os.path.getmtime)).pop()

    def capture(self, tvd_name: str, pos: dict, country: int):
        """Выполнить захват узла в указанной позиции"""
        tvd_dir = self._xgml_folder(tvd_name)
        xgml = Xgml(tvd_name, self.config.mgen)
        xgml.parse(self.get_file(tvd_name))
        grid = Grid(tvd_name, xgml.nodes, xgml.edges, self.config.mgen)
        grid.capture(pos['x'], pos['z'], country)
        index = len(list(tvd_dir.glob('*.xgml')))
        file = str(tvd_dir.joinpath('{}_{}.xgml'.format(tvd_name, index)))
        xgml.save_file(file, grid.nodes, grid.edges)
