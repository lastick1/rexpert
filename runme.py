"""Основной файл для запуска"""
import datetime
import pathlib

import utils
import configs
import core
import processing


CONFIG = configs.Config(pathlib.Path(r'./configs/conf.ini'))


def compile_log():
    """Собрать лог в один файл"""
    utils.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled')


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
    events_controller = core.EventsController(objects=configs.Objects(), config=CONFIG)
    core.LogsReader(CONFIG.main, events_controller)


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start."))

# compile_log()
# reset()
# export('moscow')
# export('stalingrad')
# generate('result1')
# run()
print(datetime.datetime.now().strftime("[%H:%M:%S] Program Finish."))
