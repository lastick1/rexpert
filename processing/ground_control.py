"""Обработка событий с наземкой (дамаг, киллы), расчёт уничтожения целей (артпозиций, складов и т.п.)"""
import log_objects
import atypes
import geometry


class GroundController:
    """Контроллер обработки событий с наземными целями"""
    def __init__(self):
        self.ground_kills = list()

    def kill(self, target: log_objects.Ground, atype: atypes.Atype3) -> None:
        """Обработать уничтожение наземного объекта"""
        if type(target) is log_objects.Ground:
            self.ground_kills.append(geometry.Point(x=atype.pos['x'], z=atype.pos['z']))
            target.kill(atype.pos)
        else:
            raise TypeError('target must be log_objects.Ground, not {}'.format(type(target)))
