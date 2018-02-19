# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_RED_TANKBATTLES; main(scg\1\blocks_quickmission\ground\tank\7vs7_red_tanks.group);
blocks_set; blocks_BLUE_TANKBATTLES; main(scg\1\blocks_quickmission\ground\tank\7vs7_blue_tanks.group);
blocks_set; blocks_SMOKE_R1; main(scg\1\blocks_quickmission\ground\effects\1smoke.group);
blocks_set; blocks_SMOKE_R2; main(scg\1\blocks_quickmission\ground\effects\1smoke.group);
blocks_set; blocks_SMOKE_B1; main(scg\1\blocks_quickmission\ground\effects\1smoke.group);
blocks_set; blocks_SMOKE_B2; main(scg\1\blocks_quickmission\ground\effects\1smoke.group);

#
## geo params
#
phase; RED_TANKBATTLES; random(<EMPTY>); blocks_RED_TANKBATTLES; clone_location;;
phase; BLUE_TANKBATTLES; random(RED_TANKBATTLES); blocks_BLUE_TANKBATTLES; clone_location;;
phase; SMOKE_R1; random(RED_TANKBATTLES); blocks_SMOKE_R1; clone_location;;
phase; SMOKE_R2; random(RED_TANKBATTLES); blocks_SMOKE_R2; clone_location;;
phase; SMOKE_B1; random(BLUE_TANKBATTLES); blocks_SMOKE_B1; clone_location;;
phase; SMOKE_B2; random(BLUE_TANKBATTLES); blocks_SMOKE_B2; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; RED_TANKBATTLES(START_effect); SMOKE_R1(START_effect);
tlink; RED_TANKBATTLES(STOP_effect); SMOKE_R1(STOP_effect);
tlink; RED_TANKBATTLES(START_effect); SMOKE_R2(START_effect);
tlink; RED_TANKBATTLES(STOP_effect); SMOKE_R2(STOP_effect);
tlink; BLUE_TANKBATTLES(STOP_effect); SMOKE_B1(STOP_effect);
tlink; BLUE_TANKBATTLES(START_effect); SMOKE_B1(START_effect);
tlink; BLUE_TANKBATTLES(STOP_effect); SMOKE_B2(STOP_effect);
tlink; BLUE_TANKBATTLES(START_effect); SMOKE_B2(START_effect);

#
## conditions
#
check; RED_TANKBATTLES; location_type(GroundObjective,Tank);
check; RED_TANKBATTLES; coalition(f);
check; RED_TANKBATTLES; in_radius(PRIMARY_LINK_PHASE,200000);
check; BLUE_TANKBATTLES; location_type(GroundObjective,Tank);
check; BLUE_TANKBATTLES; coalition(e);
check; BLUE_TANKBATTLES; range(PRIMARY_LINK_PHASE,closest_outof,40000);
check; SMOKE_R1; location_type(Decoration,CityFire);
check; SMOKE_R1; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMOKE_R1; free();
check; SMOKE_R2; location_type(Decoration,CityFire);
check; SMOKE_R2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMOKE_R2; free();
check; SMOKE_B1; location_type(Decoration,CityFire);
check; SMOKE_B1; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMOKE_B1; free();
check; SMOKE_B2; location_type(Decoration,CityFire);
check; SMOKE_B2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMOKE_B2; free();

#
## property actions
#
action; RED_TANKBATTLES(AT1,Model); set_model(Field cannon,random enemy);
action; RED_TANKBATTLES(AT2,Model); set_model(Field cannon,random enemy);
action; RED_TANKBATTLES(AT3,Model); set_model(Field cannon,random enemy);
action; RED_TANKBATTLES(AT4,Model); set_model(Field cannon,random enemy);
action; RED_TANKBATTLES(AT5,Model); set_model(Field cannon,random enemy);
action; RED_TANKBATTLES(AT6,Model); set_model(Field cannon,random enemy);
action; RED_TANKBATTLES(AT7,Model); set_model(Field cannon,random enemy);
action; RED_TANKBATTLES(RESPAWN,Time); set(Time,2400);
action; RED_TANKBATTLES(Radius,Zone); set(Zone,2500);
action; RED_TANKBATTLES(Tank1,Model); set_model(Tank,random friendly);
action; RED_TANKBATTLES(Tank2,Model); set_model(Tank,random friendly);
action; RED_TANKBATTLES(Tank3,Model); set_model(Tank,random friendly);
action; RED_TANKBATTLES(Tank4,Model); set_model(Tank,random friendly);
action; RED_TANKBATTLES(Tank5,Model); set_model(Tank,random friendly);
action; RED_TANKBATTLES(Tank6,Model); set_model(Tank,random friendly);
action; RED_TANKBATTLES(Tank7,Model); set_model(Tank,random friendly);
action; BLUE_TANKBATTLES(AT1,Model); set_model(Field cannon,random friendly);
action; BLUE_TANKBATTLES(AT2,Model); set_model(Field cannon,random friendly);
action; BLUE_TANKBATTLES(AT3,Model); set_model(Field cannon,random friendly);
action; BLUE_TANKBATTLES(AT4,Model); set_model(Field cannon,random friendly);
action; BLUE_TANKBATTLES(AT5,Model); set_model(Field cannon,random friendly);
action; BLUE_TANKBATTLES(AT6,Model); set_model(Field cannon,random friendly);
action; BLUE_TANKBATTLES(AT7,Model); set_model(Field cannon,random friendly);
action; BLUE_TANKBATTLES(RESPAWN,Time); set(Time,2400);
action; BLUE_TANKBATTLES(Radius,Zone); set(Zone,2500);
action; BLUE_TANKBATTLES(Tank1,Model); set_model(Tank,random enemy);
action; BLUE_TANKBATTLES(Tank2,Model); set_model(Tank,random enemy);
action; BLUE_TANKBATTLES(Tank3,Model); set_model(Tank,random enemy);
action; BLUE_TANKBATTLES(Tank4,Model); set_model(Tank,random enemy);
action; BLUE_TANKBATTLES(Tank5,Model); set_model(Tank,random enemy);
action; BLUE_TANKBATTLES(Tank6,Model); set_model(Tank,random enemy);
action; BLUE_TANKBATTLES(Tank7,Model); set_model(Tank,random enemy);
action; SMOKE_R1(Effect,YOri); set(YOri,$winddirection);
action; SMOKE_R2(Effect,YOri); set(YOri,$winddirection);
action; SMOKE_B1(Effect,YOri); set(YOri,$winddirection);
action; SMOKE_B2(Effect,YOri); set(YOri,$winddirection);

#
## unlinks
#

#
## gui helpers
#
gui_helper; RED_TANKBATTLES; 898; 1334;
gui_helper; BLUE_TANKBATTLES; 202; 1922;
gui_helper; SMOKE_R1; 1324; 1732;
gui_helper; SMOKE_R2; 1339; 1996;
gui_helper; SMOKE_B1; 458; 2277;
gui_helper; SMOKE_B2; 286; 2599;
gui_helper; check; 912; 1514;RED_TANKBATTLES(location_type)
gui_helper; check; 911; 1553;RED_TANKBATTLES(coalition)
gui_helper; check; 910; 1593;RED_TANKBATTLES(in_radius)
gui_helper; check; 224; 2117;BLUE_TANKBATTLES(location_type)
gui_helper; check; 223; 2154;BLUE_TANKBATTLES(coalition)
gui_helper; check; 225; 2197;BLUE_TANKBATTLES(range)
gui_helper; check; 1545; 1751;SMOKE_R1(location_type)
gui_helper; check; 1547; 1793;SMOKE_R1(range)
gui_helper; check; 1548; 1833;SMOKE_R1(free)
gui_helper; check; 1561; 2015;SMOKE_R2(location_type)
gui_helper; check; 1563; 2057;SMOKE_R2(range)
gui_helper; check; 1564; 2097;SMOKE_R2(free)
gui_helper; check; 680; 2296;SMOKE_B1(location_type)
gui_helper; check; 682; 2338;SMOKE_B1(range)
gui_helper; check; 683; 2378;SMOKE_B1(free)
gui_helper; check; 508; 2618;SMOKE_B2(location_type)
gui_helper; check; 510; 2660;SMOKE_B2(range)
gui_helper; check; 511; 2700;SMOKE_B2(free)
gui_helper; Model; 876; 763;RED_TANKBATTLES; (AT1);
gui_helper; Model; 876; 803;RED_TANKBATTLES; (AT2);
gui_helper; Model; 875; 843;RED_TANKBATTLES; (AT3);
gui_helper; Model; 876; 883;RED_TANKBATTLES; (AT4);
gui_helper; Model; 876; 923;RED_TANKBATTLES; (AT5);
gui_helper; Model; 876; 963;RED_TANKBATTLES; (AT6);
gui_helper; Model; 876; 1003;RED_TANKBATTLES; (AT7);
gui_helper; Time; 730; 1185;RED_TANKBATTLES; (RESPAWN);
gui_helper; Zone; 735; 1223;RED_TANKBATTLES; (Radius);
gui_helper; Model; 1016; 1057;RED_TANKBATTLES; (Tank1);
gui_helper; Model; 1016; 1097;RED_TANKBATTLES; (Tank2);
gui_helper; Model; 1016; 1137;RED_TANKBATTLES; (Tank3);
gui_helper; Model; 1016; 1177;RED_TANKBATTLES; (Tank4);
gui_helper; Model; 1016; 1217;RED_TANKBATTLES; (Tank5);
gui_helper; Model; 1016; 1257;RED_TANKBATTLES; (Tank6);
gui_helper; Model; 1016; 1297;RED_TANKBATTLES; (Tank7);
gui_helper; Model; 152; 1347;BLUE_TANKBATTLES; (AT1);
gui_helper; Model; 152; 1387;BLUE_TANKBATTLES; (AT2);
gui_helper; Model; 152; 1427;BLUE_TANKBATTLES; (AT3);
gui_helper; Model; 152; 1467;BLUE_TANKBATTLES; (AT4);
gui_helper; Model; 152; 1507;BLUE_TANKBATTLES; (AT5);
gui_helper; Model; 152; 1547;BLUE_TANKBATTLES; (AT6);
gui_helper; Model; 152; 1587;BLUE_TANKBATTLES; (AT7);
gui_helper; Time; 28; 1819;BLUE_TANKBATTLES; (RESPAWN);
gui_helper; Zone; 28; 1859;BLUE_TANKBATTLES; (Radius);
gui_helper; Model; 318; 1635;BLUE_TANKBATTLES; (Tank1);
gui_helper; Model; 318; 1675;BLUE_TANKBATTLES; (Tank2);
gui_helper; Model; 318; 1715;BLUE_TANKBATTLES; (Tank3);
gui_helper; Model; 318; 1755;BLUE_TANKBATTLES; (Tank4);
gui_helper; Model; 318; 1795;BLUE_TANKBATTLES; (Tank5);
gui_helper; Model; 318; 1835;BLUE_TANKBATTLES; (Tank6);
gui_helper; Model; 318; 1875;BLUE_TANKBATTLES; (Tank7);
gui_helper; YOri; 1396; 1687;SMOKE_R1; (Effect);
gui_helper; YOri; 1412; 1951;SMOKE_R2; (Effect);
gui_helper; YOri; 531; 2232;SMOKE_B1; (Effect);
gui_helper; YOri; 359; 2554;SMOKE_B2; (Effect);
