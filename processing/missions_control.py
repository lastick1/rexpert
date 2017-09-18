"Контроль миссий и хода кампании"
from pathlib import Path
from datetime import datetime
class Mission:
    "Миссия"
    def __init__(self, name: str, source: Path, additional: dict):
        self.name = name
        self.source = source
        self.additional = additional


class CampaignController:
    "Контролеер"
    def __init__(self, dogfight: Path):
        self._dogfight = dogfight
        self.missions = list()

    def start_mission(self, date: datetime,
                      file_path: str,
                      game_type_id: int,
                      countries: dict,
                      settings: tuple,
                      mods: bool,
                      preset_id: int):
        "AType:0"
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

    def end_mission(self):
        "AType:7"
        pass
