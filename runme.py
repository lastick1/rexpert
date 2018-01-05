"""Основной файл для запуска"""
import pathlib
import datetime
import codecs
import generation
import configs
import processing
import pymongo


DB_NAME = 'rexpert'
MAIN = configs.Main(pathlib.Path(r'.\configs\conf.ini'))
MGEN = configs.Mgen(MAIN)
STATS = configs.Stats(MAIN)
PARAMS = configs.GeneratorParamsConfig()
LOCATIONS = configs.LocationsConfig()
PLANES = configs.Planes()

MOSCOW_FIELDS = pathlib.Path(r'./data/moscow_fields.csv')


def export(name: str):
    """Экспортировать граф в XGML формате"""
    campaign = Campaign(MAIN, MGEN, STATS, LOCATIONS, PARAMS)
    with codecs.open(name + "_export.xgml", "w", encoding="cp1251") as stream:
        stream.write(campaign.tvds[name].grid.serialize_xgml())
        stream.close()


def initialize_airfields(tvd_name: str, fields_csv: pathlib.Path):
    """Сбросить состояние кампании"""
    mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
    rexpert = mongo[DB_NAME]
    airfields_controller = processing.AirfieldsController(MAIN, PLANES, rexpert['Airfields'])
    airfields_controller.initialize(tvd_name, fields_csv)


def generate(name: str, tvd_name: str):
    """Сгенерировать миссию"""
    mongo = pymongo.MongoClient(MAIN.mongo_host, MAIN.mongo_port)
    rexpert = mongo[DB_NAME]
    airfields_controller = processing.AirfieldsController(MAIN, PLANES, rexpert['Airfields'])
    tvd_builder = generation.TvdBuilder(
        tvd_name, '19.11.1941', MGEN, MAIN, LOCATIONS, PARAMS, PLANES, airfields_controller)
    tvd_builder.update()
    generator = generation.Generator(MAIN, MGEN)
    generator.make_ldb(tvd_name)
    generator.make_mission(name, tvd_name)


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start."))
# import helpers
# helpers.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled')

# initialize_airfields('moscow', MOSCOW_FIELDS)
# export('moscow')
# export('stalingrad')
# generate('result1', 'moscow')
# generate('result1', 'stalingrad')
# run()
print(datetime.datetime.now().strftime("[%H:%M:%S] Program Finish."))
