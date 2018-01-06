import datetime
import pathlib
from pathlib import Path
from random import randint

import geometry
import generation
import configs
import processing

DATE_FORMAT = '%d.%m.%Y'


class Stage:
    def __init__(self, raw, sides, af_templates_folder):
        """Класс этапа кампании, для которого создаются группы аэродромов с заданными самолётами"""
        self.start = datetime.datetime.strptime(raw['start'], DATE_FORMAT)
        self.end = datetime.datetime.strptime(raw['end'], DATE_FORMAT)
        self.id = int(raw['id'])
        self.af_templates = dict()
        for side in sides:
            self.af_templates[side] = af_templates_folder.joinpath(raw[side])

    def __contains__(self, item):
        return self.start <= item < self.end


class Boundary(geometry.Point):
    """Класс зоны влияния"""

    def __init__(self, x: float, z: float, polygon: list):
        super().__init__(x=x, z=z)
        self.polygon = polygon


class Tvd:
    """Настройки ТВД для генерации миссии"""
    def __init__(
            self,
            name: str,
            folder: str,
            date: str,
            right_top: dict,
            icons_group_file: pathlib.Path
    ):
        self.name = name  # имя твд
        self.folder = folder  # папка твд
        self.date = datetime.datetime.strptime(date, DATE_FORMAT)  # дата миссии
        self.right_top = right_top  # правый верхний угол карты
        self.icons_group_file = icons_group_file  # файл группы иконок
        self.border = list()  # упорядоченный список узлов линии фронта
        self.confrontation_east = list()  # восточная прифронтовая зона
        self.confrontation_west = list()  # западная прифронтовая зона
        self.influences = dict()  # инфлюенсы СССР и Германии
        self.red_front_airfields = list()  # советские аэродромы в миссии
        self.red_rear_airfield = None  # советский тыловой аэродром в миссии
        self.blue_front_airfields = list()  # немецкие аэродромы в миссии
        self.blue_rear_airfield = None  # немецкий тыловой аэродром в миссии

    def get_country(self, point: geometry.Point) -> int:
        """Определить страну, на территории которой находится точка"""
        for country in self.influences:
            for boundary in self.influences[country]:
                if point.is_in_area(boundary.polygon):
                    return country
        return 0


class TvdBuilder:
    """Класс подготовки папки ТВД, в которой лежат ресурсы для генерации миссии"""

    def __init__(
            self,
            name,
            mgen: configs.Mgen,
            main: configs.Main,
            params: configs.GeneratorParamsConfig,
            planes: configs.Planes
    ):
        self.name = name
        self.main = main
        self.mgen = mgen
        self.params = params
        self.planes = planes
        self.sides = mgen.cfg['sides']
        self.default_stages = mgen.default_stages[name]
        self.af_groups_folders = mgen.af_groups_folders[name]
        self.ldf_file = mgen.ldf_files[name]
        self.ldf_template = mgen.ldf_templates[name]
        self.tvd_folder = mgen.cfg[name]['tvd_folder']

        offset = 10000
        north = self.mgen.cfg[name]['right_top']['x'] + offset
        east = self.mgen.cfg[name]['right_top']['z'] + offset
        south = 0 - offset
        west = 0 - offset
        self.boundary_builder = generation.BoundaryBuilder(north=north, east=east, south=south, west=west)
        self.airfields_builder = generation.AirfieldsBuilder(self.af_groups_folders, mgen.subtitle_groups_folder,
                                                             planes)
        self.airfields_selector = generation.AirfieldsSelector(main=main)

        self.id = mgen.cfg[name]['tvd']
        folder = main.game_folder.joinpath(Path(mgen.cfg[name]['tvd_folder']))
        self.default_params_file = folder.joinpath(mgen.cfg[name]['default_params_dest'])
        self.default_params_template_file = main.configs_folder.joinpath(
            mgen.cfg[name]['default_params_source'])
        self.icons_group_file = folder.joinpath(mgen.cfg[name]['icons_group_file'])
        self.right_top = mgen.cfg[name]['right_top']
        xgml = generation.Xgml(name, mgen)
        xgml.parse()
        self.grid = generation.Grid(name, xgml.nodes, xgml.edges, mgen)
        # данные по сезонам из daytime.csv
        with mgen.daytime_files[name].open() as stream:
            self.seasons_data = tuple(
                (lambda z: {
                    'start': z[0],
                    'end': z[1],
                    'sunrise': z[2],
                    'sunset': z[3],
                    'min_temp': int(z[4]),
                    'max_temp': int(z[5]),
                    'season_prefix': str(z[6]).rstrip()
                })(x.split(sep=';'))
                for x in stream.readlines()
            )
        self.stages = tuple(
            Stage(x, self.sides, mgen.af_templates_folder) for x in mgen.stages[name]
        )

    def capture(self, x, z, coal_id):
        self.grid.capture(x, z, coal_id)

    def get_tvd(self, date):
        """Построить объект настроек ТВД"""
        tvd = Tvd(
            self.name,
            self.tvd_folder,
            date,
            self.mgen.cfg[self.name]['right_top'],
            self.mgen.icons_group_files[self.name]
        )
        tvd.border = self.grid.border
        nodes = self.grid.nodes_list
        influence_east = self.boundary_builder.influence_east(tvd.border)
        influence_west = self.boundary_builder.influence_west(tvd.border)
        tvd.confrontation_east = self.boundary_builder.confrontation_east(self.grid)
        tvd.confrontation_west = self.boundary_builder.confrontation_west(self.grid)
        east_boundary = Boundary(influence_east[0].x, influence_east[0].z, influence_east)
        west_boundary = Boundary(influence_west[0].x, influence_west[0].z, influence_west)
        east_influences = list(Boundary(node.x, node.z, node.neighbors_sorted) for node in nodes if node.country == 101)
        west_influences = list(Boundary(node.x, node.z, node.neighbors_sorted) for node in nodes if node.country == 201)
        east_influences.append(east_boundary)
        west_influences.append(west_boundary)
        east_influences.append(
            Boundary(tvd.confrontation_east[0].x, tvd.confrontation_east[0].z, tvd.confrontation_east))
        west_influences.append(
            Boundary(tvd.confrontation_west[0].x, tvd.confrontation_west[0].z, tvd.confrontation_west))
        if self.main.special_influences:
            areas = {
                101: east_influences,
                201: west_influences
            }
        else:
            areas = {
                101: [east_boundary],
                201: [west_boundary]
            }
        tvd.influences = areas
        return tvd

    def update(self, date, airfields):
        """Обновление групп, баз локаций и файла параметров генерации в папке ТВД (data/scg/x)"""
        tvd = self.get_tvd(date)
        print('[{}] Updating TVD folder: {} ({}) {}'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            tvd.folder,
            tvd.name,
            tvd.date
        ))
        self.update_icons(tvd)
        tvd.red_front_airfields.extend(self.airfields_selector.select_front(tvd.confrontation_east, airfields))
        tvd.blue_front_airfields.extend(self.airfields_selector.select_front(tvd.confrontation_west, airfields))
        tvd.red_rear_airfield = self.airfields_selector.select_rear(
                influence=tvd.influences[101][0].polygon,
                front_area=tvd.confrontation_east,
                airfields=airfields
            )
        tvd.blue_rear_airfield = self.airfields_selector.select_rear(
                influence=tvd.influences[201][0].polygon,
                front_area=tvd.confrontation_west,
                airfields=airfields
            )
        self.update_airfields(tvd)
        self.update_ldb(tvd)
        self.randomize_defaultparams(tvd.date, self.params.cfg[self.name])

    @staticmethod
    def update_icons(tvd: Tvd):
        """Обновление группы иконок в соответствии с положением ЛФ"""
        print('[{}] generating icons group...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        flg = generation.FrontLineGroup(tvd.border, tvd.influences, tvd.icons_group_file, tvd.right_top)
        flg.make()
        print('... icons done')

    def update_ldb(self, tvd: Tvd):
        """Обновление базы локаций до актуального состояния"""
        print('[{}] generating Locations Data Base (LDB)...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        with self.ldf_template.open() as stream:
            ldf = stream.read()
        builder = generation.LocationsBuilder(ldf_base=ldf)
        builder.apply_tvd_setup(tvd)
        ldf_text = builder.make_text()
        with Path(self.ldf_file).open(mode='w') as stream:
            stream.write(ldf_text)
        print('... LDB done')

    def update_airfields(self, tvd: Tvd):
        """Генерация групп аэродромов для ТВД"""
        print('[{}] generating airfields groups...'.format(datetime.datetime.now().strftime("%H:%M:%S")))
        for airfield in tvd.red_front_airfields + [tvd.red_rear_airfield]:
            data = self._convert_airfield(airfield, 101)
            self.airfields_builder.make_airfield_group(data, airfield.x, airfield.z)
        for airfield in tvd.blue_front_airfields + [tvd.blue_rear_airfield]:
            data = self._convert_airfield(airfield, 201)
            self.airfields_builder.make_airfield_group(data, airfield.x, airfield.z)

    def _convert_airfield(self, airfield: processing.ManagedAirfield, country: int) -> generation.Airfield:
        """Конвертировать тип управляемого аэродрома в тип генерируемого аэродрома"""

        def find_plane_in_config(config: dict, key_name: str, number: int) -> generation.Plane:
            """Найти соответствующий самолёт в конфиге для генерации аэродрома"""
            for name in config['uncommon']:
                if self.planes.name_to_key(name) == key_name:
                    return generation.Plane(number, config['common'], config['uncommon'][name])
            raise NameError('Plane {} not found in config'.format(key_name))

        planes = list()
        for key in airfield.planes:
            planes.append(find_plane_in_config(self.planes.cfg, key, airfield.planes[key]))
        return generation.Airfield(airfield.name, country, self.main.airfield_radius, planes)

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

    def date_season_data(self, date):
        """Данные по сезону на дату следующей миссии"""
        return self.season_data(date)

    def date_next(self, date: str) -> datetime.datetime:
        """Дата следующей миссии этого ТВД"""
        _date = datetime.datetime.strptime(date, DATE_FORMAT)
        d = datetime.timedelta(days=1)
        return _date + d

    @property
    def date_end(self):
        """Дата окончания ТВД"""
        return self.stages[-1].end

    def date_next_day_duration(self, date):
        """Интервал светового дня для даты следующей миссии"""
        return self.date_day_duration(date)

    @property
    def is_ended(self):
        # TODO добавить проверку на завершение по территории
        return self.date_next > self.date_end

    @staticmethod
    def random_datetime(start, end):
        """Случайный момент времени между указанными значениями"""
        return start + datetime.timedelta(seconds=randint(0, int((end - start).total_seconds())))

    def randomize_defaultparams(self, date, params_config: dict):
        """Задать случайные параметры погоды, времени года и суток"""
        with self.default_params_template_file.open(encoding='utf-8-sig') as f:
            dfpr_lines = f.readlines()
        # случайное направление и сила ветра по высотам
        wind_direction0000 = randint(0, 360)
        wind_power0000 = randint(0, 2)

        date = self.random_datetime(*self.date_next_day_duration(date))
        season = self.date_season_data(date)
        # Случайная температура для сезона
        temperature = randint(season['min_temp'], season['max_temp'])

        for setting in params_config[season['season_prefix']]:
            for i in range(len(dfpr_lines)):
                if dfpr_lines[i].startswith('${} ='.format(setting)):
                    dfpr_lines[i] = '${} = {}\n'.format(
                        setting, params_config[season['season_prefix']][setting])
        weather_type = randint(*params_config[season['season_prefix']]['wtype_diapason'])

        w_preset = generation.WeatherPreset(generation.presets[weather_type])
        # задаём параметры defaultparams в соответствии с конфигом
        for y in range(len(dfpr_lines)):
            if dfpr_lines[y].startswith('$date ='):
                dfpr_lines[y] = '$date = {}\n'.format(date.strftime(DATE_FORMAT))
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
                dfpr_lines[y] = '$loc_filename = {}\n'.format(self.ldf_file.name)
            elif dfpr_lines[y].startswith('$period ='):
                dfpr_lines[y] = '$period = {}\n'.format(1)
        with self.default_params_file.open(mode='w', encoding='utf-8-sig') as f:
            f.writelines(dfpr_lines)
