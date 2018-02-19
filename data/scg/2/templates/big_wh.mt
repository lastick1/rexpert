# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_RED_BIG_WH_DECORATIONS2; main(scg\1\blocks_quickmission\ground\static\red_big_wh_decorations_v2.group);
blocks_set; blocks_RED_BIG_WH_DECORATIONS1; main(scg\1\blocks_quickmission\ground\static\red_big_wh_decorations_v1.group);
blocks_set; blocks_BLUE_BIGWH_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_rear_warehouse_blue.group);
blocks_set; blocks_BLUE_BIGWH_DECORATIONS_V1; main(scg\1\blocks_quickmission\ground\static\blue_big_wh_decorations_v1.group);
blocks_set; blocks_BLUE_BIGWH_DECORATIONS_V2; main(scg\1\blocks_quickmission\ground\static\blue_big_wh_decorations_v2.group);
blocks_set; blocks_RED_BIGWH_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_rear_warehouse_red.group);
blocks_set; blocks_BLUE_BIGWH_MACHINE_GUN2; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_BLUE_BIGWH_MACHINE_GUN3; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_BLUE_BIGWH_LARGE_CANNON1; main(scg\1\blocks_quickmission\ground\aaa\big\smart_large_cannon_no_spawner.group);
blocks_set; blocks_RED_BIGWH_MACHINE_GUN2; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_RED_BIGWH_MACHINE_GUN3; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_RED_BIGWH_LARGE_CANNON1; main(scg\1\blocks_quickmission\ground\aaa\big\smart_large_cannon_no_spawner.group);
blocks_set; blocks_RED_BIGWH_LARGE_CANNON1_1426; main(scg\1\blocks_quickmission\ground\aaa\big\smart_large_cannon_no_spawner.group);
blocks_set; blocks_BLUE_BIGWH_LARGE_CANNON1_1440; main(scg\1\blocks_quickmission\ground\aaa\big\smart_large_cannon_no_spawner.group);

#
## geo params
#
phase; RED_BIG_WH_DECORATIONS2; at(RED_BIGWH_RECON); blocks_RED_BIG_WH_DECORATIONS2; clone_location;;
phase; RED_BIG_WH_DECORATIONS1; at(RED_BIGWH_RECON); blocks_RED_BIG_WH_DECORATIONS1; clone_location;;
phase; BLUE_BIGWH_RECON; random(<EMPTY>); blocks_BLUE_BIGWH_RECON; clone_location;;
phase; BLUE_BIGWH_DECORATIONS_V1; at(BLUE_BIGWH_RECON); blocks_BLUE_BIGWH_DECORATIONS_V1; clone_location;;
phase; BLUE_BIGWH_DECORATIONS_V2; at(BLUE_BIGWH_RECON); blocks_BLUE_BIGWH_DECORATIONS_V2; clone_location;;
phase; RED_BIGWH_RECON; random(<EMPTY>); blocks_RED_BIGWH_RECON; clone_location;;
phase; BLUE_BIGWH_MACHINE_GUN2; random(BLUE_BIGWH_RECON); blocks_BLUE_BIGWH_MACHINE_GUN2; clone_location;;
phase; BLUE_BIGWH_MACHINE_GUN3; random(BLUE_BIGWH_RECON); blocks_BLUE_BIGWH_MACHINE_GUN3; clone_location;;
phase; BLUE_BIGWH_LARGE_CANNON1; random(BLUE_BIGWH_RECON); blocks_BLUE_BIGWH_LARGE_CANNON1; clone_location;;
phase; RED_BIGWH_MACHINE_GUN2; random(RED_BIGWH_RECON); blocks_RED_BIGWH_MACHINE_GUN2; clone_location;;
phase; RED_BIGWH_MACHINE_GUN3; random(RED_BIGWH_RECON); blocks_RED_BIGWH_MACHINE_GUN3; clone_location;;
phase; RED_BIGWH_LARGE_CANNON1; random(RED_BIGWH_RECON); blocks_RED_BIGWH_LARGE_CANNON1; clone_location;;
phase; RED_BIGWH_LARGE_CANNON1_1426; random(RED_BIGWH_RECON); blocks_RED_BIGWH_LARGE_CANNON1_1426; clone_location;;
phase; BLUE_BIGWH_LARGE_CANNON1_1440; random(BLUE_BIGWH_RECON); blocks_BLUE_BIGWH_LARGE_CANNON1_1440; clone_location;;

#
## cases & switches
#
case; CASE327(RED_BIG_WH_DECORATIONS1);
case; CASE328(RED_BIG_WH_DECORATIONS2);
case; CASE290(BLUE_BIGWH_DECORATIONS_V1);
case; CASE292(BLUE_BIGWH_DECORATIONS_V2);
switch; 1; 0; 0; switch329(CASE327,CASE328);
switch; 1; 0; 0; switch329_288(CASE290,CASE292);

#
## gate links
#
tlink; BLUE_BIGWH_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BIGWH_MACHINE_GUN2(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BIGWH_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BIGWH_MACHINE_GUN2(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BIGWH_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BIGWH_MACHINE_GUN3(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BIGWH_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BIGWH_MACHINE_GUN3(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BIGWH_RECON(ACTIVATE_LARGE_CANNONS); BLUE_BIGWH_LARGE_CANNON1(ACTIVATE_LARGE_CANNONS);
tlink; BLUE_BIGWH_RECON(DEACTIVATE_LARGE_CANNONS); BLUE_BIGWH_LARGE_CANNON1(DEACTIVATE_LARGE_CANNONS);
tlink; RED_BIGWH_RECON(ACTIVATE_MACHINE_GUNS); RED_BIGWH_MACHINE_GUN2(ACTIVATE_MACHINE_GUNS);
tlink; RED_BIGWH_RECON(DEACTIVATE_MACHINE_GUNS); RED_BIGWH_MACHINE_GUN2(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BIGWH_RECON(ACTIVATE_LARGE_CANNONS); RED_BIGWH_LARGE_CANNON1(ACTIVATE_LARGE_CANNONS);
tlink; RED_BIGWH_RECON(DEACTIVATE_LARGE_CANNONS); RED_BIGWH_LARGE_CANNON1(DEACTIVATE_LARGE_CANNONS);
tlink; RED_BIGWH_RECON(ACTIVATE_MACHINE_GUNS); RED_BIGWH_MACHINE_GUN3(ACTIVATE_MACHINE_GUNS);
tlink; RED_BIGWH_RECON(DEACTIVATE_MACHINE_GUNS); RED_BIGWH_MACHINE_GUN3(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BIGWH_RECON(ACTIVATE_LARGE_CANNONS); RED_BIGWH_LARGE_CANNON1_1426(ACTIVATE_LARGE_CANNONS);
tlink; RED_BIGWH_RECON(DEACTIVATE_LARGE_CANNONS); RED_BIGWH_LARGE_CANNON1_1426(DEACTIVATE_LARGE_CANNONS);
tlink; BLUE_BIGWH_RECON(ACTIVATE_LARGE_CANNONS); BLUE_BIGWH_LARGE_CANNON1_1440(ACTIVATE_LARGE_CANNONS);
tlink; BLUE_BIGWH_RECON(DEACTIVATE_LARGE_CANNONS); BLUE_BIGWH_LARGE_CANNON1_1440(DEACTIVATE_LARGE_CANNONS);

#
## conditions
#
check; BLUE_BIGWH_RECON; location_type(GroundObjective,Building);
check; BLUE_BIGWH_RECON; coalition(e);
check; BLUE_BIGWH_RECON; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_BIGWH_RECON; location_type(GroundObjective,Building);
check; RED_BIGWH_RECON; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_BIGWH_RECON; coalition(f);
check; BLUE_BIGWH_MACHINE_GUN2; free();
check; BLUE_BIGWH_MACHINE_GUN2; coalition(e);
check; BLUE_BIGWH_MACHINE_GUN2; location_type(Decoration,AAAPosition);
check; BLUE_BIGWH_MACHINE_GUN2; in_radius(PRIMARY_LINK_PHASE,1500);
check; BLUE_BIGWH_MACHINE_GUN3; free();
check; BLUE_BIGWH_MACHINE_GUN3; coalition(e);
check; BLUE_BIGWH_MACHINE_GUN3; location_type(Decoration,AAAPosition);
check; BLUE_BIGWH_MACHINE_GUN3; in_radius(PRIMARY_LINK_PHASE,1500);
check; BLUE_BIGWH_LARGE_CANNON1; coalition(e);
check; BLUE_BIGWH_LARGE_CANNON1; location_type(Decoration,AAAPosition);
check; BLUE_BIGWH_LARGE_CANNON1; free();
check; BLUE_BIGWH_LARGE_CANNON1; in_radius(PRIMARY_LINK_PHASE,1500);
check; RED_BIGWH_MACHINE_GUN2; free();
check; RED_BIGWH_MACHINE_GUN2; coalition(f);
check; RED_BIGWH_MACHINE_GUN2; location_type(Decoration,AAAPosition);
check; RED_BIGWH_MACHINE_GUN2; in_radius(PRIMARY_LINK_PHASE,1000);
check; RED_BIGWH_MACHINE_GUN3; free();
check; RED_BIGWH_MACHINE_GUN3; coalition(f);
check; RED_BIGWH_MACHINE_GUN3; location_type(Decoration,AAAPosition);
check; RED_BIGWH_MACHINE_GUN3; in_radius(PRIMARY_LINK_PHASE,1000);
check; RED_BIGWH_LARGE_CANNON1; coalition(f);
check; RED_BIGWH_LARGE_CANNON1; location_type(Decoration,AAAPosition);
check; RED_BIGWH_LARGE_CANNON1; free();
check; RED_BIGWH_LARGE_CANNON1; in_radius(PRIMARY_LINK_PHASE,1000);
check; RED_BIGWH_LARGE_CANNON1_1426; coalition(f);
check; RED_BIGWH_LARGE_CANNON1_1426; location_type(Decoration,AAAPosition);
check; RED_BIGWH_LARGE_CANNON1_1426; free();
check; RED_BIGWH_LARGE_CANNON1_1426; in_radius(PRIMARY_LINK_PHASE,1000);
check; BLUE_BIGWH_LARGE_CANNON1_1440; coalition(e);
check; BLUE_BIGWH_LARGE_CANNON1_1440; location_type(Decoration,AAAPosition);
check; BLUE_BIGWH_LARGE_CANNON1_1440; free();
check; BLUE_BIGWH_LARGE_CANNON1_1440; in_radius(PRIMARY_LINK_PHASE,1500);

#
## property actions
#
action; BLUE_BIGWH_MACHINE_GUN2(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Axis:AAA machinegun:mg34-aa);
action; BLUE_BIGWH_MACHINE_GUN2(AAA_SMALL_TYPE,Country); set_country(enemy);
action; BLUE_BIGWH_MACHINE_GUN3(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Axis:AAA machinegun:mg34-aa);
action; BLUE_BIGWH_MACHINE_GUN3(AAA_SMALL_TYPE,Country); set_country(enemy);
action; BLUE_BIGWH_LARGE_CANNON1(AAA_BIG_TYPE,Model); set_model(AAA HVY static cannon,Axis:AAA HVY static cannon:flak37);
action; BLUE_BIGWH_LARGE_CANNON1(AAA_BIG_TYPE,Country); set_country(enemy);
action; RED_BIGWH_MACHINE_GUN2(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Allies:AAA machinegun:Maksim4-AA);
action; RED_BIGWH_MACHINE_GUN2(AAA_SMALL_TYPE,Country); set_country(friendly);
action; RED_BIGWH_MACHINE_GUN3(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Allies:AAA machinegun:Maksim4-AA);
action; RED_BIGWH_MACHINE_GUN3(AAA_SMALL_TYPE,Country); set_country(friendly);
action; RED_BIGWH_LARGE_CANNON1(AAA_BIG_TYPE,Model); set_model(AAA HVY static cannon,Allies:AAA HVY static cannon:52K);
action; RED_BIGWH_LARGE_CANNON1(AAA_BIG_TYPE,Country); set_country(friendly);
action; BLUE_BIGWH_RECON(ATTACK_AREA_RADIUS,AttackArea); <empty>();
action; BLUE_BIGWH_RECON(AUTO_CANNONS_TIME,Time); <empty>();
action; BLUE_BIGWH_RECON(Inner Zone,Zone); set(Zone,5500);
action; BLUE_BIGWH_RECON(MACHINE_GUNS_TIME,Time); <empty>();
action; BLUE_BIGWH_RECON(Outer Zone,Zone); set(Zone,6500);
action; RED_BIGWH_RECON(ATTACK_AREA_RADIUS,AttackArea); <empty>();
action; RED_BIGWH_RECON(AUTO_CANNONS_TIME,Time); <empty>();
action; RED_BIGWH_RECON(Inner Zone,Zone); <empty>();
action; RED_BIGWH_RECON(MACHINE_GUNS_TIME,Time); <empty>();
action; RED_BIGWH_RECON(Outer Zone,Zone); <empty>();
action; RED_BIGWH_LARGE_CANNON1_1426(AAA_BIG_TYPE,Model); set_model(AAA HVY static cannon,Allies:AAA HVY static cannon:52K);
action; RED_BIGWH_LARGE_CANNON1_1426(AAA_BIG_TYPE,Country); set_country(friendly);
action; BLUE_BIGWH_LARGE_CANNON1_1440(AAA_BIG_TYPE,Model); set_model(AAA HVY static cannon,Axis:AAA HVY static cannon:flak37);
action; BLUE_BIGWH_LARGE_CANNON1_1440(AAA_BIG_TYPE,Country); set_country(enemy);

#
## unlinks
#

#
## gui helpers
#
gui_helper; RED_BIG_WH_DECORATIONS2; 4054; -63;
gui_helper; RED_BIG_WH_DECORATIONS1; 4033; -271;
gui_helper; BLUE_BIGWH_RECON; 852; 55;
gui_helper; BLUE_BIGWH_DECORATIONS_V1; 521; -185;
gui_helper; BLUE_BIGWH_DECORATIONS_V2; 521; 21;
gui_helper; RED_BIGWH_RECON; 4318; 50;
gui_helper; BLUE_BIGWH_MACHINE_GUN2; 1442; -104;
gui_helper; BLUE_BIGWH_MACHINE_GUN3; 1449; 557;
gui_helper; BLUE_BIGWH_LARGE_CANNON1; 1442; 216;
gui_helper; RED_BIGWH_MACHINE_GUN2; 4874; -115;
gui_helper; RED_BIGWH_MACHINE_GUN3; 4867; 208;
gui_helper; RED_BIGWH_LARGE_CANNON1; 4866; 510;
gui_helper; RED_BIGWH_LARGE_CANNON1_1426; 4848; -446;
gui_helper; BLUE_BIGWH_LARGE_CANNON1_1440; 1432; -457;
gui_helper; CASE327; 3928; -218;
gui_helper; CASE328; 3921; 2;
gui_helper; CASE290; 450; -144;
gui_helper; CASE292; 464; 88;
gui_helper; switch329; 3924; -105;
gui_helper; switch329_288; 424; -23;
gui_helper; check; 1059; -133;BLUE_BIGWH_RECON(location_type)
gui_helper; check; 1059; -100;BLUE_BIGWH_RECON(coalition)
gui_helper; check; 1060; -67;BLUE_BIGWH_RECON(in_radius)
gui_helper; check; 4565; -144;RED_BIGWH_RECON(location_type)
gui_helper; check; 4567; -80;RED_BIGWH_RECON(in_radius)
gui_helper; check; 4566; -113;RED_BIGWH_RECON(coalition)
gui_helper; check; 1626; -167;BLUE_BIGWH_MACHINE_GUN2(free)
gui_helper; check; 1626; -200;BLUE_BIGWH_MACHINE_GUN2(coalition)
gui_helper; check; 1627; -234;BLUE_BIGWH_MACHINE_GUN2(location_type)
gui_helper; check; 1628; -133;BLUE_BIGWH_MACHINE_GUN2(in_radius)
gui_helper; check; 1633; 494;BLUE_BIGWH_MACHINE_GUN3(free)
gui_helper; check; 1633; 461;BLUE_BIGWH_MACHINE_GUN3(coalition)
gui_helper; check; 1634; 427;BLUE_BIGWH_MACHINE_GUN3(location_type)
gui_helper; check; 1635; 528;BLUE_BIGWH_MACHINE_GUN3(in_radius)
gui_helper; check; 1630; 136;BLUE_BIGWH_LARGE_CANNON1(coalition)
gui_helper; check; 1630; 102;BLUE_BIGWH_LARGE_CANNON1(location_type)
gui_helper; check; 1631; 166;BLUE_BIGWH_LARGE_CANNON1(free)
gui_helper; check; 1631; 195;BLUE_BIGWH_LARGE_CANNON1(in_radius)
gui_helper; check; 5057; -178;RED_BIGWH_MACHINE_GUN2(free)
gui_helper; check; 5057; -211;RED_BIGWH_MACHINE_GUN2(coalition)
gui_helper; check; 5058; -245;RED_BIGWH_MACHINE_GUN2(location_type)
gui_helper; check; 5059; -144;RED_BIGWH_MACHINE_GUN2(in_radius)
gui_helper; check; 5051; 145;RED_BIGWH_MACHINE_GUN3(free)
gui_helper; check; 5051; 112;RED_BIGWH_MACHINE_GUN3(coalition)
gui_helper; check; 5052; 78;RED_BIGWH_MACHINE_GUN3(location_type)
gui_helper; check; 5053; 179;RED_BIGWH_MACHINE_GUN3(in_radius)
gui_helper; check; 5054; 430;RED_BIGWH_LARGE_CANNON1(coalition)
gui_helper; check; 5054; 400;RED_BIGWH_LARGE_CANNON1(location_type)
gui_helper; check; 5055; 460;RED_BIGWH_LARGE_CANNON1(free)
gui_helper; check; 5055; 489;RED_BIGWH_LARGE_CANNON1(in_radius)
gui_helper; check; 5036; -526;RED_BIGWH_LARGE_CANNON1_1426(coalition)
gui_helper; check; 5036; -556;RED_BIGWH_LARGE_CANNON1_1426(location_type)
gui_helper; check; 5037; -496;RED_BIGWH_LARGE_CANNON1_1426(free)
gui_helper; check; 5037; -467;RED_BIGWH_LARGE_CANNON1_1426(in_radius)
gui_helper; check; 1620; -537;BLUE_BIGWH_LARGE_CANNON1_1440(coalition)
gui_helper; check; 1620; -571;BLUE_BIGWH_LARGE_CANNON1_1440(location_type)
gui_helper; check; 1621; -507;BLUE_BIGWH_LARGE_CANNON1_1440(free)
gui_helper; check; 1621; -478;BLUE_BIGWH_LARGE_CANNON1_1440(in_radius)
gui_helper; Model; 1502; -204;BLUE_BIGWH_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Country; 1502; -163;BLUE_BIGWH_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Model; 1509; 457;BLUE_BIGWH_MACHINE_GUN3; (AAA_SMALL_TYPE);
gui_helper; Country; 1509; 497;BLUE_BIGWH_MACHINE_GUN3; (AAA_SMALL_TYPE);
gui_helper; Model; 1518; 138;BLUE_BIGWH_LARGE_CANNON1; (AAA_BIG_TYPE);
gui_helper; Country; 1518; 178;BLUE_BIGWH_LARGE_CANNON1; (AAA_BIG_TYPE);
gui_helper; Model; 4933; -215;RED_BIGWH_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Country; 4933; -175;RED_BIGWH_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Model; 4927; 108;RED_BIGWH_MACHINE_GUN3; (AAA_SMALL_TYPE);
gui_helper; Country; 4927; 148;RED_BIGWH_MACHINE_GUN3; (AAA_SMALL_TYPE);
gui_helper; Model; 4942; 432;RED_BIGWH_LARGE_CANNON1; (AAA_BIG_TYPE);
gui_helper; Country; 4942; 472;RED_BIGWH_LARGE_CANNON1; (AAA_BIG_TYPE);
gui_helper; AttackArea; 932; -70;BLUE_BIGWH_RECON; (ATTACK_AREA_RADIUS);
gui_helper; Time; 932; -30;BLUE_BIGWH_RECON; (AUTO_CANNONS_TIME);
gui_helper; Zone; 1113; -20;BLUE_BIGWH_RECON; (Inner Zone);
gui_helper; Time; 932; 10;BLUE_BIGWH_RECON; (MACHINE_GUNS_TIME);
gui_helper; Zone; 1113; 13;BLUE_BIGWH_RECON; (Outer Zone);
gui_helper; AttackArea; 4399; -65;RED_BIGWH_RECON; (ATTACK_AREA_RADIUS);
gui_helper; Time; 4399; -25;RED_BIGWH_RECON; (AUTO_CANNONS_TIME);
gui_helper; Zone; 4581; -20;RED_BIGWH_RECON; (Inner Zone);
gui_helper; Time; 4401; 16;RED_BIGWH_RECON; (MACHINE_GUNS_TIME);
gui_helper; Zone; 4581; 14;RED_BIGWH_RECON; (Outer Zone);
gui_helper; Model; 4924; -524;RED_BIGWH_LARGE_CANNON1_1426; (AAA_BIG_TYPE);
gui_helper; Country; 4924; -484;RED_BIGWH_LARGE_CANNON1_1426; (AAA_BIG_TYPE);
gui_helper; Model; 1508; -535;BLUE_BIGWH_LARGE_CANNON1_1440; (AAA_BIG_TYPE);
gui_helper; Country; 1508; -495;BLUE_BIGWH_LARGE_CANNON1_1440; (AAA_BIG_TYPE);
