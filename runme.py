"""Основной файл для запуска"""
import pathlib
import datetime
import configs
import processing
import rcon


DB_NAME = 'rexpert'
MAIN = configs.Main(pathlib.Path(r'.\configs\conf.ini'))
MGEN = configs.Mgen(MAIN)
STATS = configs.Stats(MAIN)
PARAMS = configs.GeneratorParamsConfig()
PLANES = configs.Planes()
GAMEPLAY = configs.Gameplay()


def reset():
    """Сбросить состояние кампании"""
    for tvd_name in MGEN.maps:
        builder = processing.TvdBuilder(tvd_name, MGEN, MAIN, PARAMS, PLANES)
        airfields_controller = processing.AirfieldsController(MAIN, MGEN, PLANES)
        airfields_controller.initialize_airfields(builder.get_tvd('10.11.1941'))


def initialize_campaign():
    """Инициализация кампании"""
    controller = processing.CampaignController(MAIN, MGEN, PLANES, GAMEPLAY, processing.Generator(MAIN, MGEN))
    controller.initialize()


def generate(name: str, tvd_name: str):
    """Сгенерировать миссию"""
    storage = processing.Storage(MAIN)
    tvd_builder = processing.TvdBuilder(tvd_name, MGEN, MAIN, PARAMS, PLANES)
    tvd_builder.update('19.11.1941', storage.airfields.load_by_tvd(tvd_name))
    generator = processing.Generator(MAIN, MGEN)
    generator.make_ldb(tvd_name)
    generator.make_mission(name, tvd_name)


def run():
    """Запуск"""
    objects = configs.Objects()
    events_controller = processing.EventsController(
        objects=objects,
        players_controller=processing.PlayersController(
            main=MAIN,
            commands=rcon.DServerRcon(MAIN.rcon_ip, MAIN.rcon_port)
        ),
        ground_controller=processing.GroundController(objects=objects),
        campaign_controller=processing.CampaignController(MAIN, MGEN, processing.Generator(MAIN, MGEN)),
        airfields_controller=processing.AirfieldsController(MAIN, MGEN, PLANES),
        config=MAIN
    )
    reader = processing.LogsReader(MAIN, events_controller)


print(datetime.datetime.now().strftime("[%H:%M:%S] Program Start."))
# import helpers
# helpers.compile_log('./tmp', 'missionReport*.txt', './tmp/compiled')

# reset()
# export('moscow')
# export('stalingrad')
# generate('result1', 'moscow')
# generate('result1', 'stalingrad')
run()
print(datetime.datetime.now().strftime("[%H:%M:%S] Program Finish."))
