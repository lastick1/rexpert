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
                p = self.get_player(account_id, s.nickname)  # берём игрока
                if datetime.strptime(p.last_mission, date_format) > datetime.strptime(self.name, date_format):
                    # если время последней миссии позже, чем обрабатываемая миссия, то ничего не делаем
                    # т.е. не обрабатываем повторно обработанные миссии
                    i += 1
                    continue
                # если время последней миссии раньше, чем обрабатываемая миссия,
                # то сбрасываем последний тик у икрока и обновляем последнюю миссию у игрока
                if datetime.strptime(p.last_mission, date_format) < datetime.strptime(self.name, date_format):
                    p.touch(self.name, -1)
                if s.tik_spawn >= p.last_tik:
                    i += 1
                    continue
                p.touch(self.name, s.tik_spawn)
                rear_start = self._is_rear_start(s)  # проверяем, стартовал ли с тылового
                s_ended = self._is_sortie_ended(s, i, s_count)  # определяем завершён ли вылет
                mods = len(s.weapon_mods_id)  # количество модификаций
                aircraft_cls = aircrafts.aircraft_types[s.aircraft_name]  # класс самолёта (лёгкий, средний, тяжёлый)
                if s_ended:
                    decision = self._decide_ended(s)
                    give_unlocks = decision['is_rtb'] and len(s.killboard)
                    if decision['return']:
                        if give_unlocks:
                            p.unlocks += 1
                        p.planes[aircraft_cls] += 1
                    else:
                        p.unlocks -= mods
                    self.log_decision(s, decision, give_unlocks)
                else:
                    decision = self._decide_permission(s, mods, rear_start)
                    if decision['remove']:
                        p.planes[aircraft_cls] -= 1
                    if decision['notify']:
                        self.notify_player()
                    self.log_unended(s, decision)
                    raise NameError('s')
                i += 1

    def _decide_permission(self, s, mods, rear_start):
        """ Принятие решения об уведомлении игрока, списании самолёта, разрешении на взлёт """
        return {'remove': False, 'rear_start': rear_start, 'notify': True, 'mods': mods, 'permission': True}

    def log_unended(self, s, desision):
        """ Логгирование решения по взлёту (списание самолёта) """
        file = Path('./logs/business_' + self.name + '.json')
        if file.exists():
            with file.open(encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = dict()
        if s.nickname not in data.keys():
            data[s.nickname] = dict()
        if s.tik_spawn not in data[s.nickname].keys():
            data[s.nickname][s.tik_spawn] = dict()
        data[s.nickname][s.tik_spawn].update(
            {
                'mods':''
            }
        )

    def log_decision(self, s, decision, give_unlocks):
        """ Логгирование решения по вылету
        :type s: Sortie
        :type decision: dict
        :type give_unlocks: bool"""
        file = Path('./logs/business_' + self.name + '.json')
        if file.exists():
            with file.open(encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = dict()
        if s.nickname not in data.keys():
            data[s.nickname] = dict()
        if s.tik_spawn not in data[s.nickname].keys():
            data[s.nickname][s.tik_spawn] = dict()
        data[s.nickname][s.tik_spawn].update(
            {
                'aircraft_name': s.aircraft_name,
                'give_unlocks': give_unlocks,
                'sortie_status': s.sortie_status,
                'aircraft_status': s.aircraft_status
            }.update(decision)
        )
        with file.open(mode='w', encoding='utf-8') as f:
            json.dump(data, f)

    def _decide_ended(self, s):
        """ Принять решение о списании возврате самолёта по резульатам вылета
        :type s: Sortie """
        craft = s.aircraft
        killer = s.bot.killers[0] if len(s.bot.killers) else None
        if s.sortie_status.is_not_takeoff:
            return {'return': False, 'reason': 'не взлетал', 'is_rtb': craft.is_rtb}
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
            return {'return': False, 'reason': 'убит пилот', 'is_rtb': craft.is_rtb}
        return {'return': True, 'reason': 'default', 'is_rtb': craft.is_rtb}

    def get_player(self, account_id, nickname):
        """ Получить объект игрока класса Player (инициализируется при необходимости)
        :rtype Player """
        # создаём объект игрока, если его ещё нет
        if account_id not in self.players.keys():
            self.players[account_id] = Player(account_id)
            # если игрок ещё не инициализирован в базе, завершаем этот процесс необходимыми данными
            if not self.players[account_id].initialized:
                self.players[account_id].initialize(nickname)  # создаём запись в базе
                self.players[account_id].unlocks = 1  # начальное количество модификаций
        return self.players[account_id]

    def _is_sortie_ended(self, s, i, count):
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

    def _unfinished_sortie(self, sortie, rear_start):
        """ Обработка незавершённого вылета
            :type sortie: Sortie """
        p = self.players[sortie.account_id]
        mods = len(sortie.weapon_mods_id)
        aircraft_cls = aircrafts.aircraft_types[sortie.aircraft_name]

        """if sortie.tik_takeoff:
            # если взлетел
            if self.can_take(p, aircraft_cls, rear_start) and self.can_use_mods(p, aircraft_cls, mods, rear_start):
                # с разрешением на взлёт (доступный самолёт и модификации)
                if sortie not in self.flying_sorties:
                    # отнимаем одократно один самолёт, до возвращения на базу
                    self.flying_sorties.add(sortie)
                    if not rear_start:
                        p.planes[aircraft_cls] -= 1
                        return -1
            else:
                # без разрешения на взлёт
                if sortie.sortie_status.is_in_flight:
                    self._commands.append(Command(
                        self.name,
                        tik=sortie.tik_spawn,
                        cmd_type=CommandType.kick,
                        account_id=sortie.account_id,
                        subject=sortie.nickname,
                        reason='Takeoff restricted: {} {} [{}] {} [{}]'.format(
                            sortie.nickname, p.planes, p.unlocks, sortie.aircraft_name, mods)
                    ))
                    return 0
        pass
        # вылет может быть всё же завершённым - диско
        if sortie.is_disco:
            self.used_sorties.add(sortie)
            if len(sortie.aircraft.damagers) > 0:
                # За диско с дамагерами минусуем один самолёт этого класса (light, medium или heavy)
                p.planes[aircrafts.aircraft_types[sortie.aircraft_name]] -= 1
                return -2
            return 1

        if sortie.aircraft_status.is_destroyed:
            self.used_sorties.add(sortie)
            return 2

        # уведомляем о состоянии гаража и доступных модификациях
        if sortie not in self.notified_sorties:
            self.notified_sorties.add(sortie)
            name = p.squad['tag'] if p.squad else p.nickname
            self._commands.append(Command(
                self.name,
                tik=sortie.tik_spawn,
                cmd_type=CommandType.message,
                account_id=sortie.account_id,
                subject='{} available planes: Light {}, Medium {}, Heavy {}'.format(
                    name, p.planes['light'], p.planes['medium'], p.planes['heavy']),
                reason='info message'
            ))
            self._commands.append(Command(
                self.name,
                tik=sortie.tik_spawn,
                cmd_type=CommandType.message,
                account_id=sortie.account_id,
                subject='{} your available modifications is {}'.format(p.nickname, p.unlocks),
                reason='info message'
            ))
            # предупреждаем о запрете или разрешении на взлёт
            if self.can_take(p, aircraft_cls, rear_start) and self.can_use_mods(p, aircraft_cls, mods, rear_start):
                message = 'Takeoff granted!'

            else:
                message = 'TAKEOFF is FORBIDDEN for you on this aircraft!'
            self._commands.append(Command(
                self.name,
                tik=sortie.tik_spawn,
                cmd_type=CommandType.message,
                account_id=sortie.account_id,
                subject=message,
                reason='info message'
            ))
        return 0"""

    def _finished_sortie(self, sortie, rear_start):
        """ Обработка завершённого вылета
            :type sortie: Sortie """
        p = self.players[sortie.account_id]
        mods = len(sortie.weapon_mods_id)
        aircraft_cls = aircrafts.aircraft_types[sortie.aircraft_name]
        # self.flying_sorties.remove(sortie)
        if datetime.strptime(p.last_mission, date_format) > datetime.strptime(self.name, date_format):
            # если время последней миссии позже, чем обрабатываемая миссия, то ничего не делаем
            # т.е. не обрабатываем повторно обработанные миссии
            return 'second'
        if datetime.strptime(p.last_mission, date_format) < datetime.strptime(self.name, date_format):
            # если время последней миссии раньше, чем обрабатываемая миссия, то обнуляем последний тик
            # и обновляем текущую миссию
            p.touch(self.name, -1)
        if not sortie.tik_spawn:
            raise NameError('None sortie tik spawn')
        if p.last_tik < sortie.tik_spawn:
            # если последний тик раньше, чем начальный тик вылета, то обновляем последний тик и обрабатываем вылет
            p.touch(self.name, sortie.tik_spawn)
        else:
            # не обрабатываем вылеты в миссии повторно
            return 'twice'

        """При взлёте с фронтового аэродрома,
        количество доступных самолётов соответствующей категории уменьшается на единицу
        и восполняется на единицу
        только при посадке на активном аэродроме на своей территории"""
        if sortie.tik_takeoff:
            if sortie.is_disco:
                if len(sortie.aircraft.damagers) > 0 or sortie.is_bailout:
                    # за диско с дамагом от кого-либо или прыжком не восполняем
                    # минусуем анлоки
                    p.unlocks -= mods
                    return -1
            if sortie.is_captured:
                # если пленён
                p.unlocks -= 1
                return -2
            if sortie.sortie_status.is_shotdown:
                # сбит - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return -3
            if sortie.sortie_status.is_ditched:
                # дитч - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return -4
            if sortie.sortie_status.is_crashed:
                # разбился - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return -5
            if sortie.aircraft_status.is_destroyed and not sortie.sortie_status.is_landed:
                # самолёт уничтожен - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return -6
            if len(sortie.killboard) > 0:
                """Увеличение данного лимита будет происходить только при успешном выполнении боевых вылетов
                - вылетов с уничтоженными наземными целями или сбитыми самолётами противника.
                Один такой вылет повышает количество модификаций игрока на единицу"""
                p.unlocks += 1

            # определяем, была ли посадка на фронтовом аэродроме (по последней известной позиции)
            is_ended_on_front = False
            for af in self.rear_airfields:
                if af.distance_to(sortie.aircraft.last_pos['x'], sortie.aircraft.last_pos['z']) > 5000:
                    is_ended_on_front = True
                    break
            if is_ended_on_front:
                # возвращаем самолёт в случае, если сел на фронтовом аэродроме
                p.planes[aircraft_cls] += 1
                return 1
            return 2
        else:
            # у не взлетевших минусуем самолёты только за смерть от противника
            killer = sortie.bot.killers[0] if len(sortie.bot.killers) else None
            is_ff = False
            if killer and killer.coal_id == sortie.coal_id:
                is_ff = True
            if not is_ff and sortie.bot.is_killed:
                p.planes[aircraft_cls] -= 1
            return 0
        p.planes[aircraft_cls] += 1
        return 10

    @staticmethod
    def can_take(player, a_cls, rear_start):
        """ Может ли игрок брать указанный тип самолёта при таком типе старта (с тылового или фронтового) """
        """С тыловых аэродромов игроки всегда могут взлететь. На любом типе"""
        if rear_start:
            return True
        if player.planes[a_cls] > 0:
            return True
        else:
            return False

    @staticmethod
    def can_use_mods(player, aircraft_cls, mods, rear_start):
        """ Может ли игрок брать указанное количество модификаций (анлоков) """
        """С тыловых аэродромов самолёты лёгкой и средней категории можно брать только без модификаций.
        Тяжёлые можно брать с модификациями с любых аэродромов."""
        if aircraft_cls in ['heavy']:
            return mods <= player.unlocks
        else:
            if rear_start:
                return mods <= 0
            else:
                return mods <= player.unlocks
