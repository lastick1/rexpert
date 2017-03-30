from cfg import DbCfg, MainCfg
import processor
import rcon
import db
import reader
import gen
import campaign
import draw
db.PGConnector.init(DbCfg.connection_string)


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


# reset()
run()
# generate('result1', 'moscow')
print()
