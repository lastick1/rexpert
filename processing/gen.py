"""Сборка бинарных файлов в scg и генерация миссий"""
import subprocess
import time
import shutil

from datetime import datetime
from configs import Main, Mgen

from .mission_files import MissionFiles


class Generator:
    """Класс управления сборкой миссий"""
    def __init__(self, main: Main, mgen: Mgen):
        self.cfg = mgen.cfg
        self.game_folder = main.game_folder
        self.mission_gen_folder = main.mission_gen_folder
        self.resaver_folder = main.resaver_folder
        self.dogfight_folder = main.dogfight_folder
        self.msrc_directory = main.msrc_directory
        self.use_resaver = main.use_resaver
        self.tvd_folders = mgen.tvd_folders
        self.make_ldb_folder = mgen.make_ldb_folder
        self.ldf_files = mgen.ldf_files

    def make_ldb(self, tvd_name: str):
        """ Записать текстовый файл базы локаций и скомпилировать бинарный файл с помощью make_ldb.exe """
        args = [
            str(self.make_ldb_folder.joinpath('.\\make_ldb.exe').absolute()),
            str(self.ldf_files[tvd_name])
        ]
        # запуск утилиты make_ldb_folder
        generator = subprocess.Popen(args, cwd=str(self.make_ldb_folder), stdout=subprocess.DEVNULL)
        generator.wait()
        time.sleep(3)

    def make_mission(self, file_name: str, tvd_name: str):
        """
        Метод генерирует и перемещает миссию в папку Multiplayer/Dogfight
        :param file_name: имя файла миссии
        :param tvd_name: имя карты
        :return:
        """
        tvd_folder = self.tvd_folders[tvd_name]
        default_params = tvd_folder.joinpath(self.cfg[tvd_name]['default_params_dest']).absolute()
        mission_template = tvd_folder.joinpath(self.cfg[tvd_name]['mt_file']).absolute()
        print("[{}] Generating new mission: [{}]...".format(
            datetime.now().strftime("%H:%M:%S"),
            file_name
        ))
        now = str(datetime.now()).replace(":", "-").replace(" ", "_")
        with open(str(self.mission_gen_folder) + r"\missiongen_log_" + now + ".txt", "w") as missiongen_log:
            args = [
                str(self.mission_gen_folder) + r"\MissionGen.exe",
                "--params",
                str(default_params),
                "--all-langs",
                str(mission_template)
            ]
            # запуск генератора миссии
            generator = subprocess.Popen(args, cwd=str(self.mission_gen_folder), stdout=missiongen_log)
            generator.wait()
            time.sleep(0.5)

        mission_files = MissionFiles(
            self.game_folder.joinpath(r'.\data\Missions\result.Mission'),
            self.game_folder,
            self.resaver_folder)
        if self.use_resaver:
            mission_files.resave()
        mission_files.move_to_dogfight(file_name)
        mission_files.detach_src()
        print("... generation done!")

    def save_files_for_zlo(self, file_name):
        """Копирование файлов для -DED-Zlodey"""
        suffix = '_src'
        mission = '.Mission'
        if file_name == 'result1':
            src = 'result2'
        else:
            src = 'result1'
        src_file = self.dogfight_folder.joinpath(src + suffix + mission)
        dst_file = self.msrc_directory.joinpath(src + mission)
        shutil.copyfile(str(src_file), str(dst_file))
