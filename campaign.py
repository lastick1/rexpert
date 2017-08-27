import draw
import pytz
import datetime
import json
from pathlib import Path
from cfg import MissionGenCfg, MainCfg, DfprCfg, StatsCustomCfg, Gameplay
from tvd import Tvd
import mission_report
import processing
import rcon
date_format = '%d.%m.%Y'


class MissingAType0(Exception):
    pass


class Mission:
    def __init__(self, name, objects):
        self.name = name
        self._force_complete = False
        self.atypes = []
        self.last_atype = 0
        self.m_report = mission_report.report.MissionReport(objects=objects)
        self.g_report = None
        self.processed_t14 = 0
        self.capture_coals = set()

    def update(self, data):
        """
        :type data: [(str, int)]
        """
        if len(data):
            atypes = list([mission_report.parse_mission_log_line.parse(x[0]) for x in data])
            self.atypes += atypes
            self.m_report.processing_rows(list(x[0] for x in data))
            if not self.g_report:
                self.g_report = mission_report.ground_report.GroundReport(self.src, self.name)
            self.g_report.process_ground_kills(self.m_report.sorties)
            self.last_atype = data[-1][1]

    @property
    def result_name(self):
        return 'result2' if 'result2' in self.at0['file_path'] else 'result1'

    @property
    def next_name(self):
        return 'result1' if 'result2' in self.at0['file_path'] else 'result2'

    @property
    def start(self):
        """ Время начала миссии """
        return datetime.datetime.strptime(self.name, 'missionReport(%Y-%m-%d_%H-%M-%S)')

    @property
    def last_change(self):
        """ Время последнего изменения в миссии """
        lgt = 0
        for at in self.captures:
            if at['tik'] > lgt:
                lgt = at['tik']
        return lgt

    @property
    def at0(self):
        """ Событие начала миссии """
        for x in self.atypes:
            if x['atype_id'] == 0:
                return x
        raise MissingAType0()

    @property
    def captures(self):
        """ Записи событий захватов в миссии """
        return [x for x in [x for x in self.atypes if x['atype_id'] == 8] if x['task_type_id'] == 14]

    @property
    def src(self):
        # TODO реализовать хранение исходников миссий в архиве
        src = mission_report.mission_src.MissionSrc(
            src=MainCfg.dogfight_folder.joinpath('.\\result1_src.Mission').absolute())
        if 'result2' in self.at0['file_path']:
            src = mission_report.mission_src.MissionSrc(
                src=MainCfg.dogfight_folder.joinpath('.\\result2_src.Mission').absolute())
        return src

    @property
    def online_ids(self):
        online_ids = set()
        for atype in sorted(list(x for x in self.atypes if x['atype_id'] in (20, 21)), key=lambda x: x['tik']):
            if atype['atype_id'] == 20:
                online_ids.add(atype['account_id'])
            if atype['atype_id'] == 21:
                if atype['account_id'] in online_ids:
                    online_ids.remove(atype['account_id'])
        return online_ids

    @property
    def is_ended(self):
        if self._force_complete:
            return True
        at7 = [x for x in self.atypes if x['atype_id'] == 7]
        if len(at7) > 1:
            raise Warning
        return False if len(at7) == 0 else True

    def complete(self):
        self._force_complete = True

    @property
    def tvd_name(self):
        for tvd_name in MissionGenCfg.maps:
            if tvd_name in self.src.guimap:
                return tvd_name
        raise NameError('Unknown TVD NAME')

    @property
    def date(self):
        return self.src.date

    @property
    def length(self):
        return datetime.timedelta(
            hours=MainCfg.mission_time['h'],
            minutes=MainCfg.mission_time['m'],
            seconds=MainCfg.mission_time['s']
        )

    @property
    def end(self):
        return self.start + self.length

    @property
    def score(self):
        triggered_m_objectives = list([x for x in self.atypes if x['atype_id'] == 8])  # сработавшие обжективы
        score = {'1': 0, '2': 0}  # счётчики результатов по коалициям
        reverted_coal = {1: '2', 2: '1'}
        boosts = {'1': [], '2': []}  # время начала ускорения [x1.5, x2]
        pauses = {'1': [], '2': []}  # паузы, когда счётчик останавливается
        # вычисляем моменты ускорения таймера, если были
        for mo in triggered_m_objectives:
            mo_cls = MissionGenCfg.cfg['objectives'][str(mo['task_type_id'])]
            if mo_cls == "boost":
                mo_delta = datetime.timedelta(seconds=int(mo['tik'] / 50))
                boosts[str(mo['coal_id'])].append(self.start + mo_delta)
        # вычисляем паузы таймера если были
        for mo in triggered_m_objectives:
            mo_cls = MissionGenCfg.cfg['objectives'][str(mo['task_type_id'])]
            if mo_cls == "tanks" and mo['success']:
                mo_delta = datetime.timedelta(seconds=int(mo['tik'] / 50))
                pauses[reverted_coal[mo['coal_id']]].append(self.start + mo_delta)
        # начисляем ежеминутные очки захвата с учётом ускорения
        i = self.start
        while i < self.end and i < datetime.datetime.now() - datetime.timedelta(seconds=30):
            for coal in ('1', '2'):
                paused = False  # остановлено ли время
                for pause in pauses[coal]:
                    if pause < i < pause + datetime.timedelta(minutes=15):
                        paused = True
                if paused:
                    continue
                score[coal] += 1
                for boost_time in boosts[coal]:
                    if boost_time < i:
                        score[coal] += 0.5
            i = i + datetime.timedelta(minutes=1)
        # начисляем стоимость целей в очках захвата
        for mo in triggered_m_objectives:
            mo_cls = MissionGenCfg.cfg['objectives'][str(mo['task_type_id'])]
            if mo_cls not in Gameplay.cfg['objectives'].keys():
                continue  # если цели не задана стоимость - игнорируем
            # coal = coal_reverse[str(mo['coal_id'])]  # у всех кроме десанта - коалиция накрест
            # if mo_cls == 'troops':
            coal = str(mo['coal_id'])
            score[coal] += Gameplay.cfg['objectives'][mo_cls]
        return {'red': score['1'], 'blue': score['2']}

    @property
    def commands(self):
        """ Команды о счёте (инфо) и захвате (инпуты) """
        r = []
        score = self.score.copy()
        score_msg = "Capture: Blue {0} / {2}, Red {1} / {2}".format(
            int(score['blue']) if score['blue'] < MainCfg.capture_pts else MainCfg.capture_pts,
            int(score['red']) if score['red'] < MainCfg.capture_pts else MainCfg.capture_pts,
            MainCfg.capture_pts)
        r.append(rcon.Command(self.name, cmd_type=rcon.CommandType.info, subject=score_msg))
        for side in score.keys():
            if int(score[side]) >= MainCfg.capture_pts:
                if side not in self.capture_coals:  # отправляем сервер-инпуты захвата один раз
                    self.capture_coals.add(side)
                    capture_inputs = {'red': 'r_capture_1', 'blue': 'b_capture_1'}
                    r.append(rcon.Command(
                        self.name, cmd_type=rcon.CommandType.s_input, subject=capture_inputs[side], reason=str(score)))
        return r


class Campaign:
    def __init__(self):
        """ Главный класс, отвечающий за управление ходом кампании на сервере """
        cache = Path(r'.\cache\campaign.json').absolute()
        if cache.exists():
            self.data = json.load(cache.open())
        else:
            init = Path(r'.\configs\c_start.json').absolute()
            self.data = json.load(init.open())
            self.save()
        # театры военных действий, используемые в кампании
        self.tvds = {x: Tvd(x, self.data[x]['current_date'], MissionGenCfg, MainCfg) for x in MissionGenCfg.maps}
        self.generations = dict()
        self.captures = dict()
        self._saved_plans = set()

    def save(self):
        cache = Path(r'.\cache\campaign.json').absolute()
        cache.write_text(json.dumps(self.data), encoding='utf-8')

    def update(self, m):
        """ Продвигаем кампанию вперёд (обработка захвата, генерация следующей миссии, переход между ТВД)
        :type m: Mission
        :return: None """
        m_tvd_name = m.tvd_name
        r = False
        if not m.is_ended:
            if m.name not in self._saved_plans:
                self.save_mission_info(m, m_tvd_name)
                self.save_mission_plan(m, m_tvd_name)
                self._saved_plans.add(m.name)
            for c in m.captures:
                if m.name not in self.captures.keys():
                    self.captures[m.name] = set()
                if c['tik'] not in self.captures[m.name]:
                    self.tvds[m_tvd_name].capture(c['pos']['x'], c['pos']['z'], c['coal_id'])
                    self.captures[m.name].add(c['tik'])
            # (пере)генерация следующей миссии
            self.tvds[m_tvd_name].date = m.date
            self.data[m_tvd_name]['current_date'] = m.date.strftime(date_format)
            if self.tvds[m_tvd_name].is_ended:
                n_tvd_name = self.next_tvd_name(m_tvd_name)
                if n_tvd_name == m_tvd_name:
                    self.finish()
                m_tvd_name = n_tvd_name
                self.data['current_tvd'] = m_tvd_name
            if m.name not in self.generations.keys():
                self.generations[m.name] = -1
            lc = m.last_change
            if lc > self.generations[m.name]:
                next_name = m.next_name
                print('[{}] Preparing next: {}'.format(
                    datetime.datetime.now().strftime("%H:%M:%S"),
                    next_name
                ))
                # обновляем папку твд с настройками default params
                self.tvds[m_tvd_name].update(DfprCfg.cfg[m_tvd_name])
                r = next_name, m_tvd_name
                self.generations[m.name] = lc
            self.save()
        return r

    def save_mission_info(self, m, m_tvd_name):
        """ Сохранение информации о миссии в JSON для сайта (UTC время конца, самолёты, дата миссии) """
        print('[{}] Saving mission INFO: {}'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            m.name
        ))
        period_id = self.tvds[m_tvd_name].current_date_stage_id
        m_length = datetime.timedelta(
            hours=MainCfg.mission_time['h'],
            minutes=MainCfg.mission_time['m'],
            seconds=MainCfg.mission_time['s']
        )
        m_start = datetime.datetime.strptime(
            m.name, 'missionReport(%Y-%m-%d_%H-%M-%S)').replace(tzinfo=datetime.timezone.utc)
        m_start.replace(tzinfo=pytz.timezone('Europe/Moscow'))
        utc_offset = datetime.datetime.now() - datetime.datetime.utcnow()
        result_utc_datetime = m_start - utc_offset + m_length

        data = {
            'period_id': period_id,
            'm_date': str(m.src.date),
            'm_end': int(result_utc_datetime.timestamp() * 1000),
            'plane_images': list(map(
                lambda x: StatsCustomCfg.cfg['mission_info']['plane_images_files'][x],
                StatsCustomCfg.cfg['mission_info']['available_planes_by_period_id'][str(period_id)]
            ))
        }
        data_file = MainCfg.stats_static.joinpath(StatsCustomCfg.cfg['mission_info']['json'])
        with data_file.open(mode='w') as f:
            json.dump(data, f)

    def save_mission_plan(self, msn, tvd_name):
        """ Сохранение плана миссии в JSON для il2missionplanner 
        :type msn: Mission
        :type tvd_name: str """
        print('[{}] Saving mission PLAN: {}'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            msn.name
        ))
        icons = msn.src.icons
        draw.draw_graph(
            self.tvds[tvd_name].grid.neutral_line,
            self.tvds[tvd_name].grid.areas,
            tvd_name,
            icons=icons
        )
        planner_max_x = StatsCustomCfg.cfg['il2missionplanner'][tvd_name]['right_top'][0]
        planner_max_z = StatsCustomCfg.cfg['il2missionplanner'][tvd_name]['right_top'][1]
        x_c = planner_max_x / MissionGenCfg.cfg[tvd_name]['right_top']['x']
        z_c = planner_max_z / MissionGenCfg.cfg[tvd_name]['right_top']['z']

        cut = [list((x.x, x.z) for x in self.tvds[tvd_name].grid.neutral_line)]
        frontline = draw.get_splines(cut)
        frontline_resize = []
        for lines_pair in frontline:
            frontline_resize.append([])
            for line in lines_pair:
                frontline_resize[-1].append([])
                for point in line:
                    frontline_resize[-1][-1].append([round(point[0] * x_c, 3), round(point[1] * z_c, 3)])
        # lat - z
        # lng - x
        targets = []
        for coal in icons.keys():
            for cls in icons[coal].keys():
                for i in icons[coal][cls]:
                    name = StatsCustomCfg.cfg['il2missionplanner']['icon_names_mapping'][cls]
                    color = 'blue' if coal == '2' else 'red'
                    if cls == 'flames':
                        color = 'red' if coal == '2' else 'blue'
                    notes = StatsCustomCfg.cfg['il2missionplanner']['icon_notes_mapping'][cls]
                    if cls == 'airfields':
                        name = i['name']
                    targets.append({
                        'latLng': {
                            'lng': round(i['x'] * x_c, 2),
                            'lat': round(i['z'] * z_c, 2)
                        },
                        'name': name,
                        'color': color,
                        'type': StatsCustomCfg.cfg['il2missionplanner']['icons_types_mapping'][cls],
                        'notes': notes
                    })
        data = {
            'mapHash': '#{}'.format(tvd_name),
            'routes': [],
            'points': targets,
            'frontline': frontline_resize
        }
        dest = Path(MainCfg.stats_static.joinpath(StatsCustomCfg.cfg['il2missionplanner']['json']))
        with dest.open(mode='w') as f:
            json.dump(data, f)

    @staticmethod
    def next_tvd_name(current):
        if len(MissionGenCfg.maps)-1 == MissionGenCfg.maps.index(current):
            return current
        else:
            return MissionGenCfg.maps[MissionGenCfg.maps.index(current)+1]

    @property
    def score(self):
        return

    def finish(self):
        raise NameError('Campaign finished!')
