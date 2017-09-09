from cfg import DbCfg
import processor
import rcon
import db
import reader
import gen
import campaign
import datetime
import codecs
db.PGConnector.init(DbCfg.connection_string)


def create_divisions_ldb():
    c = campaign.Campaign()
    for name in c.tvds.keys():
        c.tvds[name].create_divisions()


def export(name):
    c = campaign.Campaign()
    with codecs.open(name + "_export.xgml", "w", encoding="cp1251") as f:
        f.write(c.tvds[name].grid.serialize_xgml())
        f.close()


def reset():
    db.PGConnector.Graph.reset()
    c = campaign.Campaign()
    for name in c.tvds.keys():
        c.tvds[name].grid.read_file()
        c.tvds[name].grid.write_db()
        c.tvds[name].grid.read_db()


def generate(name, tvd_name):
    c = campaign.Campaign()
    c.tvds[tvd_name].update()
    gen.Generator.make_mission(name, tvd_name)


def run():
    c = rcon.Commander()
    p = processor.Processor(c)
    r = reader.AtypesReader(p)


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start"))
# reset()
# create_divisions_ldb()
# export('moscow')
# export('stalingrad')
# generate('result1', 'moscow')
# generate('result1', 'stalingrad')
run()
