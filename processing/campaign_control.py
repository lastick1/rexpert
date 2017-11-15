"""Контроль миссий и хода кампании"""
from pathlib import Path
from datetime import datetime
from configs import Main, Mgen
from generation import Generator


class Mission:
    """Миссия"""
    def __init__(self, name: str, source: Path, additional: dict):
        self.name = name
        self.source = source
        self.additional = additional


class CampaignController:
    """Контролеер"""
    def __init__(self, main: Main, mgen: Mgen, generator: Generator):
        self._dogfight = main.dogfight_folder
        self.missions = list()
        self.main = main
        self.mgen = mgen
        self.generator = generator

    def start_mission(self, date: datetime,
                      file_path: str,
                      game_type_id: int,
                      countries: dict,
                      settings: tuple,
                      mods: bool,
                      preset_id: int):
        """AType:0"""
        name = file_path.replace(r'Multiplayer/Dogfight', '').replace('\\', '')
        name = name.replace(r'.msnbin', '')
        source = Path(self._dogfight.joinpath(name + '_src.Mission')).absolute()
        additional = {
            'date': date,
            'game_type_id': game_type_id,
            'countries': countries,
            'settings': settings,
            'mods': mods,
            'preset_id': preset_id
        }
        self.missions.append(Mission(name, source, additional))
        next_name = 'result1' if name == 'result2' else 'result2'
        self.generator.make_mission(next_name, 'moscow')

    def end_mission(self):
        """AType:7"""
        pass
