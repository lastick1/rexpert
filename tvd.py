import json
import weather
import datetime
from pathlib import Path
from random import randint
from cfg import MissionGenCfg, MainCfg, DfprCfg
from grid import Grid
from gen import Group, Ldb, FlGroup
# from campaign import Mission

date_format = '%d.%m.%Y'
default_af_cache = {'moscow': '30.09.2016', 'stalingrad': '30.09.2016'}


class Stage:
    def __init__(self, raw):
        """ Класс этапа кампании, для которого создаются группы аэродромов с заданными самолётами """
        self.start = datetime.datetime.strptime(raw['start'], date_format)
        self.end = datetime.datetime.strptime(raw['end'], date_format)
        self.id = int(raw['id'])
        self.af_templates = dict()
        for side in MissionGenCfg.cfg['sides']:
            self.af_templates[side] = MissionGenCfg.af_templates_folder.joinpath(raw[side])

    def __contains__(self, item):
        return self.start <= item < self.end


class Tvd:
    def __init__(self, name, date):
        """ Класс театра военных действий (ТВД) кампании, для которого генерируются миссии """
        self.name = name
        self.date = datetime.datetime.strptime(date, date_format)
        self.id = MissionGenCfg.cfg[name]['tvd']
        self.folder = MainCfg.game_folder.joinpath(Path(MissionGenCfg.cfg[name]['tvd_folder']))
        self.default_params_file = self.folder.joinpath(MissionGenCfg.cfg[name]['default_params_dest'])
        self.default_params_template_file = MainCfg.configs_folder.joinpath(
            MissionGenCfg.cfg[name]['default_params_source'])
        self.icons_group_file = self.folder.joinpath(MissionGenCfg.cfg[name]['icons_group_file'])
        self.right_top = MissionGenCfg.cfg[name]['right_top']
        self.grid = Grid(self.name)
        self.grid.read_db()
        # таблица аэродромов с координатами
        self.airfields_data = tuple(
            (lambda z:
             {
                 'name': z[0],
                 'xpos': z[1],
                 'zpos': z[2]
             })(x.split(sep=';'))
            for x in MissionGenCfg.af_csv[self.name].open().readlines()
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
            for x in MissionGenCfg.daytime_files[self.name].open().readlines()
        )
        self.stages = tuple(
            Stage(x) for x in MissionGenCfg.stages[self.name]
        )

    def capture(self, x, z, coal_id):
        self.grid.capture(x, z, coal_id)

    def update(self):
        """ Обновление групп, баз локаций и файла параметров генерации в папке ТВД (data/scg/x) """
        print('[{}] Updating TVD folder: {} ({})'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            MissionGenCfg.cfg[self.name]['tvd_folder'],
            self.name
        ))
        if self.is_ended:
            print('WARNING! Updating ended TVD: {}'.format(self.name))
        self.verify_grid()
        self.update_icons()
        self.update_ldb()
        self.update_airfields()
        self.randomize_defaultparams()

    def verify_grid(self):
        if not self.grid.neutral_line:
            # self.grid.restore_neutral_line()
            pass

    def update_icons(self):
        """ Обновление группы иконок в соответствии с положением ЛФ """
        print('[{}] generating icons group...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        flg = FlGroup(self.name, self.grid.neutral_line, self.grid.areas)
        flg.make()
        print('... icons done')

    def update_ldb(self):
        """ Обновление базы локаций до актуального состояния """
        print('[{}] generating Locations Data Base (LDB)...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        ldf = Ldb(self.name, self.grid.areas, self.grid.scenarios, self.grid.neutral_line)
        ldf.make()
        print('... LDB done')

    def update_airfields(self):
        """ Генерация групп аэродромов для ТВД """
        print('[{}] generating airfields groups...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        m_date_cache_file = Path(r'.\cache\airfields.json')
        if not m_date_cache_file.exists():
            m_date_cache_file.write_text(json.dumps(default_af_cache), encoding='utf-8')
        cache_data = json.load(m_date_cache_file.open())
        # with m_date_cache_file.open(mode='r') as f:
        cached_date = datetime.datetime.strptime(cache_data[self.name], date_format)

        d = datetime.timedelta(seconds=1)
        for side in MissionGenCfg.cfg['sides']:
            folder = MissionGenCfg.af_groups_folders[self.name][side]
            # шаблон по-умолчанию
            template_group = MissionGenCfg.default_stages[self.name][side]
            # ищем период для текущей даты ТВД
            for stage in self.stages:
                if self.date_next + d in stage:
                    if cached_date in stage:
                        print('... airfields generation skipped - same airfields generated already [{}] {}'.format(
                            cached_date.strftime(date_format), self.date_next.strftime(date_format)))
                        return
                    template_group = stage.af_templates[side]
                    print('... dated plane set [{}] {}'.format(side, self.date_next.strftime(date_format)))
                    break
            for row in self.airfields_data:
                group = Group(template_group)
                group.clone_to(folder)
                group.rename('!x{}z{}'.format(row['xpos'], row['zpos']))
                group.replace_content('!AFNAME!', row['name'].title())

        cache_data[self.name] = self.date_next.strftime(date_format)
        m_date_cache_file.write_text(json.dumps(cache_data), encoding='utf-8')

    def date_day_duration(self, date):
        """ Рассвет и закат для указанной даты """
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
        """ Информация по сезону на указанную дату (из daytime.csv) """
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
        """ Данные по сезону на дату следующей миссии """
        return self.season_data(self.date_next)

    @property
    def date_next(self):
        """ Дата следующей миссии этого ТВД """
        d = datetime.timedelta(days=1)
        return self.date + d

    @property
    def date_end(self):
        """ Дата окончания ТВД """
        return self.stages[-1].end

    @property
    def date_next_day_duration(self):
        """ Интервал светового дня для даты следующей миссии """
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
        """ Случайный момент времени между указанными значениями """
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

    def randomize_defaultparams(self):
        """ Задать случайные параметры погоды, времени года и суток """
        with self.default_params_template_file.open(encoding='utf-8-sig') as f:
            dfpr_lines = f.readlines()
        # случайное направление и сила ветра по высотам
        wind_direction0000 = randint(0, 360)
        wind_power0000 = randint(0, 2)
        """
        wind_direction0500 = wind_direction0000 + randint(-15, 15)
        wind_power0500 = wind_power0000 + randint(0, 2)
        wind_direction1000 = wind_direction0000 + randint(-20, 20)
        wind_power1000 = wind_power0000 + randint(2, 4)
        wind_direction2000 = wind_direction0000 + randint(-25, 25)
        wind_power2000 = wind_power0000 + randint(4, 7)
        wind_direction5000 = wind_direction0000 + randint(-30, 30)
        wind_power5000 = wind_power0000 + randint(7, 10)
        """

        date = Tvd.random_datetime(*self.date_next_day_duration)
        season = self.date_next_season_data
        # Случайная температура для сезона
        temperature = randint(season['min_temp'], season['max_temp'])

        for setting in DfprCfg.cfg[self.name][season['season_prefix']]:
            for i in range(len(dfpr_lines)):
                if dfpr_lines[i].startswith('${} ='.format(setting)):
                    dfpr_lines[i] = '${} = {}\n'.format(
                        setting, DfprCfg.cfg[self.name][season['season_prefix']][setting])
        weather_type = randint(*DfprCfg.cfg[self.name][season['season_prefix']]['wtype_diapason'])

        w_preset = weather.WeatherPreset(weather.presets[weather_type])
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
                dfpr_lines[y] = '$tvd = {}\n'.format(DfprCfg.cfg[self.name]['tvd'])
            elif dfpr_lines[y].startswith('$overlay ='):
                dfpr_lines[y] = '$overlay = {}\n'.format(DfprCfg.cfg[self.name]['overlay'])
            elif dfpr_lines[y].startswith('$xposition ='):
                dfpr_lines[y] = '$xposition = {}\n'.format(DfprCfg.cfg[self.name]['xposition'])
            elif dfpr_lines[y].startswith('$zposition ='):
                dfpr_lines[y] = '$zposition = {}\n'.format(DfprCfg.cfg[self.name]['zposition'])
            elif dfpr_lines[y].startswith('$xtargetposition ='):
                dfpr_lines[y] = '$xtargetposition = {}\n'.format(DfprCfg.cfg[self.name]['xtargetposition'])
            elif dfpr_lines[y].startswith('$ztargetposition ='):
                dfpr_lines[y] = '$ztargetposition = {}\n'.format(DfprCfg.cfg[self.name]['ztargetposition'])
            elif dfpr_lines[y].startswith('$loc_filename ='):
                dfpr_lines[y] = '$loc_filename = {}\n'.format(MissionGenCfg.cfg[self.name]['ldf_file'])
            elif dfpr_lines[y].startswith('$period ='):
                dfpr_lines[y] = '$period = {}\n'.format(self.next_date_stage_id)
        with self.default_params_file.open(mode='w', encoding='utf-8-sig') as f:
            f.writelines(dfpr_lines)
