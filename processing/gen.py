"""Сборка бинарных файлов в scg и генерация миссий"""
import datetime
import pathlib
import subprocess
import logging
import time
import shutil

import configs

from .mission_files import MissionFiles


class Generator:
    """Класс управления сборкой миссий"""
    def __init__(self, config: configs.Config):
        self.mgen = config.mgen
        self.main = config.main

    def make_ldb(self, tvd_name: str):
        """Записать текстовый файл базы локаций и скомпилировать бинарный файл с помощью make_ldb.exe"""
        logging.debug('Compiling LDB binary file...')
        args = [
            str(self.mgen.make_ldb_folder.joinpath('./make_ldb.exe').absolute()),
            str(self.mgen.ldf_files[tvd_name])
        ]
        # запуск утилиты make_ldb_folder
        generator = subprocess.Popen(args, cwd=str(self.mgen.make_ldb_folder), stdout=subprocess.DEVNULL)
        generator.wait()
        time.sleep(3)
        logging.debug('... LDB binary done')

    def make_lgb(self, tvd_name: str):
        """Скомпилировать общие (сцену) декорации ТВД"""
        lgb_file = pathlib.Path(self.mgen.lgb_files[tvd_name])
        lgb_bin_file = pathlib.Path(self.mgen.lgb_bin_files[tvd_name])
        make_lgb = self.main.mission_gen_folder.joinpath('./make_lgb.exe').absolute()
        if not lgb_bin_file.exists():
            if not make_lgb.exists():
                logging.warning(f'make_lgb.exe not found {make_lgb}')
                return
            logging.info('Generating LGB file...')
            args = [str(make_lgb), str(lgb_file)]
            generator = subprocess.Popen(args, stdout=subprocess.DEVNULL)
            generator.wait()
            time.sleep(3)
            logging.info('... LGB done')

    def make_mission(self, mission_template: str, file_name: str, tvd_name: str):
        """
        Метод генерирует и перемещает миссию в папку Multiplayer/Dogfight
        :param mission_template: путь к файлу шаблона миссии
        :param file_name: имя файла миссии
        :param tvd_name: имя карты
        :return:
        """
        tvd_folder = self.mgen.tvd_folders[tvd_name]
        default_params = tvd_folder.joinpath(self.mgen.cfg[tvd_name]['default_params_dest']).absolute()
        logging.info(f'Generating new mission: [{file_name}]...')
        now = str(datetime.datetime.now()).replace(":", "-").replace(" ", "_")
        logging.debug(f'template: [{mission_template}]')
        with open(str(self.main.mission_gen_folder) + r"\missiongen_log_" + now + ".txt", "w") as missiongen_log:
            args = [
                str(self.main.mission_gen_folder) + r"\MissionGen.exe",
                "--params",
                str(default_params),
                "--all-langs",
                mission_template
            ]
            # запуск генератора миссии
            generator = subprocess.Popen(args, cwd=str(self.main.mission_gen_folder), stdout=missiongen_log)
            generator.wait()
            time.sleep(0.5)
        if generator.returncode is 0:
            mission_files = MissionFiles(
                self.main.game_folder.joinpath(r'.\data\Missions\result.Mission'),
                self.main.game_folder,
                self.main.resaver_folder)
            if self.main.use_resaver:
                mission_files.resave()
            mission_files.move_to_dogfight(file_name, self.main.server_folder)
            mission_files.detach_src()
            logging.info('... generation done!')
        else:
            logging.error(f'...generation failed! {generator.returncode}')

    def save_files_for_zlo(self, file_name):
        """Копирование файлов для -DED-Zlodey"""
        suffix = '_src'
        mission = '.Mission'
        if file_name == 'result1':
            src = 'result2'
        else:
            src = 'result1'
        src_file = self.main.dogfight_folder.joinpath(src + suffix + mission)
        dst_file = self.main.msrc_directory.joinpath(src + mission)
        shutil.copyfile(str(src_file), str(dst_file))
