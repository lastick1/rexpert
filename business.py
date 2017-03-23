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

        for s in sorties:
            # если вылет уже использован или не пригоден для обработки - пропускаем
            if s in self.used_sorties or s.cls_base != 'aircraft':
                continue
            # создаём объект игрока, если его ещё нет
            if s.account_id not in self.players.keys():
                self.players[s.account_id] = Player(s.account_id)
                # если игрок ещё не инициализирован в базе, завершаем этот процесс необходимыми данными
                if not self.players[s.account_id].initialized:
                    self.players[s.account_id].initialize(s.nickname)  # создаём запись в базе
                    self.players[s.account_id].unlocks = 1  # начальное количество модификаций
            # определяем, вылет был начат с тылового или с фронтового аэродрома
            rear_start = False
            for af in self.rear_airfields:
                if af.distance_to(s.pos_start['x'], s.pos_start['z']) < 4000:
                    rear_start = True
            # если миссия не завершена - обрабатываем по-другому
            if not s.is_ended and not self.is_mission_ended:
                self._unfinished_sortie(s, rear_start)
                continue
            self._finished_sortie(s, rear_start)
            self.used_sorties.add(s)

    def _unfinished_sortie(self, sortie, rear_start):
        """ Обработка незавершённого вылета
            :type sortie: Sortie """
        p = self.players[sortie.account_id]
        mods = len(sortie.weapon_mods_id)
        aircraft_cls = aircrafts.aircraft_types[sortie.aircraft_name]

        if sortie.tik_takeoff:
            # если взлетел
            if self.can_take(p, aircraft_cls, rear_start) and self.can_use_mods(p, aircraft_cls, mods, rear_start):
                # с разрешением на взлёт (доступный самолёт и модификации)
                if sortie not in self.flying_sorties:
                    # отнимаем одократно один самолёт, до возвращения на базу
                    self.flying_sorties.add(sortie)
                    if not rear_start:
                        p.planes[aircraft_cls] -= 1
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
        pass
        # вылет может быть всё же завершённым - диско
        if sortie.is_disco:
            if len(sortie.aircraft.damagers) > 0:
                # За диско с дамагерами минусуем один самолёт этого класса (light, medium или heavy)
                p.planes[aircrafts.aircraft_types[sortie.aircraft_name]] -= 1
            self.used_sorties.add(sortie)
            return

        if sortie.aircraft_status.is_destroyed:
            self.used_sorties.add(sortie)
            return

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
            return
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
            return

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
                    return
            if sortie.sortie_status.is_shotdown:
                # сбит - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return
            if sortie.sortie_status.is_ditched:
                # дитч - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return
            if sortie.sortie_status.is_crashed:
                # разбился - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return
            if sortie.aircraft_status.is_destroyed:
                # самолёт уничтожен - не восполняем
                # минусуем анлоки
                p.unlocks -= mods
                return
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
        else:
            # у не взлетевших минусуем самолёты только за смерть от противника
            killer = sortie.bot.killers[0] if len(sortie.bot.killers) else None
            is_ff = False
            if killer and killer.coal_id == sortie.coal_id:
                is_ff = True
            if not is_ff and sortie.bot.is_killed:
                p.planes[aircraft_cls] -= 1
        pass

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
