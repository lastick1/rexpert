"""Чтение логов"""
import pathlib
import re
import threading

import time

import os

import configs

from .events_control import EventsController


mn = re.compile('^mission.eport\(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d\)')


class LogsReader:
    """ Класс, загружающий данные логов в БД и перемещающий лог файлы в папку для статистики
    Singleton """
    instance = None

    def __init__(self, main: configs.Main, controller: EventsController, cycle=30):
        if not LogsReader.instance:
            LogsReader.instance = LogsReader.__AtypesReader(
                main,
                controller,
                cycle=cycle
            )
        else:
            LogsReader.instance.processor = controller
            LogsReader.instance.main = main
            LogsReader.instance.cycle = cycle

    def stop(self):
        self.instance.is_stopped = True
        self.instance.join()

    def start(self):
        self.instance.is_stopped = False
        self.instance.start()

    class __AtypesReader(threading.Thread):
        def __init__(self, main: configs.Main, controller: EventsController, cycle=30):
            threading.Thread.__init__(self)
            self.is_stopped = False
            self.cycle = cycle
            self.main = main
            self.controller = controller
            self.start()

        def __str__(self):
            return repr(self) + " Working on: " + self.main.logs_directory.name + "\tarchive: " + self.main.arch_directory.name

        def run(self):
            self.do_work_until_stop()

        def do_work_until_stop(self):
            print('LogsReader started')
            while not self.is_stopped:
                names_set = sorted(self.read_mission_names())
                for i in range(len(names_set)):
                    name = names_set[i]
                    log_files = self.get_mission_log_files(name)
                    log = self.read_mission_log(log_files)
                    for line in log:
                        self.controller.process_line(line)
                time.sleep(self.cycle)
            print('LogsReader stopped')

        def read_mission_names(self):
            files = set()
            for file in self.main.logs_directory.glob("mission?eport*.txt"):
                files.add(mn.findall(file.name).pop())
            return files

        def read_mission_log(self, files):
            """
            :type files: list[Path]
            :return:
            """
            log = list()
            for file in files:
                path = pathlib.Path(file)
                with path.open() as stream:
                    log += stream.readlines()
                path.rename(self.main.arch_directory.joinpath(path.name))
            return log

        def get_mission_log_files(self, name):
            """Отсортированный по дате создания список имён файлов лога миссии"""
            return sorted(list(str(x) for x in self.main.logs_directory.glob(name + "*.txt")), key=os.path.getmtime)