# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_MAIN_REF; main(scg\1\blocks_quickmission\ref_point.group);
blocks_set; blocks_TARGET_REF; main(scg\1\blocks_quickmission\ref_point.group);
blocks_set; blocks_BLUE_ARTY_SUB; main(scg\1\blocks_quickmission\arty_sub.group);
blocks_set; blocks_BLUE_ARTY1; main(scg\1\blocks_quickmission\ground\arty\arty_v6_entities.group);
blocks_set; blocks_BLUE_ARTY1_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_arty_blue.group);
blocks_set; blocks_BLUE_ARTY2_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_arty_blue.group);
blocks_set; blocks_BLUE_ARTY3_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_arty_blue.group);
blocks_set; blocks_BLUE_ARTY1_DECORATIONS; main(scg\1\blocks_quickmission\ground\arty\arty_v6_blue_decorations.group);
blocks_set; blocks_BLUE_ARTY2; main(scg\1\blocks_quickmission\ground\arty\arty_v5_entities.group);
blocks_set; blocks_BLUE_ARTY2_DECORATIONS; main(scg\1\blocks_quickmission\ground\arty\arty_v5_blue_decorations.group);
blocks_set; blocks_BLUE_ARTY3; main(scg\1\blocks_quickmission\ground\arty\arty_v5_entities.group);
blocks_set; blocks_BLUE_ARTY3_DECORATIONS; main(scg\1\blocks_quickmission\ground\arty\arty_v5_blue_decorations.group);
blocks_set; blocks_RED_ARTY_SUB; main(scg\1\blocks_quickmission\arty_sub.group);
blocks_set; blocks_RED_ARTY1; main(scg\1\blocks_quickmission\ground\arty\arty_v6_entities.group);
blocks_set; blocks_RED_ARTY2; main(scg\1\blocks_quickmission\ground\arty\arty_v5_entities.group);
blocks_set; blocks_RED_ARTY3; main(scg\1\blocks_quickmission\ground\arty\arty_v5_entities.group);
blocks_set; blocks_RED_ARTY2_DECORATIONS; main(scg\1\blocks_quickmission\ground\arty\arty_v5_red_decorations.group);
blocks_set; blocks_RED_ARTY3_DECORATIONS; main(scg\1\blocks_quickmission\ground\arty\arty_v5_red_decorations.group);
blocks_set; blocks_RED_ARTY1_DECORATIONS; main(scg\1\blocks_quickmission\ground\arty\arty_v6_red_decorations.group);
blocks_set; blocks_RED_ARTY1_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_arty_red.group);
blocks_set; blocks_RED_ARTY2_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_arty_red.group);
blocks_set; blocks_RED_ARTY3_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_arty_red.group);
blocks_set; blocks_RED_FORT1; main(scg\1\blocks_quickmission\ground\static\fort_area_red.group);
blocks_set; blocks_RED_FORT2; main(scg\1\blocks_quickmission\ground\static\fort_area_red.group);
blocks_set; blocks_RED_FORT1_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\red_fort_area1.group);
blocks_set; blocks_RED_FORT2_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\red_fort_area2.group);
blocks_set; blocks_BLUE_FORT1; main(scg\1\blocks_quickmission\ground\static\fort_area_blue.group);
blocks_set; blocks_BLUE_FORT2; main(scg\1\blocks_quickmission\ground\static\fort_area_blue.group);
blocks_set; blocks_BLUE_FORT1_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\blue_fort_area1.group);
blocks_set; blocks_BLUE_FORT2_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\blue_fort_area2.group);

#
## geo params
#
phase; MAIN_REF; server_setpos(); blocks_MAIN_REF; ;;
phase; TARGET_REF; server_targetpos(); blocks_TARGET_REF; ;;
phase; BLUE_ARTY_SUB; at(BLUE_ARTY1); blocks_BLUE_ARTY_SUB; clone_location;;
phase; BLUE_ARTY1; random(TARGET_REF); blocks_BLUE_ARTY1; clone_location;;
phase; BLUE_ARTY1_RECON; at(BLUE_ARTY1); blocks_BLUE_ARTY1_RECON; clone_location;;
phase; BLUE_ARTY2_RECON; at(BLUE_ARTY2); blocks_BLUE_ARTY2_RECON; clone_location;;
phase; BLUE_ARTY3_RECON; at(BLUE_ARTY3); blocks_BLUE_ARTY3_RECON; clone_location;;
phase; BLUE_ARTY1_DECORATIONS; at(BLUE_ARTY1); blocks_BLUE_ARTY1_DECORATIONS; clone_location;;
phase; BLUE_ARTY2; random(TARGET_REF); blocks_BLUE_ARTY2; clone_location;;
phase; BLUE_ARTY2_DECORATIONS; at(BLUE_ARTY2); blocks_BLUE_ARTY2_DECORATIONS; clone_location;;
phase; BLUE_ARTY3; random(TARGET_REF); blocks_BLUE_ARTY3; clone_location;;
phase; BLUE_ARTY3_DECORATIONS; at(BLUE_ARTY3); blocks_BLUE_ARTY3_DECORATIONS; clone_location;;
phase; RED_ARTY_SUB; at(RED_ARTY1); blocks_RED_ARTY_SUB; clone_location;;
phase; RED_ARTY1; random(MAIN_REF); blocks_RED_ARTY1; clone_location;;
phase; RED_ARTY2; random(MAIN_REF); blocks_RED_ARTY2; clone_location;;
phase; RED_ARTY3; random(MAIN_REF); blocks_RED_ARTY3; clone_location;;
phase; RED_ARTY2_DECORATIONS; at(RED_ARTY2); blocks_RED_ARTY2_DECORATIONS; clone_location;;
phase; RED_ARTY3_DECORATIONS; at(RED_ARTY3); blocks_RED_ARTY3_DECORATIONS; clone_location;;
phase; RED_ARTY1_DECORATIONS; at(RED_ARTY1); blocks_RED_ARTY1_DECORATIONS; clone_location;;
phase; RED_ARTY1_RECON; at(RED_ARTY1); blocks_RED_ARTY1_RECON; clone_location;;
phase; RED_ARTY2_RECON; at(RED_ARTY2); blocks_RED_ARTY2_RECON; clone_location;;
phase; RED_ARTY3_RECON; at(RED_ARTY3); blocks_RED_ARTY3_RECON; clone_location;;
phase; RED_FORT1; random(MAIN_REF); blocks_RED_FORT1; clone_location;;
phase; RED_FORT2; random(MAIN_REF); blocks_RED_FORT2; clone_location;;
phase; RED_FORT1_SERVER_INPUT; at(RED_FORT1); blocks_RED_FORT1_SERVER_INPUT; clone_location;;
phase; RED_FORT2_SERVER_INPUT; at(RED_FORT2); blocks_RED_FORT2_SERVER_INPUT; clone_location;;
phase; BLUE_FORT1; random(TARGET_REF); blocks_BLUE_FORT1; clone_location;;
phase; BLUE_FORT2; random(TARGET_REF); blocks_BLUE_FORT2; clone_location;;
phase; BLUE_FORT1_SERVER_INPUT; at(BLUE_FORT1); blocks_BLUE_FORT1_SERVER_INPUT; clone_location;;
phase; BLUE_FORT2_SERVER_INPUT; at(BLUE_FORT2); blocks_BLUE_FORT2_SERVER_INPUT; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; BLUE_ARTY1(artKILLSUBblue); BLUE_ARTY_SUB(artKILLSUBblue);
tlink; BLUE_ARTY1(SERVER_INPUT); BLUE_ARTY1_RECON(SERVER_INPUT);
tlink; BLUE_ARTY1_RECON(artSUBblue); BLUE_ARTY_SUB(artSUBblue);
tlink; BLUE_ARTY1_RECON(ARTY_ENTITIES_ACTIVATE); BLUE_ARTY1(ARTY_ENTITIES_ACTIVATE);
tlink; BLUE_ARTY1_RECON(ARTY_ENTITIES_DEACTIVATE); BLUE_ARTY1(ARTY_ENTITIES_DEACTIVATE);
tlink; BLUE_ARTY2_RECON(artSUBblue); BLUE_ARTY_SUB(artSUBblue);
tlink; BLUE_ARTY2_RECON(ARTY_ENTITIES_ACTIVATE); BLUE_ARTY2(ARTY_ENTITIES_ACTIVATE);
tlink; BLUE_ARTY2_RECON(ARTY_ENTITIES_DEACTIVATE); BLUE_ARTY2(ARTY_ENTITIES_DEACTIVATE);
tlink; BLUE_ARTY3_RECON(artSUBblue); BLUE_ARTY_SUB(artSUBblue);
tlink; BLUE_ARTY3_RECON(ARTY_ENTITIES_ACTIVATE); BLUE_ARTY3(ARTY_ENTITIES_ACTIVATE);
tlink; BLUE_ARTY3_RECON(ARTY_ENTITIES_DEACTIVATE); BLUE_ARTY3(ARTY_ENTITIES_DEACTIVATE);
tlink; BLUE_ARTY2(artKILLSUBblue); BLUE_ARTY_SUB(artKILLSUBblue);
tlink; BLUE_ARTY2(SERVER_INPUT); BLUE_ARTY2_RECON(SERVER_INPUT);
tlink; BLUE_ARTY3(artKILLSUBblue); BLUE_ARTY_SUB(artKILLSUBblue);
tlink; BLUE_ARTY3(SERVER_INPUT); BLUE_ARTY3_RECON(SERVER_INPUT);
tlink; RED_ARTY1(artKILLSUBred); RED_ARTY_SUB(artKILLSUBred);
tlink; RED_ARTY1(SERVER_INPUT); RED_ARTY1_RECON(SERVER_INPUT);
tlink; RED_ARTY2(artKILLSUBred); RED_ARTY_SUB(artKILLSUBred);
tlink; RED_ARTY2(SERVER_INPUT); RED_ARTY2_RECON(SERVER_INPUT);
tlink; RED_ARTY3(artKILLSUBred); RED_ARTY_SUB(artKILLSUBred);
tlink; RED_ARTY3(SERVER_INPUT); RED_ARTY3_RECON(SERVER_INPUT);
tlink; RED_ARTY1_RECON(artSUBred); RED_ARTY_SUB(artSUBred);
tlink; RED_ARTY1_RECON(ARTY_ENTITIES_ACTIVATE); RED_ARTY1(ARTY_ENTITIES_ACTIVATE);
tlink; RED_ARTY1_RECON(ARTY_ENTITIES_DEACTIVATE); RED_ARTY1(ARTY_ENTITIES_DEACTIVATE);
tlink; RED_ARTY2_RECON(artSUBred); RED_ARTY_SUB(artSUBred);
tlink; RED_ARTY2_RECON(ARTY_ENTITIES_ACTIVATE); RED_ARTY2(ARTY_ENTITIES_ACTIVATE);
tlink; RED_ARTY2_RECON(ARTY_ENTITIES_DEACTIVATE); RED_ARTY2(ARTY_ENTITIES_DEACTIVATE);
tlink; RED_ARTY3_RECON(artSUBred); RED_ARTY_SUB(artSUBred);
tlink; RED_ARTY3_RECON(ARTY_ENTITIES_ACTIVATE); RED_ARTY3(ARTY_ENTITIES_ACTIVATE);
tlink; RED_ARTY3_RECON(ARTY_ENTITIES_DEACTIVATE); RED_ARTY3(ARTY_ENTITIES_DEACTIVATE);
tlink; RED_FORT1_SERVER_INPUT(SERVER_INPUT); RED_FORT1(SERVER_INPUT);
tlink; RED_FORT2_SERVER_INPUT(SERVER_INPUT); RED_FORT2(SERVER_INPUT);
tlink; BLUE_FORT1_SERVER_INPUT(SERVER_INPUT); BLUE_FORT1(SERVER_INPUT);
tlink; BLUE_FORT2_SERVER_INPUT(SERVER_INPUT); BLUE_FORT2(SERVER_INPUT);

#
## conditions
#
check; BLUE_ARTY1; location_type(Decoration,Artillery);
check; BLUE_ARTY1; in_radius(PRIMARY_LINK_PHASE,120000);
check; BLUE_ARTY1; coalition(e);
check; BLUE_ARTY1; free();
check; BLUE_ARTY2; location_type(Decoration,Artillery);
check; BLUE_ARTY2; free();
check; BLUE_ARTY2; coalition(e);
check; BLUE_ARTY2; in_radius(PRIMARY_LINK_PHASE,120000);
check; BLUE_ARTY3; location_type(Decoration,Artillery);
check; BLUE_ARTY3; free();
check; BLUE_ARTY3; coalition(e);
check; BLUE_ARTY3; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_ARTY1; location_type(Decoration,Artillery);
check; RED_ARTY1; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_ARTY1; coalition(f);
check; RED_ARTY1; free();
check; RED_ARTY2; location_type(Decoration,Artillery);
check; RED_ARTY2; free();
check; RED_ARTY2; coalition(f);
check; RED_ARTY2; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_ARTY3; location_type(Decoration,Artillery);
check; RED_ARTY3; free();
check; RED_ARTY3; coalition(f);
check; RED_ARTY3; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_FORT1; location_type(Decoration,Artillery);
check; RED_FORT1; coalition(f);
check; RED_FORT1; free();
check; RED_FORT1; in_radius(PRIMARY_LINK_PHASE,150000);
check; RED_FORT2; location_type(Decoration,Artillery);
check; RED_FORT2; coalition(f);
check; RED_FORT2; free();
check; RED_FORT2; in_radius(PRIMARY_LINK_PHASE,150000);
check; BLUE_FORT1; location_type(Decoration,Artillery);
check; BLUE_FORT1; in_radius(PRIMARY_LINK_PHASE,120000);
check; BLUE_FORT1; free();
check; BLUE_FORT1; coalition(e);
check; BLUE_FORT2; location_type(Decoration,Artillery);
check; BLUE_FORT2; in_radius(PRIMARY_LINK_PHASE,120000);
check; BLUE_FORT2; free();
check; BLUE_FORT2; coalition(e);

#
## property actions
#
action; BLUE_ARTY1(ARTY_TYPE,Model); set_model(Howitzer,random enemy);
action; BLUE_ARTY1(ARTY_TYPE,Country); set_country(enemy);
action; BLUE_ARTY1(MG_TYPE,Model); set_model(AAA machinegun,random enemy);
action; BLUE_ARTY1(MG_TYPE,Country); set_country(enemy);
action; BLUE_ARTY1(Objective,Coalition); set(Coalition,1);
action; BLUE_ARTY1_RECON(Tank,Zone); <empty>();
action; BLUE_ARTY1_RECON(Plane_in,Zone); <empty>();
action; BLUE_ARTY1_RECON(Plane_in,YPos); <empty>();
action; BLUE_ARTY1_RECON(Plane_out,Zone); <empty>();
action; BLUE_ARTY1_RECON(Plane_out,YPos); <empty>();
action; BLUE_ARTY1_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_ARTY1_RECON(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_ARTY1_RECON(RECON_OBJ,Success); set(Success,1);
action; BLUE_ARTY2_RECON(Tank,Zone); <empty>();
action; BLUE_ARTY2_RECON(Plane_in,Zone); <empty>();
action; BLUE_ARTY2_RECON(Plane_in,YPos); <empty>();
action; BLUE_ARTY2_RECON(Plane_out,Zone); <empty>();
action; BLUE_ARTY2_RECON(Plane_out,YPos); <empty>();
action; BLUE_ARTY2_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_ARTY2_RECON(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_ARTY2_RECON(RECON_OBJ,Success); set(Success,1);
action; BLUE_ARTY3_RECON(Tank,Zone); <empty>();
action; BLUE_ARTY3_RECON(Plane_in,Zone); <empty>();
action; BLUE_ARTY3_RECON(Plane_in,YPos); <empty>();
action; BLUE_ARTY3_RECON(Plane_out,Zone); <empty>();
action; BLUE_ARTY3_RECON(Plane_out,YPos); <empty>();
action; BLUE_ARTY3_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_ARTY3_RECON(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_ARTY3_RECON(RECON_OBJ,Success); set(Success,1);
action; BLUE_ARTY2(ARTY_TYPE,Model); set_model(Howitzer,random enemy);
action; BLUE_ARTY2(ARTY_TYPE,Country); set_country(enemy);
action; BLUE_ARTY2(MG_TYPE,Model); set_model(AAA machinegun,random enemy);
action; BLUE_ARTY2(MG_TYPE,Country); set_country(enemy);
action; BLUE_ARTY2(Objective,Coalition); set(Coalition,1);
action; BLUE_ARTY3(ARTY_TYPE,Model); set_model(Howitzer,random enemy);
action; BLUE_ARTY3(ARTY_TYPE,Country); set_country(enemy);
action; BLUE_ARTY3(MG_TYPE,Model); set_model(AAA machinegun,random enemy);
action; BLUE_ARTY3(MG_TYPE,Country); set_country(enemy);
action; BLUE_ARTY3(Objective,Coalition); set(Coalition,1);
action; RED_ARTY1(ARTY_TYPE,Model); set_model(Howitzer,random friendly);
action; RED_ARTY1(ARTY_TYPE,Country); set_country(friendly);
action; RED_ARTY1(MG_TYPE,Model); set_model(AAA machinegun,random friendly);
action; RED_ARTY1(MG_TYPE,Country); set_country(friendly);
action; RED_ARTY1(Objective,Coalition); set(Coalition,2);
action; RED_ARTY2(ARTY_TYPE,Model); set_model(Howitzer,random friendly);
action; RED_ARTY2(ARTY_TYPE,Country); set_country(friendly);
action; RED_ARTY2(MG_TYPE,Model); set_model(AAA machinegun,random friendly);
action; RED_ARTY2(MG_TYPE,Country); set_country(friendly);
action; RED_ARTY2(Objective,Coalition); set(Coalition,2);
action; RED_ARTY3(ARTY_TYPE,Model); set_model(Howitzer,random friendly);
action; RED_ARTY3(ARTY_TYPE,Country); set_country(friendly);
action; RED_ARTY3(MG_TYPE,Model); set_model(AAA machinegun,random friendly);
action; RED_ARTY3(MG_TYPE,Country); set_country(friendly);
action; RED_ARTY3(Objective,Coalition); set(Coalition,2);
action; RED_ARTY1_RECON(Tank,Zone); <empty>();
action; RED_ARTY1_RECON(Plane_in,Zone); <empty>();
action; RED_ARTY1_RECON(Plane_in,YPos); <empty>();
action; RED_ARTY1_RECON(Plane_out,Zone); <empty>();
action; RED_ARTY1_RECON(Plane_out,YPos); <empty>();
action; RED_ARTY1_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_ARTY1_RECON(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_ARTY1_RECON(RECON_OBJ,Success); set(Success,1);
action; RED_ARTY2_RECON(Tank,Zone); <empty>();
action; RED_ARTY2_RECON(Plane_in,Zone); <empty>();
action; RED_ARTY2_RECON(Plane_in,YPos); <empty>();
action; RED_ARTY2_RECON(Plane_out,Zone); <empty>();
action; RED_ARTY2_RECON(Plane_out,YPos); <empty>();
action; RED_ARTY2_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_ARTY2_RECON(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_ARTY2_RECON(RECON_OBJ,Success); set(Success,1);
action; RED_ARTY3_RECON(Tank,Zone); <empty>();
action; RED_ARTY3_RECON(Plane_in,Zone); <empty>();
action; RED_ARTY3_RECON(Plane_in,YPos); <empty>();
action; RED_ARTY3_RECON(Plane_out,Zone); <empty>();
action; RED_ARTY3_RECON(Plane_out,YPos); <empty>();
action; RED_ARTY3_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_ARTY3_RECON(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_ARTY3_RECON(RECON_OBJ,Success); set(Success,1);
action; RED_FORT1(MG_AI,AILevel); set(AILevel,2);
action; RED_FORT1(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_FORT1(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_FORT1(RECON_OBJ,Success); set(Success,1);
action; RED_FORT1(Tank,Zone); <empty>();
action; RED_FORT1(Plane_in,Zone); <empty>();
action; RED_FORT1(Plane_in,YPos); <empty>();
action; RED_FORT1(Plane_out,Zone); <empty>();
action; RED_FORT1(Plane_out,YPos); <empty>();
action; RED_FORT2(MG_AI,AILevel); set(AILevel,2);
action; RED_FORT2(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_FORT2(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_FORT2(RECON_OBJ,Success); set(Success,1);
action; RED_FORT2(Tank,Zone); <empty>();
action; RED_FORT2(Plane_in,Zone); <empty>();
action; RED_FORT2(Plane_in,YPos); <empty>();
action; RED_FORT2(Plane_out,Zone); <empty>();
action; RED_FORT2(Plane_out,YPos); <empty>();
action; BLUE_FORT1(MG_AI,AILevel); set(AILevel,2);
action; BLUE_FORT1(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_FORT1(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_FORT1(RECON_OBJ,Success); set(Success,1);
action; BLUE_FORT1(Tank,Zone); <empty>();
action; BLUE_FORT1(Plane_in,Zone); <empty>();
action; BLUE_FORT1(Plane_in,YPos); <empty>();
action; BLUE_FORT1(Plane_out,Zone); <empty>();
action; BLUE_FORT1(Plane_out,YPos); <empty>();
action; BLUE_FORT2(MG_AI,AILevel); set(AILevel,2);
action; BLUE_FORT2(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_FORT2(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_FORT2(RECON_OBJ,Success); set(Success,1);
action; BLUE_FORT2(Tank,Zone); <empty>();
action; BLUE_FORT2(Plane_in,Zone); <empty>();
action; BLUE_FORT2(Plane_in,YPos); <empty>();
action; BLUE_FORT2(Plane_out,Zone); <empty>();
action; BLUE_FORT2(Plane_out,YPos); <empty>();

#
## unlinks
#

#
## gui helpers
#
gui_helper; MAIN_REF; -590; 4208;
gui_helper; TARGET_REF; -956; 4213;
gui_helper; BLUE_ARTY_SUB; -3092; 6344;
gui_helper; BLUE_ARTY1; -2614; 7424;
gui_helper; BLUE_ARTY1_RECON; -2621; 7046;
gui_helper; BLUE_ARTY2_RECON; -3339; 7022;
gui_helper; BLUE_ARTY3_RECON; -3973; 6964;
gui_helper; BLUE_ARTY1_DECORATIONS; -2611; 7653;
gui_helper; BLUE_ARTY2; -3325; 7409;
gui_helper; BLUE_ARTY2_DECORATIONS; -3312; 7665;
gui_helper; BLUE_ARTY3; -3973; 7384;
gui_helper; BLUE_ARTY3_DECORATIONS; -3960; 7640;
gui_helper; RED_ARTY_SUB; 262; 6121;
gui_helper; RED_ARTY1; -546; 7297;
gui_helper; RED_ARTY2; 160; 7291;
gui_helper; RED_ARTY3; 896; 7286;
gui_helper; RED_ARTY2_DECORATIONS; 153; 7526;
gui_helper; RED_ARTY3_DECORATIONS; 920; 7469;
gui_helper; RED_ARTY1_DECORATIONS; -544; 7554;
gui_helper; RED_ARTY1_RECON; -556; 6880;
gui_helper; RED_ARTY2_RECON; 155; 6804;
gui_helper; RED_ARTY3_RECON; 927; 6856;
gui_helper; RED_FORT1; 2627; 6393;
gui_helper; RED_FORT2; 2329; 6846;
gui_helper; RED_FORT1_SERVER_INPUT; 2620; 6617;
gui_helper; RED_FORT2_SERVER_INPUT; 2334; 7018;
gui_helper; BLUE_FORT1; -3911; 5101;
gui_helper; BLUE_FORT2; -3400; 5353;
gui_helper; BLUE_FORT1_SERVER_INPUT; -3908; 5265;
gui_helper; BLUE_FORT2_SERVER_INPUT; -3397; 5530;
gui_helper; check; -2435; 7284;BLUE_ARTY1(location_type)
gui_helper; check; -2435; 7383;BLUE_ARTY1(in_radius)
gui_helper; check; -2434; 7316;BLUE_ARTY1(coalition)
gui_helper; check; -2434; 7350;BLUE_ARTY1(free)
gui_helper; check; -3153; 7249;BLUE_ARTY2(location_type)
gui_helper; check; -3156; 7318;BLUE_ARTY2(free)
gui_helper; check; -3154; 7283;BLUE_ARTY2(coalition)
gui_helper; check; -3155; 7350;BLUE_ARTY2(in_radius)
gui_helper; check; -3801; 7224;BLUE_ARTY3(location_type)
gui_helper; check; -3804; 7293;BLUE_ARTY3(free)
gui_helper; check; -3802; 7258;BLUE_ARTY3(coalition)
gui_helper; check; -3803; 7325;BLUE_ARTY3(in_radius)
gui_helper; check; -367; 7157;RED_ARTY1(location_type)
gui_helper; check; -367; 7256;RED_ARTY1(in_radius)
gui_helper; check; -366; 7189;RED_ARTY1(coalition)
gui_helper; check; -366; 7223;RED_ARTY1(free)
gui_helper; check; 332; 7131;RED_ARTY2(location_type)
gui_helper; check; 329; 7200;RED_ARTY2(free)
gui_helper; check; 331; 7165;RED_ARTY2(coalition)
gui_helper; check; 330; 7232;RED_ARTY2(in_radius)
gui_helper; check; 1068; 7126;RED_ARTY3(location_type)
gui_helper; check; 1065; 7195;RED_ARTY3(free)
gui_helper; check; 1067; 7160;RED_ARTY3(coalition)
gui_helper; check; 1066; 7227;RED_ARTY3(in_radius)
gui_helper; check; 2807; 6239;RED_FORT1(location_type)
gui_helper; check; 2808; 6271;RED_FORT1(coalition)
gui_helper; check; 2808; 6303;RED_FORT1(free)
gui_helper; check; 2807; 6335;RED_FORT1(in_radius)
gui_helper; check; 2509; 6692;RED_FORT2(location_type)
gui_helper; check; 2510; 6724;RED_FORT2(coalition)
gui_helper; check; 2510; 6756;RED_FORT2(free)
gui_helper; check; 2509; 6788;RED_FORT2(in_radius)
gui_helper; check; -3719; 4976;BLUE_FORT1(location_type)
gui_helper; check; -3716; 5074;BLUE_FORT1(in_radius)
gui_helper; check; -3715; 5043;BLUE_FORT1(free)
gui_helper; check; -3718; 5011;BLUE_FORT1(coalition)
gui_helper; check; -3208; 5228;BLUE_FORT2(location_type)
gui_helper; check; -3205; 5326;BLUE_FORT2(in_radius)
gui_helper; check; -3204; 5295;BLUE_FORT2(free)
gui_helper; check; -3207; 5263;BLUE_FORT2(coalition)
gui_helper; Model; -2546; 7234;BLUE_ARTY1; (ARTY_TYPE);
gui_helper; Country; -2546; 7274;BLUE_ARTY1; (ARTY_TYPE);
gui_helper; Model; -2546; 7314;BLUE_ARTY1; (MG_TYPE);
gui_helper; Country; -2546; 7354;BLUE_ARTY1; (MG_TYPE);
gui_helper; Coalition; -2546; 7394;BLUE_ARTY1; (Objective);
gui_helper; Zone; -2554; 7017;BLUE_ARTY1_RECON; (Tank);
gui_helper; Zone; -2556; 6736;BLUE_ARTY1_RECON; (Plane_in);
gui_helper; YPos; -2556; 6776;BLUE_ARTY1_RECON; (Plane_in);
gui_helper; Zone; -2556; 6816;BLUE_ARTY1_RECON; (Plane_out);
gui_helper; YPos; -2556; 6856;BLUE_ARTY1_RECON; (Plane_out);
gui_helper; TaskType; -2556; 6896;BLUE_ARTY1_RECON; (RECON_OBJ);
gui_helper; Coalition; -2556; 6936;BLUE_ARTY1_RECON; (RECON_OBJ);
gui_helper; Success; -2556; 6976;BLUE_ARTY1_RECON; (RECON_OBJ);
gui_helper; Zone; -3272; 6993;BLUE_ARTY2_RECON; (Tank);
gui_helper; Zone; -3272; 6714;BLUE_ARTY2_RECON; (Plane_in);
gui_helper; YPos; -3272; 6754;BLUE_ARTY2_RECON; (Plane_in);
gui_helper; Zone; -3272; 6794;BLUE_ARTY2_RECON; (Plane_out);
gui_helper; YPos; -3272; 6834;BLUE_ARTY2_RECON; (Plane_out);
gui_helper; TaskType; -3272; 6874;BLUE_ARTY2_RECON; (RECON_OBJ);
gui_helper; Coalition; -3272; 6914;BLUE_ARTY2_RECON; (RECON_OBJ);
gui_helper; Success; -3272; 6954;BLUE_ARTY2_RECON; (RECON_OBJ);
gui_helper; Zone; -3906; 6935;BLUE_ARTY3_RECON; (Tank);
gui_helper; Zone; -3908; 6655;BLUE_ARTY3_RECON; (Plane_in);
gui_helper; YPos; -3908; 6695;BLUE_ARTY3_RECON; (Plane_in);
gui_helper; Zone; -3908; 6735;BLUE_ARTY3_RECON; (Plane_out);
gui_helper; YPos; -3908; 6775;BLUE_ARTY3_RECON; (Plane_out);
gui_helper; TaskType; -3908; 6815;BLUE_ARTY3_RECON; (RECON_OBJ);
gui_helper; Coalition; -3908; 6855;BLUE_ARTY3_RECON; (RECON_OBJ);
gui_helper; Success; -3908; 6895;BLUE_ARTY3_RECON; (RECON_OBJ);
gui_helper; Model; -3265; 7216;BLUE_ARTY2; (ARTY_TYPE);
gui_helper; Country; -3265; 7256;BLUE_ARTY2; (ARTY_TYPE);
gui_helper; Model; -3265; 7296;BLUE_ARTY2; (MG_TYPE);
gui_helper; Country; -3265; 7336;BLUE_ARTY2; (MG_TYPE);
gui_helper; Coalition; -3265; 7376;BLUE_ARTY2; (Objective);
gui_helper; Model; -3913; 7191;BLUE_ARTY3; (ARTY_TYPE);
gui_helper; Country; -3913; 7231;BLUE_ARTY3; (ARTY_TYPE);
gui_helper; Model; -3913; 7271;BLUE_ARTY3; (MG_TYPE);
gui_helper; Country; -3913; 7311;BLUE_ARTY3; (MG_TYPE);
gui_helper; Coalition; -3913; 7351;BLUE_ARTY3; (Objective);
gui_helper; Model; -478; 7107;RED_ARTY1; (ARTY_TYPE);
gui_helper; Country; -478; 7147;RED_ARTY1; (ARTY_TYPE);
gui_helper; Model; -478; 7187;RED_ARTY1; (MG_TYPE);
gui_helper; Country; -478; 7227;RED_ARTY1; (MG_TYPE);
gui_helper; Coalition; -478; 7267;RED_ARTY1; (Objective);
gui_helper; Model; 220; 7098;RED_ARTY2; (ARTY_TYPE);
gui_helper; Country; 220; 7138;RED_ARTY2; (ARTY_TYPE);
gui_helper; Model; 220; 7178;RED_ARTY2; (MG_TYPE);
gui_helper; Country; 220; 7218;RED_ARTY2; (MG_TYPE);
gui_helper; Coalition; 220; 7258;RED_ARTY2; (Objective);
gui_helper; Model; 956; 7093;RED_ARTY3; (ARTY_TYPE);
gui_helper; Country; 956; 7133;RED_ARTY3; (ARTY_TYPE);
gui_helper; Model; 956; 7173;RED_ARTY3; (MG_TYPE);
gui_helper; Country; 956; 7213;RED_ARTY3; (MG_TYPE);
gui_helper; Coalition; 956; 7253;RED_ARTY3; (Objective);
gui_helper; Zone; -490; 6732;RED_ARTY1_RECON; (Tank);
gui_helper; Zone; -493; 6571;RED_ARTY1_RECON; (Plane_in);
gui_helper; YPos; -493; 6611;RED_ARTY1_RECON; (Plane_in);
gui_helper; Zone; -493; 6651;RED_ARTY1_RECON; (Plane_out);
gui_helper; YPos; -493; 6691;RED_ARTY1_RECON; (Plane_out);
gui_helper; TaskType; -490; 6775;RED_ARTY1_RECON; (RECON_OBJ);
gui_helper; Coalition; -490; 6815;RED_ARTY1_RECON; (RECON_OBJ);
gui_helper; Success; -490; 6855;RED_ARTY1_RECON; (RECON_OBJ);
gui_helper; Zone; 223; 6652;RED_ARTY2_RECON; (Tank);
gui_helper; Zone; 223; 6492;RED_ARTY2_RECON; (Plane_in);
gui_helper; YPos; 223; 6532;RED_ARTY2_RECON; (Plane_in);
gui_helper; Zone; 223; 6572;RED_ARTY2_RECON; (Plane_out);
gui_helper; YPos; 223; 6612;RED_ARTY2_RECON; (Plane_out);
gui_helper; TaskType; 224; 6693;RED_ARTY2_RECON; (RECON_OBJ);
gui_helper; Coalition; 224; 6733;RED_ARTY2_RECON; (RECON_OBJ);
gui_helper; Success; 224; 6773;RED_ARTY2_RECON; (RECON_OBJ);
gui_helper; Zone; 989; 6707;RED_ARTY3_RECON; (Tank);
gui_helper; Zone; 988; 6545;RED_ARTY3_RECON; (Plane_in);
gui_helper; YPos; 988; 6585;RED_ARTY3_RECON; (Plane_in);
gui_helper; Zone; 988; 6625;RED_ARTY3_RECON; (Plane_out);
gui_helper; YPos; 988; 6665;RED_ARTY3_RECON; (Plane_out);
gui_helper; TaskType; 991; 6749;RED_ARTY3_RECON; (RECON_OBJ);
gui_helper; Coalition; 991; 6789;RED_ARTY3_RECON; (RECON_OBJ);
gui_helper; Success; 991; 6829;RED_ARTY3_RECON; (RECON_OBJ);
gui_helper; AILevel; 2689; 6184;RED_FORT1; (MG_AI);
gui_helper; TaskType; 2691; 6226;RED_FORT1; (RECON_OBJ);
gui_helper; Coalition; 2691; 6266;RED_FORT1; (RECON_OBJ);
gui_helper; Success; 2691; 6306;RED_FORT1; (RECON_OBJ);
gui_helper; Zone; 2689; 6346;RED_FORT1; (Tank);
gui_helper; Zone; 3027; 6283;RED_FORT1; (Plane_in);
gui_helper; YPos; 3027; 6323;RED_FORT1; (Plane_in);
gui_helper; Zone; 3027; 6363;RED_FORT1; (Plane_out);
gui_helper; YPos; 3027; 6403;RED_FORT1; (Plane_out);
gui_helper; AILevel; 2391; 6637;RED_FORT2; (MG_AI);
gui_helper; TaskType; 2393; 6679;RED_FORT2; (RECON_OBJ);
gui_helper; Coalition; 2393; 6719;RED_FORT2; (RECON_OBJ);
gui_helper; Success; 2393; 6759;RED_FORT2; (RECON_OBJ);
gui_helper; Zone; 2391; 6799;RED_FORT2; (Tank);
gui_helper; Zone; 2150; 6701;RED_FORT2; (Plane_in);
gui_helper; YPos; 2150; 6741;RED_FORT2; (Plane_in);
gui_helper; Zone; 2150; 6781;RED_FORT2; (Plane_out);
gui_helper; YPos; 2150; 6821;RED_FORT2; (Plane_out);
gui_helper; AILevel; -3839; 5078;BLUE_FORT1; (MG_AI);
gui_helper; TaskType; -3840; 4921;BLUE_FORT1; (RECON_OBJ);
gui_helper; Coalition; -3840; 4961;BLUE_FORT1; (RECON_OBJ);
gui_helper; Success; -3840; 5001;BLUE_FORT1; (RECON_OBJ);
gui_helper; Zone; -3844; 5040;BLUE_FORT1; (Tank);
gui_helper; Zone; -3511; 4991;BLUE_FORT1; (Plane_in);
gui_helper; YPos; -3511; 5031;BLUE_FORT1; (Plane_in);
gui_helper; Zone; -3511; 5071;BLUE_FORT1; (Plane_out);
gui_helper; YPos; -3511; 5111;BLUE_FORT1; (Plane_out);
gui_helper; AILevel; -3328; 5330;BLUE_FORT2; (MG_AI);
gui_helper; TaskType; -3334; 5172;BLUE_FORT2; (RECON_OBJ);
gui_helper; Coalition; -3334; 5212;BLUE_FORT2; (RECON_OBJ);
gui_helper; Success; -3334; 5252;BLUE_FORT2; (RECON_OBJ);
gui_helper; Zone; -3333; 5292;BLUE_FORT2; (Tank);
gui_helper; Zone; -3000; 5243;BLUE_FORT2; (Plane_in);
gui_helper; YPos; -3000; 5283;BLUE_FORT2; (Plane_in);
gui_helper; Zone; -3000; 5323;BLUE_FORT2; (Plane_out);
gui_helper; YPos; -3000; 5363;BLUE_FORT2; (Plane_out);
