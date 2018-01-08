"""Основной файл для запуска"""
import datetime
import configs
import processing
import rcon


CONFIG = configs.Config()


def reset():
    """Сбросить состояние кампании"""
    for tvd_name in CONFIG.mgen.maps:
        builder = processing.TvdBuilder(tvd_name, CONFIG.mgen, CONFIG.main, CONFIG.generator, CONFIG.planes)
        airfields_controller = processing.AirfieldsController(CONFIG.main, CONFIG.mgen, CONFIG.planes)
        airfields_controller.initialize_airfields(builder.get_tvd('10.11.1941'))


def initialize_campaign():
    """Инициализация кампании"""
    controller = processing.CampaignController(
        CONFIG.main, CONFIG.mgen, CONFIG.planes, CONFIG.gameplay, processing.Generator(CONFIG.main, CONFIG.mgen))
    controller.initialize()


def generate(name: str, tvd_name: str):
    """Сгенерировать миссию"""
    storage = processing.Storage(CONFIG.main)
    tvd_builder = processing.TvdBuilder(tvd_name, CONFIG.mgen, CONFIG.main, CONFIG.generator, CONFIG.planes)
    tvd_builder.update('19.11.1941', storage.airfields.load_by_tvd(tvd_name))
    generator = processing.Generator(CONFIG.main, CONFIG.mgen)
    generator.make_ldb(tvd_name)
    generator.make_mission(name, tvd_name)


def run():
    """Запуск"""
    objects = configs.Objects()
    events_controller = processing.EventsController(
        objects=objects,
        players_controller=processing.PlayersController(
            main=CONFIG.main,
            commands=rcon.DServerRcon(CONFIG.main.rcon_ip, CONFIG.main.rcon_port)
        ),
        ground_controller=processing.GroundController(objects=objects),
        campaign_controller=processing.CampaignController(
            main=CONFIG.main,
            mgen=CONFIG.mgen,
            planes=CONFIG.planes,
            gameplay=CONFIG.gameplay,
            generator=processing.Generator(CONFIG.main, CONFIG.mgen)
        ),
        airfields_controller=processing.AirfieldsController(CONFIG.main, CONFIG.mgen, CONFIG.planes),
        config=CONFIG.main
    )
    processing.LogsReader(CONFIG.main, events_controller)


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
