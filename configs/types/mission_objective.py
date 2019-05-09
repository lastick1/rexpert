"Модель описания mission objective из логов миссии"
from __future__ import annotations
from typing import Dict, Any


class MissionObjective:
    "Конфиг для Translator:MissionObjective"
    def __init__(self, _id: int, cfg: Dict[str, Any]):
        self.name: str = cfg['name']
        self.capture_points: int = int(cfg['capture_points'])
        self.id: int = _id
