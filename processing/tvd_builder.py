"""Сборка папок ТВД (scg/1, scg/2, scg/3 итд)"""
import logging
import random
import pathlib
import datetime

import configs
import constants
import model
import processing
import storage


class Season:
    """Данные сезона"""
    def __init__(self, split: list):
        self.start = split[0]
        self.end = split[1]
        self.sunrise = split[2]
        self.sunset = split[3]
        self.min_temp = int(split[4])
        self.max_temp = int(split[5])
        self.prefix = str(split[6]).rstrip()
        self.sunrise_hour, self.sunrise_minute = self.sunrise.split(sep=':')
        self.sunset_hour, self.sunset_minute = self.sunset.split(sep=':')

    def start_for_year(self, year: int):
        """Старт сезона для указанного года"""
        return datetime.datetime(
            year,
            int(self.start.split(sep='.')[1]),
            int(self.start.split(sep='.')[0])
        )

    def end_for_year(self, year: int):
        """Конец сезона для указанного года"""
        return datetime.datetime(
                year,
                int(self.end.split(sep='.')[1]),
                int(self.end.split(sep='.')[0])
            )

    def sunrise_for_date(self, date: datetime.datetime) -> datetime.datetime:
        """Рассвет для указанной даты"""
        return datetime.datetime(
            date.year,
            date.month,
            date.day,
            hour=int(self.sunrise_hour),
            minute=int(self.sunrise_minute))

    def sunset_for_date(self, date: datetime.datetime) -> datetime.datetime:
        """Закат для указанной даты"""
        return datetime.datetime(
            date.year,
            date.month,
            date.day,
            hour=int(self.sunset_hour),
            minute=int(self.sunset_minute))


class TvdBuilder:
    """Класс подготовки папки ТВД, в которой лежат ресурсы для генерации миссии"""

    def __init__(self, name: str, ioc):
        self.name = name
        self._ioc = ioc
        self._airfields_builder: processing.AirfieldsBuilder = None
        self._airfields_selector: processing.AirfieldsSelector = None
        self._boundary_builder: processing.BoundaryBuilder = None

    @property
    def config(self) -> configs.Config:
        """Конфиг приложения"""
        return self._ioc.config

    @property
    def airfields_builder(self) -> processing.AirfieldsBuilder:
        """Сборщик групп аэродромов"""
        if not self._airfields_builder:
            self._airfields_builder = processing.AirfieldsBuilder(
                self.config.mgen.af_groups_folders[self.name],
                self.config.mgen.subtitle_groups_folder,
                self.config.planes
            )
        return self._airfields_builder

    @property
    def airfields_selector(self) -> processing.AirfieldsSelector:
        """Выборщик аэродромов"""
        if not self._airfields_selector:
            self._airfields_selector = processing.AirfieldsSelector(main=self.config.main)
        return self._airfields_selector

    @property
    def boundary_builder(self) -> processing.BoundaryBuilder:
        """Сборщик многоугольников для Influence Area"""
        if not self._boundary_builder:
            offset = 10000
            north = self.config.mgen.cfg[self.name]['right_top']['x'] + offset
            east = self.config.mgen.cfg[self.name]['right_top']['z'] + offset
            south = 0 - offset
            west = 0 - offset
            self._boundary_builder = processing.BoundaryBuilder(north=north, east=east, south=south, west=west)
        return self._boundary_builder

    @property
    def grid_controller(self) -> processing.GridController:
        """Контроллер графа"""
        return self._ioc.grid_controller

    @property
    def warehouses_controller(self) -> processing.WarehouseController:
        """Контроллер складов"""
        return self._ioc.warehouses_controller

    @property
    def storage(self) -> storage.Storage:
        """Работа с БД"""
        return self._ioc.storage

    @property
    def default_params_file(self) -> pathlib.Path:
        """Файл параметров для missiongen.exe"""
        tvd_folder = self.config.main.game_folder.joinpath(self.config.mgen.cfg[self.name]['tvd_folder'])
        return tvd_folder.joinpath(self.config.mgen.cfg[self.name]['default_params_dest'])

    @property
    def default_params_template_file(self):
        """Шаблонный файл параметров для missiongen.exe"""
        return self.config.mgen.data_folder.joinpath(self.config.mgen.cfg[self.name]['default_params_source'])

    @property
    def seasons(self) -> tuple:
        """данные по сезонам из daytime.csv"""
        with self.config.mgen.daytime_files[self.name].open() as stream:
            return tuple(
                (lambda z: Season(z))(x.split(sep=';'))
                for x in stream.readlines()
            )

    def get_tvd(self, date):
        """Построить объект настроек ТВД"""
        tvd = model.Tvd(
            self.name,
            self.config.mgen.cfg[self.name]['tvd_folder'],
            date,
            self.config.mgen.cfg[self.name]['right_top'],
            # TODO заменить на получение через divisions_controller
            self.storage.divisions.load_by_tvd(self.name),
            self.grid_controller.get_grid(self.name),
            self.config.mgen.icons_group_files[self.name]
        )
        self._make_influences(tvd)
        return tvd

    def _make_influences(self, tvd):
        """Построить зоны влияния в соответствии с графом"""
        tvd.confrontation_east = self.boundary_builder.confrontation_east(tvd.grid)
        tvd.confrontation_west = self.boundary_builder.confrontation_west(tvd.grid)

        influence_east = self.boundary_builder.influence_east(tvd.border)
        influence_west = self.boundary_builder.influence_west(tvd.border)
        east_boundary = model.Boundary(influence_east[0].x, influence_east[0].z, influence_east)
        west_boundary = model.Boundary(influence_west[0].x, influence_west[0].z, influence_west)
        east_influences = list(model.Boundary(node.x, node.z, node.neighbors_sorted)
                               for node in tvd.nodes_list if node.country == 101)
        west_influences = list(model.Boundary(node.x, node.z, node.neighbors_sorted)
                               for node in tvd.nodes_list if node.country == 201)
        east_influences.append(east_boundary)
        west_influences.append(west_boundary)
        east_influences.append(
            model.Boundary(tvd.confrontation_east[0].x, tvd.confrontation_east[0].z, tvd.confrontation_east))
        west_influences.append(
            model.Boundary(tvd.confrontation_west[0].x, tvd.confrontation_west[0].z, tvd.confrontation_west))
        if self.config.main.special_influences:
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

    def update(self, tvd, airfields: list):
        """Обновление групп, баз локаций и файла параметров генерации в папке ТВД (data/scg/x)"""
        logging.info(f'Updating TVD folder: {tvd.folder} ({tvd.name}) {tvd.date}')
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
        self.update_warehouses(tvd)
        self.update_ldb(tvd)
        self.update_defaultparams(tvd)
        logging.info('TVD folder updated')

    @staticmethod
    def update_icons(tvd: model.Tvd):
        """Обновление группы иконок в соответствии с положением ЛФ"""
        logging.debug('Generating icons group...')
        flg = processing.FrontLineGroup(tvd.border, tvd.influences, tvd.icons_group_file, tvd.right_top)
        flg.make()
        logging.debug('... icons done')

    def update_ldb(self, tvd: model.Tvd):
        """Обновление базы локаций до актуального состояния"""
        logging.debug('Generating Locations Data Base (LDB)...')
        with self.config.mgen.ldf_templates[self.name].open() as stream:
            ldf = stream.read()
        builder = processing.LocationsBuilder(ldf_base=ldf)
        builder.apply_tvd_setup(tvd)
        ldf_text = builder.make_text()
        with pathlib.Path(self.config.mgen.ldf_files[self.name]).open(mode='w') as stream:
            stream.write(ldf_text)
        logging.debug('... LDB done')

    def update_airfields(self, tvd: model.Tvd):
        """Генерация групп аэродромов для ТВД"""
        logging.debug('Generating airfields groups...')
        for airfield in tvd.red_front_airfields + [tvd.red_rear_airfield]:
            data = self._convert_airfield(airfield, 101)
            self.airfields_builder.make_airfield_group(data, airfield.x, airfield.z)
        for airfield in tvd.blue_front_airfields + [tvd.blue_rear_airfield]:
            data = self._convert_airfield(airfield, 201)
            self.airfields_builder.make_airfield_group(data, airfield.x, airfield.z)
        logging.debug('... airfields groups done')

    def update_warehouses(self, tvd: model.Tvd):
        """Выбор расположения складов"""
        tvd.warehouses.extend(self.warehouses_controller.next_warehouses(tvd))

    def _convert_airfield(self, airfield: model.ManagedAirfield, country: int) -> processing.Airfield:
        """Конвертировать тип управляемого аэродрома в тип генерируемого аэродрома"""

        def find_plane_in_config(config: dict, key_name: str, number: int) -> processing.Plane:
            """Найти соответствующий самолёт в конфиге для генерации аэродрома"""
            for name in config['uncommon']:
                if self.config.planes.name_to_key(name) == key_name:
                    return processing.Plane(number, config['common'], config['uncommon'][name])
            raise NameError(f'Plane {key_name} not found in config')

        planes = list()
        for key in airfield.planes:
            planes.append(find_plane_in_config(self.config.planes.cfg, key, airfield.planes[key]))
        return processing.Airfield(airfield.name, country, self.config.gameplay.airfield_radius, planes)

    def date_day_duration(self, date) -> tuple:
        """Рассвет и закат для указанной даты"""
        season = self.season(date)
        sunrise = season.sunrise_for_date(date)
        sunset = season.sunset_for_date(date)
        return sunrise, sunset - datetime.timedelta(hours=1, minutes=30)

    def season(self, date: datetime.datetime) -> Season:
        """Информация по сезону на указанную дату (из daytime.csv)"""
        for season in self.seasons:
            start = season.start_for_year(date.year)
            end = season.end_for_year(date.year)
            if start <= date <= end:
                return season
        raise NameError('Season not found')

    def date_season_data(self, date: datetime.datetime) -> Season:
        """Данные по сезону на указанную дату без учёта времени"""
        return self.season(datetime.datetime(date.year, date.month, date.day))

    @staticmethod
    def random_datetime(start: datetime.datetime, end: datetime.datetime) -> datetime.datetime:
        """Случайный момент времени между указанными значениями"""
        return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

    def update_defaultparams(self, tvd: model.Tvd):
        """Задать случайные параметры погоды, времени года и суток"""
        params_config = self.config.generator.cfg[self.name]
        date = self.random_datetime(*self.date_day_duration(tvd.date))
        season = self.date_season_data(date)

        # настройки погоды
        weather_type = random.randint(*params_config[season.prefix]['wtype_diapason'])
        w_preset = processing.WeatherPreset(processing.presets[weather_type])
        # случайное направление и сила ветра по высотам
        wind_direction0000 = random.randint(0, 360)
        wind_power0000 = random.randint(0, 2)
        # Случайная температура для сезона
        temperature = random.randint(season.min_temp, season.max_temp)

        prefix = season.prefix
        if prefix == 'au':
            prefix = 'su'  # либо su либо wi должно быть season prefix

        lines = [
            '\n',
            '$author = 72AG-DED-\n',
            '$language = rus\n',
            '$missiontype = 2\n',
            '$playercountryid = 101\n',
            '$starttype = 2\n',
            '$template = default\n',
            '$yorientation = 0\n',
            '$missionId = \n',
            f'$seasonprefix = {prefix}\n',
            f'$date = {date.strftime(constants.DATE_FORMAT)}\n',
            f'$time = {date.strftime("%H:%M:%S")}\n',
            f'$sunrise = {season.sunrise}\n',
            f'$sunset = {season.sunset}\n',
            f'$winddirection = {wind_direction0000}\n',
            f'$windpower = {wind_power0000}\n',
            f'$turbulence = {0}\n',  # В топку турбулентность
            f'$cloudlevel = {w_preset.cloudlevel}\n',
            f'$cloudheight = {w_preset.cloudheight}\n',
            f'$temperature = {temperature}\n',
            f'$wtype = {weather_type}\n',
            f'$prevwtype = {weather_type}\n',
            f'$tvd = {params_config["tvd"]}\n',
            f'$overlay = {params_config["overlay"]}\n',
            f'$xposition = {params_config["xposition"]}\n',
            f'$zposition = {params_config["zposition"]}\n',
            f'$xtargetposition = {params_config["xtargetposition"]}\n',
            f'$ztargetposition = {params_config["ztargetposition"]}\n',
            f'$loc_filename = {pathlib.Path(self.config.mgen.ldf_files[self.name]).name}\n',
            f'$forests = {params_config[season.prefix]["forests"]}\n',
            f'$guimap = {params_config[season.prefix]["guimap"]}\n',
            f'$hmap = {params_config[season.prefix]["hmap"]}\n',
            f'$textures = {params_config[season.prefix]["textures"]}\n',
            f'$mapId = {params_config[season.prefix]["mapId"]}\n'
        ]

        for division in tvd.divisions:
            lines.append(f'${division.name.lower()} = {int(division.units)}\n')

        with self.default_params_file.open(mode='w', encoding='utf-8-sig') as stream:
            stream.writelines(lines)
