import re
import subprocess
import time
import shutil

from pathlib import Path
from datetime import datetime
from configs import Main, Mgen

from .mission_files import MissionFiles
from .locations import *


airfields_raw_re = re.compile(
    '\nAirfield\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
decorations_raw_re = re.compile(
    '\nDecoration\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
ground_objective_raw_re = re.compile(
    '\nGroundObjective\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)
air_objective_raw_re = re.compile(
    '\nAirObjective\n\{[\n\sa-zA-Z0-9=;._ "]*\n\s*}'
)


class Generator:
    def __init__(self, main: Main, mgen: Mgen):
        self.cfg = mgen.cfg
        self.game_folder = main.game_folder
        self.mission_gen_folder = main.mission_gen_folder
        self.resaver_folder = main.resaver_folder
        self.dogfight_folder = main.dogfight_folder
        self.msrc_directory = main.msrc_directory
        self.use_resaver = main.use_resaver
        self.tvd_folders = mgen.tvd_folders

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


class Ldb:
    def __init__(self, tvd_name, areas, objective_nodes, frontline, main: Main, mgen: Mgen, loc_cfg: LocationsConfig):
        """
        Класс для присвоения наций локациям в базе по заданным параметрам
        :param tvd_name: имя ТВД для получения конфига локаций
        :param areas: зоны влияния стран для покраски локаций
        :param objective_nodes: активные узлы
        :param frontline: линия фронта
        """
        folder = main.game_folder.joinpath(Path(mgen.cfg[tvd_name]['tvd_folder']))
        self.ldf_file = folder.joinpath(mgen.cfg[tvd_name]['ldf_file'])
        self.make_ldb_folder = mgen.make_ldb_folder
        with folder.joinpath(mgen.cfg[tvd_name]['ldf_base_file']).open() as f:
            self.ldf_base = f.read()
        self.locations = {
            'airfields': [],
            'air_objectives_recons': [],
            'ground_objectives': [],
            'decorations': [],
            'objective_nodes': []
        }
        for m in air_objective_raw_re.findall(self.ldf_base):
            self.locations['air_objectives_recons'].append(AirObjectiveRecon(str(m)))
        for m in ground_objective_raw_re.findall(self.ldf_base):
            self.locations['ground_objectives'].append(
                GroundObjectiveLocation(str(m), tvd_name, areas, frontline, objective_nodes, loc_cfg))
        for m in decorations_raw_re.findall(self.ldf_base):
            self.locations['decorations'].append(
                DecorationLocation(str(m), tvd_name, areas, frontline, objective_nodes, loc_cfg))

        for country in objective_nodes.keys():
            for node in objective_nodes[country]:
                self.locations['objective_nodes'].append(AirObjectiveLocation(node))
                self.locations['objective_nodes'][-1].loc_country = country

    @property
    def text(self):
        """Текст исходного файла базы локаций"""
        text = '#1CGS Location Database file'
        for k in self.locations:
            for loc in self.locations[k]:
                text += '\n\n{}'.format(loc)
        text += '\n\n#end of file'
        return text

    def make(self):
        """Записать текстовый файл базы локаций и скомпилировать бинарный файл с помощью make_ldb.exe"""
        self.ldf_file.write_text(self.text)
        args = [
            str(self.make_ldb_folder.joinpath('.\\make_ldb.exe').absolute()),
            str(self.ldf_file)
        ]
        # запуск утилиты make_ldb_folder
        generator = subprocess.Popen(args, cwd=str(self.make_ldb_folder), stdout=subprocess.DEVNULL)
        generator.wait()
        time.sleep(3)


class Divisions:
    """Дивизии"""
    def __init__(self, tvd_name, edges, main: Main, mgen: Mgen):
        folder = main.game_folder.joinpath(Path(mgen.cfg[tvd_name]['tvd_folder']))
        self.ldf_file = folder.joinpath(mgen.cfg[tvd_name]['ldf_file'])
        self.divisions = []
        for edge in edges:
            self.divisions.append(Division(
                edge,
                mgen.cfg[tvd_name]['division_margin'],
                mgen.cfg[tvd_name]['division_depth']
            ))

    @property
    def text(self):
        """Текст исходного файла базы локаций"""
        text = '#1CGS Location Database file'
        for division in self.divisions:
            text += '\n\n{}'.format(division)
        text += '\n\n#end of file'
        return text

    def make(self):
        """Записать текстовый файл базы локаций и скомпилировать бинарный файл с помощью make_ldb.exe"""
        self.ldf_file.write_text(self.text)
