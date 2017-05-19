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
                    log_files = self.get_mission_log_files(name)
                    log = self.read_mission_log(log_files)
                    self.write_mission_log(log, name, len(names_set) - 1 - i)
                    self.archive_log_files(log_files)
                    self.processor.notify(name)
                time.sleep(self.cycle)
            print('AtypesReader stopped')

        def read_mission_names(self):
            files = set()
            for file in self.directory.glob("mission?eport*.txt"):
                files.add(mn.findall(file.name).pop())
            return files

        def get_mission_log_files(self, name):
            mission_file_names = set()
            for file in self.directory.glob(name + "*.txt"):
                mission_file_names.add(MainCfg.logs_directory.joinpath(file.name))
            return mission_file_names

        def read_mission_log(self, files):
            """
            
            :type files: list[Path] 
            :return: 
            """
            log = list()
            for file in files:
                with file.open() as fd:
                    log += fd.readlines()
            return log

        def is_mission_finished(self, atypes):
            for a in atypes:
                if a[1] == 7:
                    return True
            return False

        def format_atypes(self, atypes, name):
            def f(x):
                m = parse(x)
                return m, name, x
            return list(map(f, atypes))

        def write_mission_log(self, logs, name, recent_missions):
            atypes = []
            for line in logs:
                if 'AType:15' in line:
                    continue
                atype_id = int(line.partition('AType:')[2][:2])
                tik = int(line.partition('T:')[2][:2])
                atypes.append((tik, atype_id, line, name))
            c = connector.Log.insert_atypes(atypes)

            if self.is_mission_finished(atypes):
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

        def archive_log_files(self, files):
            for file in files:
                file = Path(file)
                file.rename(self.archive.joinpath(file.name))
