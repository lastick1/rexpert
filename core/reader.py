"""Чтение логов"""
import logging
import pathlib
import re
import threading
import datetime
import shutil
import time
import os


MISSION_LOG_FILE_RE = re.compile(
    r'^mission.eport\(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d\)')  # pylint:disable=W1401
MISSION_NAME = re.compile(
    r'^mission.eport\((?P<mission_name>\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)\)')  # pylint:disable=W1401


class MissionLogs:
    """Класс файлов лога миссии"""

    def __init__(self, *args, **kwargs):
        self._args: tuple = args
        self.name: str = kwargs['name']
        self.arch_directory: pathlib.Path = pathlib.Path(
            kwargs['arch_directory'])
        self.datetime: datetime.datetime = datetime.datetime.strptime(
            kwargs['name'], '%Y-%m-%d_%H-%M-%S')
        self.files: list = []

    def __eq__(self, value):
        return self.name.__eq__(value)

    def read_mission_log(self):
        """
        :type files: list[Path]
        :return:
        """
        log = list()
        new_files = list()
        for file in self._log_files:
            with open(file) as stream:
                log += stream.readlines()
            file_name = pathlib.Path(file).name
            new_name = str(self.arch_directory.joinpath(file_name))
            shutil.move(file, new_name)
            new_files.append(new_name)
        return log

    @property
    def _log_files(self):
        """Отсортированный по дате создания список имён файлов лога миссии"""
        return sorted(list(str(x) for x in self.files), key=os.path.getmtime)


class LogsReader:
    """Класс, загружающий данные логов в БД и перемещающий лог файлы в папку для статистики"""
    instance = None

    def __init__(self, _ioc, cycle=30):
        if not LogsReader.instance:
            LogsReader.instance = LogsReader._AtypesReader(_ioc, cycle)
        else:
            LogsReader.instance.processor = _ioc.events_controller
            LogsReader.instance.main = _ioc.config.main
            LogsReader.instance.cycle = cycle

    def stop(self):
        """Остановить процесс чтения логов"""
        self.instance.is_stopped = True
        self.instance.join()

    def start(self):
        """Запустить процесс чтения логов"""
        self.instance.is_stopped = False
        self.instance.start()

    class _AtypesReader(threading.Thread):
        """Singleton"""

        def __init__(self, _ioc, cycle: int):
            threading.Thread.__init__(self)
            self._ioc = _ioc
            self.is_stopped = False
            self.cycle = cycle

        def __str__(self):
            return repr(self) + " Working on: " + self._ioc.config.main.logs_directory.name\
                + "\tarchive: " + self._ioc.config.main.arch_directory.name

        def run(self):
            self.do_work_until_stop()

        def do_work_until_stop(self):
            """Запустить бесконечный цикл"""
            logging.info('LogsReader started {}'.format(
                self._ioc.config.main.logs_directory))
            while not self.is_stopped:
                missions = sorted(self.read_mission_names().values())
                for mission in missions:
                    log = mission.read_mission_log()
                    for line in log:
                        self._ioc.events_controller.process_line(line)
                time.sleep(self.cycle)
            logging.info('LogsReader stopped')

        def read_mission_names(self) -> dict:
            """Прочитать имена миссий в папке логов"""
            result = dict()
            files = [x for x in os.listdir(
                self._ioc.config.main.logs_directory) if MISSION_LOG_FILE_RE.match(x)]
            for file in files:
                mission_name = MISSION_NAME.match(
                    file).groupdict()['mission_name']
                if mission_name not in result:
                    result[mission_name] = MissionLogs(
                        name=mission_name,
                        arch_directory=self._ioc.config.main.arch_directory
                    )
                result[mission_name].files.append(
                    str(pathlib.Path(self._ioc.config.main.logs_directory).joinpath(file)))
            return result
