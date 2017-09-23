""" Основной файл для запуска """
import pathlib
import datetime
import codecs
import generation
from campaign import Campaign
from configs import Main, Mgen, Stats, GeneratorParamsConfig, LocationsConfig

MAIN = Main(pathlib.Path(r'.\configs\conf.ini'))
MGEN = Mgen(MAIN)
STATS = Stats(MAIN)
PARAMS = GeneratorParamsConfig()
LOCATIONS = LocationsConfig()

def create_divisions_ldb():
    """ Создать базу локаций, обозначающих расположения дивизий """
    campaign = Campaign(MAIN, MGEN, STATS, LOCATIONS, PARAMS)
    for name in campaign.tvds.keys():
        campaign.tvds[name].create_divisions()


def export(name: str):
    """ Экспортировать граф в XGML формате """
    campaign = Campaign(MAIN, MGEN, STATS, LOCATIONS, PARAMS)
    with codecs.open(name + "_export.xgml", "w", encoding="cp1251") as stream:
        stream.write(campaign.tvds[name].grid.serialize_xgml())
        stream.close()


def reset():
    """ Сбросить состояние кампании """
    raise NotImplementedError
    campaign = Campaign(MAIN, MGEN, STATS, LOCATIONS, PARAMS)
    for name in campaign.tvds.keys():
        campaign.tvds[name].grid.read_file()
        campaign.tvds[name].grid.write_db()
        campaign.tvds[name].grid.read_db()


def generate(name: str, tvd_name: str):
    """ Сгенерировать миссию """
    campaign = Campaign(MAIN, MGEN, STATS, LOCATIONS, PARAMS)
    campaign.tvds[tvd_name].update()
    generation.Generator(MAIN, MGEN).make_mission(name, tvd_name)


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start"))
# reset()
# create_divisions_ldb()
# export('moscow')
# export('stalingrad')
generate('result1', 'moscow')
# generate('result1', 'stalingrad')
# run()
