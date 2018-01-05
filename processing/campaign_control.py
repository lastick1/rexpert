"""Контроль миссий и хода кампании"""
import json
from pathlib import Path
import datetime

import pytz

import draw
from configs import Main, Mgen
from generation import Generator


class Mission:
    """Миссия"""
    def __init__(self, name: str, source: Path, additional: dict):
        self.name = name
        self.source = source
        self.additional = additional


class CampaignController:
    """Контролеер"""
    def __init__(self, main: Main, mgen: Mgen, generator: Generator):
        self.current_tvd = 'moscow'  # TODO убрать заглушку и реализовать свойство
        self._dogfight = main.dogfight_folder
        self.missions = list()
        self.main = main
        self.mgen = mgen
        self.generator = generator

    def initialize(self):
        """Инициализировать кампанию в БД"""

    def start_mission(self, date: datetime,
                      file_path: str,
                      game_type_id: int,
                      countries: dict,
                      settings: tuple,
                      mods: bool,
                      preset_id: int):
        """AType:0"""
        name = file_path.replace(r'Multiplayer/Dogfight', '').replace('\\', '')
        name = name.replace(r'.msnbin', '')
        source = Path(self._dogfight.joinpath(name + '_src.Mission')).absolute()
        additional = {
            'date': date,
            'game_type_id': game_type_id,
            'countries': countries,
            'settings': settings,
            'mods': mods,
            'preset_id': preset_id
        }
        self.missions.append(Mission(name, source, additional))
        next_name = 'result1' if name == 'result2' else 'result2'
        self.generator.make_mission(next_name, 'moscow')

    def end_mission(self):
        """AType:7"""
        pass

    def save_mission_info(self, m, m_tvd_name):
        """ Сохранение информации о миссии в JSON для сайта (UTC время конца, самолёты, дата миссии) """
        print('[{}] Saving mission INFO: {}'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            m.name
        ))
        period_id = self.tvds[m_tvd_name].current_date_stage_id
        m_length = datetime.timedelta(
            hours=self.main.mission_time['h'],
            minutes=self.main.mission_time['m'],
            seconds=self.main.mission_time['s']
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
                lambda x: self.stats.cfg['mission_info']['plane_images_files'][x],
                self.stats.cfg['mission_info']['available_planes_by_period_id'][str(period_id)]
            ))
        }
        with self.mission_info_file.open(mode='w') as stream:
            json.dump(data, stream)

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
            self.tvds[tvd_name].grid.border_nodes,
            self.tvds[tvd_name].grid.areas,
            tvd_name,
            icons=icons
        )
        planner_max_x = StatsCustomCfg.cfg['il2missionplanner'][tvd_name]['right_top'][0]
        planner_max_z = StatsCustomCfg.cfg['il2missionplanner'][tvd_name]['right_top'][1]
        x_c = planner_max_x / self.cfg[tvd_name]['right_top']['x']
        z_c = planner_max_z / self.cfg[tvd_name]['right_top']['z']

        cut = [list((x.x, x.z) for x in self.tvds[tvd_name].grid.border_nodes)]
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
                    name = self.stats.cfg['il2missionplanner']['icon_names_mapping'][cls]
                    color = 'blue' if coal == '2' else 'red'
                    if cls == 'flames':
                        color = 'red' if coal == '2' else 'blue'
                    notes = self.stats.cfg['il2missionplanner']['icon_notes_mapping'][cls]
                    if cls == 'airfields':
                        name = i['name']
                    targets.append({
                        'latLng': {
                            'lng': round(i['x'] * x_c, 2),
                            'lat': round(i['z'] * z_c, 2)
                        },
                        'name': name,
                        'color': color,
                        'type': self.stats.cfg['il2missionplanner']['icons_types_mapping'][cls],
                        'notes': notes
                    })
        data = {
            'mapHash': '#{}'.format(tvd_name),
            'routes': [],
            'points': targets,
            'frontline': frontline_resize
        }
        dest = Path(self.main.stats_static.joinpath(self.stats.cfg['il2missionplanner']['json']))
        with dest.open(mode='w') as f:
            json.dump(data, f)

