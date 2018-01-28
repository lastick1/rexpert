"""Парсинг исходников миссий"""
import pathlib
import datetime

import configs
import model
from .source_re import GUIMAP_RE, MISSION_DATE_RE, SERVER_INPUT_RE, MISSION_OBJECTIVE_RE
from .source_re import AIRFIELD_RE, AIRFIELD_DATA_RE, TRIGGER_TIMER_RE

SRC_DATE_FORMAT = '%d.%m.%Y'
DATE_FORMAT = '%d.%m.%Y'


def _find_date(text: str) -> str:
    """Найти значение даты миссии в исходнике"""
    for match in MISSION_DATE_RE.findall(text):
        return datetime.datetime.strptime(match, SRC_DATE_FORMAT).strftime(DATE_FORMAT)


def _find_server_inputs(mission: model.SourceMission, text: str):
    """Найти MCU сервер инпутов в миссии"""
    for match in SERVER_INPUT_RE.findall(text):
        mission.server_inputs.append({'name': match[0], 'pos': {'x': float(match[1]), 'z': float(match[2])}})


def _find_mission_objectives(mission: model.SourceMission, text: str):
    """Найти MCU Translator:Mission Objective в миссии"""
    for match in MISSION_OBJECTIVE_RE.findall(text):
        mission.objectives.append(
            {
                'obj_type': int(match[2]),
                'pos': {'x': float(match[0]), 'z': float(match[1])},
                'coalition': int(match[3]),
                'success': int(match[4])
            }
        )


def _find_airfields(mission: model.SourceMission, text: str):
    """Найти аэродромы в исходнике миссии"""
    for match in AIRFIELD_RE.findall(text):
        data = AIRFIELD_DATA_RE.match(match).groupdict()
        mission.airfields.append(
            {
                'name': data['name'],
                'pos': {'x': float(data['XPos']), 'z': float(data['ZPos'])},
                'country': int(data['country'])
            }
        )


def _find_division_units_and_kind(mission: model.SourceMission, text: str):
    """Найти все юниты дивизий в исходнике миссий по триггерам (таймерам-меткам)"""
    for match in TRIGGER_TIMER_RE.findall(text):
        timer = {'name': match[0], 'pos': {'x': float(match[1]), 'z': float(match[2])}}
        if 'REXPERT' in timer['name']:
            if 'REGULAR' in timer['name']:
                mission.kind = 'regular'
                continue
            if 'ASSAULT' in timer['name']:
                mission.kind = 'assault'
                continue
            mission.division_units.append(timer)


class SourceParser:
    """Извлекает данные из исходников миссий"""
    def __init__(self, config: configs.Config):
        self._config = config

    def parse_in_dogfight(self, name: str) -> model.SourceMission:
        """Считать миссию из исходника в папке dogfight"""
        source = self._config.main.dogfight_folder.joinpath('{}_src.Mission'.format(name))
        if source.exists():
            return self.parse(name, source)

    def _find_guimap(self, text: str) -> str:
        """Найти значение guimap в исходнике миссии"""
        for match in GUIMAP_RE.findall(text, pos=0, endpos=10000):
            for tvd_name in self._config.mgen.maps:
                if tvd_name in match:
                    return tvd_name

    def parse(self, name: str, path: pathlib.Path) -> model.SourceMission:
        """Считать миссию из исходника"""
        text = path.read_text()
        result = model.SourceMission(
            name=name,
            file=path,
            date=_find_date(text),
            guimap=self._find_guimap(text)
        )
        _find_server_inputs(result, text)
        _find_mission_objectives(result, text)
        _find_airfields(result, text)
        _find_division_units_and_kind(result, text)
        return result
