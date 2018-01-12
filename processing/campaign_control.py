"""Контроль миссий и хода кампании"""
import json
from pathlib import Path
import datetime

import pytz

import configs
import processing

from .tvd import Tvd
from .campaign_map import CampaignMap, DATE_FORMAT
from .airfields_control import AirfieldsController

START_DATE = 'start_date'
END_DATE = 'end_date'


class Mission:
    """Миссия"""
    def __init__(self, name: str, source: Path, additional: dict):
        self.name = name
        self.source = source
        self.additional = additional


class CampaignController:
    """Контролеер кампании"""
    def __init__(self, config: configs.Config):
        self._dogfight = config.main.dogfight_folder
        self.missions = list()
        self.main = config.main
        self.mgen = config.mgen
        self.vendor = processing.AircraftVendor(config.planes, config.gameplay)
        self.generator = processing.Generator(config)
        self.tvd_builders = {x: processing.TvdBuilder(x, config) for x in config.mgen.maps}
        self.storage = processing.Storage(config.main)

    def initialize_map(self, tvd_name: str):
        """Инициализировать карту кампании"""
        start = self.mgen.cfg[tvd_name][START_DATE]
        order = list(self.mgen.maps).index(tvd_name) + 1
        campaign_map = CampaignMap(order=order, date=start, mission_date=start, tvd_name=tvd_name, months=list())
        airfields = AirfieldsController.initialize_managed_airfields(self.mgen.airfields_data[campaign_map.tvd_name])
        tvd_builder = self.tvd_builders[campaign_map.tvd_name]
        tvd = tvd_builder.get_tvd(campaign_map.date.strftime(DATE_FORMAT))
        supply = self.vendor.get_month_supply(campaign_map.current_month, campaign_map)
        self.vendor.deliver_month_supply(campaign_map, tvd.to_country_dict_rear(airfields), supply)
        self.vendor.initial_front_supply(campaign_map, tvd.to_country_dict_front(airfields))
        self.storage.campaign_maps.update(campaign_map)
        self.storage.airfields.update_airfields(airfields)

    def reset(self):
        """Сбросить состояние кампании"""
        self.storage.airfields.collection.drop()
        self.storage.campaign_maps.collection.drop()

    def _generate(self, mission_name: str, campaign_map: CampaignMap):
        """Сгенерировать миссию для указанной карты кампании"""
        tvd_builder = self.tvd_builders[campaign_map.tvd_name]
        tvd = tvd_builder.get_tvd(campaign_map.date.strftime(DATE_FORMAT))
        # Генерация первой миссии
        tvd_builder.update(tvd, self.storage.airfields.load_by_tvd(campaign_map.tvd_name))
        self.generator.make_ldb(campaign_map.tvd_name)
        self.generator.make_mission(mission_name, campaign_map.tvd_name)

    def generate(self, mission_name):
        """Сгенерировать текущую миссию кампании с указанным именем"""
        self._generate(mission_name, self.campaign_map)

    def initialize(self):
        """Инициализировать кампанию в БД"""
        for tvd_name in self.mgen.maps:
            self.initialize_map(tvd_name)

        campaign_map = self.storage.campaign_maps.load_by_order(1)
        self._generate('result1', campaign_map)

    @property
    def campaign_map(self) -> CampaignMap:
        """Текущая карта кампании"""
        maps = self.storage.campaign_maps.load_all()
        for campaign in maps:
            if not campaign.is_ended(self.mgen.cfg[campaign.tvd_name][END_DATE]):
                return campaign
        raise NameError('Campaign finished')

    @property
    def current_tvd(self) -> Tvd:
        """Текущий ТВД"""
        campaign_map = self.campaign_map
        tvd_builder = self.tvd_builders[campaign_map.tvd_name]
        return tvd_builder.get_tvd(campaign_map.date.strftime(DATE_FORMAT))

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
