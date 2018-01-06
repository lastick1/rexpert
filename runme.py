"""Основной файл для запуска"""
import pathlib
import datetime
import configs
import processing
import pymongo
import rcon


DB_NAME = 'rexpert'
MAIN = configs.Main(pathlib.Path(r'.\configs\conf.ini'))
MGEN = configs.Mgen(MAIN)
STATS = configs.Stats(MAIN)
PARAMS = configs.GeneratorParamsConfig()
LOCATIONS = configs.LocationsConfig()
PLANES = configs.Planes()


def initialize_airfields(tvd_name: str):
    """Сбросить состояние кампании"""
    builder = processing.TvdBuilder(tvd_name, MGEN, MAIN, PARAMS, PLANES)
    mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
    rexpert = mongo[DB_NAME]
    airfields_controller = processing.AirfieldsController(MAIN, MGEN, PLANES, rexpert['Airfields'])
    airfields_controller.initialize_airfields(builder.get_tvd('10.11.1941'))


def initialize_campaign():
    """Инициализация кампании"""
    controller = processing.CampaignController(MAIN, MGEN, processing.Generator(MAIN, MGEN))
    controller.initialize()


def generate(name: str, tvd_name: str):
    """Сгенерировать миссию"""
    mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
    rexpert = mongo[DB_NAME]
    airfields_controller = processing.AirfieldsController(MAIN, MGEN, PLANES, rexpert['Airfields'])
    tvd_builder = processing.TvdBuilder(tvd_name, MGEN, MAIN, PARAMS, PLANES)
    tvd_builder.update('19.11.1941', airfields_controller.get_airfields(tvd_name))
    generator = processing.Generator(MAIN, MGEN)
    generator.make_ldb(tvd_name)
    generator.make_mission(name, tvd_name)


def run():
    """Запуск"""
    objects = configs.Objects()
    mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
    rexpert = mongo['rexpert']
    events_controller = processing.EventsController(
        objects=objects,
        players_controller=processing.PlayersController(
            main=MAIN,
            commands=rcon.DServerRcon(MAIN.rcon_ip, MAIN.rcon_port),
            players=rexpert['Players']
        ),
        ground_controller=processing.GroundController(objects=objects),
        campaign_controller=processing.CampaignController(MAIN, MGEN, processing.Generator(MAIN, MGEN)),
        airfields_controller=processing.AirfieldsController(MAIN, MGEN, PLANES, rexpert['Airfields']),
        config=MAIN
    )
    reader = processing.LogsReader(MAIN, events_controller)


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start."))
# import helpers
# helpers.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled')

# initialize_airfields('moscow')
# initialize_campaign()
# export('moscow')
# export('stalingrad')
# generate('result1', 'moscow')
# generate('result1', 'stalingrad')
run()
print(datetime.datetime.now().strftime("[%H:%M:%S] Program Finish."))
