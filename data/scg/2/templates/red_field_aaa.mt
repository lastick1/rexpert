# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_RED_DEFENCE_AF_1; main(scg\2\blocks_quickmission\airfields_red\!x100505z156297.group);
blocks_set; blocks_RED_SMART_CHECKZONE; main(scg\2\blocks_quickmission\smart_red_checkzone.group);
blocks_set; blocks_LARGE_CANNON; main(scg\2\blocks_quickmission\ground\aaa\big\smart_large_cannon.group);
blocks_set; blocks_MEDIUM_CANNON; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON2; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON3; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON4; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON5; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON6; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_SMALL_CANNON; main(scg\2\blocks_quickmission\ground\aaa\small\smart_machine_gun.group);
blocks_set; blocks_SMALL_CANNON2; main(scg\2\blocks_quickmission\ground\aaa\small\smart_machine_gun.group);
blocks_set; blocks_MEDIUM_CANNON_504; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON2_505; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON4_516; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);

#
## geo params
#
phase; RED_DEFENCE_AF_1; random(<EMPTY>); blocks_RED_DEFENCE_AF_1; clone_location;scg\2\blocks_quickmission\airfields_red;
phase; RED_SMART_CHECKZONE; at(RED_DEFENCE_AF_1); blocks_RED_SMART_CHECKZONE; clone_location;;
phase; LARGE_CANNON; random(RED_SMART_CHECKZONE); blocks_LARGE_CANNON; clone_location;;
phase; MEDIUM_CANNON; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON; clone_location;;
phase; MEDIUM_CANNON2; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON2; clone_location;;
phase; MEDIUM_CANNON3; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON3; clone_location;;
phase; MEDIUM_CANNON4; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON4; clone_location;;
phase; MEDIUM_CANNON5; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON5; clone_location;;
phase; MEDIUM_CANNON6; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON6; clone_location;;
phase; SMALL_CANNON; random(RED_SMART_CHECKZONE); blocks_SMALL_CANNON; clone_location;;
phase; SMALL_CANNON2; random(RED_SMART_CHECKZONE); blocks_SMALL_CANNON2; clone_location;;
phase; MEDIUM_CANNON_504; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON_504; clone_location;;
phase; MEDIUM_CANNON2_505; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON2_505; clone_location;;
phase; MEDIUM_CANNON4_516; random(RED_SMART_CHECKZONE); blocks_MEDIUM_CANNON4_516; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; RED_DEFENCE_AF_1(AAA_OFF); RED_SMART_CHECKZONE(AAA_OFF);
tlink; RED_DEFENCE_AF_1(AAA_ON); RED_SMART_CHECKZONE(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); SMALL_CANNON2(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); SMALL_CANNON(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON6(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON5(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON4(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON3(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON2(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); LARGE_CANNON(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON_504(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON2_505(AAA_ON);
tlink; RED_DEFENCE_AF_1(AAA_ON); MEDIUM_CANNON4_516(AAA_ON);
tlink; RED_SMART_CHECKZONE(ACTIVATE_LARGE_CANNONS); LARGE_CANNON(ACTIVATE_LARGE_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_LARGE_CANNONS); LARGE_CANNON(DEACTIVATE_LARGE_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON3(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON3(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON4(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON4(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON5(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON5(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON6(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON6(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_MACHINE_GUNS); SMALL_CANNON(ACTIVATE_MACHINE_GUNS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_MACHINE_GUNS); SMALL_CANNON(DEACTIVATE_MACHINE_GUNS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_MACHINE_GUNS); SMALL_CANNON2(ACTIVATE_MACHINE_GUNS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_MACHINE_GUNS); SMALL_CANNON2(DEACTIVATE_MACHINE_GUNS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON_504(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON_504(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2_505(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2_505(DEACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON4_516(ACTIVATE_AUTO_CANNONS);
tlink; RED_SMART_CHECKZONE(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON4_516(DEACTIVATE_AUTO_CANNONS);

#
## conditions
#
check; RED_DEFENCE_AF_1; coalition(f);
check; RED_DEFENCE_AF_1; free();
check; RED_DEFENCE_AF_1; location_type(Decoration,Parking);
check; RED_DEFENCE_AF_1; range(PRIMARY_LINK_PHASE,closest_outof,40000);
check; LARGE_CANNON; location_type(Decoration,AAAPosition);
check; LARGE_CANNON; free();
check; LARGE_CANNON; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON; free();
check; MEDIUM_CANNON2; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON2; free();
check; MEDIUM_CANNON3; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON3; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON3; free();
check; MEDIUM_CANNON4; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON4; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON4; free();
check; MEDIUM_CANNON5; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON5; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON5; free();
check; MEDIUM_CANNON6; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON6; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON6; free();
check; SMALL_CANNON; location_type(Decoration,AAAPosition);
check; SMALL_CANNON; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMALL_CANNON; free();
check; SMALL_CANNON2; location_type(Decoration,AAAPosition);
check; SMALL_CANNON2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMALL_CANNON2; free();
check; MEDIUM_CANNON_504; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON_504; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON_504; free();
check; MEDIUM_CANNON2_505; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON2_505; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON2_505; free();
check; MEDIUM_CANNON4_516; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON4_516; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON4_516; free();

#
## property actions
#
action; RED_DEFENCE_AF_1(Repair,Time); set(Time,2400);
action; RED_SMART_CHECKZONE(AUTO_CANNONS,Time); <empty>();
action; RED_SMART_CHECKZONE(Inner Zone,Zone); set(Zone,8000);
action; RED_SMART_CHECKZONE(MACHINE_GUNS,Time); <empty>();
action; RED_SMART_CHECKZONE(Outer Zone,Zone); set(Zone,9000);
action; LARGE_CANNON(AAA_BIG_TYPE,Model); set_model(AAA HVY static cannon,Allies:AAA HVY static cannon:52K);
action; LARGE_CANNON(AAA_BIG_TYPE,Country); set_country(friendly);
action; LARGE_CANNON(AAA_BIG_TYPE,AILevel); set(AILevel,3);
action; MEDIUM_CANNON(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON(AAA_MED_TYPE,Country); set_country(friendly);
action; MEDIUM_CANNON2(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON2(AAA_MED_TYPE,Country); set_country(friendly);
action; MEDIUM_CANNON3(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON3(AAA_MED_TYPE,Country); set_country(friendly);
action; MEDIUM_CANNON4(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON4(AAA_MED_TYPE,Country); set_country(friendly);
action; MEDIUM_CANNON5(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON5(AAA_MED_TYPE,Country); set_country(friendly);
action; MEDIUM_CANNON6(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON6(AAA_MED_TYPE,Country); set_country(friendly);
action; SMALL_CANNON(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Allies:AAA machinegun:Maksim4-AA);
action; SMALL_CANNON(AAA_SMALL_TYPE,Country); set_country(friendly);
action; SMALL_CANNON(AAA_SMALL_TYPE,AILevel); set(AILevel,3);
action; SMALL_CANNON2(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Allies:AAA machinegun:Maksim4-AA);
action; SMALL_CANNON2(AAA_SMALL_TYPE,Country); set_country(friendly);
action; SMALL_CANNON2(AAA_SMALL_TYPE,AILevel); set(AILevel,3);
action; MEDIUM_CANNON_504(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON_504(AAA_MED_TYPE,Country); set_country(friendly);
action; MEDIUM_CANNON2_505(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON2_505(AAA_MED_TYPE,Country); set_country(friendly);
action; MEDIUM_CANNON4_516(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random friendly);
action; MEDIUM_CANNON4_516(AAA_MED_TYPE,Country); set_country(friendly);

#
## unlinks
#

#
## gui helpers
#
gui_helper; RED_DEFENCE_AF_1; 9274; -3918;
gui_helper; RED_SMART_CHECKZONE; 9901; -4374;
gui_helper; LARGE_CANNON; 8889; -6638;
gui_helper; MEDIUM_CANNON; 8891; -6223;
gui_helper; MEDIUM_CANNON2; 9272; -6632;
gui_helper; MEDIUM_CANNON3; 8910; -5395;
gui_helper; MEDIUM_CANNON4; 8904; -4990;
gui_helper; MEDIUM_CANNON5; 8877; -4537;
gui_helper; MEDIUM_CANNON6; 9320; -5410;
gui_helper; SMALL_CANNON; 9321; -4536;
gui_helper; SMALL_CANNON2; 9316; -4958;
gui_helper; MEDIUM_CANNON_504; 8888; -5812;
gui_helper; MEDIUM_CANNON2_505; 9283; -6225;
gui_helper; MEDIUM_CANNON4_516; 9291; -5803;
gui_helper; check; 9331; -3945;RED_DEFENCE_AF_1(coalition)
gui_helper; check; 9416; -3730;RED_DEFENCE_AF_1(free)
gui_helper; check; 9414; -3942;RED_DEFENCE_AF_1(location_type)
gui_helper; check; 9316; -3733;RED_DEFENCE_AF_1(range)
gui_helper; check; 8910; -6464;LARGE_CANNON(location_type)
gui_helper; check; 8910; -6415;LARGE_CANNON(free)
gui_helper; check; 8910; -6378;LARGE_CANNON(range)
gui_helper; check; 8911; -6047;MEDIUM_CANNON(location_type)
gui_helper; check; 8912; -6003;MEDIUM_CANNON(range)
gui_helper; check; 8913; -5968;MEDIUM_CANNON(free)
gui_helper; check; 9292; -6456;MEDIUM_CANNON2(location_type)
gui_helper; check; 9291; -6418;MEDIUM_CANNON2(range)
gui_helper; check; 9292; -6383;MEDIUM_CANNON2(free)
gui_helper; check; 8930; -5219;MEDIUM_CANNON3(location_type)
gui_helper; check; 8926; -5177;MEDIUM_CANNON3(range)
gui_helper; check; 8927; -5142;MEDIUM_CANNON3(free)
gui_helper; check; 8924; -4814;MEDIUM_CANNON4(location_type)
gui_helper; check; 8924; -4775;MEDIUM_CANNON4(range)
gui_helper; check; 8925; -4740;MEDIUM_CANNON4(free)
gui_helper; check; 8897; -4361;MEDIUM_CANNON5(location_type)
gui_helper; check; 8897; -4323;MEDIUM_CANNON5(range)
gui_helper; check; 8898; -4288;MEDIUM_CANNON5(free)
gui_helper; check; 9340; -5234;MEDIUM_CANNON6(location_type)
gui_helper; check; 9340; -5199;MEDIUM_CANNON6(range)
gui_helper; check; 9341; -5164;MEDIUM_CANNON6(free)
gui_helper; check; 9348; -4365;SMALL_CANNON(location_type)
gui_helper; check; 9349; -4328;SMALL_CANNON(range)
gui_helper; check; 9348; -4294;SMALL_CANNON(free)
gui_helper; check; 9343; -4789;SMALL_CANNON2(location_type)
gui_helper; check; 9344; -4751;SMALL_CANNON2(range)
gui_helper; check; 9343; -4717;SMALL_CANNON2(free)
gui_helper; check; 8908; -5636;MEDIUM_CANNON_504(location_type)
gui_helper; check; 8909; -5592;MEDIUM_CANNON_504(range)
gui_helper; check; 8910; -5557;MEDIUM_CANNON_504(free)
gui_helper; check; 9303; -6049;MEDIUM_CANNON2_505(location_type)
gui_helper; check; 9302; -6011;MEDIUM_CANNON2_505(range)
gui_helper; check; 9303; -5976;MEDIUM_CANNON2_505(free)
gui_helper; check; 9311; -5627;MEDIUM_CANNON4_516(location_type)
gui_helper; check; 9311; -5588;MEDIUM_CANNON4_516(range)
gui_helper; check; 9312; -5553;MEDIUM_CANNON4_516(free)
gui_helper; Time; 9350; -3997;RED_DEFENCE_AF_1; (Repair);
gui_helper; Time; 9976; -4515;RED_SMART_CHECKZONE; (AUTO_CANNONS);
gui_helper; Zone; 9974; -4443;RED_SMART_CHECKZONE; (Inner Zone);
gui_helper; Time; 9975; -4480;RED_SMART_CHECKZONE; (MACHINE_GUNS);
gui_helper; Zone; 9975; -4404;RED_SMART_CHECKZONE; (Outer Zone);
gui_helper; Model; 8967; -6705;LARGE_CANNON; (AAA_BIG_TYPE);
gui_helper; Country; 8967; -6665;LARGE_CANNON; (AAA_BIG_TYPE);
gui_helper; AILevel; 8969; -6745;LARGE_CANNON; (AAA_BIG_TYPE);
gui_helper; Model; 8969; -6290;MEDIUM_CANNON; (AAA_MED_TYPE);
gui_helper; Country; 8969; -6250;MEDIUM_CANNON; (AAA_MED_TYPE);
gui_helper; Model; 9350; -6699;MEDIUM_CANNON2; (AAA_MED_TYPE);
gui_helper; Country; 9350; -6659;MEDIUM_CANNON2; (AAA_MED_TYPE);
gui_helper; Model; 8988; -5462;MEDIUM_CANNON3; (AAA_MED_TYPE);
gui_helper; Country; 8988; -5422;MEDIUM_CANNON3; (AAA_MED_TYPE);
gui_helper; Model; 8982; -5057;MEDIUM_CANNON4; (AAA_MED_TYPE);
gui_helper; Country; 8982; -5017;MEDIUM_CANNON4; (AAA_MED_TYPE);
gui_helper; Model; 8955; -4604;MEDIUM_CANNON5; (AAA_MED_TYPE);
gui_helper; Country; 8955; -4564;MEDIUM_CANNON5; (AAA_MED_TYPE);
gui_helper; Model; 9398; -5477;MEDIUM_CANNON6; (AAA_MED_TYPE);
gui_helper; Country; 9398; -5437;MEDIUM_CANNON6; (AAA_MED_TYPE);
gui_helper; Model; 9397; -4601;SMALL_CANNON; (AAA_SMALL_TYPE);
gui_helper; Country; 9397; -4561;SMALL_CANNON; (AAA_SMALL_TYPE);
gui_helper; AILevel; 9390; -4639;SMALL_CANNON; (AAA_SMALL_TYPE);
gui_helper; Model; 9392; -5025;SMALL_CANNON2; (AAA_SMALL_TYPE);
gui_helper; Country; 9392; -4985;SMALL_CANNON2; (AAA_SMALL_TYPE);
gui_helper; AILevel; 9394; -5062;SMALL_CANNON2; (AAA_SMALL_TYPE);
gui_helper; Model; 8966; -5879;MEDIUM_CANNON_504; (AAA_MED_TYPE);
gui_helper; Country; 8966; -5839;MEDIUM_CANNON_504; (AAA_MED_TYPE);
gui_helper; Model; 9361; -6292;MEDIUM_CANNON2_505; (AAA_MED_TYPE);
gui_helper; Country; 9361; -6252;MEDIUM_CANNON2_505; (AAA_MED_TYPE);
gui_helper; Model; 9369; -5870;MEDIUM_CANNON4_516; (AAA_MED_TYPE);
gui_helper; Country; 9369; -5830;MEDIUM_CANNON4_516; (AAA_MED_TYPE);
