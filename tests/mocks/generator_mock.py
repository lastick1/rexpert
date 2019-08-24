"""Заглушки, фальшивки и т.п. для тестирования"""
from __future__ import annotations

from configs import Config
from processing import Generator



class GeneratorMock(Generator):
    """Заглушка генератора миссий"""

    def __init__(self, config: Config):
        super().__init__(config)
        self.generations = []

    def make_mission(self, mission_template: str, file_name: str, tvd_name: str):
        self.generations.append((file_name, tvd_name))

    def make_ldb(self, tvd_name: str):
        pass

