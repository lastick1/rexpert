"""Контроль ТВД"""

DEFAULT_VALUE = 100
DIVISIONS_COUNT = 4
SUPPLY_COUNT = 2


class Division:
    """Повреждаемый объект"""
    def __init__(self, value: int, coal_id: int, name: str):
        self.value = value
        self.max = value
        self.name = name
        self.coal_id = coal_id

    def __str__(self) -> str:
        return '{}:{}.'.format(self.name, self.value)

    def damage(self, amount: int):
        """Принять урон"""
        if amount > self.value:
            self.value = 0
        else:
            self.value -= amount

class Supply(Division):
    """Объект снабжения"""
    def __init__(self, value: int, coal_id: int, name: str, divisions: list):
        super().__init__(value, coal_id, name)
        self._default = value
        self.divisions = divisions

    def repair(self, objects: list, power: float) -> None:
        """Отремонтировать объекты"""
        repair = int(self.value / len(objects)  * power)
        self.value = 0
        for obj in sorted(objects, key=lambda x: x.value):
            if obj.value + repair > obj.max:
                repair -= obj.max - obj.value
                obj.value = obj.max
            else:
                obj.value += repair
                repair = 0

    def resupply(self):
        """Восполнить ресурсы"""
        self.value = self._default

class DivisionsManager:
    """Управление дивизиями"""
    def __init__(self, value: int, repair: int, power: float):
        self.value = value
        self.power = power
        self.supply = dict()
        self.supply_damage = dict()
        self.divisions = dict()
        self.divisions_damage = dict()
        name = 'R1'
        self.divisions[name] = Division(value, 1, name)
        name = 'R2'
        self.divisions[name] = Division(value, 1, name)
        name = 'R3'
        self.divisions[name] = Division(value, 1, name)
        name = 'R4'
        self.divisions[name] = Division(value, 1, name)
        name = 'B1'
        self.divisions[name] = Division(value, 2, name)
        name = 'B2'
        self.divisions[name] = Division(value, 2, name)
        name = 'B3'
        self.divisions[name] = Division(value, 2, name)
        name = 'B4'
        self.divisions[name] = Division(value, 2, name)
        name = 'SR1'
        self.supply[name] = Supply(repair, 1, name, [self.divisions['R1'], self.divisions['R2']])
        name = 'SR2'
        self.supply[name] = Supply(repair, 1, name, [self.divisions['R3'], self.divisions['R4']])
        name = 'SB1'
        self.supply[name] = Supply(repair, 2, name, [self.divisions['B1'], self.divisions['B2']])
        name = 'SB2'
        self.supply[name] = Supply(repair, 2, name, [self.divisions['B3'], self.divisions['B4']])

    def damage_division(self, name: str, amount: int) -> None:
        """Нанести урон дивизии"""
        # self.divisions[name].damage(amount)
        if name not in self.divisions_damage:
            self.divisions_damage[name] = 0
        self.divisions_damage[name] += amount

    def damage_supply(self, name: str, amount: int) -> None:
        """Нанести урон снабжению"""
        if name not in self.supply_damage:
            self.supply_damage[name] = 0
        self.supply_damage[name] += amount

    def start_mission(self):
        self.divisions_damage = dict()
        self.supply_damage = dict()
        for name in self.supply:
            self.supply[name].resupply()

        for name in sorted(self.divisions.keys()):
            division = self.divisions[name]
            print(division)

    def end_mission(self):
        """Обсчитать завершение миссиии"""
        print('X')
        for name in  sorted(self.divisions_damage):
            print('{}: -{}'.format(name, self.divisions_damage[name]))
            self.divisions[name].damage(self.divisions_damage[name])
        for name in  sorted(self.supply_damage):
            print('{}: -{}'.format(name, self.supply_damage[name]))
            self.supply[name].damage(self.supply_damage[name])
        for name in self.supply:
            supply = self.supply[name]
            supply.repair(supply.divisions, self.power)

        for name in sorted(self.divisions.keys()):
            division = self.divisions[name]
            if division.value < 30:
                print('{} Division destroyed!'.format(division))
                division.value = self.value
        print()

manager = DivisionsManager(100, 40, 1.6)


for i in range(5):
    print(i+1)
    manager.start_mission()
    manager.damage_supply('SB1', 15)
    manager.damage_division('B1', 35)
    manager.damage_division('B2', 35)

    manager.damage_supply('SB2', 15)
    manager.damage_division('B3', 35)
    manager.damage_division('B4', 35)
    manager.end_mission()
manager.start_mission()
# manager.damage_division('B4', 10)
# manager.damage_supply('SB2', 40)
# manager.end_mission()
