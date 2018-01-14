import datetime


class MissingAType0(Exception):
    pass


class Mission:
    def __init__(self, name):
        self.name = name
        self._force_complete = False
        self.atypes = []
        self.last_atype = 0
        self.g_report = None
        self.processed_t14 = 0
        self.capture_coals = set()

    @property
    def result_name(self):
        return 'result2' if 'result2' in self.at0['file_path'] else 'result1'

    @property
    def next_name(self):
        return 'result1' if 'result2' in self.at0['file_path'] else 'result2'

    @property
    def start(self):
        """ Время начала миссии """
        return datetime.datetime.strptime(self.name, 'missionReport(%Y-%m-%d_%H-%M-%S)')

    @property
    def last_change(self):
        """ Время последнего изменения в миссии """
        lgt = 0
        for at in self.captures:
            if at['tik'] > lgt:
                lgt = at['tik']
        return lgt

    @property
    def at0(self):
        """ Событие начала миссии """
        for x in self.atypes:
            if x['atype_id'] == 0:
                return x
        raise MissingAType0()

    @property
    def captures(self):
        """ Записи событий захватов в миссии """
        return [x for x in [x for x in self.atypes if x['atype_id'] == 8] if x['task_type_id'] == 14]

    @property
    def src(self):
        # TODO реализовать хранение исходников миссий в архиве
        src = mission_report.mission_src.MissionSrc(
            src=MainCfg.dogfight_folder.joinpath('.\\result1_src.Mission').absolute())
        if 'result2' in self.at0['file_path']:
            src = mission_report.mission_src.MissionSrc(
                src=MainCfg.dogfight_folder.joinpath('.\\result2_src.Mission').absolute())
        return src

    @property
    def online_ids(self):
        online_ids = set()
        for atype in sorted(list(x for x in self.atypes if x['atype_id'] in (20, 21)), key=lambda x: x['tik']):
            if atype['atype_id'] == 20:
                online_ids.add(atype['account_id'])
            if atype['atype_id'] == 21:
                if atype['account_id'] in online_ids:
                    online_ids.remove(atype['account_id'])
        return online_ids

    @property
    def is_ended(self):
        if self._force_complete:
            return True
        at7 = [x for x in self.atypes if x['atype_id'] == 7]
        if len(at7) > 1:
            raise Warning
        return False if len(at7) == 0 else True

    def complete(self):
        self._force_complete = True

    @property
    def tvd_name(self):
        for tvd_name in MissionGenCfg.maps:
            if tvd_name in self.src.guimap:
                return tvd_name
        raise NameError('Unknown TVD NAME')

    @property
    def date(self):
        return self.src.date

    @property
    def length(self):
        return datetime.timedelta(
            hours=MainCfg.mission_time['h'],
            minutes=MainCfg.mission_time['m'],
            seconds=MainCfg.mission_time['s']
        )

    @property
    def end(self):
        return self.start + self.length
