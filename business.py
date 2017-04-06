import json
from pathlib import Path
from player import Player
from mission_report.report import Sortie
from rcon import Command, CommandType
from cfg import MissionGenCfg
from grid import Point
from datetime import datetime
import aircrafts
date_format = 'missionReport(%Y-%m-%d_%H-%M-%S)'


class Business:
    def __init__(self, m_name):
        """ Класс бизнес-логики (обработка вылетов) """
        self.name = m_name
        self.players = dict()
        self.used_sorties = set()
        self.flying_sorties = set()
        self.notified_sorties = set()
        self._commands = []
        self.is_mission_ended = False
        self.rear_airfields = []
        self.granted_permissions = set()

    @property
    def commands(self):
        r = []
        while len(self._commands):
            r.append(self._commands.pop())
        r.reverse()
        return r

    def update(self, sorties, is_mission_ended, tvd_name):
        """ Использовать вылет для обновления данных игроков и выполнения комманд
            :type sorties: list[Sortie]
            :type is_mission_ended: bool
            :type tvd_name: str """
        self.is_mission_ended = is_mission_ended
        self.rear_airfields = tuple(Point(x=x['x'], z=x['z']) for x in MissionGenCfg.cfg[tvd_name]['rear_airfields'])

        s_data = dict()
        for s in sorties:
            # если вылет уже использован или не пригоден для обработки - пропускаем
            if s.cls_base != 'aircraft' or s in self.used_sorties:
                continue

            # раскидываем sortie по account_id и обрабатываем каждого отдельно
            if s.account_id not in s_data.keys():
                s_data[s.account_id] = []
            s_data[s.account_id].append(s)
        self.process_players(s_data)

    def process_players(self, s_data):
        """ Последовательная обработка вылетов каждого игрока
        :type s_data: dict """
        for account_id in s_data.keys():
            s_count = len(s_data[account_id])
            i = 0
            while i < s_count:
                s = s_data[account_id][i]  # берём очередной вылет
                aircraft_cls = aircrafts.aircraft_types[s.aircraft_name]  # класс самолёта (лёгкий, средний, тяжёлый)
                p = self.get_player(account_id, s.nickname, 'aircraft_{}'.format(aircraft_cls))  # берём игрока

                rear_start = self._is_rear_start(s)  # проверяем, стартовал ли с тылового
                s_ended = self._is_sortie_ended(s, i, s_count)  # определяем завершён ли вылет
                mods = len(s.weapon_mods_id)  # количество модификаций
                if s_ended:
                    if datetime.strptime(p.last_mission, date_format) > datetime.strptime(self.name, date_format):
                        # если время последней миссии позже, чем обрабатываемая миссия, то ничего не делаем
                        # т.е. не обрабатываем повторно обработанные миссии
                        i += 1
                        continue
                    # если время последней миссии раньше, чем обрабатываемая миссия,
                    # то сбрасываем последний тик у икрока и обновляем последнюю миссию у игрока
                    if datetime.strptime(p.last_mission, date_format) < datetime.strptime(self.name, date_format):
                        p.touch(self.name, -1)
                    if s.tik_spawn <= p.last_tik:
                        i += 1
                        continue
                    p.touch(self.name, s.tik_spawn)
                    decision = self._decide_ended(s)
                    message = '{} {} {} '.format(s.nickname, s.aircraft_name, decision)
                    if decision['return']:
                        has_kill = False
                        for key in s.killboard.keys():
                            for obj in s.killboard[key]:
                                if s.coal_id != obj.coal_id:
                                    has_kill = True
                        if decision['is_rtb'] and has_kill:  # дать анлок за результативный вылет
                            p.unlocks += 1
                            message += '+mod '
                        if rear_start and decision['is_rtb'] and self.is_supply_valid(s):
                            p.planes[aircraft_cls] += 1  # добавляем самолёт за посадку на фронтовом при взлёте с тыла
                            message += '+plane({}) '.format(aircraft_cls)
                    else:
                        # списываем самолёт и анлоки при невозврате с фронтового аэродрома
                        if not rear_start:
                            if p.planes == 0:
                                raise NameError('Ты что творишь, сука!?')
                            p.unlocks -= mods
                            p.planes[aircraft_cls] -= 1
                            message += '-mods({}) -plane({}) '.format(mods, aircraft_cls)
                        else:
                            message += 'rear start '
                    with Path('./logs/business_' + self.name + '.txt').open(mode='a', encoding='utf-8') as f:
                        f.write(message + '\n')
                else:
                    self._interact(p, s, s_data, rear_start, mods)
                i += 1

    def _interact(self, p, s, s_data, rear_start, mods):
        """ Взаимодействие с игроком на сервере
        :type p: Player
        :type s: Sortie
        :type s_data: dict """
        aircraft_cls = aircrafts.aircraft_types[s.aircraft_name]  # класс самолёта (лёгкий, средний, тяжёлый)
        checkout = {'light': 0, 'medium': 0, 'heavy': 0}
        if p.squad:
            for account_id in s_data.keys():
                if account_id == p.account_id:
                    continue
                if len(s_data[account_id]):
                    sq_mate_s = s_data[account_id][-1]
                    sq_mate = self.get_player(
                        sq_mate_s.account_id,
                        sq_mate_s.nickname,
                        'aircraft_{}'.format(aircrafts.aircraft_types[sq_mate_s.aircraft_name]))
                    if not sq_mate.squad:
                        continue
                    if sq_mate.squad['id'] != p.squad['id']:
                        continue
                    if not sq_mate_s.is_disco and not sq_mate_s.is_ended and not self._is_rear_start(sq_mate_s):
                        checkout[aircrafts.aircraft_types[sq_mate_s.aircraft_name]] += 1
        aircraft_permission = self.can_take(p, aircraft_cls, rear_start, checkout)
        mods_permission = self.can_use_mods(p, aircraft_cls, mods, rear_start)

        if s.sortie_status.is_in_flight:
            if s not in self.granted_permissions:
                if not (aircraft_permission and mods_permission):  # кик за несанкционированный взлёт
                    if s.sortie_status.is_in_flight:
                        self._commands.append(Command(
                            self.name,
                            tik=s.tik_spawn,
                            cmd_type=CommandType.kick,
                            account_id=s.account_id,
                            subject=s.nickname,
                            reason='Takeoff restricted: {} | {}({}:{}){} | unlocks({}:{}){} | RS:{}'.format(
                                s.aircraft_name,
                                aircraft_cls,
                                p.planes[aircraft_cls],
                                checkout[aircraft_cls],
                                aircraft_permission,
                                p.unlocks,
                                mods,
                                mods_permission,
                                rear_start
                            )
                        ))
                else:
                    self.granted_permissions.add(s)
        else:
            # раскомментировать следующие 2 строки чтобы оповещать однократно
            if s not in self.notified_sorties:
                self.notified_sorties.add(s)
                name = p.squad['tag'] if p.squad else p.nickname
                self._commands.append(Command(
                    self.name,
                    tik=s.tik_spawn,
                    cmd_type=CommandType.message,
                    account_id=s.account_id,
                    subject='{} available planes: Light {}, Heavy {}'.format(
                        name,
                        p.planes['light'] - checkout['light'] if p.planes['light'] - checkout['light'] >= 0 else 0,
                        p.planes['heavy'] - checkout['heavy'] if p.planes['heavy'] - checkout['heavy'] >= 0 else 0
                    ),
                    reason='info message'
                ))
                self._commands.append(Command(
                    self.name,
                    tik=s.tik_spawn,
                    cmd_type=CommandType.message,
                    account_id=s.account_id,
                    subject='{} your available modifications is {}'.format(p.nickname, p.unlocks),
                    reason='info message'
                ))
                # предупреждаем о запрете или разрешении на взлёт
                if aircraft_permission and mods_permission:
                    message = 'Takeoff granted!'
                    self.granted_permissions.add(s)

                else:
                    message = 'TAKEOFF is FORBIDDEN for you on this aircraft!'
                self._commands.append(Command(
                    self.name,
                    tik=s.tik_spawn,
                    cmd_type=CommandType.message,
                    account_id=s.account_id,
                    subject=message,
                    reason='info message'
                ))

    @staticmethod
    def is_supply_valid(sortie):
        """ Является ли вылет снабжения действительным
        :param sortie: Sortie
        :return: bool """
        def distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        if not sortie.pos_start or not sortie.aircraft:
            return False
        if 5000.0 < distance(sortie.pos_start['x'], sortie.pos_start['z'],
                             sortie.aircraft.last_pos['x'], sortie.aircraft.last_pos['z']):
            return True
        else:
            return False

    @staticmethod
    def _decide_ended(s):
        """ Принять решение о списании возврате самолёта по резульатам вылета
        :type s: Sortie """
        craft = s.aircraft

        killer = s.bot.killers[0] if (s.bot and len(s.bot.killers)) else None
        if s.sortie_status.is_not_takeoff:
            return {'return': True, 'reason': 'не взлетал', 'is_rtb': craft.is_rtb}
        if s.is_disco and s.aircraft_damage > 5:
            return {'return': False, 'reason': 'диско с уроном', 'is_rtb': craft.is_rtb}
        if s.is_bailout:
            return {'return': False, 'reason': 'на тряпке', 'is_rtb': craft.is_rtb}
        if s.sortie_status.is_in_flight:
            return {'return': True, 'reason': 'завершил в воздухе', 'is_rtb': craft.is_rtb}
        if s.is_captured:
            return {'return': False, 'reason': 'плен', 'is_rtb': craft.is_rtb}
        if craft.life_status.is_destroyed and not craft.is_rtb:
            return {'return': False, 'reason': 'самолёт уничтожен', 'is_rtb': craft.is_rtb}
        if s.sortie_status.is_ditched and not craft.is_rtb:
            return {'return': True, 'reason': 'сел без поломки ВМГ вне базы (дитч)', 'is_rtb': craft.is_rtb}
        if s.sortie_status.is_crashed and not craft.is_rtb:
            return {'return': False, 'reason': 'сел с поломкой ВМГ вне базы (краш)', 'is_rtb': craft.is_rtb}
        if killer and killer.coal_id != s.coal_id:
            return {'return': False, 'reason': 'убит пилот кем-то', 'is_rtb': craft.is_rtb}
        if s.bot and s.bot.is_killed and not s.sortie_status.is_not_takeoff:
            return {'return': False, 'reason': 'умер после взлёта', 'is_rtb': craft.is_rtb}
        return {'return': True, 'reason': 'default', 'is_rtb': craft.is_rtb}

    def get_player(self, account_id, nickname, specialization):
        """ Получить объект игрока класса Player (инициализируется при необходимости)
        :rtype Player """
        # создаём объект игрока, если его ещё нет
        if account_id not in self.players.keys():
            self.players[account_id] = Player(account_id)
            # если игрок ещё не инициализирован в базе, завершаем этот процесс необходимыми данными
            if not self.players[account_id].initialized:
                self.players[account_id].initialize(nickname, specialization)  # создаём запись в базе
                self.players[account_id].unlocks = 1  # начальное количество модификаций
        return self.players[account_id]

    @staticmethod
    def _is_sortie_ended(s, i, count):
        """:type s: Sortie """
        if i < count-1 or s.is_ended or s.is_disco:
            return True
        return False

    def _is_rear_start(self, s):
        """:type s: Sortie"""
        for af in self.rear_airfields:
            if af.distance_to(s.pos_start['x'], s.pos_start['z']) < 5000:
                return True
        return False

    @staticmethod
    def can_take(player, a_cls, rear_start, checkout):
        """ Может ли игрок брать указанный тип самолёта при таком типе старта (с тылового или фронтового) """
        """С тыловых аэродромов игроки всегда могут взлететь. На любом типе"""
        if rear_start:
            return True
        if player.planes[a_cls] - checkout[a_cls] > 0:
            return True
        else:
            return False

    @staticmethod
    def can_use_mods(player, aircraft_cls, mods, rear_start):
        """ Может ли игрок брать указанное количество модификаций (анлоков) """
        """С тыловых аэродромов самолёты лёгкой и средней категории можно брать только без модификаций.
        Тяжёлые можно брать с модификациями с любых аэродромов."""
        # если самолётов нет, использовать анлоки нельзя
        if player.planes[aircraft_cls] == 0:
            return mods <= 0
        if aircraft_cls in ['heavy']:
            return mods <= player.unlocks
        else:
            if rear_start:
                return mods <= 0
            else:
                return mods <= player.unlocks
