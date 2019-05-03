"Сервис управления кампанией"
from __future__ import annotations
from typing import Dict

import logging
import pathlib
import shutil
import datetime

from constants import DATE_FORMAT
from core import EventsEmitter, Atype0, Atype7, Atype8, Atype15, Atype19
from configs import Config
from storage import Storage
from processing import Generator, SourceParser

from model import CampaignMission, \
    CampaignMap, \
    Tvd, \
    GameplayAction, \
    SourceMission, \
    TanksCoverFail, \
    ArtilleryKill, \
    DivisionKill, \
    WarehouseDisable, \
    AirfieldKill, \
    MessageAll


from .base_event_service import BaseEventService
from .players_service import PlayersService
from .graph_service import GraphService
from .warehouses_service import WarehouseService
from .airfields_service import AirfieldsService
from .divisions_service import DivisionsService
from .tvd_service import TvdService
START_DATE = 'start_date'
END_DATE = 'end_date'


class CampaignService(BaseEventService):
    "Сервис управления кампанией"

    def __init__(
            self,
            emitter: EventsEmitter,
            config: Config,
            storage: Storage,
            players_service: PlayersService,
            graph_service: GraphService,
            warehouse_service: WarehouseService,
            airfields_service: AirfieldsService,
            divisions_service: DivisionsService,
            tvd_services: Dict[str, TvdService],
            source_parser: SourceParser,
            generator: Generator
    ):
        super().__init__(emitter)
        self._config: Config = config
        self._storage: Storage = storage
        self._players_service: PlayersService = players_service
        self._graph_service: GraphService = graph_service
        self._warehouse_service: WarehouseService = warehouse_service
        self._airfields_service: AirfieldsService = airfields_service
        self._divisions_service: DivisionsService = divisions_service
        self._tvd_services: Dict[str, TvdService] = tvd_services
        self._source_parser: SourceParser = source_parser
        self._generator: Generator = generator
        self._mission: CampaignMission = None
        self._campaign_map: CampaignMap = None
        self._current_tvd: Tvd = None
        self._round_ended: bool = False
        self.won_country: int = 0

    def init(self) -> None:
        self.register_subscriptions([
            self.emitter.events_mission_start.subscribe_(self._start_mission),
            self.emitter.events_mission_end.subscribe_(self._end_mission),
            self.emitter.events_mission_result.subscribe_(
                self._mission_result),
            self.emitter.events_log_version.subscribe_(self._notify),
            self.emitter.events_round_end.subscribe_(self._end_round),
            self.emitter.gameplay_division_kill.subscribe_(
                self.register_action),
            self.emitter.gameplay_warehouse_disable.subscribe_(
                self.register_action),
        ])

    @property
    def campaign_map(self) -> CampaignMap:
        """Текущая карта кампании"""
        return self._campaign_map

    @property
    def next_name(self) -> str:
        """Имя файла следующей миссии"""
        return 'result1' if self._mission.file == 'result2' else 'result2'

    @property
    def current_tvd(self) -> Tvd:
        """Текущий ТВД"""
        return self._current_tvd

    @property
    def mission(self) -> CampaignMission:
        """Текущая миссия кампании"""
        return self._mission

    def _update_tik(self, tik: int) -> None:
        """Обновить тик"""
        if self._mission.tik_last > tik:
            raise NameError('некорректный порядок лога')
        self._mission.tik_last = tik

    def initialize_map(self, tvd_name: str):
        """Инициализировать карту кампании"""
        self._graph_service.initialize(tvd_name)
        self._warehouse_service.initialize_warehouses(tvd_name)
        start = self._config.mgen.cfg[tvd_name][START_DATE]
        order = list(self._config.mgen.maps).index(tvd_name) + 1
        campaign_map = CampaignMap(
            order=order, date=start, mission_date=start, tvd_name=tvd_name, months=list())
        tvd = self._tvd_services[campaign_map.tvd_name].get_tvd(
            campaign_map.date.strftime(DATE_FORMAT))
        self._airfields_service.initialize_tvd(tvd, campaign_map)
        self._storage.campaign_maps.update(campaign_map)
        self._divisions_service.initialize_divisions(tvd_name)
        logging.info(f'{tvd_name} initialized')

    def reset(self):
        """Сбросить состояние кампании"""
        self._storage.airfields.collection.drop()
        self._storage.campaign_maps.collection.drop()
        self._storage.campaign_missions.collection.drop()
        self._storage.divisions.collection.drop()
        self._storage.warehouses.collection.drop()
        logging.info('Database cleaned.')

    def _generate(self,
                  mission_name: str,
                  date: str,
                  tvd_name: str):
        """Сгенерировать миссию для указанной даты и ТВД кампании"""
        tvd_builder: TvdService = self._tvd_services[tvd_name]
        tvd = tvd_builder.get_tvd(date)
        airfields = self._storage.airfields.load_by_tvd(tvd_name)
        tvd_builder.update(
            tvd, self._divisions_service.filter_airfields(tvd_name, airfields))
        self._generator.make_ldb(tvd_name)
        self._generator.make_lgb(tvd_name)

        mission_template: str = str(self._config.mgen.tvd_folders[tvd_name].joinpath(
            self._config.mgen.cfg[tvd_name]['mission_template']).absolute())

        self._generator.make_mission(mission_template, mission_name, tvd_name)

    def generate(self, mission_name, tvd_name: str, date: str):
        """Сгенерировать текущую миссию кампании с указанным именем"""
        self._generate(mission_name, date, tvd_name)

    def initialize(self):
        """Инициализировать кампанию в БД, обновить файлы в data/scg и сгенерировать первую миссию"""
        scg_path = pathlib.Path(
            self._config.main.game_folder.joinpath('data/scg'))
        if not scg_path.exists():
            logging.info('Copy data/scg to game/data/scg.')
            shutil.copytree(r'./data/scg', str(scg_path.absolute()))
        for tvd_name in self._config.mgen.maps:
            self.initialize_map(tvd_name)

        self._campaign_map = self._storage.campaign_maps.load_by_order(2)
        self.generate('result1', self._campaign_map.tvd_name,
                      self._campaign_map.date.strftime(DATE_FORMAT))
        self._players_service.reset()

    def _start_mission(self, atype: Atype0):
        """Обработать начало миссии"""
        self._round_ended = False
        source_mission = self._source_parser.parse_in_dogfight(
            atype.file_path.replace('Multiplayer/Dogfight', '').replace('\\', '').replace('.msnbin', ''))
        self._mission = self._make_campaign_mission(atype, source_mission)
        self._campaign_map = self._storage.campaign_maps.load_by_tvd_name(
            self._mission.tvd_name)
        self._update_tik(atype.tik)
        self._campaign_map.mission = self._mission
        self._campaign_map.date = self._mission.date
        self._current_tvd = self._get_tvd(
            self._campaign_map.tvd_name, self._campaign_map.date.strftime(DATE_FORMAT))
        self.emitter.current_tvd.on_next(self._current_tvd)
        self._storage.campaign_maps.update(self._campaign_map)
        logging.info(
            f'mission started {self._campaign_map.mission.date.strftime(DATE_FORMAT)}, ' +
            f'{self._mission.tvd_name}, {self._campaign_map.mission.file}')
        # TODO сохранить миссию в базу (в документ CampaignMap и в коллекцию CampaignMissions)
        # TODO удалить файлы предыдущей миссии

    def register_action(self, action: GameplayAction) -> None:
        """Зарегистрировать игровое событие"""
        action.date = self._mission.date
        if not self._round_ended:
            self._mission.register_action(action)
            self._storage.campaign_maps.update(self._campaign_map)
        else:
            logging.warning(
                f'{action.__class__.__name__} after round end {action.object_name}')

    def _get_tvd(self, tvd_name: str, date: str) -> Tvd:
        """Получить ТВД (создаётся заново)"""
        result = self._tvd_services[tvd_name].get_tvd(date)
        if not result:
            logging.critical(f'tvd not built')
        return result

    def _end_mission(self, atype: Atype7):
        """Обработать завершение миссии"""
        logging.info('mission ended')
        self._current_tvd = None
        self._update_tik(atype.tik)
        self._mission.is_correctly_completed = True
        self._storage.campaign_missions.update(self._mission)
        # TODO "приземлить" всех

    # этот метод должен вызываться последним среди всех контроллеров
    def _end_round(self, atype: Atype19):
        """Обработать завершение раунда (4-минутный отсчёт до конца миссии)"""
        logging.info('round ended')
        self._update_tik(atype.tik)
        self._round_ended = True
        # TODO подвести итог миссии
        # TODO отправить инпут завершения миссии (победа/ничья)
        # TODO подвести итог кампании, если она закончилась
        # TODO подвести итог ТВД, если он изменился
        # TODO определить имя ТВД для следующей миссии
        # TODO отремонтировать дивизии
        invert = {101: 201, 201: 101}
        self._calculate_result()
        if self.won_country:
            lost = self._airfields_service.get_weakest_airfield(
                invert[self.won_country])
            self._graph_service.capture(
                self._campaign_map.tvd_name,
                {'x': lost.x, 'z': lost.z},
                self.won_country)
        self._generate(
            self.next_name,
            (self._campaign_map.date + datetime.timedelta(days=1)).strftime(DATE_FORMAT),
            self._campaign_map.tvd_name)
        self._storage.campaign_maps.update(self._campaign_map)

    @staticmethod
    def _make_campaign_mission(atype: Atype0, source_mission: SourceMission) -> CampaignMission:
        return CampaignMission(
            file=source_mission.name,
            date=source_mission.date.strftime(DATE_FORMAT),
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
            units=source_mission.units,
            actions=list()
        )

    def _notify(self, atype: Atype15) -> None:
        "Оповестить о состоянии очков захвата"
        result = self._calculate_result()
        message = f'Capture points: {result[101]} red team, {result[201]} blue team'
        self.emitter.commands_rcon.on_next(MessageAll(message))

    def _calculate_result(self) -> dict:
        "Посчитать текущий результат сторон"
        rewards = {
            AirfieldKill.__name__: 1,
            ArtilleryKill.__name__: 2,
            DivisionKill.__name__: 3,
            WarehouseDisable.__name__: 4,
            TanksCoverFail.__name__: -1,
        }
        invert = {101: 201, 201: 101}
        result = {101: 0, 201: 0}
        if self._mission:
            for action in self._mission.actions:
                result[action.country] += rewards[action.__class__.__name__]
                if result[action.country] >= 13 and not self.won_country:
                    self.won_country = action.country
        if self.won_country:
            result[self.won_country] = 13
            result[invert[self.won_country]] = 0
        return result

    def _mission_result(self, atype: Atype8) -> None:
        """Обработать mission objective из логов"""
        invert = {101: 201, 201: 101}
        config = self._config.mgen.cfg['objectives'][str(atype.task_type_id)]
        coals = {1: 'Allies', 2: 'Axis'}
        results = {True: 'completed', False: 'failed'}
        sign = {True: '+', False: ''}
        result = results[atype.success]
        name: str = config['name']
        country: int = atype.coal_id * 100 + 1
        coal: str = coals[atype.coal_id]
        capture_points: int = '{0}{1}'.format(
            sign[atype.success], config['capture_points'])
        logging.info(
            f'Mission Objective {result}: {name} by {coal}. {capture_points} capture points')
        action: GameplayAction = None
        if atype.task_type_id == 6:
            action = TanksCoverFail(atype.tik, invert[country])
        elif atype.task_type_id == 4:
            action = ArtilleryKill(atype.tik, country)
        if action:
            self.register_action(action)
