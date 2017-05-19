import psycopg2
from psycopg2.extras import RealDictCursor


class ConstructorNotAllowed(Warning):
    pass


class PGConnector:
    """ Коннектор базы данных """
    def __init__(self):
        raise ConstructorNotAllowed()

    __connection_string = None

    @staticmethod
    def init(connection_string):
        """ Инициализация строкой подключения всех подклассов работы с данными """
        PGConnector.__connection_string = connection_string
        PGConnector.Log._init(connection_string)
        PGConnector.Missions._init(connection_string)
        PGConnector.Graph._init(connection_string)
        PGConnector.Player._init(connection_string)
        PGConnector.Squad._init(connection_string)

    @staticmethod
    def get_objects_dict():
        """ Извлечь словарь данных для MissionReport """
        with psycopg2.connect(PGConnector.__connection_string) as connection:
            cur = connection.cursor(cursor_factory=RealDictCursor)
            sql = 'SELECT name, id, score_id, cls_base, cls, is_playable, log_name FROM objects'
            cur.execute(sql)
            results = {}
            f = cur.fetchall()

            for row in f:
                results[row["log_name"]] = row

            return results

    class Log:
        """ Подкласс для сохранения получаемых логов миссий в БД """
        def __init__(self):
            raise ConstructorNotAllowed()

        __connection_string = None

        @staticmethod
        def _init(connection_string):
            PGConnector.Log.__connection_string = connection_string

        @staticmethod
        def insert_atypes(atypes):
            """
            :param atypes: [tik, atype, atype_string, mission_name] 
            """
            with psycopg2.connect(PGConnector.Log.__connection_string) as connection:
                cursor = connection.cursor()
                records_list_template = ','.join(['%s'] * len(atypes))
                insert_query = """INSERT INTO custom_atypes_cache(tik, atype, atype_string, mission_name)
                                    VALUES {0} RETURNING key""".format(records_list_template)
                if len(atypes) > 0:
                    cursor.execute(insert_query, atypes)
                    connection.commit()
                    return cursor.fetchall()
                return [0]

        @staticmethod
        def force_complete_old_missions():
            sql_sel = """SELECT mission_name
                            FROM custom_missions_log
                            ORDER BY key DESC
                            LIMIT 1"""
            sql_upd = """UPDATE custom_missions_log
                            SET is_ended=%s
                            WHERE mission_name!=%s"""
            with psycopg2.connect(PGConnector.Log.__connection_string) as connection:
                cursor = connection.cursor()
                cursor.execute(sql_sel)
                last_mission = cursor.fetchone()[0]
                cursor.execute(sql_upd,(
                    True,
                    last_mission
                ))
                connection.commit()

        @staticmethod
        def insert_or_update_mission_row(
                is_processed=False,
                mission_name="",
                is_ended_correctly=False,
                is_ended=False,
                won_coal_id=-1,
                block=-1,
                red_score_points=0.0,
                blue_score_points=0.0,
                file_name=""):
            sql_select = """SELECT count(*)
                                FROM custom_missions_log
                                WHERE mission_name = %s"""
            sql_insert = """INSERT INTO custom_missions_log(
                                    is_processed, mission_name, is_ended_correctly, is_ended,
                                    won_coal_id, block, red_score_points, blue_score_points, file_name)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            sql_update = """UPDATE custom_missions_log
                                SET is_processed=%s, is_ended_correctly=%s, is_ended=%s, won_coal_id=%s,
                                    block=%s, red_score_points=%s, blue_score_points=%s, file_name=%s
                                WHERE mission_name=%s;"""
            with psycopg2.connect(PGConnector.Log.__connection_string) as connection:
                cursor = connection.cursor()
                cursor.execute(sql_select, [mission_name])
                count = list(cursor.fetchone())
                if count[0] == 0:
                    cursor.execute(sql_insert, (
                        is_processed,
                        mission_name,
                        is_ended_correctly,
                        is_ended,
                        won_coal_id,
                        block,
                        red_score_points,
                        blue_score_points,
                        file_name
                    ))
                    connection.commit()

                elif count[0] == 1:
                    cursor.execute(sql_update, (
                        is_processed,
                        is_ended_correctly,
                        is_ended,
                        won_coal_id,
                        block,
                        red_score_points,
                        blue_score_points,
                        file_name,
                        mission_name
                    ))
                    connection.commit()
                else:
                    raise Warning
            PGConnector.Log.force_complete_old_missions()

    class Missions:
        """ Подкласс для работы с данными миссий в БД """
        def __init__(self):
            raise ConstructorNotAllowed()

        __connection_string = None

        @staticmethod
        def _init(connection_string):
            PGConnector.Missions.__connection_string = connection_string

        @staticmethod
        def select_unprocessed():
            sql = """SELECT mission_name, key
                        FROM custom_missions_log
                        WHERE is_processed = false
                        ORDER BY is_processed DESC, key"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cursor = connection.cursor()
                cursor.execute(sql)
                try:
                    results = list(zip(*cursor.fetchall()))[0]
                    return results
                except IndexError:
                    return []

        @staticmethod
        def select_unprocessed_count():
            sql = """SELECT count(*) as unprocessed
                        FROM custom_missions_log
                        WHERE is_processed = false
                        ORDER BY is_processed DESC, key"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cursor = connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute(sql)
                return cursor.fetchone()['unprocessed']

        @staticmethod
        def select_mission_log_atypes(mission_name, last_atype=0):
            sql = """SELECT atype_string, key
                        FROM custom_atypes_cache
                        WHERE mission_name = %s
                        AND key > %s
                        ORDER BY tik, key"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cursor = connection.cursor()
                cursor.execute(sql, (mission_name, last_atype))
                if cursor.rowcount:
                    return cursor.fetchall()
                else:
                    return []

        @staticmethod
        def select_mission_row(mission_name):
            sql = """SELECT is_processed, mission_name, is_ended_correctly, is_ended,
                                            won_coal_id, block, red_score_points, blue_score_points, file_name
                                        FROM custom_missions_log
                                        WHERE mission_name = %s"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, [mission_name])
                return cur.fetchall()[0]

        @staticmethod
        def ended_count():
            sql = """SELECT count(*) AS mc FROM custom_missions_log WHERE is_ended_correctly=true"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql)
                fetch = cur.fetchall()[0]
                return fetch['mc']

        @staticmethod
        def update_mission_row(mission_name, won_coal_id, block, red_score, blue_score):
            sql = """UPDATE custom_missions_log
                            SET is_processed=true,
                                won_coal_id=%s,
                                block=%s,
                                red_score_points=%s,
                                blue_score_points=%s
                            WHERE mission_name=%s"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql, (
                    won_coal_id,
                    block,
                    red_score,
                    blue_score,
                    mission_name
                ))
                connection.commit()

        @staticmethod
        def map_drawn(mission_name):
            sql = """SELECT mission_name
                        FROM custom_missions_log
                        WHERE mission_name = %s and map_drawn = false"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (mission_name,))
                if cur.rowcount:
                    return False
                return True

        @staticmethod
        def set_map_drawn(mission_name):
            sql = """UPDATE custom_missions_log
                        SET map_drawn=%s
                        WHERE mission_name = %s"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (True, mission_name))
                connection.commit()

        @staticmethod
        def skip(n):
            if n <= 0:
                return
            sql = """SELECT mission_name
                    FROM custom_missions_log
                    WHERE is_ended_correctly = true
                    AND is_ended = true
                    ORDER BY key DESC
                    LIMIT 1"""
            sql_insert = """INSERT INTO custom_missions_log(
                                is_processed, mission_name, is_ended_correctly, is_ended)
                            VALUES (true, %s, true, false)"""
            with psycopg2.connect(PGConnector.Missions.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql)
                fall = cur.fetchall()
                mission_name = fall[0]['mission_name']
                i = 0
                while i < n:
                    cur.execute(sql_insert, (mission_name, ))
                    i += 1

                connection.commit()

    class Graph:
        """ Подкласс для работы с данными графа в БД """
        def __init__(self):
            raise ConstructorNotAllowed()

        __connection_string = None

        @staticmethod
        def _init(connection_string):
            PGConnector.Graph.__connection_string = connection_string

        @staticmethod
        def select(tvd):
            sql_sel_nodes = """
                SELECT country, coordinate_x, coordinate_z, weight, key, text, selectable, is_aux, changed_date
                    FROM custom_graph_nodes
                    WHERE tvd=%s"""
            sql_sel_edges = """SELECT node_a, node_b FROM custom_graph_edges WHERE tvd=%s"""
            with psycopg2.connect(PGConnector.Graph.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql_sel_nodes, (tvd,))
                nodes = cur.fetchall()
                cur.execute(sql_sel_edges, (tvd,))
                edges = cur.fetchall()
                return nodes, edges

        @staticmethod
        def reset():
            sql_tr_nodes = """TRUNCATE TABLE custom_graph_nodes CASCADE"""
            sql_tr_edges = """TRUNCATE TABLE custom_graph_edges CASCADE"""
            with psycopg2.connect(PGConnector.Graph.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql_tr_nodes)
                cur.execute(sql_tr_edges)

        @staticmethod
        def insert(tvd, nodes=tuple(), edges=tuple()):
            sql_ins_node = """INSERT INTO custom_graph_nodes(
                                country, coordinate_x, coordinate_z, weight, key, selectable, text, is_aux, tvd)
                                VALUES (%s, %s, %s, 10, %s, %s, %s, %s, %s);"""
            sql_ins_edge = """INSERT INTO custom_graph_edges(node_a, node_b, tvd)
                                VALUES (%s, %s, %s);"""
            with psycopg2.connect(PGConnector.Graph.__connection_string) as connection:
                cur = connection.cursor()
                for n in nodes:
                    cur.execute(sql_ins_node, (
                                n['country'],
                                n['coordinate_x'],
                                n['coordinate_z'],
                                n['key'],
                                n['selectable'],
                                n['text'],
                                n['is_aux'],
                                tvd))
                connection.commit()
                for e in edges:
                    cur.execute(sql_ins_edge, (
                                e['node_a'],
                                e['node_b'],
                                tvd))
                connection.commit()

        @staticmethod
        def update_graph_node(key, tvd, country):
            sql = """UPDATE custom_graph_nodes
                        SET country=%s, changed_date=now()::timestamp
                        WHERE key=%s
                        AND tvd=%s"""
            with psycopg2.connect(PGConnector.Graph.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql, (
                    country,
                    key,
                    tvd
                ))
                connection.commit()

    class Player:
        """ Подкласс для работы с данными игроков в БД """
        def __init__(self):
            raise ConstructorNotAllowed()

        __connection_string = None

        @staticmethod
        def _init(connection_string):
            PGConnector.Player.__connection_string = connection_string

        @staticmethod
        def select_all():
            sql = """SELECT account_id, id FROM custom_profiles_extension, profiles WHERE account_id = uuid"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql)
                if cur.rowcount:
                    return cur.fetchall()
                else:
                    return []

        @staticmethod
        def initialize_player(account_id, nickname, specialization):
            sql_sel_profiles = """SELECT id, uuid, nickname, is_hide, user_id, squad_id
                                        FROM profiles
                                        WHERE uuid = %s or nickname = %s"""
            sql_sel_custom = """SELECT account_id, planes
                                        FROM custom_profiles_extension
                                        WHERE account_id = %s"""
            sql_upd_profiles = """UPDATE profiles
                                        SET nickname=%s
                                        WHERE uuid = %s"""
            sql_ins_custom = """INSERT INTO custom_profiles_extension(
                                        account_id, specialization)
                                        VALUES (%s, %s)"""
            sql_ins_player = """INSERT INTO profiles(
                                        uuid, nickname, is_hide)
                                        VALUES (%s, %s, %s)"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                # обновление сменивших ник
                cur.execute(sql_sel_custom, (account_id,))
                cur.fetchall()
                if cur.rowcount > 0:
                    cur.execute(sql_upd_profiles, (nickname, account_id))
                    connection.commit()
                else:
                    cur.execute(sql_sel_profiles, (account_id, nickname))
                    fetch = cur.fetchall()
                    if len(fetch) > 0:
                        cur.execute(sql_ins_custom, (account_id, specialization))
                        connection.commit()
                    else:
                        cur.execute(sql_ins_player, (account_id, nickname, False))
                        cur.execute(sql_ins_custom, (account_id, specialization))
                        connection.commit()

        @staticmethod
        def select_by_account(account_id):
            sql = """SELECT
                u.id as                 user_id,
                s.squad_id as           squad_id,
                p.uuid as               account_id,
                p.nickname as           nickname,
                e.planes as 		    planes,
                sd.name as 		        squad_name,
                sd.tag as 			    squad_tag,
                pl.sorties_cls as 		sorties_cls,
                e.last_mission as       last_mission,
                e.last_tik as           last_tik,
                (SELECT count(*) FROM profiles WHERE squad_id = s.squad_id) as squad_strength
                    FROM profiles as p
                    JOIN custom_profiles_extension as e ON p.uuid = e.account_id
                    LEFT JOIN users as u ON u.username = p.nickname
                    LEFT JOIN squads_members as s ON s.member_id = u.id
                    LEFT JOIN squads as sd ON sd.id = s.squad_id
                    LEFT JOIN players as pl ON pl.profile_id = p.id
                    --WHERE pl.tour_id = (SELECT max(id) FROM tours)
                    WHERE account_id = %s
                    ORDER BY pl.tour_id DESC"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (account_id, ))
                # if cur.rowcount > 1:
                #     raise NameError('More than 1 account! {}'.format(account_id))
                if cur.rowcount >= 1:
                    return cur.fetchall()[0]
                return

        @staticmethod
        def select_id_by_nickname(nickname):
            sql = """SELECT
                    p.uuid as               account_id,
                    p.nickname as           nickname
                        FROM profiles as p
                        JOIN custom_profiles_extension as e ON p.uuid = e.account_id
                        WHERE nickname = %s"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (nickname, ))
                if cur.rowcount > 1:
                    raise NameError('More than 1 nickname! {}'.format(nickname))
                if cur.rowcount == 1:
                    return cur.fetchall()[0]
                return

        @staticmethod
        def select_specialization(account_id):
            sql = """SELECT 
                        profiles.uuid, 
                        profiles.nickname, 
                        players.sorties_cls,
                        custom_profiles_extension.specialization
                    FROM 
                        custom_profiles_extension
                        LEFT JOIN profiles ON custom_profiles_extension.account_id = profiles.uuid
                        LEFT JOIN players ON players.profile_id = profiles.id
                    WHERE 
                        profiles.uuid = %s AND
                        players.tour_id = (SELECT max(id) FROM tours)"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (account_id, ))
                if cur.rowcount > 0:
                    return cur.fetchone()
                else:
                    sql = """SELECT * FROM custom_profiles_extension WHERE account_id = %s ;"""
                    cur.execute(sql, (account_id,))
                    if cur.rowcount > 0:
                        return cur.fetchone()
                return

        @staticmethod
        def set_specialization(account_id, specialization):
            sql = """UPDATE custom_profiles_extension
                    SET specialization = %s
                    WHERE account_id = %s ;"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql, (specialization, account_id))
                connection.commit()

        @staticmethod
        def select_players_table():
            sql = """SELECT uuid as account_id, nickname, ban_expire_date, credits
                            FROM profiles, custom_profiles_extension as cpe
                            WHERE profiles.uuid = cpe.account_id"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql)
                return cur.fetchall()

        @staticmethod
        def get_planes(account_id):
            sql = """SELECT *
                    FROM custom_profiles_extension
                    WHERE account_id = %s"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (account_id,))
                if cur.rowcount > 1:
                    raise NameError('Unexpected rowcount for account_id {}'.format(account_id))
                if cur.rowcount == 1:
                    return cur.fetchall()[0]
                return

        @staticmethod
        def set_planes(account_id, planes):
            sql = """UPDATE custom_profiles_extension
                    SET planes=%s
                    WHERE account_id=%s"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql, (
                    planes,
                    account_id
                ))
                connection.commit()

        @staticmethod
        def set_unlocks(account_id, unlocks):
            sql = """UPDATE custom_profiles_extension
                    SET unlocks=%s
                    WHERE account_id=%s"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql, (
                    unlocks,
                    account_id
                ))
                connection.commit()

        @staticmethod
        def update_nickname(account_id, nickname):
            sql = """UPDATE profiles
                        SET nickname=%s
                        WHERE uuid=%s"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql, (
                    nickname,
                    account_id
                ))
                connection.commit()

        @staticmethod
        def get_last_flight_time(account_id):
            sql = """SELECT pl.date_last_sortie
                        FROM players as pl
                        JOIN profiles as pr ON pl.profile_id = pr.id
                        WHERE pr.uuid = %s
                        ORDER BY pl.date_last_sortie DESC
                        LIMIT 1"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (account_id,))
                if cur.rowcount:
                    ret = cur.fetchall()
                    return ret[0]['date_last_sortie']

        @staticmethod
        def select_profiles():
            sql = """SELECT p.uuid as account_id, p.nickname as nickname, e.credits as credits, s.credits as squad_credits
                    FROM profiles as p
                    LEFT JOIN custom_profiles_extension as e ON p.uuid = e.account_id
                    LEFT JOIN custom_squads_extension as s ON p.squad_id = s.squad_id"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql)
                return cur.fetchall()

        @staticmethod
        def touch(account_id, last_mission, last_tik):
            sql = """UPDATE custom_profiles_extension
                    SET last_mission=%s, last_tik=%s
                    WHERE account_id=%s"""
            with psycopg2.connect(PGConnector.Player.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (last_mission, last_tik, account_id))
                connection.commit()

    class Squad:
        """ Подкласс для работы с данными сквадов в БД """
        def __init__(self):
            raise ConstructorNotAllowed()

        __connection_string = None

        @staticmethod
        def _init(connection_string):
            PGConnector.Squad.__connection_string = connection_string

        @staticmethod
        def select_by_id(squad_id):
            sql = """SELECT *
                    FROM squads as s
                    JOIN custom_squads_extension as e ON s.id = e.squad_id
                    WHERE id = %s AND is_removed = false"""
            with psycopg2.connect(PGConnector.Squad.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (squad_id,))
                if cur.rowcount:
                    if cur.rowcount > 1:
                        raise NameError('Two squads with same id! {}'.format(squad_id))
                    return cur.fetchone()
                raise NoSuchSquadId

        @staticmethod
        def last_flight(squad_id):
            sql = """SELECT
                u.id as                 user_id,
                s.squad_id as           squad_id,
                p.uuid as               account_id,
                p.nickname as           nickname,
                e.planes as 		    planes,
                sd.name as 		        squad_name,
                sd.tag as 			    squad_tag,
                pl.sorties_cls as 		sorties_cls,
                e.last_mission as       last_mission,
                e.last_tik as           last_tik,
                (SELECT count(*) FROM profiles WHERE squad_id = s.squad_id) as squad_strength
                    FROM profiles as p
                    JOIN custom_profiles_extension as e ON p.uuid = e.account_id
                    LEFT JOIN users as u ON u.username = p.nickname
                    LEFT JOIN squads_members as s ON s.member_id = u.id
                    LEFT JOIN squads as sd ON sd.id = s.squad_id
                    LEFT JOIN players as pl ON pl.profile_id = p.id
                    WHERE s.squad_id = %s
                    ORDER BY pl.tour_id DESC, e.last_mission DESC, e.last_tik DESC"""
            with psycopg2.connect(PGConnector.Squad.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (squad_id,))
                if cur.rowcount:
                    return cur.fetchone()
                raise NameError('NoSuchSquadId {}'.format(squad_id))

        @staticmethod
        def initialize(squad_id):
            sql = """INSERT INTO custom_squads_extension(squad_id) VALUES (%s);"""
            with psycopg2.connect(PGConnector.Squad.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (squad_id,))
                connection.commit()
            return PGConnector.Squad.select_by_id(squad_id)

        @staticmethod
        def sid_by_account_id(account_id):
            sql = """SELECT p.nickname as nickname, e.account_id as account_id, sm.squad_id
                    FROM squads_members as sm
                    JOIN users as u ON u.id = sm.member_id
                    JOIN squads as s ON s.id = sm.squad_id
                    JOIN profiles as p ON p.nickname = u.username
                    JOIN custom_profiles_extension as e ON p.uuid = e.account_id
                    WHERE s.is_removed = false
                    AND e.account_id = %s"""
            with psycopg2.connect(PGConnector.Squad.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (account_id,))
                if cur.rowcount == 1:
                    fall = cur.fetchall()
                    return fall['squad_id']
                if cur.rowcount > 1:
                    raise NameError('Unexpected rowcount')
                return None

        @staticmethod
        def get_planes(squad_id):
            sql = """SELECT *
                    FROM custom_squads_extension
                    WHERE squad_id = %s"""
            with psycopg2.connect(PGConnector.Squad.__connection_string) as connection:
                cur = connection.cursor(cursor_factory=RealDictCursor)
                cur.execute(sql, (squad_id,))
                if cur.rowcount > 1:
                    raise NameError('Unexpected rowcount for squad_id {}'.format(squad_id))
                if cur.rowcount == 1:
                    return cur.fetchall()[0]
                return

        @staticmethod
        def set_planes(sid, planes):
            sql = """UPDATE custom_squads_extension
                        SET planes=%s
                        WHERE squad_id=%s"""
            with psycopg2.connect(PGConnector.Squad.__connection_string) as connection:
                cur = connection.cursor()
                cur.execute(sql, (planes, sid))
                connection.commit()
