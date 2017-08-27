class EventsController:
    def __init__(self, objects):
        self.objects = objects
        self.tik_last = 0
        self.is_correctly_completed = False

        # порядок важен т.к. позиция в tuple соответствует ID события
        self.events_handlers = (self.event_mission_start, self.event_hit, self.event_damage, self.event_kill,
                                self.event_sortie_end, self.event_takeoff, self.event_landing, self.event_mission_end,
                                self.event_mission_result, self.event_airfield, self.event_player, self.event_group,
                                self.event_game_object, self.event_influence_area, self.event_influence_area_boundary,
                                self.event_log_version, self.event_bot_deinitialization, self.event_pos_changed,
                                self.event_bot_eject_leave, self.event_round_end, self.event_player_connected,
                                self.event_player_disconnected)

    def update_tik(self, tik):
        self.tik_last = tik

    def event_mission_start(self, tik, date, file_path, game_type_id, countries, settings, mods, preset_id):
        self.update_tik(tik)

    def event_hit(self, tik, ammo, attacker_id, target_id):
        self.update_tik(tik)

    def event_damage(self, tik, damage, attacker_id, target_id, pos):
        self.update_tik(tik)
        # дамага может не быть из-за бага логов

    def event_kill(self, tik, attacker_id, target_id, pos):
        self.update_tik(tik)
        # в логах так бывает что кто-то умер, а кто не известно :)

    def event_sortie_end(self, tik, aircraft_id, bot_id, cartridges, shells, bombs, rockets, pos):
        self.update_tik(tik)
        # бывают события дубли - проверяем

    def event_takeoff(self, tik, aircraft_id, pos):
        self.update_tik(tik)

    def event_landing(self, tik, aircraft_id, pos):
        self.update_tik(tik)

    def event_mission_end(self, tik):
        self.update_tik(tik)
        self.is_correctly_completed = True

    def event_mission_result(self, tik, object_id, coal_id, task_type_id, success, icon_type_id, pos):
        self.update_tik(tik)

    def event_airfield(self, tik, airfield_id, country_id, coal_id, aircraft_id_list, pos):
        self.update_tik(tik)

    def event_player(self, tik, aircraft_id, bot_id, account_id, profile_id, name, pos, aircraft_name, country_id,
                     coal_id, airfield_id, airstart, parent_id, payload_id, fuel, skin, weapon_mods_id,
                     cartridges, shells, bombs, rockets, form):
        self.update_tik(tik)

    def event_group(self, tik, group_id, members_id, leader_id):
        self.update_tik(tik)

    def event_game_object(self, tik, object_id, object_name, country_id, coal_id, name, parent_id):
        self.update_tik(tik)

    def event_influence_area(self, tik, area_id, country_id, coal_id, enabled, in_air):
        self.update_tik(tik)

    def event_influence_area_boundary(self, tik, area_id, boundary):
        self.update_tik(tik)

    def event_log_version(self, tik, version):
        self.update_tik(tik)

    def event_bot_deinitialization(self, tik, bot_id, pos):
        self.update_tik(tik)

    def event_pos_changed(self, tik, object_id, pos):
        self.update_tik(tik)

    def event_bot_eject_leave(self, tik, bot_id, parent_id, pos):
        self.update_tik(tik)

    def event_round_end(self, tik):
        self.update_tik(tik)

    def event_player_connected(self, tik, account_id, profile_id):
        self.update_tik(tik)

    def event_player_disconnected(self, tik, account_id, profile_id):
        self.update_tik(tik)
