""" Основной файл для запуска """
import datetime
import codecs
from processor import Processor
import rcon
import db
import reader
import gen
from campaign import Campaign
from configs import Main


def create_divisions_ldb():
    """ Создать базу локаций, обозначающих расположения дивизий """
    campaign = Campaign()
    for name in campaign.tvds.keys():
        campaign.tvds[name].create_divisions()


def export(name: str):
    """ Экспортировать граф в XGML формате """
    campaign = Campaign()
    with codecs.open(name + "_export.xgml", "w", encoding="cp1251") as stream:
        stream.write(campaign.tvds[name].grid.serialize_xgml())
        stream.close()


def reset():
    """ Сбросить состояние графа """
    db.PGConnector.Graph.reset()
    campaign = Campaign()
    for name in campaign.tvds.keys():
        campaign.tvds[name].grid.read_file()
        campaign.tvds[name].grid.write_db()
        campaign.tvds[name].grid.read_db()


def generate(name: str, tvd_name: str):
    """ Сгенерировать миссию """
    campaign = Campaign()
    campaign.tvds[tvd_name].update()
    gen.Generator.make_mission(name, tvd_name)


def run():
    """ Запустить коммандер """
    config = Main()
    commander = rcon.Commander(config)
    processor = Processor(config, commander)
    reader.AtypesReader(processor)

print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start"))
# reset()
# create_divisions_ldb()
# export('moscow')
# export('stalingrad')
# generate('result1', 'moscow')
# generate('result1', 'stalingrad')
# run()
