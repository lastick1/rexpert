# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_GT_WP1; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GT_WP2; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RT_WP1; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RT_WP2; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GER_TRAIN; main(scg\2\blocks_quickmission\ground\train\train_ger_aaa.group);
blocks_set; blocks_RUS_TRAIN; main(scg\2\blocks_quickmission\ground\train\train_rus_aaa.group);

#
## geo params
#
phase; GT_WP1; random(GER_TRAIN); blocks_GT_WP1; clone_location;;
phase; GT_WP2; random(GER_TRAIN); blocks_GT_WP2; clone_location;;
phase; RT_WP1; random(RUS_TRAIN); blocks_RT_WP1; clone_location;;
phase; RT_WP2; random(RUS_TRAIN); blocks_RT_WP2; clone_location;;
phase; GER_TRAIN; random(<EMPTY>); blocks_GER_TRAIN; clone_location;;
phase; RUS_TRAIN; random(<EMPTY>); blocks_RUS_TRAIN; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; GT_WP1(TARGET_TO_WP); GT_WP2(TARGET_TO_WP);
tlink; GT_WP2(TARGET_TO_WP); GT_WP1(TARGET_TO_WP);
tlink; RT_WP1(TARGET_TO_WP); RT_WP2(TARGET_TO_WP);
tlink; RT_WP2(TARGET_TO_WP); RT_WP1(TARGET_TO_WP);
tlink; GER_TRAIN(TARGET_TO_WP); GT_WP1(TARGET_TO_WP);
olink; GT_WP1(OBJECT_WP_TO_VEHICLE); GER_TRAIN(OBJECT_WP_TO_VEHICLE);
olink; GT_WP2(OBJECT_WP_TO_VEHICLE); GER_TRAIN(OBJECT_WP_TO_VEHICLE);
olink; RT_WP2(OBJECT_WP_TO_VEHICLE); RUS_TRAIN(OBJECT_WP_TO_VEHICLE);
olink; RT_WP1(OBJECT_WP_TO_VEHICLE); RUS_TRAIN(OBJECT_WP_TO_VEHICLE);
tlink; RUS_TRAIN(TARGET_TO_WP); RT_WP1(TARGET_TO_WP);

#
## conditions
#
check; GT_WP1; location_type(Decoration,Train);
check; GT_WP1; coalition(e);
check; GT_WP1; range(PRIMARY_LINK_PHASE,closest_outof,10000);
check; GT_WP1; free();
check; GT_WP2; location_type(Decoration,Train);
check; GT_WP2; coalition(e);
check; GT_WP2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; GT_WP2; free();
check; RT_WP1; location_type(Decoration,Train);
check; RT_WP1; coalition(f);
check; RT_WP1; range(PRIMARY_LINK_PHASE,closest_outof,10000);
check; RT_WP1; free();
check; RT_WP2; location_type(Decoration,Train);
check; RT_WP2; coalition(f);
check; RT_WP2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; RT_WP2; free();
check; GER_TRAIN; location_type(Decoration,Train);
check; GER_TRAIN; coalition(e);
check; GER_TRAIN; free();

#
## property actions
#
action; GER_TRAIN(CLOSER,Zone); set(Zone,3000);
action; GER_TRAIN(KILL,Counter); set(Counter,7);
action; GER_TRAIN(RESPAWN,Time); set(Time,600);
action; RUS_TRAIN(CLOSER,Zone); set(Zone,3000);
action; RUS_TRAIN(KILL,Counter); set(Counter,7);
action; RUS_TRAIN(RESPAWN,Time); set(Time,600);

#
## unlinks
#

#
## gui helpers
#
gui_helper; GT_WP1; -2003; 5169;
gui_helper; GT_WP2; -2092; 5584;
gui_helper; RT_WP1; -823; 5212;
gui_helper; RT_WP2; -988; 5603;
gui_helper; GER_TRAIN; -2490; 5019;
gui_helper; RUS_TRAIN; -1336; 4993;
gui_helper; check; -1983; 5352;GT_WP1(location_type)
gui_helper; check; -1981; 5395;GT_WP1(coalition)
gui_helper; check; -1981; 5434;GT_WP1(range)
gui_helper; check; -1978; 5471;GT_WP1(free)
gui_helper; check; -2062; 5761;GT_WP2(location_type)
gui_helper; check; -2062; 5802;GT_WP2(coalition)
gui_helper; check; -2063; 5842;GT_WP2(range)
gui_helper; check; -2066; 5878;GT_WP2(free)
gui_helper; check; -810; 5389;RT_WP1(location_type)
gui_helper; check; -812; 5425;RT_WP1(coalition)
gui_helper; check; -808; 5461;RT_WP1(range)
gui_helper; check; -807; 5504;RT_WP1(free)
gui_helper; check; -958; 5780;RT_WP2(location_type)
gui_helper; check; -960; 5822;RT_WP2(coalition)
gui_helper; check; -960; 5864;RT_WP2(range)
gui_helper; check; -959; 5902;RT_WP2(free)
gui_helper; check; -2468; 5197;GER_TRAIN(location_type)
gui_helper; check; -2468; 5233;GER_TRAIN(coalition)
gui_helper; check; -2467; 5269;GER_TRAIN(free)
gui_helper; Zone; -2404; 4879;GER_TRAIN; (CLOSER);
gui_helper; Counter; -2404; 4919;GER_TRAIN; (KILL);
gui_helper; Time; -2404; 4959;GER_TRAIN; (RESPAWN);
gui_helper; Zone; -1264; 4872;RUS_TRAIN; (CLOSER);
gui_helper; Counter; -1264; 4912;RUS_TRAIN; (KILL);
gui_helper; Time; -1264; 4952;RUS_TRAIN; (RESPAWN);
