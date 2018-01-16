"""Контроль миссий и хода кампании"""
import json
import pathlib
import datetime
import pytz

import atypes
import processing

from .tvd import Tvd
from .campaign_map import CampaignMap, DATE_FORMAT
from .airfields_control import AirfieldsController

START_DATE = 'start_date'
END_DATE = 'end_date'


class Mission:
    """Миссия"""
    def __init__(self, name: str, source: pathlib.Path, additional: dict):
        self.name = name
        self.source = source
        self.additional = additional


class CampaignController:
    """Контролеер кампании"""
    def __init__(self, ioc):
        self._ioc = ioc
        self._dogfight = ioc.config.main.dogfight_folder
        self.missions = list()
        self.main = ioc.config.main
        self.mgen = ioc.config.mgen
        self.vendor = processing.AircraftVendor(ioc.config.planes, ioc.config.gameplay)
        self.tvd_builders = {x: processing.TvdBuilder(x, ioc) for x in ioc.config.mgen.maps}

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
        self._ioc.storage.campaign_maps.update(campaign_map)
        self._ioc.storage.airfields.update_airfields(airfields)

    def reset(self):
        """Сбросить состояние кампании"""
        self._ioc.storage.airfields.collection.drop()
        self._ioc.storage.campaign_maps.collection.drop()

    def _generate(self, mission_name: str, campaign_map: CampaignMap):
        """Сгенерировать миссию для указанной карты кампании"""
        tvd_builder = self.tvd_builders[campaign_map.tvd_name]
        tvd = tvd_builder.get_tvd(campaign_map.date.strftime(DATE_FORMAT))
        # Генерация первой миссии
        tvd_builder.update(tvd, self._ioc.storage.airfields.load_by_tvd(campaign_map.tvd_name))
        self._ioc.generator.make_ldb(campaign_map.tvd_name)
        self._ioc.generator.make_mission(mission_name, campaign_map.tvd_name)

    def generate(self, mission_name):
        """Сгенерировать текущую миссию кампании с указанным именем"""
        self._generate(mission_name, self.campaign_map)

    def initialize(self):
        """Инициализировать кампанию в БД"""
        for tvd_name in self.mgen.maps:
            self.initialize_map(tvd_name)

        campaign_map = self._ioc.storage.campaign_maps.load_by_order(1)
        self._generate('result1', campaign_map)

    @property
    def campaign_map(self) -> CampaignMap:
        """Текущая карта кампании"""
        maps = self._ioc.storage.campaign_maps.load_all()
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

    def start_mission(self, atype: atypes.Atype0):
        """Обработать начало миссии"""
        name = atype.file_path.replace('Multiplayer/Dogfight', '').replace('\\', '')
        name = name.replace('.msnbin', '')
        source = pathlib.Path(self._dogfight.joinpath(name + '_src.Mission')).absolute()
        additional = {
            'date': atype.date,
            'game_type_id': atype.game_type_id,
            'countries': atype.countries,
            'settings': atype.settings,
            'mods': atype.mods,
            'preset_id': atype.preset_id
        }
        self.missions.append(Mission(name, source, additional))
        next_name = 'result1' if name == 'result2' else 'result2'
        self._ioc.generator.make_mission(next_name, 'moscow')
        # TODO удалить предыдущую миссию

    def end_mission(self, atype: atypes.Atype7):
        """Обработать завершение миссии"""
        # TODO "приземлить" всех

    def end_round(self, atype: atypes.Atype19):
        """Обработать завершение раунда (4-минутный отсчёт до конца миссии)"""
        # TODO подвести итог миссии
        # TODO отправить инпут завершения миссии (победа/ничья)
        # TODO сгенерировать следующую миссию

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
