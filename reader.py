import threading
import re
import os
import time
import db
from mission_report.parse_mission_log_line import parse
from pathlib import Path
from cfg import MainCfg
connector = db.PGConnector

# missionReport(2016-06-03_22-37-00)[0]
mn = re.compile('^mission.eport\(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d\)')
at = re.compile('^T:(?P<tik>\d+) AType:(?P<atype>\d+)')


class AtypesReader:
    """ Класс, загружающий данные логов в БД и перемещающий лог файлы в папку для статистики
    Singleton """
    instance = None

    def __init__(self, processor, cycle=30):
        if not AtypesReader.instance:
            AtypesReader.instance = AtypesReader.__AtypesReader(
                processor,
                MainCfg.logs_directory,
                MainCfg.arch_directory,
                cycle=cycle
            )
        else:
            AtypesReader.instance.processor = processor
            AtypesReader.instance.directory = MainCfg.logs_directory
            AtypesReader.instance.archive = MainCfg.arch_directory
            AtypesReader.instance.cycle = cycle

    def stop(self):
        self.instance.is_stopped = True
        self.instance.join()

    def start(self):
        self.instance.is_stopped = False
        self.instance.start()

    class __AtypesReader(threading.Thread):
        def __init__(self, processor, directory, archive, cycle=30):
            threading.Thread.__init__(self)
            self.is_stopped = False
            self.cycle = cycle
            self.directory = Path(directory)
            self.archive = Path(archive)
            self.processor = processor
            self.start()

        def __str__(self):
            return repr(self) + " Working on: " + self.directory.name + "\tarchive: " + self.archive.name

        def run(self):
            self.do_work_until_stop()

        def do_work_until_stop(self):
            print('AtypesReader started')
            while not self.is_stopped:
                names_set = sorted(self.read_mission_names())
                for i in range(len(names_set)):
                    name = names_set[i]
                    formatted = self.format_atypes(self.read_mission_log(name), name)
                    self.write_mission_log(formatted, name, len(names_set) - 1 - i)
                    self.processor.notify(name)
                    self.move_mission_log_files(self.get_mission_log_file_names(name))
                time.sleep(self.cycle)
            print('AtypesReader stopped')

        def read_mission_names(self):
            files = set()
            for file in self.directory.glob("mission?eport*.txt"):
                files.add(mn.findall(file.name).pop())
            return files

        def get_mission_log_file_names(self, name):
            mission_file_names = set()
            for file in self.directory.glob(name + "*.txt"):
                mission_file_names.add(file.name)
            return mission_file_names

        def read_mission_log(self, name):
            log = list()
            for file in self.get_mission_log_file_names(name):
                var = str(self.directory.joinpath(file).absolute())
                with open(var) as fd:
                    log += fd.readlines()
            return log

        def is_mission_finished(self, atypes):
            at7 = [x for x in atypes if x[0]['atype_id'] == 7]
            if len(at7) > 1:
                raise Warning
            return False if len(at7) == 0 else True

        def format_atypes(self, atypes, name):
            def f(x):
                m = parse(x)
                return m, name, x
            return list(map(f, atypes))

        def write_mission_log(self, formatted, name, recent_missions):
            c = connector.Log.insert_atypes(sorted([x for x in formatted if x[0]['atype_id'] != 15], key=lambda k: k[0]['tik']))

            if self.is_mission_finished(formatted):
                connector.Log.insert_or_update_mission_row(
                    is_processed=False,
                    mission_name=name,
                    is_ended_correctly=True,
                    is_ended=True
                )
            else:
                if recent_missions < 0:
                    raise Exception
                if recent_missions > 0:
                    connector.Log.insert_or_update_mission_row(
                        is_processed=False,
                        mission_name=name,
                        is_ended_correctly=False,
                        is_ended=True
                    )
                else:
                    connector.Log.insert_or_update_mission_row(
                        is_processed=False,
                        mission_name=name,
                        is_ended_correctly=False,
                        is_ended=False
                    )
            return c[-1]

        def move_mission_log_files(self, file_names):
            for file in file_names:
                file_src_abs = str(self.directory.joinpath(file).absolute())
                file_dest_abs = str(self.archive.joinpath(file).absolute())
                os.rename(file_src_abs, file_dest_abs)
