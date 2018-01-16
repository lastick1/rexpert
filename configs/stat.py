"""Конфиг работы со статистикой"""
import json
import pathlib


class Stats:
    """Конфиг"""
    def __init__(self, stats_static: pathlib.Path):
        with open('.\\configs\\stats_custom.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.map_main_page = str(stats_static.joinpath(src['image_files']['map_main_page']).absolute())
        self.map_full_size = str(stats_static.joinpath(src['image_files']['map_full_size']).absolute())
        self.json_files = src['json_files']
        self.image_files = src['image_files']
        self.online = stats_static.joinpath(self.json_files['online_players'])
        self.time_remaining = stats_static.joinpath(self.json_files['elapsed_time'])
        self.credits_data = stats_static.joinpath(self.json_files['planes_data'])
        self.payloads = stats_static.joinpath(self.json_files['payloads'])