"""Управление графом
Текущее состояние хранится в папке из конфига (по-умолчанию в папке проекта папка current)
Состояние графа версионируется по изменению принадлежности его вершин"""
from __future__ import annotations
import os
import pathlib
import shutil

from core import EventsEmitter, Capture
from configs import Config
from model.grid import Grid

from processing import Xgml

from .base_event_service import BaseEventService


class GraphService(BaseEventService):
    """Класс, выполняющий управление графами в кампании"""

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config
    ):
        super().__init__(emitter)
        self._config = config
        self.xgml_folders = {tvd_name: pathlib.Path(self._config.main.current_grid_folder.joinpath(tvd_name))
                             for tvd_name in config.mgen.maps}

    def init(self) -> None:
        self.register_subscription(
            self.emitter.gameplay_capture.subscribe_(self._capture)
        )

    def _capture(self, capture: Capture) -> None:
        "Обработать событие захвата территории"
        self.capture(capture.tvd_name, capture.pos, capture.country)

    def initialize(self, tvd_name: str):
        """Инициализировать граф указанного ТВД в кампании"""
        xgml_file = str(self._config.mgen.xgml[tvd_name])
        tvd_dir = self.xgml_folders[tvd_name]
        if not tvd_dir.exists():
            tvd_dir.mkdir(parents=True)
        dest_file = str(tvd_dir.joinpath('{}_0.xgml'.format(tvd_name)))
        shutil.copy(xgml_file, dest_file)

    def reset(self, tvd_name: str):
        """Сбросить граф указанного ТВД в кампании"""
        for file in pathlib.Path(self.xgml_folders[tvd_name]).glob('*.xgml'):
            file.unlink()

    def get_file(self, tvd_name: str) -> str:
        """Получить последний файл графа для ТВД кампании"""
        files = pathlib.Path(self.xgml_folders[tvd_name]).glob('*.xgml')
        return list(sorted(list(str(x) for x in files), key=os.path.getmtime)).pop()

    def get_grid(self, tvd_name: str) -> Grid:
        """Получить граф указанного ТВД кампании"""
        xgml = Xgml(tvd_name, self._config.mgen)
        xgml.parse(self.get_file(tvd_name))
        return Grid(tvd_name, xgml.nodes, xgml.edges, self._config.mgen)

    def capture(self, tvd_name: str, pos: dict, country: int):
        """Выполнить захват узла в указанной позиции"""
        tvd_dir = self.xgml_folders[tvd_name]
        grid = self.get_grid(tvd_name)
        grid.capture(pos['x'], pos['z'], country)
        index = len(list(tvd_dir.glob('*.xgml')))
        file = str(tvd_dir.joinpath('{}_{}.xgml'.format(tvd_name, index)))
        xgml = Xgml(tvd_name, self._config.mgen)
        xgml.save_file(file, grid.nodes, grid.edges)
