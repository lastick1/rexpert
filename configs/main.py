"""Парсер главного конфига"""
from __future__ import annotations
from pathlib import Path
import json


class Main:  # pylint: disable=R0903,R0902,C0301
    """Класс конфига"""
    def __init__(self, path: Path):
        with open(str(path.absolute())) as stream:
            src = json.load(stream)
        self.cfg = src
        self.logs_read_interval: int = src['program']['logs_read_interval']
        self.game_folder = Path(src['program']['game_folder']).absolute()
        self.server_folder = Path(src['program']['server_folder']).absolute()
        self.dogfight_folder = self.server_folder.joinpath('./data/Multiplayer/Dogfight').absolute()
        self.mission_gen_folder = Path(src['missiongen']['mission_gen_folder']).absolute()
        self.stats_folder = Path(src['program']['stats_folder'])
        self.stats_static = Path(self.stats_folder.joinpath('./static')).absolute()
        self.maps_archive_folder = Path(src['program']['maps_archive_folder'])
        self.graph_folder = Path('./configs/').absolute()
        self.current_grid_folder = Path(Path('./current/').absolute())
        self.resaver_folder = Path(src['missiongen']['resaver_folder'])
        self.generate_missions = src['missiongen']['generate_missions']
        self.special_influences = src['missiongen']['special_influences']
        self.use_resaver = src['missiongen']['use_resaver']
        self.test_mode = src['program']['test_mode']
        self.offline_mode = src['program']['offline_mode']
        self.debug_mode = src['program']['debug_mode']
        self.console_cmd_output = src['program']['console_cmd_output']
        self.console_chat_output = src['program']['console_chat_output']
        self.minimal_chat_interval = int(src['program']['minimal_chat_interval'])
        self.rcon_ip = src['rcon']['ip']
        self.rcon_port = int(src['rcon']['port'])
        self.rcon_login = src['rcon']['login']
        self.rcon_password = src['rcon']['password']
        self.logs_directory = src['dserver']['logs_directory']
        self.arch_directory = src['dserver']['arch_directory']
        self.chat_directory = src['dserver']['chat_directory']
        self.connection_string = 'dbname={} host={} port={} user={} password={}'.format(
            src['stats']['database'],
            src['stats']['host'],
            src['stats']['port'],
            src['stats']['user'],
            src['stats']['password']
        )
        self.database = src['stats']['database']
        self.host = src['stats']['host']
        self.port = src['stats']['port']
        self.user = src['stats']['user']
        self.password = src['stats']['password']
        self.mongo_host = src['mongo']['host']
        self.mongo_port = int(src['mongo']['port'])
        self.mongo_database = src['mongo']['database']

    @property
    def instances(self):
        """ Количество сущностей конфига """
        return Main.instances
