"RX-based logs parser"
# pylint:disable=E1101
from __future__ import annotations

import re
import os
import logging
import time
import datetime
import shutil

from pathlib import Path
from rx import interval
from rx.core.abc.observer import Observer
from rx.core.abc.disposable import Disposable
from model import ManagedAirfield
from configs import Config
from core import EventsEmitter, Atype9
from services import AirfieldsService


LOG_FILE_INDEX_RE = re.compile(r'^.*\[(?P<index>\d+)\].*$')

MISSION_LOG_FILE_RE = re.compile(
    r'^.*port\(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d\)')  # pylint:disable=W1401
MISSION_NAME = re.compile(
    r'^.*port\((?P<mission_name>\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)\)')  # pylint:disable=W1401


class MissionLogs:
    """Класс файлов лога миссии"""

    def __init__(self, *args, **kwargs):
        self._args: tuple = args
        self.name: str = kwargs['name']
        self.arch_directory: Path = Path(
            kwargs['arch_directory'])
        self.datetime: datetime.datetime = datetime.datetime.strptime(
            kwargs['name'], '%Y-%m-%d_%H-%M-%S')
        self.files: list = []

    def __eq__(self, value):
        return self.name.__eq__(value)

    def read_mission_log(self) -> list:
        """
        :type files: list[Path]
        :return:
        """
        log = list()
        for file in self._log_files:
            with open(file) as stream:
                log += stream.readlines()
        return log

    def move_files(self) -> None:
        "Двинуть файлы в папку для il2_stats"
        for file in self._log_files:
            file_name = Path(file).name
            new_name = str(self.arch_directory.joinpath(file_name))
            shutil.move(file, new_name)

    @property
    def has_first_log_file(self):
        "Есть ли первый лог файл миссии"
        return len(list([x for x in self.files if x.find('[0]') != -1])) == 1

    def write_airfields(self, airfields: dict) -> None:
        "Записать аэродромы в первый лог файл миссии"
        _id = 100
        atypes = list()
        for country in airfields:
            for item in airfields[country]:
                airfield: ManagedAirfield = item
                atypes.append(str(Atype9(10, _id, country, int(
                    country/100), [], {'x': airfield.x, 'z': airfield.z})) + '\n')
                _id += 2
        for file in sorted(self._log_files, key=lambda x: int(LOG_FILE_INDEX_RE.match(x).groupdict()['index'])):
            if file.find('[0]') != -1:
                with open(self._log_files[0], 'a',) as stream:
                    stream.writelines(atypes)
            else:
                Path(file).touch()
            time.sleep(0.01)

    @property
    def _log_files(self):
        """Отсортированный по дате создания список имён файлов лога миссии"""
        return sorted(list(str(x) for x in self.files), key=os.path.getmtime)


class LogsReaderRx(Observer):
    "Класс чтения логов миссий"

    def __init__(
            self,
            config: Config,
            emitter: EventsEmitter,
            airfields_service: AirfieldsService,
    ):
        self._config: Config = config
        self._emitter: EventsEmitter = emitter
        self._airfields_service: AirfieldsService = airfields_service
        self.subscription: Disposable = None
        self.is_reading: bool = False

    def start(self):
        "Запустить чтение логов"
        self.subscription = interval(
            self._config.main.logs_read_interval).subscribe(self)
        self.read()

    def stop(self):
        "Остановить чтение логов"
        self.subscription.dispose()

    def on_next(self, value):
        "Обработка очередного значения потока"
        if not self.is_reading:
            self.read()

    def read(self):
        "Выполнить чтение логов"
        self.is_reading = True
        missions = self._read_mission_names()
        mission_names = sorted(missions.keys())
        for item in mission_names:
            mission: MissionLogs = missions[item]
            log = mission.read_mission_log()
            for line in log:
                if self._config.main.debug_mode:
                    self._emitter.process_line(line)
                else:
                    try:
                        self._emitter.process_line(line)
                    except (AttributeError, Exception) as exception:
                        logging.exception(f'Error {exception} on line: {line}')
            if mission.has_first_log_file:
                airfields = self._airfields_service.inactive_airfield_by_countries
                mission.write_airfields(airfields)
            if not self._config.main.debug_mode:
                mission.move_files()
        self.is_reading = False

    def on_completed(self):
        "Завершение потока"
        logging.info("completed")

    def on_error(self, error):
        "Ошибка потока"
        logging.info("error")

    def _read_mission_names(self) -> dict:
        """Прочитать имена миссий в папке логов"""
        result = dict()
        files = [x for x in os.listdir(
            self._config.main.logs_directory) if MISSION_LOG_FILE_RE.match(x)]
        for file in files:
            mission_name = MISSION_NAME.match(
                file).groupdict()['mission_name']
            if mission_name not in result:
                result[mission_name] = MissionLogs(
                    name=mission_name,
                    arch_directory=self._config.main.arch_directory
                )
            result[mission_name].files.append(
                str(Path(self._config.main.logs_directory).joinpath(file)))
        return result
