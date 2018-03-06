"""Контроль миссий и хода кампании"""

import atypes
import configs
import constants
import model
import processing
import storage

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
        for campaign_maps in self.storage.campaign_maps.load_all():
            if not campaign_maps.is_ended(self.config.mgen.cfg[campaign_maps.tvd_name][END_DATE]):
                return campaign_maps
        raise NameError('Campaign finished')

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
        campaign_map = model.CampaignMap(order=order, date=start, mission_date=start, tvd_name=tvd_name, months=list())
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

    def _generate(self, mission_name: str, campaign_map: model.CampaignMap):
        """Сгенерировать миссию для указанной карты кампании"""
        tvd_builder = self.tvd_builders[campaign_map.tvd_name]
        tvd = tvd_builder.get_tvd(campaign_map.date.strftime(constants.DATE_FORMAT))
        # Генерация первой миссии
        airfields = self.storage.airfields.load_by_tvd(campaign_map.tvd_name)
        tvd_builder.update(tvd, self.divisions_controller.filter_airfields(campaign_map.tvd_name, airfields))
        self.generator.make_ldb(campaign_map.tvd_name)
        self.generator.make_lgb(campaign_map.tvd_name)
        self.generator.make_mission(mission_name, campaign_map.tvd_name)

    def generate(self, mission_name):
        """Сгенерировать текущую миссию кампании с указанным именем"""
        self._generate(mission_name, self.campaign_map)

    def initialize(self):
        """Инициализировать кампанию в БД"""
        for tvd_name in self.config.mgen.maps:
            self.initialize_map(tvd_name)

        campaign_map = self.storage.campaign_maps.load_by_order(1)
        self._generate('result1', campaign_map)
        self.players_controller.reset()

    def start_mission(self, atype: atypes.Atype0):
        """Обработать начало миссии"""
        source_mission = self.source_parser.parse_in_dogfight(
            atype.file_path.replace('Multiplayer/Dogfight', '').replace('\\', '').replace('.msnbin', ''))
        self._mission = self._make_campaign_mission(atype, source_mission)
        self._update_tik(atype.tik)
        campaign_map = self.campaign_map
        campaign_map.mission = self._mission
        self._current_tvd = self._get_tvd(campaign_map.tvd_name, campaign_map.date.strftime(constants.DATE_FORMAT))
        self.storage.campaign_maps.update(campaign_map)
        # TODO сохранить миссию в базу (в документ model.CampaignMap и в коллекцию model.CampaignMissions)
        # TODO удалить файлы предыдущей миссии

    def _get_tvd(self, tvd_name: str, date: str) -> model.Tvd:
        """"""
        return self.tvd_builders[tvd_name].get_tvd(date)

    def end_mission(self, atype: atypes.Atype7):
        """Обработать завершение миссии"""
        self._current_tvd = None
        self._update_tik(atype.tik)
        self._mission.is_correctly_completed = True
        self.storage.campaign_missions.update(self._mission)
        # TODO "приземлить" всех
        # TODO подвести итог ТВД, если он изменился
        # TODO подвести итог кампании, если она закончилась

    def end_round(self, atype: atypes.Atype19):  # этот метод должен вызываться последним среди всех контроллеров
        """Обработать завершение раунда (4-минутный отсчёт до конца миссии)"""
        self._update_tik(atype.tik)
        # TODO подвести итог миссии
        # TODO отправить инпут завершения миссии (победа/ничья)
        # TODO определить имя ТВД для следующей миссии
        # TODO обновить папку ТВД
        self.generate(self.next_name)

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
