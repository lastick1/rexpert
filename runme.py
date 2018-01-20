"""Основной файл для запуска"""
import datetime
import pathlib

import utils
import configs
import core
import processing
import ioc


CONFIG = configs.Config(pathlib.Path(r'./configs/conf.ini'))


def compile_log():
    """Собрать лог в один файл"""
    utils.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled.txt')


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
# reset()
# initialize_campaign()
# export('moscow')
# export('stalingrad')
# generate('result1')
run()
