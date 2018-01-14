from calendar import monthrange
import hashlib

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import connection, models
from django.db.models import Avg, Count, Sum
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from mission_report.constants import Coalition, Country
from mission_report.statuses import BotLifeStatus, SortieStatus, LifeStatus

from stuff.fields import CaseInsensitiveCharField

#(player) -тур в стате
#(sortie) -вылет
#(player_mission) -миссия
#За 10 боевых вылетов
def USSR_10_sorties(player):
    return player.sorties_total >= 10 and player.coal_pref == Coalition.Allies and player.landed >= 10 and player.score >= 200

#pilot Germany 10 sortie
def Germ_10_sorties(player):
    return player.sorties_total >= 10 and player.coal_pref == Coalition.Axis and player.landed >= 10 and player.score >= 200

#pilot USSR  50 sortie
def USSR_50_sorties(player):
    return player.sorties_total >= 50 and player.coal_pref == Coalition.Allies and player.landed >= 50 and player.score >= 1000

#pilot Germany 50 sortie
def Germ_50_sorties(player):
    return player.sorties_total >= 50 and player.coal_pref == Coalition.Axis and player.landed >= 50 and player.score >= 1000

#pilot USSR  100 sortie
def USSR_100_sorties(player):
    return player.sorties_total >= 100 and player.coal_pref == Coalition.Allies and player.landed >= 100 and player.score >= 2000

#pilot Germany 100 sortie
def Germ_100_sorties(player):
    return player.sorties_total >= 100 and player.coal_pref == Coalition.Axis and player.landed >= 100 and player.score >= 2000

#pilot USSR  150 sortie
def USSR_150_sorties(player):
    return player.sorties_total >= 150 and player.coal_pref == Coalition.Allies and player.landed >= 150 and player.score >= 3000

#pilot Germany 150 sortie
def Germ_150_sorties(player):
    return player.sorties_total >= 150 and player.coal_pref == Coalition.Axis and player.landed >= 150 and player.score >= 3000

#pilot USSR  200 sortie
def USSR_200_sorties(player):
    return player.sorties_total >= 200 and player.coal_pref == Coalition.Allies and player.landed >= 200 and player.score >= 4000

#pilot Germany 200 sortie
def Germ_200_sorties(player):
    return player.sorties_total >= 200 and player.coal_pref == Coalition.Axis and player.landed >= 200 and player.score >= 4000

#pilot USSR  250 sortie
def USSR_250_sorties(player):
    return player.sorties_total >= 250 and player.coal_pref == Coalition.Allies and player.landed >= 250 and player.score >= 5000

#pilot Germany 250 sortie
def Germ_250_sorties(player):
    return player.sorties_total >= 250 and player.coal_pref == Coalition.Axis and player.landed >= 250 and player.score >= 5000

#За ранение 
def USSR_wound(sortie):
    if sortie.player.coal_pref == Coalition.Allies or (sortie.player.sorties_coal[Coalition.Allies] == sortie.player.sorties_total):
        return sortie.score > 0 and sortie.status == SortieStatus.landed and sortie.bot_status == BotLifeStatus.wounded and sortie.wound > 15

#pilot Germ wounded 
def Germ_wound(sortie):
    if sortie.player.coal_pref == Coalition.Axis or (sortie.player.sorties_coal[Coalition.Axis] == sortie.player.sorties_total):
        return sortie.score > 0 and sortie.status == SortieStatus.landed and sortie.bot_status == BotLifeStatus.wounded and sortie.wound > 15

#За 10 часов налёта в кампании (player.flight_time in seconds!)
def USSR_10_hours(player):
        return player.flight_time >= 36000 and player.coal_pref == Coalition.Allies

#pilot Germ 10 hours in sorties (player.flight_time in seconds!)
def Germ_10_hours(player):
        return player.flight_time >= 36000 and player.coal_pref == Coalition.Axis

#pilot USSR 50 hours in sorties (player.flight_time in seconds!)
def USSR_50_hours(player):
        return player.flight_time >= 180000 and player.coal_pref == Coalition.Allies

#pilot Germ 50 hours in sorties (player.flight_time in seconds!)
def Germ_50_hours(player):
        return player.flight_time >= 180000 and player.coal_pref == Coalition.Axis

#pilot USSR 100 hours in sorties (player.flight_time in seconds!)
def USSR_100_hours(player):
        return player.flight_time >= 360000 and player.coal_pref == Coalition.Allies

#pilot Germ 100 hours in sorties (player.flight_time in seconds!)
def Germ_100_hours(player):
        return player.flight_time >= 360000 and player.coal_pref == Coalition.Axis

#За первый сбитый
def USSR_ak1(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 1 and player.landed >= 1

# pilot Germ 1 A/K
def Germ_ak1(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 1 and player.landed >= 1

# pilot USSR 5 A/K 
def USSR_ak5(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 5

# pilot Germ 5 A/K
def Germ_ak5(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 5
# pilot USSR 10 A/K 
def USSR_ak10(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 10

# pilot Germ 10 A/K
def Germ_ak10(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 10
# pilot USSR 20 A/K 
def USSR_ak20(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 20

# pilot Germ 20 A/K
def Germ_ak20(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 20
# pilot USSR 30 A/K 
def USSR_ak30(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 30

# pilot Germ 30 A/K
def Germ_ak30(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 30
# pilot USSR 50 A/K 
def USSR_ak50(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 50

# pilot Germ 50 A/K
def Germ_ak50(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 50

# pilot USSR 80 A/K 
def USSR_ak80(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 80

# pilot Germ 80 A/K
def Germ_ak80(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 80
# pilot USSR 100 A/K 
def USSR_ak100(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 100

# pilot Germ 100 A/K
def Germ_ak100(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 100

# pilot USSR 150 A/K 
def USSR_ak150(player):
        return player.coal_pref == Coalition.Allies and player.ak_total >= 150

# pilot Germ 150 A/K
def Germ_ak150(player):
        return player.coal_pref == Coalition.Axis and player.ak_total >= 150

#За 10 автомобилей и бронемашин
def USSR_Car10_Arm10(player):
        return player.coal_pref == Coalition.Allies and  (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 10

# Germ armored & truck >=10
def Germ_Car10_Arm10(player):
        return player.coal_pref == Coalition.Axis and  (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 10

# USSR armored & truck >=25
def USSR_Car25_Arm25(player):
        return player.coal_pref == Coalition.Allies and  (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 25

# Germ armored & truck >=25
def Germ_Car25_Arm25(player):
        return player.coal_pref == Coalition.Axis and  (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 25

# USSR armored & truck >=50
def USSR_Car50_Arm50(player):
        return player.coal_pref == Coalition.Allies and  (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 50

# Germ armored & truck >=50
def Germ_Car50_Arm50(player):
        return player.coal_pref == Coalition.Axis and  (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 50

# USSR armored & truck >=100
def USSR_Car100_Arm100(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 100

# Germ armored & truck >=100
def Germ_Car100_Arm100(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('car', 0)+ player.killboard_pve.get('truck', 0) + player.killboard_pve.get('armoured_vehicle', 0)) >= 100

#За 10 танков
def USSR_tanks10(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 10

def Germ_tanks10(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 10

#За 25 танков
def USSR_tanks25(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 25

def Germ_tanks25(player):
        return player.coal_pref == Coalition.Axis and  (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 25

#За 50 танков
def USSR_tanks50(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 50

def Germ_tanks50(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 50

#За 100 танков
def USSR_tanks100(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 100

def Germ_tanks100(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('tank_heavy', 0) + player.killboard_pve.get('tank_medium', 0)  + player.killboard_pve.get('tank_light', 0)) >= 100

#За 10 локомотивов и ж/д вагонов
def USSR_Locomotiv_wagons_10(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('locomotive', 0) + player.killboard_pve.get('wagon', 0)) >= 10

def Germ_Locomotiv_wagons_10(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('locomotive', 0) + player.killboard_pve.get('wagon', 0)) >= 10

#За 25 локомотивов и ж/д вагонов
def USSR_Locomotiv_wagons_25(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('locomotive', 0) + player.killboard_pve.get('wagon', 0)) >= 25

def Germ_Locomotiv_wagons_25(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('locomotive', 0) + player.killboard_pve.get('wagon', 0)) >= 25

#За 50 локомотивов и ж/д вагонов
def USSR_Locomotiv_wagons_50(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('locomotive', 0) + player.killboard_pve.get('wagon', 0)) >= 50

def Germ_Locomotiv_wagons_50(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('locomotive', 0) + player.killboard_pve.get('wagon', 0)) >= 50

#за победу в миссии
def USSR_mission_win(player_mission):
        return player_mission.player.coal_pref == Coalition.Allies and player_mission.mission.winning_coalition == Coalition.Allies and player_mission.mission.players_total >=32 and player_mission.mission.win_reason == 'task'

def Ger_mission_win(player_mission):
        return player_mission.player.coal_pref == Coalition.Axis and player_mission.mission.winning_coalition == Coalition.Axis and player_mission.mission.players_total >=32 and player_mission.mission.win_reason == 'task'

#За 10 кораблей и катеров
def USSR_ships_10(player):
        return player.coal_pref == Coalition.Allies and player.killboard_pve.get('ship', 0) >= 10

def Germ_ships_10(player):
        return player.coal_pref == Coalition.Axis and player.killboard_pve.get('ship', 0) >= 10

#За 25 кораблей и катеров
def USSR_ships_25(player):
        return player.coal_pref == Coalition.Allies and player.killboard_pve.get('ship', 0) >= 25

def Germ_ships_25(player):
        return player.coal_pref == Coalition.Axis and player.killboard_pve.get('ship', 0) >= 25

#За 25 кораблей и катеров
def USSR_ships_50(player):
        return player.coal_pref == Coalition.Allies and player.killboard_pve.get('ship', 0) >= 50

def Germ_ships_50(player):
        return player.coal_pref == Coalition.Axis and player.killboard_pve.get('ship', 0) >= 50

#За 10 артиллерийских орудий
def USSR_arty_10(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 10

def Germ_arty_10(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 10

#За 25 артиллерийских орудий
def USSR_arty_25(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 25

def Germ_arty_25(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 25

#За 50 артиллерийских орудий
def USSR_arty_50(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 50

def Germ_arty_50(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 50

#За 100 артиллерийских орудий
def USSR_arty_100(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 100

def Germ_arty_100(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('artillery_field', 0) + player.killboard_pve.get('artillery_howitzer', 0) + player.killboard_pve.get('artillery_rocket', 0)) >= 100

#За 10 зенитных орудий
def USSR_aa_10(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 10

def Germ_aa_10(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 10

#За 25 зенитных орудий
def USSR_aa_25(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 25

def Germ_aa_25(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 25

#За 50 зенитных орудий
def USSR_aa_50(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 50

def Germ_aa_50(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 50

#За 100 зенитных орудий
def USSR_aa_100(player):
        return player.coal_pref == Coalition.Allies and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 100

def Germ_aa_100(player):
        return player.coal_pref == Coalition.Axis and (player.killboard_pve.get('aaa_mg', 0) + player.killboard_pve.get('aaa_light', 0) + player.killboard_pve.get('aaa_heavy', 0)) >= 100

#За 50 наземных сооружений
def USSR_ground_50(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 50

def Germ_ground_50(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 50

#За 100 наземных сооружений
def USSR_ground_100(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 100

def Germ_ground_100(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 100

#За 250 наземных сооружений
def USSR_ground_250(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 250

def Germ_ground_250(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 250

#За 500 наземных сооружений
def USSR_ground_500(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 500

def Germ_ground_500(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 500

#За 1000 наземных сооружений
def USSR_ground_1000(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 1000

def Germ_ground_1000(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 1000

#За 1500 наземных сооружений
def USSR_ground_1500(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 1500

def Germ_ground_1500(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 1500

#За 2500 наземных сооружений
def USSR_ground_2500(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 2500

def Germ_ground_2500(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 2500

#За 5000 наземных сооружений
def USSR_ground_5000(player):
        return player.coal_pref == Coalition.Allies and player.gk_total >= 5000

def Germ_ground_5000(player):
        return player.coal_pref == Coalition.Axis and player.gk_total >= 5000

#Стрик 10 по воздушным целям
def USSR_air_streak_10(player):
        return player.coal_pref == Coalition.Allies and player.streak_max >= 10

def Germ_air_streak_10(player):
        return player.coal_pref == Coalition.Axis and player.streak_max >= 10

#Стрик 25 по воздушным целям
def USSR_air_streak_25(player):
        return player.coal_pref == Coalition.Allies and player.streak_max >= 25

def Germ_air_streak_25(player):
        return player.coal_pref == Coalition.Axis and player.streak_max >= 25

#Стрик 50 по воздушным целям
def USSR_air_streak_50(player):
        return player.coal_pref == Coalition.Allies and player.streak_max >= 50

def Germ_air_streak_50(player):
        return player.coal_pref == Coalition.Axis and player.streak_max >= 50

#Стрик 100 по воздушным целям
def USSR_air_streak_100(player):
        return player.coal_pref == Coalition.Allies and player.streak_max >= 100

def Germ_air_streak_100(player):
        return player.coal_pref == Coalition.Axis and player.streak_max >= 100


#Стрик 100 по наземным целям
def USSR_ground_streak_100(player):
        return player.coal_pref == Coalition.Allies and player.streak_ground_max >= 100

def Germ_ground_streak_100(player):
        return player.coal_pref == Coalition.Axis and player.streak_ground_max >= 100

#Стрик 250 по наземным целям
def USSR_ground_streak_250(player):
        return player.coal_pref == Coalition.Allies and player.streak_ground_max >= 250

def Germ_ground_streak_250(player):
        return player.coal_pref == Coalition.Axis and player.streak_ground_max >= 250

#Стрик 500 по наземным целям
def USSR_ground_streak_500(player):
        return player.coal_pref == Coalition.Allies and player.streak_ground_max >= 500

def Germ_ground_streak_500(player):
        return player.coal_pref == Coalition.Axis and player.streak_ground_max >= 500

#Стрик 1000 по наземным целям
def USSR_ground_streak_1000(player):
        return player.coal_pref == Coalition.Allies and player.streak_ground_max >= 1000

def Germ_ground_streak_1000(player):
        return player.coal_pref == Coalition.Axis and player.streak_ground_max >= 1000


#1 место в туре
def USSR_tour_1(player):
        return player.coal_pref == Coalition.Allies and player.tour.is_ended and player.rating == 1

def Germ_tour_1(player):
        return player.coal_pref == Coalition.Axis and player.tour.is_ended and player.rating == 1

#лучший шнуродер
def USSR_50_disco(player):
    return player.coal_pref == Coalition.Allies and player.disco >= 50

def Germ_50_disco(player):
    return player.coal_pref == Coalition.Axis and player.disco >= 50

#тестер
def betatest(player):
    return player.takeoff >= 1 and player.tour_id == 1

"""
examples:

# Tour awards
# available parameters stats/models.py/class Player


# streak 100 or more
def fighter_ace(player):
    return player.streak_max >= 100


# total air kills 20 or more
def example_2(player):
    if player.ak_total >= 20:
        return True


# 20 air kills and 200 ground kills
def example_3(player):
    return player.ak_total >= 20 and player.gk_total >= 200


# Sortie awards
# available parameters stats/models.py/class Sortie


# 5 air kills in one sortie
def fighter_hero(sortie):
    return sortie.ak_total >= 5


# Mission awards
# available parameters stats/models.py/class PlayerMission


# 10 air kills in one mission
def mission_fighter_hero(player_mission):
    return player_mission.ak_total >= 15

"""


# streak 100 or more
def fighter_ace(player):
    return player.streak_max >= 100


# 5 air kills in one sortie
def fighter_hero(sortie):
    return sortie.ak_total >= 5


# 10 air kills in one mission
def mission_hero(player_mission):
    return player_mission.ak_total >= 15

