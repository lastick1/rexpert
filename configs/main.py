"""Парсер главного конфига"""
from pathlib import Path
import configparser


class Main:  # pylint: disable=R0903,R0902,C0301
    """Класс конфига"""
    def __init__(self, path: Path):
        src = configparser.ConfigParser()
        src.read(str(path.absolute()))
        self.game_folder = Path(src['PROGRAM']['game_folder']).absolute()
        self.dogfight_folder = self.game_folder.joinpath('./data/Multiplayer/Dogfight').absolute()
        self.mission_gen_folder = Path(src['MISSIONGEN']['mission_gen_folder']).absolute()
        self.stats_folder = Path(src['PROGRAM']['stats_folder'])
        self.stats_static = Path(self.stats_folder.joinpath('./static')).absolute()
        self.maps_archive_folder = Path(src['PROGRAM']['maps_archive_folder'])
        self.graph_folder = Path('./configs/').absolute()
        self.current_grid_folder = Path(Path('./current/').absolute())
        self.resaver_folder = Path(src['MISSIONGEN']['resaver_folder'])
        self.generate_missions = True if "true" in src['MISSIONGEN']['generate_missions'].lower() else False
        self.special_influences = True if "true" in src['MISSIONGEN']['special_influences'].lower() else False
        self.use_resaver = True if "true" in src['MISSIONGEN']['use_resaver'].lower() else False
        self.test_mode = True if "true" in src['PROGRAM']['test_mode'].lower() else False
        self.offline_mode = True if "true" in src['PROGRAM']['offline_mode'].lower() else False
        self.debug_mode = True if "true" in src['PROGRAM']['debug_mode'].lower() else False
        self.console_cmd_output = True if "true" in src['PROGRAM']['console_cmd_output'].lower() else False
        self.console_chat_output = True if "true" in src['PROGRAM']['console_chat_output'].lower() else False
        self.minimal_chat_interval = int(src['PROGRAM']['minimal_chat_interval'])
        self.rcon_ip = src['RCON']['rcon_ip']
        self.rcon_port = int(src['RCON']['rcon_port'])
        self.rcon_login = src['RCON']['rcon_login']
        self.rcon_password = src['RCON']['rcon_password']
        self.logs_directory = Path(src['DSERVER']['logs_directory'])
        self.arch_directory = Path(src['DSERVER']['arch_directory'])
        self.chat_directory = Path(src['DSERVER']['chat_directory'])
        self.msrc_directory = Path(src['NEW_STATS']['msrc_directory'])
        self.connection_string = 'dbname={} host={} port={} user={} password={}'.format(
            src['STATS']['database'],
            src['STATS']['host'],
            src['STATS']['port'],
            src['STATS']['user'],
            src['STATS']['password']
        )
        self.database = src['STATS']['database']
        self.host = src['STATS']['host']
        self.port = src['STATS']['port']
        self.user = src['STATS']['user']
        self.password = src['STATS']['password']
        self.mongo_host = src['MONGO']['host']
        self.mongo_port = int(src['MONGO']['port'])
        self.mongo_database = src['MONGO']['database']

    @property
    def instances(self):
        """ Количество сущностей конфига """
        return Main.instances