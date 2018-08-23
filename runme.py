"""Основной файл для запуска"""
import sys
import logging

import utils
import core
import processing
import dependency_container


MAIN_HELP = """
Usage: runme.py <command>

where <command> is one of:
    run, initialize, reset, generate, compile

runme.py help <command>"""

GENERATE_HELP = """
generate usage: runme.py generate [attack] <mission_name> <tvd_name> <date>
    [<attacking_country> <attacked_airfield_name>]

where
    mission_name is one of: result1, result2
    tvd_name is one of: moscow, stalingrad, kuban
    date is mission date in format dd.MM.yyyy
    attack is an option to generate attacking mission type with required parameters:
        attacking_country is one of: 101, 201
        attacked_airfield_name is the airfield name from moscow_fields.csv or stalin_fields.csv or kuban_fields.csv"""

RUN_HELP = """
run usage: runme.py run
    program start reading game log files, produced by dserver.exe and begin controlling campaign"""

COMPILE_HELP = """
compile usage: runme.py compile <task>

where task is one of: gif, ldf, log
    gif: program compiles map thumbnails from current/map_thumbnails directory into gif animation file
    ldf: program compiles separate location database files into one large
    log: program compiles game text log file from ./tmp directory into one large"""

RESET_HELP = """
reset usage: runme.py reset
    program resets campaign and players progress to initial values"""

INITIALIZE_HELP = """
initialize usage: runme.py initialize
    program creates required database, files and prepares all to start up the server"""


def show_help(command: str):
    """Вывести помощь в консоль"""
    if command == 'run':
        print(RUN_HELP)
    elif command == 'compile':
        print(COMPILE_HELP)
    elif command == 'reset':
        print(RESET_HELP)
    elif command == 'initialize':
        print(INITIALIZE_HELP)
    elif command == 'generate':
        print(GENERATE_HELP)
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
    # TODO добавить аргумент: ТВД
    for tvd_name in ('moscow', ):
        utils.compile_ldf(f'./data/ldf/{tvd_name}',
                          f'./data/ldf/{tvd_name}_base.ldf')


def _compile(args: list):
    """Обработка команды компиляции gif/лога/ldf"""
    _args_count = len(args)
    if _args_count > 0:
        _command = args[0]
        if _command == 'ldf':
            compile_ldf()
        elif _command == 'gif':
            compile_gif()
        elif _command == 'log':
            compile_log()
        else:
            print(COMPILE_HELP)
    else:
        print(COMPILE_HELP)


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
            show_help('generate')
    else:
        show_help('generate')


def run():
    """Запуск"""
    core.LogsReader(dependency_container.DependencyContainer()).start()


def main(args: list):
    """Основная точка входа в приложение"""
    _args_count = len(args)
    if _args_count > 0:
        logging.basicConfig(
            format=u'%(asctime)s %(levelname)-8s %(filename)-40s:%(lineno)-3d # %(message)s', level=logging.DEBUG)
        logging.getLogger('PIL').setLevel(logging.WARNING)
        logging.info("Program Start.")
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
