"""Контроль миссий и хода кампании"""
import json
import datetime
import pytz

import atypes
import processing
import constants

from .tvd import Tvd
from .campaign_map import CampaignMap
from .campaign_mission import CampaignMission

START_DATE = 'start_date'
END_DATE = 'end_date'


class CampaignController:
    """Контролеер кампании"""
    def __init__(self, ioc):
        self._ioc = ioc
        self._dogfight = ioc.config.main.dogfight_folder
        self._mission: CampaignMission = None
        self._campaign_map: CampaignMap = None
        self._current_tvd: Tvd = None
        self.vendor = processing.AircraftVendor(ioc.config.planes, ioc.config.gameplay)
        self.tvd_builders = {x: processing.TvdBuilder(x, ioc) for x in ioc.config.mgen.maps}

    def _update_tik(self, tik: int) -> None:
        """Обновить тик"""
        if self._mission.tik_last > tik:
            raise NameError('некорректный порядок лога')
        self._mission.tik_last = tik

    def initialize_map(self, tvd_name: str):
        """Инициализировать карту кампании"""
        self._ioc.grid_controller.initialize(tvd_name)
        start = self._ioc.config.mgen.cfg[tvd_name][START_DATE]
        order = list(self._ioc.config.mgen.maps).index(tvd_name) + 1
        campaign_map = CampaignMap(order=order, date=start, mission_date=start, tvd_name=tvd_name, months=list())
        airfields = processing.AirfieldsController.initialize_managed_airfields(
            self._ioc.config.mgen.airfields_data[campaign_map.tvd_name])
        tvd = self.tvd_builders[campaign_map.tvd_name].get_tvd(campaign_map.date.strftime(constants.DATE_FORMAT))
        supply = self.vendor.get_month_supply(campaign_map.current_month, campaign_map)
        self.vendor.deliver_month_supply(campaign_map, tvd.to_country_dict_rear(airfields), supply)
        self.vendor.initial_front_supply(campaign_map, tvd.to_country_dict_front(airfields))
        self._ioc.storage.campaign_maps.update(campaign_map)
        self._ioc.storage.airfields.update_airfields(airfields)

    def reset(self):
        """Сбросить состояние кампании"""
        self._ioc.storage.airfields.collection.drop()
        self._ioc.storage.campaign_maps.collection.drop()

    def _generate(self, mission_name: str, campaign_map: CampaignMap):
        """Сгенерировать миссию для указанной карты кампании"""
        tvd_builder = self.tvd_builders[campaign_map.tvd_name]
        tvd = tvd_builder.get_tvd(campaign_map.date.strftime(constants.DATE_FORMAT))
        # Генерация первой миссии
        tvd_builder.update(tvd, self._ioc.storage.airfields.load_by_tvd(campaign_map.tvd_name))
        self._ioc.generator.make_ldb(campaign_map.tvd_name)
        self._ioc.generator.make_mission(mission_name, campaign_map.tvd_name)

    def generate(self, mission_name):
        """Сгенерировать текущую миссию кампании с указанным именем"""
        self._generate(mission_name, self.campaign_map)

    def initialize(self):
        """Инициализировать кампанию в БД"""
        for tvd_name in self._ioc.config.mgen.maps:
            self.initialize_map(tvd_name)

        campaign_map = self._ioc.storage.campaign_maps.load_by_order(1)
        self._generate('result1', campaign_map)

    @property
    def campaign_map(self) -> CampaignMap:
        """Текущая карта кампании"""
        for campaign_maps in self._ioc.storage.campaign_maps.load_all():
            if not campaign_maps.is_ended(self._ioc.config.mgen.cfg[campaign_maps.tvd_name][END_DATE]):
                return campaign_maps
        raise NameError('Campaign finished')

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

    def start_mission(self, atype: atypes.Atype0):
        """Обработать начало миссии"""
        source_mission = self._ioc.source_parser.parse_in_dogfight(
            atype.file_path.replace('Multiplayer/Dogfight', '').replace('\\', '').replace('.msnbin', ''))
        self._mission = self._make_campaign_mission(atype, source_mission)
        self._update_tik(atype.tik)
        campaign_map = self.campaign_map
        campaign_map.mission = self._mission
        self._current_tvd = self.tvd_builders[campaign_map.tvd_name].get_tvd(campaign_map.date.strftime(constants.DATE_FORMAT))
        self._ioc.storage.campaign_maps.update(campaign_map)
        # TODO сохранить миссию в базу (в документ CampaignMap и в коллекцию CampaignMissions)
        # TODO удалить файлы предыдущей миссии

    def end_mission(self, atype: atypes.Atype7):
        """Обработать завершение миссии"""
        self._current_tvd = None
        self._update_tik(atype.tik)
        self._mission.is_correctly_completed = True
        self._ioc.storage.campaign_missions.update(self._mission)
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
        self._ioc.generator.make_mission(self.next_name, 'moscow')

    @staticmethod
    def _make_campaign_mission(atype: atypes.Atype0, source_mission: processing.SourceMission) -> CampaignMission:
        return CampaignMission(
            kind=source_mission.kind,
            file=source_mission.name,
            date=source_mission.date.strftime(constants.DATE_FORMAT),
            guimap=source_mission.guimap,
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
            division_units=source_mission.division_units
        )

    def save_mission_info(self, m, m_tvd_name):
        """ Сохранение информации о миссии в JSON для сайта (UTC время конца, самолёты, дата миссии) """
        print('[{}] Saving mission INFO: {}'.format(
            datetime.datetime.now().strftime("%H:%M:%S"),
            m.name
        ))
        period_id = self.tvds[m_tvd_name].current_date_stage_id
        m_length = datetime.timedelta(
            hours=self._ioc.config.main.mission_time['h'],
            minutes=self._ioc.config.main.mission_time['m'],
            seconds=self._ioc.config.main.mission_time['s']
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
