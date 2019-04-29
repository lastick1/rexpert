"Обработка событий из логов с использованием потоков (Rx)"
from __future__ import annotations
import logging
from typing import Tuple
from rx.subjects import Subject
from rx.core.abc.disposable import Disposable
from .atypes import Atype0, Atype1, Atype2, Atype3, Atype4, Atype5, Atype6, Atype7, Atype8, Atype9, \
    Atype10, Atype11, Atype12, Atype13, Atype14, Atype15, Atype16, Atype17, Atype18, Atype19, \
    Atype20, Atype21, Atype22
from .parse_mission_log_line import parse, UnexpectedATypeWarning


class AtypesEmitter(Disposable):
    "Источник событий из логов"

    def __init__(self):
        self._countries = dict()
        self._constructors = (Atype0, Atype1, Atype2, Atype3, Atype4, Atype5, Atype6, Atype7, Atype8, Atype9,
                              Atype10, Atype11, Atype12, Atype13, Atype14, Atype15, Atype16, Atype17, Atype18, Atype19,
                              Atype20, Atype21, Atype22)
        self._atypes: Tuple[Subject] = tuple(Subject() for x in range(22))

    def dispose(self):
        for subject in self._atypes:
            subject.on_completed()
            subject.dispose()

    def process_line(self, line: str):
        "Обработать строчку из логов"
        try:
            if 'AType' not in line:
                raise NameError(f'ignored bad string: [{line}]')

            if r'T:0 AType:0 GDate:1942.7.1 GTime:17:52:45 MFile' in line:
                print('AType:0')

            atype = parse(line)
            atype_id = atype.pop('atype_id')
            if atype_id == 0:
                self._countries = atype['countries']
            if 'country_id' in atype.keys():
                atype['coal_id'] = self._countries[atype['country_id']]
            obj = self._constructors[atype_id](**atype)
            self._atypes[atype_id].on_next(obj)

        except UnexpectedATypeWarning:
            logging.warning(f'unexpected atype: [{line}]')
        except Exception as exception:
            print(exception)
