import config
import pgconnector
from economics.payloads import types_map, aircraft_types, restricted_aircrafts, available_payloads
connector = pgconnector.PGConnector


class Aircraft:
    """ Класс самолёта, представляющий данные о самолёте и его цене """
    economic_statistics = None
    aircrafts = None

    def __init__(self, name, weight, fuel):
        self.name = name
        self.weight = weight
        self.value = born_formula(self.name)
        self.fuel = fuel
        self.payloads = {}
        self.mods = []
        self.k_type = config.Gameplay.economics['coefficients'][types_map[aircraft_types[self.name]]]
        self.supply_value = config.Gameplay.supply['amount'] * config.Gameplay.aircraft_multipliers[
            types_map[
                aircraft_types[
                    self.name]]]

    def price(self, payload_id):
        """ Цена указанной загрузки """
        if payload_id not in available_payloads[self.name]:
            return 0
        return self.payloads[payload_id].price

    @property
    def part_sorties_aircraft(self):
        """ Доля вылетов самолёта от всех вылетов по коалиции """
        coals_sorties = dict()
        aircraft_sorties = 0
        coal_id = None
        if Aircraft.economic_statistics:
            for x in Aircraft.economic_statistics:
                if x['coal_id'] not in coals_sorties:
                    coals_sorties[x['coal_id']] = x['sortie']
                    coal_id = x['coal_id']
                else:
                    coals_sorties[x['coal_id']] += x['sortie']
            for x in Aircraft.economic_statistics:
                if x['aircraft_name'] == self.name:
                    aircraft_sorties += x['sortie']
        if coal_id is not None:
            return aircraft_sorties / coals_sorties[coal_id]
        return 0

    @staticmethod
    def all_prices():
        """ Данные по всем ценам самолётов """
        data = dict()
        for a_name in Aircraft.aircrafts:
            if a_name in restricted_aircrafts:
                continue
            if a_name not in data:
                data[a_name] = dict()
            for payload_id in Aircraft.aircrafts[a_name].payloads:
                if payload_id not in available_payloads[a_name]:
                    continue
                data[a_name][payload_id] = (
                    Aircraft.aircrafts[a_name].payloads[payload_id].name,
                    Aircraft.aircrafts[a_name].payloads[payload_id].price,
                    Aircraft.aircrafts[a_name].payloads[payload_id].sorties
                )
        return data


class Payload:
    """ Класс комплектации вооружения """
    def __init__(self, name, log_id, weight, aircraft, fuel):
        self.name = name
        self.log_id = log_id
        self.weight = weight
        self.aircraft = aircraft
        self.fuel = fuel
        self._price = config.Gameplay.economics['min_price']

    @property
    def sorties(self):
        """ Вылеты загрузки """
        if Aircraft.economic_statistics:
            for x in Aircraft.economic_statistics:
                if x['aircraft_name'] == self.aircraft.name and x['payload_id'] == self.log_id:
                    return x['sortie']
        return 0

    @property
    def part_points_payload(self):
        """ Доля очков загрузки от всех очков, набитых самолётом"""
        payloads_points = dict()
        if Aircraft.economic_statistics:
            for x in Aircraft.economic_statistics:
                if x['aircraft_name'] not in payloads_points:
                    payloads_points[x['aircraft_name']] = x['points'] if x['points'] > 0 else 1
                else:
                    payloads_points[x['aircraft_name']] += x['points']
            for x in Aircraft.economic_statistics:
                if x['aircraft_name'] == self.aircraft.name and x['payload_id'] == self.log_id:
                    return x['points'] / payloads_points[x['aircraft_name']]
        return 0

    @property
    def part_sorties_payload(self):
        """ Доля вылетов загрузки от всех вылетов самолёта"""
        aircrafts_sorties = dict()
        if Aircraft.economic_statistics:
            for x in Aircraft.economic_statistics:
                if x['aircraft_name'] not in aircrafts_sorties:
                    aircrafts_sorties[x['aircraft_name']] = x['sortie']
                else:
                    aircrafts_sorties[x['aircraft_name']] += x['sortie']
            for x in Aircraft.economic_statistics:
                if x['aircraft_name'] == self.aircraft.name and x['payload_id'] == self.log_id:
                    return x['sortie'] / aircrafts_sorties[x['aircraft_name']]
        return 0

    @property
    def price(self):
        """ Цена загрузки для указанной заправки """
        return self.manul_formula

    @property
    def manul_formula(self):
        """ Формула расчёта стоимости самолёта """
        # вес оружия у бомбардировщиков или цена по формуле Бьёрна у истребителей
        w = self.weight if not self.aircraft.value else self.aircraft.value / 3000
        k_type = self.aircraft.k_type  # коэффициент типа
        ppp = self.part_points_payload  # доля очков   загрузки по самолёту
        psa = self.aircraft.part_sorties_aircraft  # доля вылетов самолёта по коалиции
        psp = self.part_sorties_payload  # доля вылетов загрузки по самолёту
        kw = config.Gameplay.k['w']  # коэффициент влияния веса оружия на базу
        kb = config.Gameplay.k['b']  # коэффициент базы (регулировка общего уровня цен - всех сразу)
        ks = config.Gameplay.k['s']  # коэффициент влияния доли вылетов самолёта по коалиции
        kp = config.Gameplay.k['p']  # коэффициент влияния доли очков   загрузки по самолёту
        kl = config.Gameplay.k['l']  # коэффициент влияния доли вылетов загрузки по самолёту
        min_p = 0.0
        max_p = 0.5
        if psa < min_p:
            psa = min_p
        if ppp < min_p:
            ppp = min_p
        if psp < min_p:
            psp = min_p

        if psa > max_p:
            psa = max_p
        if ppp > max_p:
            ppp = max_p
        if psp > max_p:
            psp = max_p

        if self.log_id == 0:
            kp /= 2
            kl /= 2
        base = (w * kw * k_type) * kb
        kk = 1 + psp * kl + ppp * kp + psa * ks
        price = int(base * kk)
        if price < config.Gameplay.economics['min_price']:
            price = config.Gameplay.economics['min_price']
        elif price > config.Gameplay.economics['max_price']:
            price = config.Gameplay.economics['max_price']
        return price

    def manul_formula_with_fuel(self, f, pct_f, k_type, psp, ppp, psa):
        """ Формула расчёта стоимости самолёта
        :param w: вес оружия
        :param f: вес топлива (полного бака)
        :param pct_f: процент заправки
        :param k_type: коэффициент типа
        :param psp: доля вылетов загрузки по самолёту
        :param ppp: доля очков   загрузки по самолёту
        :param psa: доля вылетов самолёта по коалиции
        :return: цена """
        kw = config.Gameplay.k['w']  # коэффициент влияния веса оружия на базу
        kf = config.Gameplay.k['f']  # коэффицинет влияния веса топлива на базу
        kb = config.Gameplay.k['b']  # коэффициент базы (регулировка общего уровня цен - всех сразу)
        ks = config.Gameplay.k['s']  # коэффициент влияния доли вылетов самолёта по коалиции
        kp = config.Gameplay.k['p']  # коэффициент влияния доли очков   загрузки по самолёту
        kl = config.Gameplay.k['l']  # коэффициент влияния доли вылетов загрузки по самолёту
        min_p = 0.0
        if psp < min_p:
            psp = min_p
        if psa < min_p:
            psa = min_p
        if ppp < min_p:
            ppp = min_p
        base = (self.weight * kw * k_type + f * pct_f / 100 * kf) * kb
        kk = 1 + psp * kl + ppp * kp + psa * ks
        price = int(base * kk - base)  # int(base * kk)
        if price < config.Gameplay.economics['min_price']:
            price = config.Gameplay.economics['min_price']
        elif price > config.Gameplay.economics['max_price']:
            price = config.Gameplay.economics['max_price']
        return price


def born_formula(a_name):
    return config.Metadata.horse_power[a_name] * config.Metadata.max_speed[a_name]


def aircrafts():
    """ Загрузить данные самолётов из payloads.csv """
    aircrafts = {}
    with config.payload_csv().open() as csv:
        lines = csv.readlines()[1:]
        current = ''
        for line in lines:
            spl = line.split(sep=';')
            if spl[0] != current:
                current = spl[0]
                aircrafts[current] = Aircraft(spl[0], int(spl[3]), int(spl[5]))
            aircrafts[current].payloads[int(spl[1])] = (
                Payload(spl[2], int(spl[1]), int(spl[4]), aircrafts[current], int(spl[5])))
        return aircrafts
