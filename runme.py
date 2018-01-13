"""Основной файл для запуска"""
import datetime
import pathlib

import configs
import processing


CONFIG = configs.Config(pathlib.Path(r'./configs/conf.ini'))


def reset():
    """Сбросить состояние кампании"""
    controller = processing.CampaignController(CONFIG)
    controller.reset()


def initialize_campaign():
    """Инициализация кампании"""
    controller = processing.CampaignController(CONFIG)
    controller.initialize()


def generate(name: str):
    """Сгенерировать миссию"""
    controller = processing.CampaignController(CONFIG)
    controller.generate(name)


def run():
    """Запуск"""
    objects = configs.Objects()
    events_controller = processing.EventsController(objects=objects, config=CONFIG)
    processing.LogsReader(CONFIG.main, events_controller)


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start."))
# import helpers
# helpers.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled')

# reset()
# export('moscow')
# export('stalingrad')
# generate('result1')
run()
print(datetime.datetime.now().strftime("[%H:%M:%S] Program Finish."))
