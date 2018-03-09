"""Основной файл для запуска"""
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


def generate(name: str, tvd_name: str, date: str, attacking_country=0):
    """Сгенерировать миссию"""
    controller = processing.CampaignController(dependency_container.DependencyContainer())
    controller.generate(name, tvd_name, date, attacking_country=attacking_country)


def run():
    """Запуск"""
    core.LogsReader(dependency_container.DependencyContainer()).start()


logging.basicConfig(
    format=u'%(asctime)s %(levelname)-8s %(filename)-40s:%(lineno)-3d # %(message)s', level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)
logging.info("Program Start.")
# compile_log()
# compile_gif()
# compile_ldf()
# reset()
# initialize_campaign()
# generate('result1', 'moscow', '01.09.1941', attacking_country=0)
run()
