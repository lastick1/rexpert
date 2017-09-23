"Конфиг работы со статистикой"
import json
from .main import Main

class Stats:
    "Конфиг"
    def __init__(self, main: Main):
        with open('.\\configs\\stats_custom.json') as stream:
            src = json.load(stream)
        self.cfg = src
        self.map_main_page = str(main.stats_static.joinpath(src['image_files']['map_main_page']).absolute())
        self.map_full_size = str(main.stats_static.joinpath(src['image_files']['map_full_size']).absolute())
        self.json_files = src['json_files']
        self.image_files = src['image_files']
        self.online = main.stats_static.joinpath(self.json_files['online_players'])
        self.time_remaining = main.stats_static.joinpath(self.json_files['elapsed_time'])
        self.credits_data = main.stats_static.joinpath(self.json_files['planes_data'])
        self.payloads = main.stats_static.joinpath(self.json_files['payloads'])
        self.maps_archive_folder = main.maps_archive_folder
