"""Управление графом"""
import pathlib
import shutil

import configs


class GridController:
    """Класс, выполняющий управление графами в кампании"""
    def __init__(self, config: configs.Config):
        self.config = config

    def initialize(self, tvd_name: str):
        """Инициализировать граф указанного твд в кампании"""
        xgml_file = str(self.config.mgen.xgml[tvd_name])
        tvd_dir = pathlib.Path(self.config.main.current_grid_folder.joinpath(tvd_name))
        if not tvd_dir.exists():
            tvd_dir.mkdir(parents=True)
        dest_file = str(tvd_dir.joinpath('{}_0.xgml'.format(tvd_name)))
        shutil.copy(xgml_file, dest_file)

    def capture(self, tvd_name: str, pos: dict, country: int):
        """Выполнить захват узла в указанной позиции"""
