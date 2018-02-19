# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_GER-NODE-1; main(scg\2\blocks_quickmission\node_point.group);
blocks_set; blocks_RUS-NODE-1; main(scg\2\blocks_quickmission\node_point.group);
blocks_set; blocks_WINDSOCK_357; main(scg\2\blocks_quickmission\windsock.group);
blocks_set; blocks_GER-PARKING-1; main(scg\2\blocks_quickmission\ground\blue_field.group);
blocks_set; blocks_RUS-PARKING-1; main(scg\2\blocks_quickmission\ground\red_field.group);
blocks_set; blocks_WINDSOCK_331_384; main(scg\2\blocks_quickmission\windsock.group);
blocks_set; blocks_RUS-1-TRANSPORT-1; main(scg\2\blocks_quickmission\ground\vehicle\vehicle_6rus_6km_no_recon.group);
blocks_set; blocks_RUS-1-TRANSPORT-1-WP-1; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RUS-1-TRANSPORT-1-WP-2; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GER-1-TRANSPORT-1; main(scg\2\blocks_quickmission\ground\vehicle\vehicle_6ger_6km_no_recon.group);
blocks_set; blocks_GER-1-TRANSPORT-1-WP-1; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GER-1-TRANSPORT-1-WP-2; main(scg\2\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_FRONTLINE; main(scg\2\blocks_quickmission\icons\fl_icon.group);
blocks_set; blocks_REF; main(scg\2\blocks_quickmission\ref_point.group);
blocks_set; blocks_RUS-AT-ARTY-1; main(scg\2\blocks_quickmission\ground\arty\at_arty_russia_e13.group);
blocks_set; blocks_RUS-AT-ARTY-2; main(scg\2\blocks_quickmission\ground\arty\at_arty_russia_e13.group);
blocks_set; blocks_RUS-DEPOT-1-LONG; main(scg\2\blocks_quickmission\ground\static\red_depot_long.group);
blocks_set; blocks_RUS-DEPOT-1-SQUARE; main(scg\2\blocks_quickmission\ground\static\red_depot_square.group);
blocks_set; blocks_RUS-DEPOT-1-REF; main(scg\2\blocks_quickmission\ref_point.group);
blocks_set; blocks_RUS-DEPOT-1-CONTROL; main(scg\2\blocks_quickmission\ground\static\red_depot_control.group);
blocks_set; blocks_PHASE_95; main(scg\2\blocks_quickmission\inputs\red_front_warehouse1.group);
blocks_set; blocks_GER-DEPOT-1-LONG; main(scg\2\blocks_quickmission\ground\static\blue_depot_long.group);
blocks_set; blocks_GER-DEPOT-1-SQUARE; main(scg\2\blocks_quickmission\ground\static\blue_depot_square.group);
blocks_set; blocks_GER-DEPOT-1-REF; main(scg\2\blocks_quickmission\ref_point.group);
blocks_set; blocks_GER-DEPOT-1-CONTROL; main(scg\2\blocks_quickmission\ground\static\blue_depot_control.group);
blocks_set; blocks_PHASE_94; main(scg\2\blocks_quickmission\inputs\blue_front_warehouse1.group);
blocks_set; blocks_GER-AT-ARTY-1; main(scg\2\blocks_quickmission\ground\arty\at_arty_germany_e13.group);
blocks_set; blocks_GER-AT-ARTY-2; main(scg\2\blocks_quickmission\ground\arty\at_arty_germany_e13.group);

#
## geo params
#
phase; GER-NODE-1; random(REF); blocks_GER-NODE-1; clone_location;;
phase; RUS-NODE-1; random(REF); blocks_RUS-NODE-1; clone_location;;
phase; WINDSOCK_357; random(GER-PARKING-1); blocks_WINDSOCK_357; clone_location;;
phase; GER-PARKING-1; random(RUS-NODE-1); blocks_GER-PARKING-1; clone_location;;
phase; RUS-PARKING-1; random(GER-NODE-1); blocks_RUS-PARKING-1; clone_location;;
phase; WINDSOCK_331_384; random(RUS-PARKING-1); blocks_WINDSOCK_331_384; clone_location;;
phase; RUS-1-TRANSPORT-1; random(RUS-NODE-1); blocks_RUS-1-TRANSPORT-1; clone_location;;
phase; RUS-1-TRANSPORT-1-WP-1; random(RUS-1-TRANSPORT-1); blocks_RUS-1-TRANSPORT-1-WP-1; clone_location;;
phase; RUS-1-TRANSPORT-1-WP-2; at(RUS-1-TRANSPORT-1); blocks_RUS-1-TRANSPORT-1-WP-2; clone_location;;
phase; GER-1-TRANSPORT-1; random(GER-NODE-1); blocks_GER-1-TRANSPORT-1; clone_location;;
phase; GER-1-TRANSPORT-1-WP-1; random(GER-1-TRANSPORT-1); blocks_GER-1-TRANSPORT-1-WP-1; clone_location;;
phase; GER-1-TRANSPORT-1-WP-2; at(GER-1-TRANSPORT-1); blocks_GER-1-TRANSPORT-1-WP-2; clone_location;;
phase; FRONTLINE; at(REF); blocks_FRONTLINE; clone_location;;
phase; REF; server_setpos(); blocks_REF; ;;
phase; RUS-AT-ARTY-1; random(RUS-NODE-1); blocks_RUS-AT-ARTY-1; clone_location;;
phase; RUS-AT-ARTY-2; random(RUS-NODE-1); blocks_RUS-AT-ARTY-2; clone_location;;
phase; RUS-DEPOT-1-LONG; at(RUS-DEPOT-1-REF); blocks_RUS-DEPOT-1-LONG; clone_location;;
phase; RUS-DEPOT-1-SQUARE; at(RUS-DEPOT-1-REF); blocks_RUS-DEPOT-1-SQUARE; clone_location;;
phase; RUS-DEPOT-1-REF; random(RUS-NODE-1); blocks_RUS-DEPOT-1-REF; clone_location;;
phase; RUS-DEPOT-1-CONTROL; at(RUS-DEPOT-1-REF); blocks_RUS-DEPOT-1-CONTROL; clone_location;;
phase; PHASE_95; at(RUS-DEPOT-1-REF); blocks_PHASE_95; clone_location;;
phase; GER-DEPOT-1-LONG; at(GER-DEPOT-1-REF); blocks_GER-DEPOT-1-LONG; clone_location;;
phase; GER-DEPOT-1-SQUARE; at(GER-DEPOT-1-REF); blocks_GER-DEPOT-1-SQUARE; clone_location;;
phase; GER-DEPOT-1-REF; random(GER-NODE-1); blocks_GER-DEPOT-1-REF; clone_location;;
phase; GER-DEPOT-1-CONTROL; at(GER-DEPOT-1-REF); blocks_GER-DEPOT-1-CONTROL; clone_location;;
phase; PHASE_94; at(GER-DEPOT-1-REF); blocks_PHASE_94; clone_location;;
phase; GER-AT-ARTY-1; random(GER-NODE-1); blocks_GER-AT-ARTY-1; clone_location;;
phase; GER-AT-ARTY-2; random(GER-NODE-1); blocks_GER-AT-ARTY-2; clone_location;;

#
## cases & switches
#
case; CASE64(RUS-DEPOT-1-LONG);
case; CASE65(RUS-DEPOT-1-SQUARE);
case; CASE50(GER-DEPOT-1-LONG);
case; CASE51(GER-DEPOT-1-SQUARE);
switch; 1; 0; 0; switch66(CASE64,CASE65);
switch; 1; 0; 0; switch52(CASE50,CASE51);

#
## gate links
#
tlink; RUS-1-TRANSPORT-1(TARGET_TO_WP); RUS-1-TRANSPORT-1-WP-1(TARGET_TO_WP);
olink; RUS-1-TRANSPORT-1-WP-1(OBJECT_WP_TO_VEHICLE); RUS-1-TRANSPORT-1(OBJECT_WP_TO_VEHICLE);
tlink; RUS-1-TRANSPORT-1-WP-1(TARGET_TO_WP); RUS-1-TRANSPORT-1-WP-2(TARGET_TO_WP);
olink; RUS-1-TRANSPORT-1-WP-2(OBJECT_WP_TO_VEHICLE); RUS-1-TRANSPORT-1(OBJECT_WP_TO_VEHICLE);
tlink; GER-1-TRANSPORT-1(TARGET_TO_WP); GER-1-TRANSPORT-1-WP-1(TARGET_TO_WP);
tlink; GER-1-TRANSPORT-1-WP-1(TARGET_TO_WP); GER-1-TRANSPORT-1-WP-2(TARGET_TO_WP);
olink; GER-1-TRANSPORT-1-WP-1(OBJECT_WP_TO_VEHICLE); GER-1-TRANSPORT-1(OBJECT_WP_TO_VEHICLE);
olink; GER-1-TRANSPORT-1-WP-2(OBJECT_WP_TO_VEHICLE); GER-1-TRANSPORT-1(OBJECT_WP_TO_VEHICLE);
tlink; RUS-AT-ARTY-1(KILLED_EVENT); RUS-NODE-1(KILLED_EVENT);
tlink; RUS-AT-ARTY-2(KILLED_EVENT); RUS-NODE-1(KILLED_EVENT);
tlink; PHASE_95(SERVER_INPUT); RUS-DEPOT-1-CONTROL(SERVER_INPUT);
tlink; PHASE_94(SERVER_INPUT); GER-DEPOT-1-CONTROL(SERVER_INPUT);
tlink; GER-AT-ARTY-1(KILLED_EVENT); GER-NODE-1(KILLED_EVENT);
tlink; GER-AT-ARTY-2(KILLED_EVENT); GER-NODE-1(KILLED_EVENT);

#
## conditions
#
check; GER-NODE-1; free();
check; GER-NODE-1; coalition(e);
check; GER-NODE-1; location_type(AirObjective,Balloon);
check; RUS-NODE-1; coalition(f);
check; RUS-NODE-1; location_type(AirObjective,Balloon);
check; RUS-NODE-1; free();
check; WINDSOCK_357; location_type(Decoration,Windsock);
check; WINDSOCK_357; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; WINDSOCK_357; free();
check; GER-PARKING-1; location_type(Decoration,Parking);
check; GER-PARKING-1; coalition(f);
check; GER-PARKING-1; in_radius(PRIMARY_LINK_PHASE,15000);
check; RUS-PARKING-1; location_type(Decoration,Parking);
check; RUS-PARKING-1; coalition(e);
check; RUS-PARKING-1; in_radius(PRIMARY_LINK_PHASE,15000);
check; WINDSOCK_331_384; location_type(Decoration,Windsock);
check; WINDSOCK_331_384; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; WINDSOCK_331_384; free();
check; RUS-1-TRANSPORT-1; location_type(Decoration,Transport);
check; RUS-1-TRANSPORT-1; coalition(f);
check; RUS-1-TRANSPORT-1; free();
check; RUS-1-TRANSPORT-1; in_radius(PRIMARY_LINK_PHASE,15000);
check; RUS-1-TRANSPORT-1-WP-1; range(PRIMARY_LINK_PHASE,closest_outof,5000);
check; RUS-1-TRANSPORT-1-WP-1; coalition(f);
check; GER-1-TRANSPORT-1; in_radius(PRIMARY_LINK_PHASE,15000);
check; GER-1-TRANSPORT-1; coalition(e);
check; GER-1-TRANSPORT-1; free();
check; GER-1-TRANSPORT-1-WP-1; range(PRIMARY_LINK_PHASE,closest_outof,5000);
check; GER-1-TRANSPORT-1-WP-1; coalition(e);
check; RUS-AT-ARTY-1; in_radius(PRIMARY_LINK_PHASE,15000);
check; RUS-AT-ARTY-1; location_type(Decoration,Artillery);
check; RUS-AT-ARTY-1; free();
check; RUS-AT-ARTY-1; coalition(f);
check; RUS-AT-ARTY-2; location_type(Decoration,Artillery);
check; RUS-AT-ARTY-2; free();
check; RUS-AT-ARTY-2; coalition(f);
check; RUS-AT-ARTY-2; in_radius(PRIMARY_LINK_PHASE,15000);
check; RUS-DEPOT-1-REF; location_type(GroundObjective,Building,Factory);
check; RUS-DEPOT-1-REF; free();
check; RUS-DEPOT-1-REF; coalition(f);
check; RUS-DEPOT-1-REF; in_radius(PRIMARY_LINK_PHASE,15000);
check; GER-DEPOT-1-REF; location_type(GroundObjective,Building,Factory);
check; GER-DEPOT-1-REF; free();
check; GER-DEPOT-1-REF; coalition(e);
check; GER-DEPOT-1-REF; in_radius(PRIMARY_LINK_PHASE,15000);
check; GER-AT-ARTY-1; free();
check; GER-AT-ARTY-1; in_radius(PRIMARY_LINK_PHASE,15000);
check; GER-AT-ARTY-1; coalition(e);
check; GER-AT-ARTY-1; location_type(Decoration,Artillery);
check; GER-AT-ARTY-2; free();
check; GER-AT-ARTY-2; in_radius(PRIMARY_LINK_PHASE,15000);
check; GER-AT-ARTY-2; coalition(e);
check; GER-AT-ARTY-2; location_type(Decoration,Artillery);

#
## property actions
#
action; GER-NODE-1(COUNTER,Counter); set(Counter,2);
action; GER-NODE-1(OBJECTIVE,TaskType); set(TaskType,14);
action; GER-NODE-1(OBJECTIVE,Coalition); set(Coalition,2);
action; GER-NODE-1(OBJECTIVE,Success); set(Success,0);
action; RUS-NODE-1(COUNTER,Counter); set(Counter,2);
action; RUS-NODE-1(OBJECTIVE,TaskType); set(TaskType,14);
action; RUS-NODE-1(OBJECTIVE,Coalition); set(Coalition,1);
action; RUS-NODE-1(OBJECTIVE,Success); set(Success,0);
action; RUS-1-TRANSPORT-1(VEHICLE_0_TYPE,Model); set_model(APC-arm-car,Allies:APC-arm-car:BA64);
action; RUS-1-TRANSPORT-1(VEHICLE_1_TYPE,Model); set_model(Cargo truck,random friendly);
action; RUS-1-TRANSPORT-1(VEHICLE_2_TYPE,Model); set_model(Cargo truck,random friendly);
action; RUS-1-TRANSPORT-1(VEHICLE_3_TYPE,Model); set_model(Cargo truck,random friendly);
action; RUS-1-TRANSPORT-1(VEHICLE_4_TYPE,Model); set_model(Cargo truck,random friendly);
action; RUS-1-TRANSPORT-1(VEHICLE_5_TYPE,Model); set_model(AAA SP cannon,random friendly);
action; GER-1-TRANSPORT-1(VEHICLE_0_TYPE,Model); set_model(APC-arm-car,random enemy);
action; GER-1-TRANSPORT-1(VEHICLE_1_TYPE,Model); set_model(Cargo truck,random enemy);
action; GER-1-TRANSPORT-1(VEHICLE_2_TYPE,Model); set_model(Cargo truck,random enemy);
action; GER-1-TRANSPORT-1(VEHICLE_3_TYPE,Model); set_model(Cargo truck,random enemy);
action; GER-1-TRANSPORT-1(VEHICLE_4_TYPE,Model); set_model(Cargo truck,random enemy);
action; GER-1-TRANSPORT-1(VEHICLE_5_TYPE,Model); set_model(AAA SP cannon,random enemy);
action; RUS-DEPOT-1-CONTROL(Plane_in,Zone); <empty>();
action; RUS-DEPOT-1-CONTROL(Plane_in,YPos); <empty>();
action; RUS-DEPOT-1-CONTROL(Plane_out,Zone); <empty>();
action; RUS-DEPOT-1-CONTROL(Plane_out,YPos); <empty>();
action; GER-DEPOT-1-CONTROL(Plane_in,Zone); <empty>();
action; GER-DEPOT-1-CONTROL(Plane_in,YPos); <empty>();
action; GER-DEPOT-1-CONTROL(Plane_out,Zone); <empty>();
action; GER-DEPOT-1-CONTROL(Plane_out,YPos); <empty>();

#
## unlinks
#

#
## gui helpers
#
gui_helper; GER-NODE-1; -157; 128;
gui_helper; RUS-NODE-1; 788; 177;
gui_helper; WINDSOCK_357; -237; -618;
gui_helper; GER-PARKING-1; -197; -313;
gui_helper; RUS-PARKING-1; 638; -293;
gui_helper; WINDSOCK_331_384; 667; -626;
gui_helper; RUS-1-TRANSPORT-1; 1627; 205;
gui_helper; RUS-1-TRANSPORT-1-WP-1; 1626; 536;
gui_helper; RUS-1-TRANSPORT-1-WP-2; 2140; 394;
gui_helper; GER-1-TRANSPORT-1; -1330; 293;
gui_helper; GER-1-TRANSPORT-1-WP-1; -1633; 545;
gui_helper; GER-1-TRANSPORT-1-WP-2; -1086; 542;
gui_helper; FRONTLINE; 308; 541;
gui_helper; REF; 328; 266;
gui_helper; RUS-AT-ARTY-1; 1272; -603;
gui_helper; RUS-AT-ARTY-2; 1310; -222;
gui_helper; RUS-DEPOT-1-LONG; 856; 697;
gui_helper; RUS-DEPOT-1-SQUARE; 861; 1026;
gui_helper; RUS-DEPOT-1-REF; 1169; 663;
gui_helper; RUS-DEPOT-1-CONTROL; 1413; 916;
gui_helper; PHASE_95; 1183; 1085;
gui_helper; GER-DEPOT-1-LONG; -588; 705;
gui_helper; GER-DEPOT-1-SQUARE; -575; 1031;
gui_helper; GER-DEPOT-1-REF; -295; 674;
gui_helper; GER-DEPOT-1-CONTROL; -39; 863;
gui_helper; PHASE_94; -300; 1046;
gui_helper; GER-AT-ARTY-1; -769; -422;
gui_helper; GER-AT-ARTY-2; -867; -103;
gui_helper; CASE64; 797; 859;
gui_helper; CASE65; 796; 1008;
gui_helper; CASE50; -703; 852;
gui_helper; CASE51; -698; 1023;
gui_helper; switch66; 941; 934;
gui_helper; switch52; -570; 934;
gui_helper; check; 75; 48;GER-NODE-1(free)
gui_helper; check; 76; 88;GER-NODE-1(coalition)
gui_helper; check; 74; 4;GER-NODE-1(location_type)
gui_helper; check; 957; 137;RUS-NODE-1(coalition)
gui_helper; check; 958; 60;RUS-NODE-1(location_type)
gui_helper; check; 954; 97;RUS-NODE-1(free)
gui_helper; check; -174; -726;WINDSOCK_357(location_type)
gui_helper; check; -177; -687;WINDSOCK_357(range)
gui_helper; check; -177; -647;WINDSOCK_357(free)
gui_helper; check; -142; -426;GER-PARKING-1(location_type)
gui_helper; check; -143; -390;GER-PARKING-1(coalition)
gui_helper; check; -145; -349;GER-PARKING-1(in_radius)
gui_helper; check; 649; -407;RUS-PARKING-1(location_type)
gui_helper; check; 652; -365;RUS-PARKING-1(coalition)
gui_helper; check; 650; -327;RUS-PARKING-1(in_radius)
gui_helper; check; 755; -765;WINDSOCK_331_384(location_type)
gui_helper; check; 752; -726;WINDSOCK_331_384(range)
gui_helper; check; 752; -686;WINDSOCK_331_384(free)
gui_helper; check; 1493; 31;RUS-1-TRANSPORT-1(location_type)
gui_helper; check; 1501; 74;RUS-1-TRANSPORT-1(coalition)
gui_helper; check; 1496; 130;RUS-1-TRANSPORT-1(free)
gui_helper; check; 1501; 177;RUS-1-TRANSPORT-1(in_radius)
gui_helper; check; 1571; 428;RUS-1-TRANSPORT-1-WP-1(range)
gui_helper; check; 1576; 472;RUS-1-TRANSPORT-1-WP-1(coalition)
gui_helper; check; -1103; 151;GER-1-TRANSPORT-1(in_radius)
gui_helper; check; -1100; 189;GER-1-TRANSPORT-1(coalition)
gui_helper; check; -1107; 229;GER-1-TRANSPORT-1(free)
gui_helper; check; -1579; 420;GER-1-TRANSPORT-1-WP-1(range)
gui_helper; check; -1574; 464;GER-1-TRANSPORT-1-WP-1(coalition)
gui_helper; check; 1370; -743;RUS-AT-ARTY-1(in_radius)
gui_helper; check; 1372; -678;RUS-AT-ARTY-1(location_type)
gui_helper; check; 1372; -707;RUS-AT-ARTY-1(free)
gui_helper; check; 1375; -644;RUS-AT-ARTY-1(coalition)
gui_helper; check; 1409; -297;RUS-AT-ARTY-2(location_type)
gui_helper; check; 1409; -326;RUS-AT-ARTY-2(free)
gui_helper; check; 1412; -263;RUS-AT-ARTY-2(coalition)
gui_helper; check; 1407; -362;RUS-AT-ARTY-2(in_radius)
gui_helper; check; 1179; 577;RUS-DEPOT-1-REF(location_type)
gui_helper; check; 1182; 613;RUS-DEPOT-1-REF(free)
gui_helper; check; 1177; 544;RUS-DEPOT-1-REF(coalition)
gui_helper; check; 1172; 511;RUS-DEPOT-1-REF(in_radius)
gui_helper; check; -251; 587;GER-DEPOT-1-REF(location_type)
gui_helper; check; -248; 623;GER-DEPOT-1-REF(free)
gui_helper; check; -253; 554;GER-DEPOT-1-REF(coalition)
gui_helper; check; -258; 521;GER-DEPOT-1-REF(in_radius)
gui_helper; check; -688; -553;GER-AT-ARTY-1(free)
gui_helper; check; -689; -435;GER-AT-ARTY-1(in_radius)
gui_helper; check; -693; -475;GER-AT-ARTY-1(coalition)
gui_helper; check; -695; -513;GER-AT-ARTY-1(location_type)
gui_helper; check; -786; -234;GER-AT-ARTY-2(free)
gui_helper; check; -787; -116;GER-AT-ARTY-2(in_radius)
gui_helper; check; -791; -156;GER-AT-ARTY-2(coalition)
gui_helper; check; -793; -194;GER-AT-ARTY-2(location_type)
gui_helper; Counter; -81; -27;GER-NODE-1; (COUNTER);
gui_helper; TaskType; -81; 13;GER-NODE-1; (OBJECTIVE);
gui_helper; Coalition; -82; 54;GER-NODE-1; (OBJECTIVE);
gui_helper; Success; -81; 93;GER-NODE-1; (OBJECTIVE);
gui_helper; Counter; 823; 16;RUS-NODE-1; (COUNTER);
gui_helper; TaskType; 823; 56;RUS-NODE-1; (OBJECTIVE);
gui_helper; Coalition; 823; 96;RUS-NODE-1; (OBJECTIVE);
gui_helper; Success; 823; 136;RUS-NODE-1; (OBJECTIVE);
gui_helper; Model; 1693; -35;RUS-1-TRANSPORT-1; (VEHICLE_0_TYPE);
gui_helper; Model; 1693; 5;RUS-1-TRANSPORT-1; (VEHICLE_1_TYPE);
gui_helper; Model; 1693; 45;RUS-1-TRANSPORT-1; (VEHICLE_2_TYPE);
gui_helper; Model; 1693; 85;RUS-1-TRANSPORT-1; (VEHICLE_3_TYPE);
gui_helper; Model; 1693; 125;RUS-1-TRANSPORT-1; (VEHICLE_4_TYPE);
gui_helper; Model; 1693; 165;RUS-1-TRANSPORT-1; (VEHICLE_5_TYPE);
gui_helper; Model; -1272; 62;GER-1-TRANSPORT-1; (VEHICLE_0_TYPE);
gui_helper; Model; -1272; 102;GER-1-TRANSPORT-1; (VEHICLE_1_TYPE);
gui_helper; Model; -1272; 142;GER-1-TRANSPORT-1; (VEHICLE_2_TYPE);
gui_helper; Model; -1272; 182;GER-1-TRANSPORT-1; (VEHICLE_3_TYPE);
gui_helper; Model; -1272; 222;GER-1-TRANSPORT-1; (VEHICLE_4_TYPE);
gui_helper; Model; -1272; 262;GER-1-TRANSPORT-1; (VEHICLE_5_TYPE);
gui_helper; Zone; 1482; 761;RUS-DEPOT-1-CONTROL; (Plane_in);
gui_helper; YPos; 1482; 801;RUS-DEPOT-1-CONTROL; (Plane_in);
gui_helper; Zone; 1482; 841;RUS-DEPOT-1-CONTROL; (Plane_out);
gui_helper; YPos; 1482; 881;RUS-DEPOT-1-CONTROL; (Plane_out);
gui_helper; Zone; 21; 707;GER-DEPOT-1-CONTROL; (Plane_in);
gui_helper; YPos; 21; 747;GER-DEPOT-1-CONTROL; (Plane_in);
gui_helper; Zone; 21; 787;GER-DEPOT-1-CONTROL; (Plane_out);
gui_helper; YPos; 21; 827;GER-DEPOT-1-CONTROL; (Plane_out);
