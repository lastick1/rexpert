"""Основной файл для запуска"""
import sys
import logging

import utils
import core
import processing
import dependency_container


MAIN_HELP = """Usage: runme.py <command>

where <command> is one of:
    run, initialize, reset, generate, compile

runme.py help <command>"""


def show_help(command: str):
    """Вывести помощь в консоль"""
    if command == 'run':
        print()
    else:
        print(MAIN_HELP)


def compile_log():
    """Собрать лог в один файл"""
    utils.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled.txt')


def compile_gif():
    """Сделать кино"""
    utils.compile_gif('./current/map_thumbnails/')


def compile_ldf():
    """Собрать декомпозировнаные базы локаций в базы локаций для покраски"""
    for tvd_name in ('moscow', ):
        utils.compile_ldf(f'./data/ldf/{tvd_name}',
                          f'./data/ldf/{tvd_name}_base.ldf')


def _compile(args: list):
    """Обработка команды компиляции gif/лога/ldf"""


def reset():
    """Сбросить состояние кампании"""
    controller = processing.CampaignController(
        dependency_container.DependencyContainer())
    controller.reset()


def initialize_campaign():
    """Инициализация кампании"""
    controller = processing.CampaignController(
        dependency_container.DependencyContainer())
    controller.initialize()


GENERATE_HELP = """generate usage: runme.py generate [attack] <mission_name> <tvd_name> <date>
    [<attacking_country> <attacked_airfield_name>]

where
    mission_name is one of: result1, result2
    tvd_name is one of: moscow, stalingrad, kuban
    date is mission date in format dd.MM.yyyy
    attack is an option to generate attacking mission type with required parameters:
        attacking_country is one of: 101, 201
        attacked_airfield_name is the airfield name from moscow_fields.csv or stalin_fields.csv or kuban_fields.csv
"""


def generate(name: str, tvd_name: str, date: str, attacking_country=0, attacked_airfield_name: str = None):
    """Сгенерировать миссию"""
    controller = processing.CampaignController(
        dependency_container.DependencyContainer())
    controller.generate(name, tvd_name, date,
                        attacking_country, attacked_airfield_name)


def _generate(args: list):
    """Обработка команды генерации миссии"""
    _args_count = len(args)
    if _args_count > 0:
        _type = args[0].lower()
        if _type == 'attack' and _args_count == 5:
            generate(*args)
        elif _args_count == 3:
            generate(*args)
        else:
            show_help(GENERATE_HELP)
    else:
        show_help(GENERATE_HELP)


def run():
    """Запуск"""
    core.LogsReader(dependency_container.DependencyContainer()).start()


logging.basicConfig(
    format=u'%(asctime)s %(levelname)-8s %(filename)-40s:%(lineno)-3d # %(message)s', level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.WARNING)
logging.info("Program Start.")
# compile_log()  # объединить лог в один файл
# compile_gif()  # собрать картинки в гифку
# compile_ldf()  # объединить файлы баз локаций

# reset()  # обнуление состояния кампании
# initialize_campaign()
# генерация атаки
# generate('result1', 'moscow', '01.09.1941', attacking_country=201, attacked_airfield_name='vatulino')
# генерация противостояния
# generate('result1', 'moscow', '01.09.1941')
# run()


def main(args: list):
    """Основная точка входа в приложение"""
    _args_count = len(args)
    if _args_count > 0:
        _command = args[1].lower()
        if _command == 'run':
            run()
        elif _command == '':
            initialize_campaign()
        elif _command == 'reset':
            reset()
        elif _args_count > 2:
            if _command == 'generate':
                _generate(args[2:])
            elif _command == 'compile':
                _compile(args[2:])
            elif _command == 'help':
                if _args_count > 2:
                    show_help(args[2])
        else:
            show_help(MAIN_HELP)
    else:
        show_help(MAIN_HELP)


if __name__ == '__main__':
    main(sys.argv)
