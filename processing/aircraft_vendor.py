"""Распределение самолётов по аэродромам"""
import random

import configs
from .campaign import CampaignMap


class MonthSupply:
    """Класс месячной поставки"""
    def __init__(self, date: str, csv_lines: list):
        self.month = date
        self.amounts = list()
        csv_lines.reverse()
        self.aircrafts = csv_lines.pop().split(';')[1:]
        csv_lines.reverse()
        for line in csv_lines:
            split = line.split(';')
            month = split[0]
            if date == month:
                self.amounts.extend(int(x) for x in split[1:])
        if len(self.amounts) != len(self.aircrafts):
            raise NameError('Некорректная поставка')

    def get_amounts_dict(self, name_convert) -> dict:
        """Сформировать поставку в формате словаря для MongoDB"""
        result = dict()
        for i in range(len(self.aircrafts)):
            result[name_convert(self.aircrafts[i])] = self.amounts[i]
        return result

    @property
    def has_aircrafts(self):
        """Остались ли самолёты в поставке"""
        return sum(self.amounts) > 0

    @property
    def remain_aircrafts(self) -> list:
        """Названия оставщихся самолётов"""
        result = list()
        for i in range(len(self.aircrafts)):
            if self.amounts[i] > 0:
                result.append(self.aircrafts[i])
        return result

    def take_aircrafts(self, aircraft_name, amount: int) -> int:
        """Взять самолёты из поставки"""
        self.amounts[self.aircrafts.index(aircraft_name)] -= amount
        return amount


class AircraftVendor:
    """Класс, распределяющий самолёты по аэродромам"""
    def __init__(self, config: configs.Planes, gameplay: configs.Gameplay):
        self.config = config
        self.gameplay = gameplay

    def get_month_supply(self, month: str, campaign_map: CampaignMap):
        """Сформировать месячную поставку"""
        map_supply_csv = self.gameplay.supply_csv[campaign_map.tvd_name]
        with map_supply_csv.open() as stream:
            return MonthSupply(month, stream.readlines())

    def transfer_aircrafts(self, aircraft_name, amount, month_supply, managed_airfield):
        """Переместить самолёты из поставки на аэродром"""
        aircraft_key = self.config.name_to_key(aircraft_name)
        if aircraft_key not in managed_airfield.planes:
            managed_airfield.planes[aircraft_key] = 0
        managed_airfield.planes[aircraft_key] += month_supply.take_aircrafts(aircraft_name, amount)

    def deliver_month_supply(self, campaign_map: CampaignMap, managed_airfields: dict, supply: MonthSupply):
        """Распределить месячную поставку на тыловые аэродромы"""
        if supply.month not in campaign_map.months:
            while supply.has_aircrafts:
                aircrafts = supply.remain_aircrafts
                aircraft_name = random.choice(aircrafts)
                country = self.config.cfg['uncommon'][aircraft_name]['country']
                managed_airfield = random.choice(list(x for x in managed_airfields[country]
                                                      if x.planes_count < self.gameplay.rear_max_power))
                self.transfer_aircrafts(aircraft_name, self.gameplay.supply_unit_size, supply, managed_airfield)
            campaign_map.months.append(supply.month)
        else:
            raise NameError('нельзя применять поставку дважды на одной карте')
