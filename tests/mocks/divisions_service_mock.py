"""Заглушка сервиса дивизий"""
from configs import Config
from core.events import DivisionDamage
from services import DivisionsService


class DivisionsServiceMock(DivisionsService):
    """Заглушка сервиса дивизий"""
    def __init__(self, emitter, config: Config):
        super().__init__(emitter, config, None)
        self.damaged_divisions = set()

    def damage_division(self, damage: DivisionDamage):
        self.damaged_divisions.add(damage.unit_name.split(sep='_')[1])
