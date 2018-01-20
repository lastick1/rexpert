"""Обработка событий с наземкой (дамаг, киллы), расчёт уничтожения целей (артпозиций, складов и т.п.)"""
import log_objects
import atypes
import geometry


class GroundController:
    """Контроллер обработки событий с наземными целями"""
    def __init__(self, ioc):
        self.ground_kills = list()
        self._ioc = ioc

    def start_mission(self):
        """Обработать начало миссии"""
        self.ground_kills.clear()

    def kill(self, atype: atypes.Atype3) -> None:
        """Обработать уничтожение наземного объекта"""
        target = self._ioc.objects_controller.get_object(atype.target_id)
        if isinstance(target, log_objects.Ground):
            self.ground_kills.append(geometry.Point(x=atype.pos['x'], z=atype.pos['z']))
            target.kill(atype.pos)
        else:
            raise TypeError('target must be log_objects.Ground, not {}'.format(type(target)))
