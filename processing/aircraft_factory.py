"""Распределение самолётов по аэродромам"""
import configs
from .campaign import CampaignMap


class MonthSupply:
    """Класс месячной поставки"""
    def __init__(self, date: str, csv_lines: list):
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


class AircraftFactory:
    """Класс, распределяющий самолёты по аэродромам"""
    def __init__(self, config: configs.Planes, gameplay: configs.Gameplay):
        self.config = config
        self.gameplay = gameplay

    def get_month_supply(self, month: str, campaign_map: CampaignMap):
        """Сформировать месячную поставку"""
        map_supply_csv = self.gameplay.supply_csv[campaign_map.tvd_name]
        with map_supply_csv.open() as stream:
            return MonthSupply(month, stream.readlines())
