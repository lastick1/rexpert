""" Конфиги """
# pylint: disable=no-member
from pathlib import Path
import json
import configparser

conf = configparser.ConfigParser()
conf.read('.\\configs\\conf.ini')
main_game_folder = Path(conf['PROGRAM']['game_folder']).absolute()
mgen_cfg = json.load(open('.\\configs\\missiongen.json'))
mgen_tvd_folders = {x: main_game_folder.joinpath(mgen_cfg[x]['tvd_folder']).absolute() for x in mgen_cfg['maps']}
mgen_af_tf = Path('.\\af_templates\\').absolute()

dfpr_cfg = json.load(open('.\\configs\\dfpr.json'))
draw_cfg = json.load(open('.\\configs\\draw_settings.json'))
img_fld = Path('.\\img\\').absolute()

stats_cfg = json.load(open('.\\configs\\stats_custom.json'))
loc_cfg = json.load(open('.\\configs\\loc_cfg.json'))
gp_cfg = json.load(open('.\\configs\\gameplay.json'))


class MainCfg:
    game_folder = main_game_folder
    dogfight_folder = main_game_folder.joinpath('.\\data\\Multiplayer\\Dogfight').absolute()
    mission_gen_folder = Path(conf['MISSIONGEN']['mission_gen_folder']).absolute()
    stats_static = Path(conf['PROGRAM']['stats_folder']).joinpath('.\\static\\').absolute()
    graph_folder = Path('.\\configs\\').absolute()
    configs_folder = Path('.\\configs\\').absolute()
    cache_folder = Path('.\\cache\\').absolute()
    resaver_folder = Path(conf['MISSIONGEN']['resaver_folder'])
    generate_missions = True if "true" in conf['MISSIONGEN']['generate_missions'].lower() else False
    use_resaver = True if "true" in conf['MISSIONGEN']['use_resaver'].lower() else False
    test_mode = True if "true" in conf['PROGRAM']['test_mode'].lower() else False
    offline_mode = True if "true" in conf['PROGRAM']['offline_mode'].lower() else False
    debug_mode = True if "true" in conf['PROGRAM']['debug_mode'].lower() else False
    console_cmd_output = True if "true" in conf['PROGRAM']['console_cmd_output'].lower() else False
    console_chat_output = True if "true" in conf['PROGRAM']['console_chat_output'].lower() else False
    minimal_chat_interval = int(conf['PROGRAM']['minimal_chat_interval'])
    rcon_ip = conf['RCON']['rcon_ip']
    rcon_port = int(conf['RCON']['rcon_port'])
    rcon_login = conf['RCON']['rcon_login']
    rcon_password = conf['RCON']['rcon_password']
    logs_directory = Path(conf['DSERVER']['logs_directory'])
    arch_directory = Path(conf['DSERVER']['arch_directory'])
    logs_copy_directory = Path(conf['NEW_STATS']['logs_directory'])
    zips_copy_directory = Path(conf['NEW_STATS']['zips_directory'])
    chat_directory = Path(conf['DSERVER']['chat_directory'])
    msrc_directory = Path(conf['NEW_STATS']['msrc_directory'])
    mission_time = {
        'h': int(conf['GAMEPLAY']['mission_time'].split(sep=':')[0]),
        'm': int(conf['GAMEPLAY']['mission_time'].split(sep=':')[1]),
        's': int(conf['GAMEPLAY']['mission_time'].split(sep=':')[2])
    }
    capture_pts = int(conf['GAMEPLAY']['capture_pts'])


class DbCfg:
    """ Конфиг подключения к базе данных """
    connection_string = 'dbname={} host={} port={} user={} password={}'.format(
        conf['STATS']['database'],
        conf['STATS']['host'],
        conf['STATS']['port'],
        conf['STATS']['user'],
        conf['STATS']['password']
    )
    database = conf['STATS']['database']
    host = conf['STATS']['host']
    port = conf['STATS']['port']
    user = conf['STATS']['user']
    password = conf['STATS']['password']


class MissionGenCfg:
    cfg = mgen_cfg
    maps = mgen_cfg['maps']
    af_templates_folder = mgen_af_tf
    make_ldb_folder = MainCfg.game_folder.joinpath('.\\bin\\missiongen\\').absolute()
    af_csv = {x: Path('.\\configs\\').joinpath(mgen_cfg[x]['airfields_csv']).absolute() for x in maps}
    tvd_folders = mgen_tvd_folders
    ldf_files = {x: mgen_tvd_folders[x].joinpath(mgen_cfg[x]['ldf_file']).absolute() for x in maps}
    ldf_templates = {x: mgen_tvd_folders[x].joinpath(mgen_cfg[x]['ldf_base_file']).absolute() for x in maps}
    daytime_files = {x: Path('.\\configs\\').joinpath(mgen_cfg[x]['daytime_csv']).absolute() for x in maps}
    af_groups_folders = {x: {z: mgen_tvd_folders[x].joinpath(mgen_cfg[x]['af_groups_folders'][z]).absolute()
                             for z in mgen_cfg['sides']}
                         for x in maps}
    stages = {x: mgen_cfg[x]['stages'] for x in maps}
    default_stages = {x: {z: mgen_af_tf.joinpath(mgen_cfg[x]['default_templates'][z]).absolute()
                          for z in mgen_cfg['sides']}
                      for x in maps}
    xgml = {x: MainCfg.configs_folder.joinpath(mgen_cfg[x]['graph_file']) for x in maps}
    generate_influences = True if "true" in conf['MISSIONGEN']['generate_influences'].lower() else False
    icons_group_files = {x: mgen_tvd_folders[x].joinpath(mgen_cfg[x]['icons_group_file']).absolute() for x in maps}


class DfprCfg:
    cfg = dfpr_cfg


class DrawCfg:
    cfg = draw_cfg
    coals = draw_cfg['coals']
    img_folder = img_fld
    background = {x: str(img_fld.joinpath(draw_cfg['backgrounds'][x])) for x in MissionGenCfg.maps}
    flame = str(img_fld.joinpath(draw_cfg['flames']))
    airfield = str(img_fld.joinpath(draw_cfg['airfields']))
    icons = {x: {z: str(img_fld.joinpath(draw_cfg[x][z]).absolute()) for z in draw_cfg['coal_icons']} for x in coals}
    draw_edges = True if "true" in conf['PROGRAM']['draw_edges'].lower() else False
    draw_nodes = True if "true" in conf['PROGRAM']['draw_nodes'].lower() else False
    draw_nodes_text = True if "true" in conf['PROGRAM']['draw_nodes_text'].lower() else False
    draw_influences = True if "true" in conf['PROGRAM']['draw_influences'].lower() else False


class StatsCustomCfg:
    cfg = stats_cfg
    map_main_page = str(MainCfg.stats_static.joinpath(stats_cfg['image_files']['map_main_page']).absolute())
    map_full_size = str(MainCfg.stats_static.joinpath(stats_cfg['image_files']['map_full_size']).absolute())
    json_files = stats_cfg['json_files']
    image_files = stats_cfg['image_files']
    online = MainCfg.stats_static.joinpath(json_files['online_players'])
    time_remaining = MainCfg.stats_static.joinpath(json_files['elapsed_time'])
    credits_data = MainCfg.stats_static.joinpath(json_files['planes_data'])
    payloads = MainCfg.stats_static.joinpath(json_files['payloads'])
    maps_archive_folder = Path(conf['PROGRAM']['maps_archive_folder'])


class LocationsCfg:
    cfg = loc_cfg


class Gameplay:
    cfg = gp_cfg
    penalties = gp_cfg['penalties']
    aircraft_lost = gp_cfg['aircraft_lost']
    grounds = gp_cfg['grounds']
    supply = gp_cfg['supply']
    free_plane_hours = supply['free_plane_hours']
    renew_minutes = supply['renew_minutes']
    flight_second_price = supply['flight_second_price']
    max_suppliable_amount = supply['max_suppliable']
    kill_weight_reward = supply['kill_weight_reward']
    aircraft_multipliers = {
        'light': supply['aircraft_multipliers']['light'],
        'medium': supply['aircraft_multipliers']['medium'],
        'heavy': supply['aircraft_multipliers']['heavy'],
        'transport': supply['aircraft_multipliers']['transport']
    }
    economics = gp_cfg['economics']
    startup_capital = economics['startup_capital']
    max_capital = economics['max_capital']
    min_capital = economics['min_capital']
    fee = economics['takeoff_fee'] / 100
    k = {
        'w': economics['coefficients']['weapons'],
        'f': economics['coefficients']['fuel'],
        'b': economics['coefficients']['base'],
        's': economics['coefficients']['sorties'],
        'p': economics['coefficients']['points'],
        'l': economics['coefficients']['payloads']
    }
