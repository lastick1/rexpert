import re
import subprocess
import time
import shutil
import os

from pathlib import Path
from datetime import datetime
from grid import Point
from cfg import MissionGenCfg, MainCfg, LocationsCfg
from geometry import Segment


class Group:
    def __init__(self, group_file):
        """ Класс групп-файлов, из которых генератор по шаблону собирает миссию
        :param group_file: Path """
        tmp = group_file.absolute()
        self.files = {
            'Group': tmp,
            'eng': Path(''.join(str(tmp).split('.')[:-1]) + '.eng'),
            'fra': Path(''.join(str(tmp).split('.')[:-1]) + '.fra'),
            'rus': Path(''.join(str(tmp).split('.')[:-1]) + '.rus'),
            'ger': Path(''.join(str(tmp).split('.')[:-1]) + '.ger'),
            'pol': Path(''.join(str(tmp).split('.')[:-1]) + '.pol'),
            'spa': Path(''.join(str(tmp).split('.')[:-1]) + '.spa')
        }

    def clone_to(self, folder):
        """ Копирование файлов группы в указанную папку """
        f = str(folder)
        for file_ext in self.files:
            self.files[file_ext] = Path(shutil.copy(str(self.files[file_ext]), f))

    def rename(self, dst):
        """ Смена имён файлов на dst """
        dst_path = os.path.dirname(str(self.files['Group'])) + '\\' + dst
        for file_ext in self.files:
            tmp = Path(dst_path + '.' + file_ext)
            if tmp.exists():
                os.remove(str(tmp))
            self.files[file_ext].rename(tmp)
            self.files[file_ext] = tmp

    def replace_content(self, src, dst):
        """ Замена src в содержимом файлов группы на dst """
        for file_ext in self.files:
            if file_ext == 'Group':
                content = self.files[file_ext].read_text(encoding='utf-8').replace(src, dst)
                self.files[file_ext].write_text(content, encoding='utf-8')
            else:
                content = self.files[file_ext].read_text(encoding='utf-16-le').replace(src, dst)
                self.files[file_ext].write_text(content, encoding='utf-16-le')


class MissionFiles:
    def __init__(self, mission_file):
        """ Класс миссии в файловой системе, для перемещения и переименования файлов миссии """
        tmp = mission_file.absolute()
        self.files = {
            'Mission': tmp,
            'msnbin': Path(''.join(str(tmp).split('.')[:-1]) + '.msnbin'),
            'list': Path(''.join(str(tmp).split('.')[:-1]) + '.list'),
            'eng': Path(''.join(str(tmp).split('.')[:-1]) + '.eng'),
            'fra': Path(''.join(str(tmp).split('.')[:-1]) + '.fra'),
            'rus': Path(''.join(str(tmp).split('.')[:-1]) + '.rus'),
            'ger': Path(''.join(str(tmp).split('.')[:-1]) + '.ger'),
            'pol': Path(''.join(str(tmp).split('.')[:-1]) + '.pol'),
            'spa': Path(''.join(str(tmp).split('.')[:-1]) + '.spa')
        }

    def _replace(self, dst):
        """ Перемещение файлов миссии в указанную папку с заменой """
        for file_ext in self.files:
            tmp = Path(str(dst) + '.' + file_ext)
            self.files[file_ext].replace(tmp)
            self.files[file_ext] = tmp

    def move_to_dogfight(self, name):
        """ Перемещение файлов миссии в папку Multiplayer/Dogfight с заменой
        :param name: Имя файлов миссии"""
        # меняем в лист-файле пути к файлам локализации
        content = self.files['list'].read_text(encoding='utf-8').replace('missions/', 'multiplayer/dogfight/')
        content = content.replace('result', name)
        self.files['list'].write_text(content, encoding='utf-8')
        # вычисляем путь к папке data
        d = os.path.dirname(str(self.files['Mission']))
        while d.split(sep='\\')[-1] != 'data':
            d = str(Path(d).joinpath(os.pardir).resolve())
        # переносим файлы с заменой
        self._replace(Path(d).joinpath('.\\Multiplayer\\Dogfight\\' + name))

    def resave(self):
        now = str(datetime.now()).replace(":", "-").replace(" ", "_")
        resaver_folder = str(MainCfg.resaver_folder)
        data_folder = str(MainCfg.game_folder.joinpath(r'.\data'))
        with open(resaver_folder + r"\resaver_log_" + now + ".txt", "w") as resaver_log:
            args = [
                str(MainCfg.resaver_folder) + r"\MissionResaver.exe",
                "-d",
                data_folder,
                "-f",
                str(self.files['Mission'])
            ]
            resaver = subprocess.Popen(args, cwd=str(resaver_folder), stdout=resaver_log)
            resaver.wait()
            time.sleep(0.5)

    def detach_src(self):
        """ Переименование файла исходника миссии с заменой, чтобы он не был использован DServer """
        p = Path(os.path.splitext(str(self.files['Mission']))[0] + '_src.Mission')
        self.files['Mission'].replace(p)
        self.files['Mission'] = p

    # TODO сделать вместо detach - zip архив
    def zip_src(self):
        raise NotImplemented


class Generator:
    @staticmethod
    def make_mission(file_name, tvd_name):
        """
        Метод генерирует и перемещает миссию в папку Multiplayer/Dogfight
        :param file_name: имя файла миссии
        :param tvd_name: имя карты
        :return:
        """
        Generator.save_files_for_zlo(file_name)

        default_params = MissionGenCfg.tvd_folders[tvd_name].joinpath(
            MissionGenCfg.cfg[tvd_name]['default_params_dest']).absolute()
        mission_template = MissionGenCfg.tvd_folders[tvd_name].joinpath(
            MissionGenCfg.cfg[tvd_name]['mt_file']).absolute()
        print("[{}] Generating new mission: [{}]...".format(
            datetime.now().strftime("%H:%M:%S"),
            file_name
        ))
        now = str(datetime.now()).replace(":", "-").replace(" ", "_")
        with open(str(MainCfg.mission_gen_folder) + r"\missiongen_log_" + now + ".txt", "w") as missiongen_log:
            args = [
                str(MainCfg.mission_gen_folder) + r"\MissionGen.exe",
                "--params",
                str(default_params),
                "--all-langs",
                str(mission_template)
            ]
            # запуск генератора миссии
            generator = subprocess.Popen(args, cwd=str(MainCfg.mission_gen_folder), stdout=missiongen_log)
            generator.wait()
            time.sleep(0.5)

        mission_files = MissionFiles(MainCfg.game_folder.joinpath(r'.\data\Missions\result.Mission'))
        if MainCfg.use_resaver:
            mission_files.resave()
        mission_files.move_to_dogfight(file_name)
        mission_files.detach_src()
        print("... generation done!")

    @staticmethod
    def save_files_for_zlo(file_name):
        """ Копирование файлов для -DED-Zlodey """
        suffix = '_src'
        mission = '.Mission'
        if file_name == 'result1':
            src = 'result2'
        else:
            src = 'result1'
        src_file = MainCfg.dogfight_folder.joinpath(src + suffix + mission)
        dst_file = MainCfg.msrc_directory.joinpath(src + mission)
        shutil.copyfile(str(src_file), str(dst_file))

        logs_dir = MainCfg.arch_directory.joinpath('mission_report_backup')
        now = datetime.now()
        for year in logs_dir.glob(str(now.year)):
            for month in year.glob(str(now.month)):
                days = dict()
                for day in month.glob('*'):
                    days[int(day.parts[len(day.parts) - 1])] = day
                    pass
                keys = sorted(days.keys())
                last = days[keys[len(keys) - 1]]
                archives = sorted(last.glob('*.zip'))
                last_arch = Path(archives[len(archives) - 1])
                name = last_arch.parts[len(last_arch.parts) - 1]
                shutil.copyfile(str(last_arch), str(MainCfg.zips_copy_directory.joinpath(name)))
                return


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

decorations_format = """Decoration
{{
  Name = {0};
  Desc = {1};
  XPos = {2};
  YPos = {3};
  ZPos = {4};
  OY = {5};
  Length = {6:.0f};
  Width = {7:.0f};{8}
  Dogfight = {9};
  Transport = {10};
  Train = {11};
  Tank = {12};
  Artillery = {13};
  AAAPosition = {14};
  Ship = {15};
  Balloon = {16};
  Windsock = {17};
  CityFire = {18};
  Spotter = {19};
  Bridge = {20};
  AtArtPosition = {21};
  FiringPoint = {22};
  Siren = {23};
  Parking = {24};
}}"""

ground_objective_format = """GroundObjective
{{
  Name = {0};
  Desc = {1};
  XPos = {2};
  YPos = {3};
  ZPos = {4};
  OY = {5};
  Length = {6};
  Width = {7};{8}
  Transport = {9};
  Armoured = {10};
  Tank = {11};
  AAAPosition = {12};
  Artillery = {13};
  Building = {14};
  Ship = {15};
  Train = {16};
  RailwayStation = {17};
  SupplyDump = {18};
  Factory = {19};
  Airfield = {20};
  Port = {21};
  ReconArea = {22};
}}"""
airfields_format = """Airfield
{{
  Name = "Airfield";
  Desc = "";
  XPos = {0:.3f};
  YPos = {1:.3f};
  ZPos = {2:.3f};
  OY = 0.000;
  Length = 10;
  Width = 10;{3}
  GrassField = 0;
  WaterField = 0;
}}"""
air_objectives_format = """AirObjective
{{
  Name = "AirObjective";
  Desc = "";
  XPos = {0:.3f};
  YPos = 75.515;
  ZPos = {1:.3f};
  OY = 0.000;
  Length = 1000;
  Width = 1000;
  Country = {2};
  ReconFlight = 0;
  BomberFlight = 0;
  FighterPatrolFlight = 0;
  Dogfight = 0;
  DuelOpponent = 0;
  Balloon = 1;
}}"""


class AirObjectiveLocation(Point):
    def __init__(self, node):
        super().__init__(x=node.x, z=node.z, country=node.country)
        self.loc_country = None

    def __str__(self):
        if not self.loc_country:
            raise NameError('AirObjectiveLocation must have loc_country')
        return air_objectives_format.format(
            self.x, self.z, self.loc_country
        )


class DecorationLocation(Point):
    def __init__(self, string, tvd_name, areas, frontline, objective_nodes):
        tmp = str(string).split(';')
        super().__init__(x=float(tmp[2].partition('= ')[-1]), z=float(tmp[4].partition('= ')[-1]))
        self.cls = 'decoration'
        self.tvd_name = tvd_name
        self.frontline = frontline
        self.objective_nodes = objective_nodes
        self.name = str(tmp[0].partition('= ')[-1])
        self.desc = str(tmp[1].partition('= ')[-1])
        self.y = float(tmp[3].partition('= ')[-1])
        self.oy = float(tmp[5].partition('= ')[-1])
        self.length = float(tmp[6].partition('= ')[-1])
        self.width = float(tmp[7].partition('= ')[-1])
        self.types = {
            'dogfight': int(tmp[-17].partition('= ')[-1]),
            'transport': int(tmp[-16].partition('= ')[-1]),
            'train': int(tmp[-15].partition('= ')[-1]),
            'tank': int(tmp[-14].partition('= ')[-1]),
            'artillery': int(tmp[-13].partition('= ')[-1]),
            'aaa_position': int(tmp[-12].partition('= ')[-1]),
            'ship': int(tmp[-11].partition('= ')[-1]),
            'balloon': int(tmp[-10].partition('= ')[-1]),
            'windsock': int(tmp[-9].partition('= ')[-1]),
            'city_fire': int(tmp[-8].partition('= ')[-1]),
            'spotter': int(tmp[-7].partition('= ')[-1]),
            'bridge': int(tmp[-6].partition('= ')[-1]),
            'at_art_position': int(tmp[-5].partition('= ')[-1]),
            'firing_point': int(tmp[-4].partition('= ')[-1]),
            'siren': int(tmp[-3].partition('= ')[-1]),
            'parking': int(tmp[-2].partition('= ')[-1])
        }
        self.areas = areas

    @property
    def loc_country(self):
        fl_first = self.frontline[0]
        for country in self.areas:
            for area in self.areas[country]:
                if self.is_in_area(area):
                    for t in (x for x in self.types.keys() if self.types[x] == 1):
                        fl_rule = LocationsCfg.cfg[self.cls][self.tvd_name][str(country)]['frontline'][t]
                        on_rule = LocationsCfg.cfg[self.cls][self.tvd_name][str(country)]['scenario'][t]
                        if len(fl_rule) or len(on_rule):
                            if len(fl_rule) and not len(on_rule):
                                # только правило "от линии фронта"
                                closest = fl_first
                                for node in self.frontline:
                                    if self.distance_to(closest.x, closest.z) > self.distance_to(node.x, node.z):
                                        closest = node
                                if fl_rule[0] < self.distance_to(closest.x, closest.z) < fl_rule[1]:
                                    return country
                            if len(on_rule) and not len(fl_rule):
                                for node in self.objective_nodes[country]:
                                    if on_rule[0] < self.distance_to(node.x, node.z) < on_rule[1]:
                                        return country
                            if len(on_rule) and len(fl_rule):
                                on = []
                                for c in self.objective_nodes.keys():
                                    on += self.objective_nodes[c]
                                for node in on:
                                    if self.distance_to(node.x, node.z) < on_rule[1]:
                                        for fl_node in self.frontline:
                                            if self.distance_to(fl_node.x, fl_node.z) < fl_rule[0]:
                                                return
                                        return country
                            return
                        else:
                            return country
        return

    def __str__(self):
        c = '' if not self.loc_country else '\n  Country = {};'.format(self.loc_country)
        return decorations_format.format(
            self.name, self.desc, self.x, self.y, self.z, self.oy, self.length, self.width,
            c,
            self.types['dogfight'], self.types['transport'], self.types['train'], self.types['tank'],
            self.types['artillery'], self.types['aaa_position'], self.types['ship'], self.types['balloon'],
            self.types['windsock'], self.types['city_fire'], self.types['spotter'], self.types['bridge'],
            self.types['at_art_position'], self.types['firing_point'], self.types['siren'], self.types['parking']
        )


# TODO объединить классы GroundObjectiveLocation и DecorationLocation в один класс
class GroundObjectiveLocation(Point):
    def __init__(self, string, tvd_name, areas, frontline, objective_nodes):
        tmp = str(string).split(';')
        super().__init__(x=float(tmp[2].partition('= ')[-1]), z=float(tmp[4].partition('= ')[-1]))
        self.cls = 'ground_objective'
        self.tvd_name = tvd_name
        self.frontline = frontline
        self.objective_nodes = objective_nodes
        self.name = str(tmp[0].partition('= ')[-1])
        self.desc = str(tmp[1].partition('= ')[-1])
        self.y = float(tmp[3].partition('= ')[-1])
        self.oy = float(tmp[5].partition('= ')[-1])
        self.length = float(tmp[6].partition('= ')[-1])
        self.width = float(tmp[7].partition('= ')[-1])
        self.types = {
            'transport': int(tmp[-15].partition('= ')[-1]),
            'armoured': int(tmp[-14].partition('= ')[-1]),
            'tank': int(tmp[-13].partition('= ')[-1]),
            'aaa_position': int(tmp[-12].partition('= ')[-1]),
            'artillery': int(tmp[-11].partition('= ')[-1]),
            'building': int(tmp[-10].partition('= ')[-1]),
            'ship': int(tmp[-9].partition('= ')[-1]),
            'train': int(tmp[-8].partition('= ')[-1]),
            'railway_station': int(tmp[-7].partition('= ')[-1]),
            'supply_dump': int(tmp[-6].partition('= ')[-1]),
            'factory': int(tmp[-5].partition('= ')[-1]),
            'airfield': int(tmp[-4].partition('= ')[-1]),
            'port': int(tmp[-3].partition('= ')[-1]),
            'recon_area': int(tmp[-2].partition('= ')[-1])
        }
        self.areas = areas
        self._loc_country = None

    @property
    def loc_country(self):
        fl_first = self.frontline[0]
        for country in self.areas:
            for area in self.areas[country]:
                if self.is_in_area(area):
                    for t in (x for x in self.types.keys() if self.types[x] == 1):
                        fl_rule = LocationsCfg.cfg[self.cls][self.tvd_name][str(country)]['frontline'][t]
                        on_rule = LocationsCfg.cfg[self.cls][self.tvd_name][str(country)]['scenario'][t]
                        if len(fl_rule) or len(on_rule):
                            if len(fl_rule) and not len(on_rule):
                                # только правило "от линии фронта"
                                closest = fl_first
                                for node in self.frontline:
                                    if self.distance_to(closest.x, closest.z) > self.distance_to(node.x, node.z):
                                        closest = node
                                if fl_rule[0] < self.distance_to(closest.x, closest.z) < fl_rule[1]:
                                    return country
                            if len(on_rule) and not len(fl_rule):
                                for node in self.objective_nodes[country]:
                                    if on_rule[0] < self.distance_to(node.x, node.z) < on_rule[1]:
                                        return country
                            if len(on_rule) and len(fl_rule):
                                on = []
                                for c in self.objective_nodes.keys():
                                    on += self.objective_nodes[c]
                                for node in on:
                                    if self.distance_to(node.x, node.z) < on_rule[1]:
                                        for fl_node in self.frontline:
                                            if self.distance_to(fl_node.x, fl_node.z) < fl_rule[0]:
                                                return
                                        return country
                            return
                        else:
                            return country
        return

    def __str__(self):
        c = '' if not self.loc_country else '\n  Country = {};'.format(self.loc_country)
        return ground_objective_format.format(
            self.name, self.desc, self.x, self.y, self.z, self.oy, self.length, self.width,
            c,
            self.types['transport'], self.types['armoured'], self.types['tank'], self.types['aaa_position'],
            self.types['artillery'], self.types['building'], self.types['ship'], self.types['train'],
            self.types['railway_station'], self.types['supply_dump'], self.types['factory'], self.types['airfield'],
            self.types['port'], self.types['recon_area']
        )


division_format = """AirObjective
{{
  Name = "AirObjective";
  Desc = "";
  XPos = {0:.3f};
  YPos = 75.515;
  ZPos = {1:.3f};
  OY = {2:.3f};
  Length = {3:.3f};
  Width = {4:.3f};
  ReconFlight = 0;
  BomberFlight = 0;
  FighterPatrolFlight = 0;
  Dogfight = 0;
  DuelOpponent = 1;
  Balloon = 0;
}}"""


class Division(Segment):
    def __init__(self, segment_coordinates, frontline_margin_distance, depth):
        super().__init__(
            segment_coordinates[0][0],
            segment_coordinates[0][1],
            segment_coordinates[1][0],
            segment_coordinates[1][1]
        )
        self.frame = super().parallel_segments(frontline_margin_distance)
        self.depth = depth

    def __str__(self):
        return division_format.format(
            self.frame[0].center[0],
            self.frame[0].center[1],
            self.frame[0].angle,
            self.depth,
            self.frame[0].length
        ) + '\n\n' + division_format.format(
            self.frame[1].center[0],
            self.frame[1].center[1],
            self.frame[1].angle,
            self.depth,
            self.frame[1].length
        )


class AirObjectiveRecon:
    def __init__(self, string):
        self.cls = 'air_objective_recon'
        self.string = string

    def __str__(self):
        return self.string


class Ldb:
    def __init__(self, tvd_name, areas, objective_nodes, frontline):
        """
        Класс для присвоения наций локациям в базе по заданным параметрам
        :param tvd_name: имя ТВД для получения конфига локаций
        :param areas: зоны влияния стран для покраски локаций
        :param objective_nodes: активные узлы
        :param frontline: линия фронта
        """
        folder = MainCfg.game_folder.joinpath(Path(MissionGenCfg.cfg[tvd_name]['tvd_folder']))
        self.ldf_file = folder.joinpath(MissionGenCfg.cfg[tvd_name]['ldf_file'])
        with folder.joinpath(MissionGenCfg.cfg[tvd_name]['ldf_base_file']).open() as f:
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
                GroundObjectiveLocation(str(m), tvd_name, areas, frontline, objective_nodes))
        for m in decorations_raw_re.findall(self.ldf_base):
            self.locations['decorations'].append(
                DecorationLocation(str(m), tvd_name, areas, frontline, objective_nodes))

        for country in objective_nodes.keys():
            for node in objective_nodes[country]:
                self.locations['objective_nodes'].append(AirObjectiveLocation(node))
                self.locations['objective_nodes'][-1].loc_country = country

    @property
    def text(self):
        """ Текст исходного файла базы локаций """
        text = '#1CGS Location Database file'
        for k in self.locations:
            for loc in self.locations[k]:
                # if k in ('decorations', 'objective_nodes'):
                    # if not loc.loc_country:
                    #     continue
                text += '\n\n{}'.format(loc)
        text += '\n\n#end of file'
        return text

    def make(self):
        """ Записать текстовый файл базы локаций и скомпилировать бинарный файл с помощью make_ldb.exe """
        self.ldf_file.write_text(self.text)
        args = [
            str(MissionGenCfg.make_ldb_folder.joinpath('.\\make_ldb.exe').absolute()),
            str(self.ldf_file)
        ]
        # запуск утилиты make_ldb_folder
        generator = subprocess.Popen(args, cwd=str(MissionGenCfg.make_ldb_folder), stdout=subprocess.DEVNULL)
        generator.wait()
        time.sleep(3)


class Divisions:
    def __init__(self, tvd_name, edges):
        folder = MainCfg.game_folder.joinpath(Path(MissionGenCfg.cfg[tvd_name]['tvd_folder']))
        self.ldf_file = folder.joinpath(MissionGenCfg.cfg[tvd_name]['ldf_file'])
        self.divisions = []
        for edge in edges:
            self.divisions.append(Division(
                edge,
                MissionGenCfg.cfg[tvd_name]['division_margin'],
                MissionGenCfg.cfg[tvd_name]['division_depth']
            ))

    @property
    def text(self):
        """ Текст исходного файла базы локаций """
        text = '#1CGS Location Database file'
        for division in self.divisions:
            text += '\n\n{}'.format(division)
        text += '\n\n#end of file'
        return text

    def make(self):
        """ Записать текстовый файл базы локаций и скомпилировать бинарный файл с помощью make_ldb.exe """
        self.ldf_file.write_text(self.text)

icon_text = """MCU_Icon
{{
  Index = {0};
  Targets = [{1}];
  Objects = [];
  XPos = {2:.3f};
  YPos = 200.000;
  ZPos = {3:.3f};
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Enabled = 1;
  LCName = {4};
  LCDesc = {5};
  IconId = 0;
  RColor = 255;
  GColor = 255;
  BColor = 255;
  LineType = 13;
  Coalitions = [1, 2, 0];
}}

"""  # не двигать кавычки!

ref_point_helper_format = """MCU_H_ReferencePoint
{{
  Index = {0};
  Name = "";
  Desc = "";
  Targets = [];
  Objects = [];
  XPos = {1:.3f};
  YPos = 0.000;
  ZPos = {2:.3f};
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Forward = 1;
  Backward = 1;
  Left = 1;
  Right = 1;
}}

"""  # не двигать кавычки!

influence_text = """MCU_TR_InfluenceArea
{{
  Index = {};
  Name = "Translator Influence Area";
  Desc = "";
  Targets = [];
  Objects = [];
  XPos = {:.3f};
  YPos = 17.795;
  ZPos = {:.3f};
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Enabled = 1;
  Country = {};
  Boundary
  {{
{}  }}
}}

"""  # не двигать кавычки!


class FrontLineIcon(Point):
    def __init__(self, id, point, target=None):
        """
        Класс иконки, из которых состоит линия фронта
        :param id: ИД объекта MCU_Icon
        :param point: узел, иконки
        :param target: ИД следующей иконки в цепочке
        """
        super().__init__(x=point.x, z=point.z)
        self.target = target
        self.id = id
        self.lc_name = id*2-1
        self.lc_desc = id*2

    def __str__(self):
        if self.target is not None:
            return icon_text.format(self.id, self.target, self.x, self.z, self.lc_name, self.lc_desc)
        else:
            return icon_text.format(self.id, '', self.x, self.z, self.lc_name, self.lc_desc)


class InfluenceArea:
    def __init__(self, id, boundary, country):
        """
        Класс зоны влияния, которая определяет принадлежность территории к какой-то стране
        :param id: ИД объекта MCU_TR_InfluenceArea
        :param boundary: список вершин многоугольника зоны (по часовой стрелке)
        :param country: страна, к которой относится территория зоны
        """
        self.id = id
        self.boundary = boundary
        self.country = country

    def __str__(self):
        boundary_text = ''
        for point in self.boundary:
            boundary_text += '    {:.2f}, {:.2f};\n'.format(point.x, point.z)
        point = self.boundary[0]
        return influence_text.format(self.id, float(point.x), float(point.z), self.country, boundary_text)


class FlGroup(Group):
    def __init__(self, tvd_name, line, areas):
        """
        Класс группы линии фронта
        :param tvd_name: имя ТВД
        :param line: линия фронта (снизу вверх)
        :param areas: зоны влияния (словарь многоугольников по странам)
        """
        super().__init__(MissionGenCfg.icons_group_files[tvd_name])
        self.icons = []
        self.influences = []
        self._loc_text = None
        i = 2
        for point in line:
            self.icons.append(FrontLineIcon(i, point, target=i+1))
            i += 1
        self.icons[len(self.icons)-1].target = None
        for country in areas.keys():
            for boundary in areas[country]:
                self.influences.append(InfluenceArea(i, boundary, country))
                i += 1
        ref_point = MissionGenCfg.cfg[tvd_name]['right_top']
        self.ref_point_text = ref_point_helper_format.format(i, ref_point['x'], ref_point['z'])

    def make(self):
        """ Записать файлы группы (включая локализацию) """
        for file_ext in self.files.keys():
            if file_ext == 'Group':
                text = ''
                for icon in self.icons:
                    text += str(icon)
                for area in self.influences:
                    text += str(area)
                text += self.ref_point_text
                self.files[file_ext].write_text(text, encoding='utf-8')
            else:
                # файлы локализации нужны, чтобы уменьшить вероятные проблемы (фризы)
                content = '{}\n{}'.format('\ufeff', self.loc_text)
                self.files[file_ext].write_text(content, encoding='utf-16-le')

    @property
    def loc_text(self):
        """ Текст файлов локализации (пустые строки) """
        if self._loc_text:
            return self._loc_text
        else:
            self._loc_text = ''
            for icon in self.icons:
                self._loc_text += '{}:\n{}:\n'.format(icon.lc_name, icon.lc_desc)
            return self._loc_text
