"""Обработка событий с наземкой (дамаг, киллы), расчёт уничтожения целей (артпозиций, складов и т.п.)"""
import configs
import log_objects


class GroundController:
    """Контроллер обработки событий с наземными объектами"""
    def __init__(self, objects: configs.Objects):
        self.objects = objects
        self.units = list()
        self.grounds = dict()

    def ground_object(self, tik: int, obj: log_objects.Ground, object_name: str, country_id: int,
                      coal_id: int, name: str, parent_id: int) -> None:
        """Появление объекта"""
        self.units.append(obj)

    def damage(self, attacker: log_objects.Object, damage: float, target: log_objects.Ground, pos: dict) -> None:
        """Обработать урон наземному объекту"""
        if target.cls_base == 'ground':
            self.grounds[str(pos)] = target

    def kill(self, attacker: log_objects.Object, target: log_objects.Ground, pos: dict) -> None:
        """Обработать уничтожение наземного объекта"""
        if target.cls_base == 'ground':
            key = str(pos)
            ground = self.grounds[key]
            target.killed = True
            if target is not ground:
                raise NameError('Wrong ground object reference')
        # Для целей другого типа ничего не делаем
