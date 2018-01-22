"""Основной файл для запуска"""
import datetime
import pathlib

import utils
import configs
import core
import processing
import dependency_container


CONFIG = configs.Config(pathlib.Path(r'./configs/conf.ini'))


def compile_log():
    """Собрать лог в один файл"""
    utils.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled.txt')


def compile_gif():
    """Сделать кино"""
    utils.compile_gif('./current/map_thumbnails/')


def reset():
    """Сбросить состояние кампании"""
    controller = processing.CampaignController(ioc.DependencyContainer())
    controller.reset()


def initialize_campaign():
    """Инициализация кампании"""
    controller = processing.CampaignController(ioc.DependencyContainer())
    controller.initialize()


def generate(name: str):
    """Сгенерировать миссию"""
    controller = processing.CampaignController(ioc.DependencyContainer())
    controller.generate(name)


def run():
    """Запуск"""
    core.LogsReader(ioc.DependencyContainer()).start()


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start."))

# compile_log()
# compile_gif()
# reset()
# initialize_campaign()
# generate('result1')
# run()
