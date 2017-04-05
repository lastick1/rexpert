import datetime
import db
import json
connector = db.PGConnector


class Player:
    class PDict(dict):
        def __init__(self, callback):
            super(Player.PDict, self).__init__()
            self.callback = callback

        def __setitem__(self, item, value):
            # print("You are changing the value of {} to {}!".format(item, value))
            super(Player.PDict, self).__setitem__(item, value)
            self.callback(self)

    def __init__(self, account_id):
        """ Класс игрока, инкапсулирующий данные игрока и их обновление по результатам вылетов
        :param account_id: UUID игрока
        :type account_id: str """
        self.account_id = account_id
        self.squad = None
        self.user_id = None
        self.nickname = None
        self.last_mission = 'missionReport(1980-01-01_00-00-00)'
        self.last_tik = -1
        self.load()

    @property
    def initialized(self):
        return True if self.nickname else False

    @property
    def specialization(self):
        sp = connector.Player.select_specialization(self.account_id)
        if sp:
            if 'sorties_cls' not in sp.keys():
                return sp['specialization']
            sp_stats_spec = {
                'aircraft_light': sp['sorties_cls']['aircraft_light'],
                'aircraft_heavy': sp['sorties_cls']['aircraft_medium'] + sp['sorties_cls']['aircraft_heavy']
            }
            sp_stats = None
            for cls in sp_stats_spec.keys():
                if sp_stats_spec[cls] > 0:
                    if sp_stats:
                        if sp_stats_spec[cls] > sp_stats_spec[sp_stats]:
                            sp_stats = cls
                    else:
                        sp_stats = cls
            if sp_stats:
                return sp_stats
            else:
                return sp['specialization']
        raise NameError('Player must have specialization')

    def initialize(self, nickname, specialization):
        """ Инициализация игрока, если он ещё не известен программе """
        self.nickname = nickname
        if not self.nickname or len(self.nickname) == 0:
            raise NameError('Invalid data for initialization: {} {}'.format(self.account_id, nickname))

        connector.Player.initialize_player(self.account_id, nickname, specialization)
        print('[{}] {} {} {} initialized'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            self.nickname,
            self.account_id,
            specialization
        ))
        self.load()

    def load(self):
        """ Загрузка данных игрока из базы данных по его UUID """
        data = connector.Player.select_by_account(self.account_id)
        if data:
            self.user_id = data['user_id']
            self.nickname = data['nickname']
            self.last_mission = data['last_mission']
            self.last_tik = data['last_tik']
            if data['squad_id']:
                self.squad = {
                    'id': data['squad_id'],
                    'name': data['squad_name'],
                    'tag': data['squad_tag'],
                    'strength': data['squad_strength']
                }
                if not connector.Squad.get_planes(self.squad['id']):
                    connector.Squad.initialize(self.squad['id'])
                    print('[{}] squad {} initialized: {} id, {} strength'.format(
                        datetime.datetime.now().strftime("%H:%M:%S"),
                        data['squad_name'],
                        data['squad_id'],
                        data['squad_strength']
                    ))
                self.planes_to_squad()

    def __str__(self):
        if self.squad:
            return "[{}] {} [Planes:{}]".format(self.nickname, self.squad['name'], self.planes)
        else:
            return "[{}] [Planes:{}]".format(self.nickname, self.planes)

    def planes_to_squad(self):
        self.planes = self.planes

    def get_planes(self):
        if self.squad:
            data = connector.Squad.get_planes(self.squad['id'])
            err_msg = 'No such squad_id in custom_squads_extension {}'.format(self.account_id)
        else:
            data = connector.Player.get_planes(self.account_id)
            err_msg = 'No such account_id in custom_profiles_extension {}'.format(self.account_id)
        if data:
            planes = Player.PDict(self.set_planes)
            planes.update({'light': data['planes'][0], 'medium': data['planes'][1], 'heavy': data['planes'][2]})
            return planes
        else:
            raise NameError(err_msg)

    def set_planes(self, value):
        if self.squad:
            p_pln = connector.Player.get_planes(self.account_id)['planes']
            connector.Squad.set_planes(self.squad['id'], [
                value['light'] + (p_pln[0] if self.specialization == 'aircraft_light' else 0),
                value['medium'] + (p_pln[1] if self.specialization == 'aircraft_medium' else 0),
                value['heavy'] + (p_pln[2] if self.specialization == 'aircraft_heavy' else 0)])
            connector.Player.set_planes(self.account_id, [0, 0, 0])
        else:
            connector.Player.set_planes(self.account_id, [value['light'], value['medium'], value['heavy']])

    planes = property(fget=get_planes, fset=set_planes, doc="Самолёты игрока или сквада, если игрок в нём состоит")

    def get_unlocks(self):
        data = connector.Player.get_planes(self.account_id)
        if data:
            return data['unlocks']
        else:
            raise NameError('No such account_id in custom_profiles_extension {}'.format(self.account_id))

    def set_unlocks(self, value):
        if value < 0:
            value = 0
        connector.Player.set_unlocks(self.account_id, value)

    unlocks = property(fget=get_unlocks, fset=set_unlocks, doc="Количество модификаций, доступное игроку")

    def touch(self, last_mission, last_tik):
        connector.Player.touch(self.account_id, last_mission, last_tik)
        self.last_mission = last_mission
        self.last_tik = last_tik
