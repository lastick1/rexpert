"""Контроль миссий и хода кампании"""
import logging

import atypes
import configs
import constants
import model
import processing
import storage

from .ground_control import GroundController
from .divisions_control import DivisionsController
from .warehouses_control import WarehouseController
from .grid_control import GridController
from .source_parser import SourceParser
from .airfields_control import AirfieldsController

START_DATE = 'start_date'
END_DATE = 'end_date'


class CampaignController:
    """Контролеер кампании"""
    def __init__(self, ioc):
        self._ioc = ioc
        self._mission: model.CampaignMission = None
        self._campaign_map: model.CampaignMap = None
        self._current_tvd: model.Tvd = None
        self._round_ended: bool = False
        self.tvd_builders = {x: processing.TvdBuilder(x, ioc) for x in ioc.config.mgen.maps}

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def divisions_controller(self) -> DivisionsController:
        """Контроллер дивизий"""
        return self._ioc.divisions_controller

    @property
    def warehouses_controller(self) -> WarehouseController:
        return self._ioc.warehouses_controller
    
    @property
    def players_controller(self) -> processing.PlayersController:
        """Контроллер игроков"""
        return self._ioc.players_controller

    @property
    def grid_controller(self) -> GridController:
        """Контроллер графа"""
        return self._ioc.grid_controller

    @property
    def airfields_controller(self) -> AirfieldsController:
        """Поставщик самолётов"""
        return self._ioc.airfields_controller

    @property
    def ground_controller(self) -> GroundController:
        """Контроллер наземки"""
        return self._ioc.ground_controller

    @property
    def source_parser(self) -> SourceParser:
        """Парсер исходников миссий"""
        return self._ioc.source_parser

    @property
    def storage(self) -> storage.Storage:
        """Объект для работы с БД"""
        return self._ioc.storage
    
    @property
    def generator(self) -> processing.Generator:
        """Генератор миссий (управляет missiongen.exe)"""
        return self._ioc.generator

    @property
    def campaign_map(self) -> model.CampaignMap:
        """Текущая карта кампании"""
        return self._campaign_map

    @property
    def next_name(self) -> str:
        """Имя файла следующей миссии"""
        return 'result1' if self._mission.file == 'result2' else 'result2'

    @property
    def current_tvd(self) -> model.Tvd:
        """Текущий ТВД"""
        return self._current_tvd

    @property
    def mission(self) -> model.CampaignMission:
        """Текущая миссия кампании"""
        return self._mission

    def _update_tik(self, tik: int) -> None:
        """Обновить тик"""
        if self._mission.tik_last > tik:
            raise NameError('некорректный порядок лога')
        self._mission.tik_last = tik

    def initialize_map(self, tvd_name: str):
        """Инициализировать карту кампании"""
        self.grid_controller.initialize(tvd_name)
        self.warehouses_controller.initialize_warehouses(tvd_name)
        start = self.config.mgen.cfg[tvd_name][START_DATE]
        order = list(self.config.mgen.maps).index(tvd_name) + 1
        campaign_map = model.CampaignMap(
            order=order, date=start, mission_date=start, tvd_name=tvd_name, months=list(), actions=list())
        tvd = self.tvd_builders[campaign_map.tvd_name].get_tvd(campaign_map.date.strftime(constants.DATE_FORMAT))
        self.airfields_controller.initialize_tvd(tvd, campaign_map)
        self.storage.campaign_maps.update(campaign_map)
        self.divisions_controller.initialize_divisions(tvd_name)

    def reset(self):
        """Сбросить состояние кампании"""
        self.storage.airfields.collection.drop()
        self.storage.campaign_maps.collection.drop()
        self.storage.campaign_missions.collection.drop()
        self.storage.divisions.collection.drop()
        self.storage.warehouses.collection.drop()

    def _generate(self,
                  mission_name: str,
                  date: str,
                  tvd_name: str,
                  attacking_country: int,
                  attacked_airfield_name: str = None):
        """Сгенерировать миссию для указанной даты и ТВД кампании"""
        tvd_builder = self.tvd_builders[tvd_name]
        tvd = tvd_builder.get_tvd(date)
        # Генерация первой миссии
        airfields = self.storage.airfields.load_by_tvd(tvd_name)
        if attacked_airfield_name:
            tvd_builder.update(
                tvd, airfields, self.airfields_controller.get_airfield_by_name(tvd_name, attacked_airfield_name))
        else:
            tvd_builder.update(tvd, self.divisions_controller.filter_airfields(tvd_name, airfields))
        self.generator.make_ldb(tvd_name)
        self.generator.make_lgb(tvd_name)

        mission_template = str(self.config.mgen.tvd_folders[tvd_name].joinpath(
            self.config.mgen.cfg[tvd_name]['mission_templates'][str(attacking_country)]).absolute())

        self.generator.make_mission(mission_template, mission_name, tvd_name)

    def generate(self, mission_name, tvd_name: str, date: str, attacking_country=0, attacked_airfield_name: str = None):
        """Сгенерировать текущую миссию кампании с указанным именем"""
        self._generate(mission_name, date, tvd_name, attacking_country, attacked_airfield_name)

    def initialize(self):
        """Инициализировать кампанию в БД и сгенерировать первую миссию"""
        for tvd_name in self.config.mgen.maps:
            self.initialize_map(tvd_name)

        self._campaign_map = self.storage.campaign_maps.load_by_order(1)
        self.generate('result1', self._campaign_map.tvd_name, self._campaign_map.date.strftime(constants.DATE_FORMAT))
        self.players_controller.reset()

    def start_mission(self, atype: atypes.Atype0):
        """Обработать начало миссии"""
        self._round_ended = False
        source_mission = self.source_parser.parse_in_dogfight(
            atype.file_path.replace('Multiplayer/Dogfight', '').replace('\\', '').replace('.msnbin', ''))
        self._mission = self._make_campaign_mission(atype, source_mission)
        self._campaign_map = self.storage.campaign_maps.load_by_tvd_name(self._mission.tvd_name)
        self._update_tik(atype.tik)
        self._campaign_map.mission = self._mission
        self._current_tvd = self._get_tvd(
            self._campaign_map.tvd_name, self._campaign_map.date.strftime(constants.DATE_FORMAT))
        self.storage.campaign_maps.update(self._campaign_map)
        logging.info(f'mission started {self._campaign_map.mission.date}, {self._campaign_map.mission.file}')
        # TODO сохранить миссию в базу (в документ model.CampaignMap и в коллекцию model.CampaignMissions)
        # TODO удалить файлы предыдущей миссии

    def register_action(self, action: model.GameplayAction) -> None:
        """Зарегистрировать игровое событие"""
        action.date = self._mission.date
        if not self._round_ended:
            self._campaign_map.register_action(action)
            self.storage.campaign_maps.update(self._campaign_map)
        else:
            logging.warning(f'{action.__class__.__name__} after round end {action.object_name}')

    def _get_tvd(self, tvd_name: str, date: str) -> model.Tvd:
        """Получить ТВД (создаётся заново)"""
        return self.tvd_builders[tvd_name].get_tvd(date)

    def end_mission(self, atype: atypes.Atype7):
        """Обработать завершение миссии"""
        logging.info('mission ended')
        self._current_tvd = None
        self._update_tik(atype.tik)
        self._mission.is_correctly_completed = True
        self.storage.campaign_missions.update(self._mission)
        # TODO "приземлить" всех

    def end_round(self, atype: atypes.Atype19):  # этот метод должен вызываться последним среди всех контроллеров
        """Обработать завершение раунда (4-минутный отсчёт до конца миссии)"""
        logging.info('round ended')
        self._update_tik(atype.tik)
        self._round_ended = True
        # TODO подвести итог миссии
        # TODO если сторона переходит в наступление, то увеличить счётчик смертей у склада и "починить" его
        # TODO отправить инпут завершения миссии (победа/ничья)
        # TODO подвести итог кампании, если она закончилась
        # TODO подвести итог ТВД, если он изменился
        # TODO определить имя ТВД для следующей миссии
        if self._mission.kind == constants.CampaignMission.Kinds.ASSAULT:
            country = self._mission.assault_country
            if self.ground_controller.killed_stations(country) < 2 and self.ground_controller.killed_bridges(country) < 3:
                pos = self._mission.assault_pos
                logging.info(f'{country} captured airfield at {pos}')
                self.grid_controller.capture(self._mission.tvd_name, pos, country)
                self._campaign_map.register_capture()
                self.storage.campaign_maps.update(self._campaign_map)

        killed_airfields = self._campaign_map.killed_airfields
        attack = self._campaign_map.country_attacked()
        self._generate(
            self.next_name,
            self._campaign_map.date.strftime(constants.DATE_FORMAT),
            self._campaign_map.tvd_name,
            attack,
            killed_airfields[attack] if attack else None)
        self.storage.campaign_maps.update(self._campaign_map)

    @staticmethod
    def _make_campaign_mission(atype: atypes.Atype0, source_mission: model.SourceMission) -> model.CampaignMission:
        return model.CampaignMission(
            kind=source_mission.kind,
            file=source_mission.name,
            date=source_mission.date.strftime(constants.DATE_FORMAT),
            tvd_name=source_mission.guimap,
            additional={
                'date': atype.date,
                'game_type_id': atype.game_type_id,
                'settings': atype.settings,
                'mods': atype.mods,
                'preset_id': atype.preset_id
            },
            server_inputs=source_mission.server_inputs,
            objectives=source_mission.objectives,
            airfields=source_mission.airfields,
            units=source_mission.units
        )

    def mission_result(self, atype: atypes.Atype8) -> None:
        """Обработать mission objective из логов"""
        pass
