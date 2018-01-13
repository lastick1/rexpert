"""Парсинг исходников миссий"""
import pathlib
import datetime

import configs
from .source_mission import SourceMission
from .source_re import GUIMAP_RE, MISSION_DATE_RE, SERVER_INPUT_RE, MISSION_OBJECTIVE_RE

SRC_DATE_FORMAT = '%d.%m.%Y'
DATE_FORMAT = '%d.%m.%Y'


def _find_date(text: str) -> str:
    """Найти значение даты миссии в исходнике"""
    for match in MISSION_DATE_RE.findall(text):
        return datetime.datetime.strptime(match, SRC_DATE_FORMAT).strftime(DATE_FORMAT)


def _find_server_inputs(mission: SourceMission, text: str):
    """Найти MCU сервер инпутов в миссии"""
    for match in SERVER_INPUT_RE.findall(text):
        mission.server_inputs.append({'name': match[0], 'pos': {'x': float(match[1]), 'z': float(match[2])}})


def _find_mission_objectives(mission: SourceMission, text: str):
    """Найти MCU Translator:Mission Objective в миссии"""
    for match in MISSION_OBJECTIVE_RE.findall(text):
        mission.objectives.append(
            {
                'obj_type': int(match[2]),
                'pos': {'x': float(match[0]), 'z': float(match[1])},
                'coalition': int(match[3]),
                'success': int(match[4])
            })


class SourceParser:
    """Извлекает данные из исходников миссий"""
    def __init__(self, config: configs.Config):
        self.config = config

    def parse_in_dogfight(self, name: str) -> SourceMission:
        """Считать миссию из исходника в папке dogfight"""
        source = self.config.main.dogfight_folder.joinpath('{}_src.Mission'.format(name))
        if source.exists():
            return self.parse(name, source)

    def _find_guimap(self, text: str) -> str:
        """Найти значение guimap в исходнике миссии"""
        for match in GUIMAP_RE.findall(text, pos=0, endpos=10000):
            for tvd_name in self.config.mgen.maps:
                if tvd_name in match:
                    return tvd_name

    def parse(self, name: str, path: pathlib.Path) -> SourceMission:
        """Считать миссию из исходника"""
        text = path.read_text()
        result = SourceMission(name=name, date=_find_date(text), guimap=self._find_guimap(text))
        _find_server_inputs(result, text)
        _find_mission_objectives(result, text)
        return result
