import json
import datetime
from pathlib import Path
from random import randint

from geometry import Point
from .influences import BoundaryBuilder
from .grid import Grid
from .groups import Group, FrontLineGroup
from .weather import presets, WeatherPreset
from .xgml_io import Xgml
import configs

date_format = '%d.%m.%Y'
default_af_cache = {'moscow': '30.09.2016', 'stalingrad': '30.09.2016'}


class Stage:
    def __init__(self, raw, sides, af_templates_folder):
        """Класс этапа кампании, для которого создаются группы аэродромов с заданными самолётами"""
        self.start = datetime.datetime.strptime(raw['start'], date_format)
        self.end = datetime.datetime.strptime(raw['end'], date_format)
        self.id = int(raw['id'])
        self.af_templates = dict()
        for side in sides:
            self.af_templates[side] = af_templates_folder.joinpath(raw[side])

    def __contains__(self, item):
        return self.start <= item < self.end


class Boundary(Point):
    """Класс зоны влияния"""
    def __init__(self, x: float, z: float, polygon: list):
        super().__init__(x=x, z=z)
        self.polygon = polygon


class Tvd:
    def __init__(self, name, date, mgen: configs.Mgen, main: configs.Main, loc_cfg: configs.LocationsConfig, params: configs.GeneratorParamsConfig):
        """Класс театра военных действий (ТВД) кампании, для которого генерируются миссии"""
        self.name = name
        self.main = main
        self.mgen = mgen
        self.loc_cfg = loc_cfg
        self.params = params
        self.sides = mgen.cfg['sides']
        self.default_stages = mgen.default_stages[name]
        self.af_groups_folders = mgen.af_groups_folders[name]
        self.ldf_file = mgen.cfg[name]['ldf_file']
        self.tvd_folder = mgen.cfg[name]['tvd_folder']

        offset = 10000
        north = self.mgen.cfg[name]['right_top']['x'] + offset
        east = self.mgen.cfg[name]['right_top']['z'] + offset
        south = 0 - offset
        west = 0 - offset
        self.boundary_builder = BoundaryBuilder(north=north, east=east, south=south, west=west)

        self.date = datetime.datetime.strptime(date, date_format)
        self.id = mgen.cfg[name]['tvd']
        folder = main.game_folder.joinpath(Path(mgen.cfg[name]['tvd_folder']))
        self.default_params_file = folder.joinpath(mgen.cfg[name]['default_params_dest'])
        self.default_params_template_file = main.configs_folder.joinpath(
            mgen.cfg[name]['default_params_source'])
        self.icons_group_file = folder.joinpath(mgen.cfg[name]['icons_group_file'])
        self.right_top = mgen.cfg[name]['right_top']
        xgml = Xgml(name, mgen)
        xgml.parse()
        self.grid = Grid(name, xgml.nodes, xgml.edges, mgen)
        # таблица аэродромов с координатами
        self.airfields_data = tuple(
            (lambda z:
             {
                 'name': z[0],
                 'xpos': z[1],
                 'zpos': z[2]
             })(x.split(sep=';'))
            for x in mgen.af_csv[name].open().readlines()
        )
        # данные по сезонам из daytime.csv
        self.seasons_data = tuple(
            (lambda z:
             {
                 'start': z[0],
                 'end': z[1],
                 'sunrise': z[2],
                 'sunset': z[3],
                 'min_temp': int(z[4]),
                 'max_temp': int(z[5]),
                 'season_prefix': str(z[6]).rstrip()
             })(x.split(sep=';'))
            for x in mgen.daytime_files[name].open().readlines()
        )
        self.stages = tuple(
            Stage(x, self.sides, mgen.af_templates_folder) for x in mgen.stages[name]
        )

    def capture(self, x, z, coal_id):
        self.grid.capture(x, z, coal_id)

    def update(self):
        """Обновление групп, баз локаций и файла параметров генерации в папке ТВД (data/scg/x)"""
        print('[{}] Updating TVD folder: {} ({}) {}'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            self.tvd_folder,
            self.name,
            self.date_next.strftime(date_format)
        ))
        if self.is_ended:
            print('WARNING! Updating ended TVD: {}'.format(self.name))
        self.verify_grid()
        self.update_icons()
        self.update_ldb()
        self.update_airfields()
        self.randomize_defaultparams(self.params.cfg[self.name])

    def verify_grid(self):
        """Проверка и самопочинка графа"""
        # TODO доделать
        if not self.grid.border_nodes:
            # self.grid.restore_neutral_line()
            pass

    def update_icons(self):
        """Обновление группы иконок в соответствии с положением ЛФ"""
        print('[{}] generating icons group...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        border = self.grid.border
        nodes = self.grid.nodes_list
        influence_east = self.boundary_builder.influence_east(border)
        influence_west = self.boundary_builder.influence_west(border)
        confrontation_east = self.boundary_builder.confrontation_east(self.grid)
        confrontation_west = self.boundary_builder.confrontation_west(self.grid)
        east_boundary = Boundary(influence_east[0].x, influence_east[0].z, influence_east)
        west_boundary = Boundary(influence_west[0].x, influence_west[0].z, influence_west)
        east_influences = list(Boundary(node.x, node.z, node.neighbors_sorted) for node in nodes if node.country == 101)
        west_influences = list(Boundary(node.x, node.z, node.neighbors_sorted) for node in nodes if node.country == 201)
        east_influences.append(east_boundary)
        west_influences.append(west_boundary)
        east_influences.append(Boundary(confrontation_east[0].x, confrontation_east[0].z, confrontation_east))
        west_influences.append(Boundary(confrontation_west[0].x, confrontation_west[0].z, confrontation_west))
        areas = {
            101: east_influences,
            201: west_influences
        }
        flg = FrontLineGroup(
            self.grid.border, areas, self.mgen.icons_group_files[self.name], self.mgen.cfg[self.name]['right_top']
        )
        flg.make()
        print('... icons done')

    def update_ldb(self):
        """Обновление базы локаций до актуального состояния"""
        print('[{}] generating Locations Data Base (LDB)...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        border = self.grid.border
        areas = {
            101: self.boundary_builder.influence_east(border),
            201: self.boundary_builder.influence_west(border)
        }
        # TODO добавить модуль, который будет отвечать за выбор аэродромов и их глобальное состояние
        ldf = Ldb(self.name, areas, self.grid.scenarios, self.grid.border_nodes, self.main, self.mgen, self.loc_cfg)
        ldf.make()
        print('... LDB done')

    def update_airfields(self):
        """Генерация групп аэродромов для ТВД"""
        print('[{}] generating airfields groups...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        m_date_cache_file = Path(r'.\cache\airfields.json')
        if not m_date_cache_file.exists():
            m_date_cache_file.write_text(json.dumps(default_af_cache), encoding='utf-8')
        cache_data = json.load(m_date_cache_file.open())
        # with m_date_cache_file.open(mode='r') as f:
        cached_date = datetime.datetime.strptime(cache_data[self.name], date_format)

        d = datetime.timedelta(seconds=1)
        for side in self.sides:
            folder = self.af_groups_folders[side]
            # шаблон по-умолчанию
            template_group = self.default_stages[side]
            # ищем период для текущей даты ТВД
            for stage in self.stages:
                if self.date_next + d in stage:
                    if cached_date in stage:
                        print('... airfields generation skipped - same airfields generated already [{}]'.format(
                            cached_date.strftime(date_format)))
                        return
                    template_group = stage.af_templates[side]
                    print('... dated plane set [{}]'.format(side))
                    break
            for row in self.airfields_data:
                group = Group(template_group)
                group.clone_to(folder)
                group.rename('!x{}z{}'.format(row['xpos'], row['zpos']))
                group.replace_content('!AFNAME!', row['name'].title())

        cache_data[self.name] = self.date_next.strftime(date_format)
        m_date_cache_file.write_text(json.dumps(cache_data), encoding='utf-8')

    def date_day_duration(self, date):
        """Рассвет и закат для указанной даты"""
        season = self.season_data(date)
        sunrise = datetime.datetime(
            date.year,
            date.month,
            date.day,
            hour=int(season['sunrise'].split(sep=':')[0]),
            minute=int(season['sunrise'].split(sep=':')[1])
        )
        sunset = datetime.datetime(
            date.year,
            date.month,
            date.day,
            hour=int(season['sunset'].split(sep=':')[0]),
            minute=int(season['sunset'].split(sep=':')[1])
        )
        return sunrise, sunset - datetime.timedelta(hours=1, minutes=30)

    def season_data(self, date):
        """Информация по сезону на указанную дату (из daytime.csv)"""
        for season in self.seasons_data:
            start = datetime.datetime(
                date.year,
                int(season['start'].split(sep='.')[1]),
                int(season['start'].split(sep='.')[0])
            )
            end = datetime.datetime(
                date.year,
                int(season['end'].split(sep='.')[1]),
                int(season['end'].split(sep='.')[0])
            )
            if start <= date <= end:
                return season
        raise NameError('Season not found')

    @property
    def date_next_season_data(self):
        """Данные по сезону на дату следующей миссии"""
        return self.season_data(self.date_next)

    @property
    def date_next(self):
        """Дата следующей миссии этого ТВД"""
        d = datetime.timedelta(days=1)
        return self.date + d

    @property
    def date_end(self):
        """Дата окончания ТВД"""
        return self.stages[-1].end

    @property
    def date_next_day_duration(self):
        """Интервал светового дня для даты следующей миссии"""
        return self.date_day_duration(self.date_next)

    @property
    def is_ended(self):
        # TODO добавить проверку на завершение по территории
        return self.date_next > self.date_end

    @property
    def score(self):
        return NotImplemented

    @staticmethod
    def random_datetime(start, end):
        """Случайный момент времени между указанными значениями"""
        return start + datetime.timedelta(seconds=randint(0, int((end - start).total_seconds())))

    @property
    def next_date_stage_id(self):
        for stage in self.stages:
            if self.date_next in stage:
                return stage.id
        raise NameError('Incorrect date for all stages: {}'.format(self.date_next))

    @property
    def current_date_stage_id(self):
        for stage in self.stages:
            if self.date in stage:
                return stage.id
        raise NameError('Incorrect date for all stages: {}'.format(self.date))

    def randomize_defaultparams(self, params_config: dict):
        """Задать случайные параметры погоды, времени года и суток"""
        with self.default_params_template_file.open(encoding='utf-8-sig') as f:
            dfpr_lines = f.readlines()
        # случайное направление и сила ветра по высотам
        wind_direction0000 = randint(0, 360)
        wind_power0000 = randint(0, 2)

        date = Tvd.random_datetime(*self.date_next_day_duration)
        season = self.date_next_season_data
        # Случайная температура для сезона
        temperature = randint(season['min_temp'], season['max_temp'])

        for setting in params_config[season['season_prefix']]:
            for i in range(len(dfpr_lines)):
                if dfpr_lines[i].startswith('${} ='.format(setting)):
                    dfpr_lines[i] = '${} = {}\n'.format(
                        setting, params_config[season['season_prefix']][setting])
        weather_type = randint(*params_config[season['season_prefix']]['wtype_diapason'])

        w_preset = WeatherPreset(presets[weather_type])
        # задаём параметры defaultparams в соответствии с конфигом
        for y in range(len(dfpr_lines)):
            if dfpr_lines[y].startswith('$date ='):
                dfpr_lines[y] = '$date = {}\n'.format(date.strftime(date_format))
            elif dfpr_lines[y].startswith('$time ='):
                dfpr_lines[y] = '$time = {}\n'.format(date.strftime('%H:%M:%S'))
            elif dfpr_lines[y].startswith('$seasonprefix ='):
                sp = season['season_prefix']
                if sp == 'au':
                    sp = 'su'  # либо su либо wi должно быть season prefix
                dfpr_lines[y] = '$seasonprefix = {}\n'.format(sp)
            elif dfpr_lines[y].startswith('$sunrise ='):
                dfpr_lines[y] = '$sunrise = {}\n'.format(season['sunrise'])
            elif dfpr_lines[y].startswith('$sunset ='):
                dfpr_lines[y] = '$sunset = {}\n'.format(season['sunset'])
            elif dfpr_lines[y].startswith('$winddirection ='):
                dfpr_lines[y] = '$winddirection = {}\n'.format(wind_direction0000)
            elif dfpr_lines[y].startswith('$windpower ='):
                dfpr_lines[y] = '$windpower = {}\n'.format(wind_power0000)
            elif dfpr_lines[y].startswith('$turbulence ='):
                dfpr_lines[y] = '$turbulence = {}\n'.format(w_preset.turbulence)
            elif dfpr_lines[y].startswith('$cloudlevel ='):
                dfpr_lines[y] = '$cloudlevel = {}\n'.format(w_preset.cloudlevel)
            elif dfpr_lines[y].startswith('$cloudheight ='):
                dfpr_lines[y] = '$cloudheight = {}\n'.format(w_preset.cloudheight)
            elif dfpr_lines[y].startswith('$temperature ='):
                dfpr_lines[y] = '$temperature = {}\n'.format(temperature)
            elif dfpr_lines[y].startswith('$wtype ='):
                dfpr_lines[y] = '$wtype = {}\n'.format(weather_type)
            elif dfpr_lines[y].startswith('$prevwtype ='):
                dfpr_lines[y] = '$prevwtype = {}\n'.format(weather_type)
            elif dfpr_lines[y].startswith('$tvd ='):
                dfpr_lines[y] = '$tvd = {}\n'.format(params_config['tvd'])
            elif dfpr_lines[y].startswith('$overlay ='):
                dfpr_lines[y] = '$overlay = {}\n'.format(params_config['overlay'])
            elif dfpr_lines[y].startswith('$xposition ='):
                dfpr_lines[y] = '$xposition = {}\n'.format(params_config['xposition'])
            elif dfpr_lines[y].startswith('$zposition ='):
                dfpr_lines[y] = '$zposition = {}\n'.format(params_config['zposition'])
            elif dfpr_lines[y].startswith('$xtargetposition ='):
                dfpr_lines[y] = '$xtargetposition = {}\n'.format(params_config['xtargetposition'])
            elif dfpr_lines[y].startswith('$ztargetposition ='):
                dfpr_lines[y] = '$ztargetposition = {}\n'.format(params_config['ztargetposition'])
            elif dfpr_lines[y].startswith('$loc_filename ='):
                dfpr_lines[y] = '$loc_filename = {}\n'.format(self.ldf_file)
            elif dfpr_lines[y].startswith('$period ='):
                dfpr_lines[y] = '$period = {}\n'.format(self.next_date_stage_id)
        with self.default_params_file.open(mode='w', encoding='utf-8-sig') as f:
            f.writelines(dfpr_lines)
