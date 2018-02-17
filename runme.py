"""Основной файл для запуска"""
import datetime
import pathlib
import logging

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


def compile_ldf():
    """Собрать декомпозировнаные базы локаций в базы локаций для покраски"""
    for tvd_name in ('moscow', ):
        utils.compile_ldf(f'./data/ldf/{tvd_name}', f'./data/ldf/{tvd_name}_base.ldf')


def reset():
    """Сбросить состояние кампании"""
    controller = processing.CampaignController(dependency_container.DependencyContainer())
    controller.reset()


def initialize_campaign():
    """Инициализация кампании"""
    controller = processing.CampaignController(dependency_container.DependencyContainer())
    controller.initialize()


def generate(name: str):
    """Сгенерировать миссию"""
    controller = processing.CampaignController(dependency_container.DependencyContainer())
    controller.generate(name)


def run():
    """Запуск"""
    core.LogsReader(dependency_container.DependencyContainer()).start()


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start."))
logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

# compile_log()
# compile_gif()
# compile_ldf()
# reset()
# initialize_campaign()
# generate('result1')
run()
