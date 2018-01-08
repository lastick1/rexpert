"""Контроль миссий и хода кампании"""
import json
from pathlib import Path
import datetime

import pytz

import configs
import processing

from .tvd import Tvd
from .campaign import ORDER, DATE, MISSION_DATE, TVD_NAME, MONTHS, CampaignMap, DATE_FORMAT

START_DATE = 'start_date'
END_DATE = 'end_date'


class Mission:
    """Миссия"""
    def __init__(self, name: str, source: Path, additional: dict):
        self.name = name
        self.source = source
        self.additional = additional


class CampaignController:
    """Контролеер"""
    def __init__(self, main: configs.Main, mgen: configs.Mgen, generator: processing.Generator):
        self._dogfight = main.dogfight_folder
        self.missions = list()
        self.main = main
        self.mgen = mgen
        self.generator = generator
        self.tvd_builders = {x: processing.TvdBuilder(x, mgen, main, configs.GeneratorParamsConfig(), configs.Planes())
                             for x in mgen.maps}
        self.storage = processing.Storage(main)

    def initialize(self):
        """Инициализировать кампанию в БД"""
        i = 1
        for tvd_name in self.mgen.maps:
            start = self.mgen.cfg[tvd_name][START_DATE]
            self.storage.campaign_maps.update(
                CampaignMap(order=i, date=start, mission_date=start, tvd_name=tvd_name, months=list()))
            i += 1

    @property
    def campaign_map(self) -> CampaignMap:
        """Текущая карта кампании"""
        for campaign in self.storage.campaign_maps.load_all():
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
