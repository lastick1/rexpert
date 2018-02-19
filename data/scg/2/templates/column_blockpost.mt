# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_RAC1; main(scg\1\blocks_quickmission\ground\vehicle\vehicle_6rus_5km.group);
blocks_set; blocks_RWP11; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RWP12; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RAC2; main(scg\1\blocks_quickmission\ground\vehicle\vehicle_6rus_5km.group);
blocks_set; blocks_RWP21; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RWP22; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GAC1; main(scg\1\blocks_quickmission\ground\vehicle\vehicle_6ger_5km.group);
blocks_set; blocks_GWP11; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GWP12; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GAC2; main(scg\1\blocks_quickmission\ground\vehicle\vehicle_6ger_5km.group);
blocks_set; blocks_GWP21; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GWP22; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GWP31; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GWP32; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RWP31; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_RWP32; main(scg\1\blocks_quickmission\ground\vehicle_wp.group);
blocks_set; blocks_GMC; main(scg\1\blocks_quickmission\ground\vehicle\tanks_5ger_5km.group);
blocks_set; blocks_RMC; main(scg\1\blocks_quickmission\ground\vehicle\tanks_5rus_5km.group);
blocks_set; blocks_BLUE_BLOCK_POST1; main(scg\1\blocks_quickmission\ground\static\block_post_blue.group);
blocks_set; blocks_BLUE_BLOCK_POST1_AAA; main(scg\1\blocks_quickmission\ground\aaa\small\smart_block_post_machine_guns_blue.group);
blocks_set; blocks_BLUE_BLOCK_POST1_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_block_post_blue.group);
blocks_set; blocks_BLUE_BLOCK_POSTS_SUB; main(scg\1\blocks_quickmission\block_post_sub.group);
blocks_set; blocks_RED_BLOCK_POST1_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_block_post_red.group);
blocks_set; blocks_RED_BLOCK_POSTS_SUB; main(scg\1\blocks_quickmission\block_post_sub.group);
blocks_set; blocks_RED_BLOCK_POST1_AAA; main(scg\1\blocks_quickmission\ground\aaa\small\smart_block_post_machine_guns_red.group);
blocks_set; blocks_RED_BLOCK_POST1_DECORATIONS; main(scg\1\blocks_quickmission\ground\static\block_post_red.group);
blocks_set; blocks_BLUE_BLOCK_POST2; main(scg\1\blocks_quickmission\ground\static\block_post_blue.group);
blocks_set; blocks_BLUE_BLOCK_POST2_AAA; main(scg\1\blocks_quickmission\ground\aaa\small\smart_block_post_machine_guns_blue.group);
blocks_set; blocks_BLUE_BLOCK_POST2_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_block_post_blue.group);
blocks_set; blocks_BLUE_BLOCK_POST1_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\blue_block_post1.group);
blocks_set; blocks_BLUE_BLOCK_POST2_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\blue_block_post2.group);
blocks_set; blocks_RED_BLOCK_POST1_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\red_block_post1.group);
blocks_set; blocks_RED_BLOCK_POST2_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_block_post_red.group);
blocks_set; blocks_RED_BLOCK_POST2_AAA; main(scg\1\blocks_quickmission\ground\aaa\small\smart_block_post_machine_guns_red.group);
blocks_set; blocks_RED_BLOCK_POST1_DECORATIONS_1516; main(scg\1\blocks_quickmission\ground\static\block_post_red.group);
blocks_set; blocks_RED_BLOCK_POST2_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\red_block_post2.group);

#
## geo params
#
phase; RAC1; random(<EMPTY>); blocks_RAC1; clone_location;;
phase; RWP11; random(RAC1); blocks_RWP11; clone_location;;
phase; RWP12; at(RAC1); blocks_RWP12; clone_location;;
phase; RAC2; random(RAC1); blocks_RAC2; clone_location;;
phase; RWP21; random(RAC2); blocks_RWP21; clone_location;;
phase; RWP22; at(RAC2); blocks_RWP22; clone_location;;
phase; GAC1; random(<EMPTY>); blocks_GAC1; clone_location;;
phase; GWP11; random(GAC1); blocks_GWP11; clone_location;;
phase; GWP12; at(GAC1); blocks_GWP12; clone_location;;
phase; GAC2; random(GAC1); blocks_GAC2; clone_location;;
phase; GWP21; random(GAC2); blocks_GWP21; clone_location;;
phase; GWP22; at(GAC2); blocks_GWP22; clone_location;;
phase; GWP31; random(GMC); blocks_GWP31; clone_location;;
phase; GWP32; at(GMC); blocks_GWP32; clone_location;;
phase; RWP31; random(RMC); blocks_RWP31; clone_location;;
phase; RWP32; at(RMC); blocks_RWP32; clone_location;;
phase; GMC; random(GAC2); blocks_GMC; clone_location;;
phase; RMC; random(RAC2); blocks_RMC; clone_location;;
phase; BLUE_BLOCK_POST1; at(BLUE_BLOCK_POST1_RECON); blocks_BLUE_BLOCK_POST1; clone_location;;
phase; BLUE_BLOCK_POST1_AAA; at(BLUE_BLOCK_POST1_RECON); blocks_BLUE_BLOCK_POST1_AAA; clone_location;;
phase; BLUE_BLOCK_POST1_RECON; random(<EMPTY>); blocks_BLUE_BLOCK_POST1_RECON; clone_location;;
phase; BLUE_BLOCK_POSTS_SUB; at(BLUE_BLOCK_POST1_RECON); blocks_BLUE_BLOCK_POSTS_SUB; clone_location;;
phase; RED_BLOCK_POST1_RECON; random(<EMPTY>); blocks_RED_BLOCK_POST1_RECON; clone_location;;
phase; RED_BLOCK_POSTS_SUB; at(RED_BLOCK_POST1_RECON); blocks_RED_BLOCK_POSTS_SUB; clone_location;;
phase; RED_BLOCK_POST1_AAA; at(RED_BLOCK_POST1_RECON); blocks_RED_BLOCK_POST1_AAA; clone_location;;
phase; RED_BLOCK_POST1_DECORATIONS; at(RED_BLOCK_POST1_RECON); blocks_RED_BLOCK_POST1_DECORATIONS; clone_location;;
phase; BLUE_BLOCK_POST2; at(BLUE_BLOCK_POST2_RECON); blocks_BLUE_BLOCK_POST2; clone_location;;
phase; BLUE_BLOCK_POST2_AAA; at(BLUE_BLOCK_POST2_RECON); blocks_BLUE_BLOCK_POST2_AAA; clone_location;;
phase; BLUE_BLOCK_POST2_RECON; random(BLUE_BLOCK_POST1_RECON); blocks_BLUE_BLOCK_POST2_RECON; clone_location;;
phase; BLUE_BLOCK_POST1_SERVER_INPUT; at(BLUE_BLOCK_POST1_RECON); blocks_BLUE_BLOCK_POST1_SERVER_INPUT; clone_location;;
phase; BLUE_BLOCK_POST2_SERVER_INPUT; at(BLUE_BLOCK_POST2_RECON); blocks_BLUE_BLOCK_POST2_SERVER_INPUT; clone_location;;
phase; RED_BLOCK_POST1_SERVER_INPUT; at(RED_BLOCK_POST1_RECON); blocks_RED_BLOCK_POST1_SERVER_INPUT; clone_location;;
phase; RED_BLOCK_POST2_RECON; random(RED_BLOCK_POST1_RECON); blocks_RED_BLOCK_POST2_RECON; clone_location;;
phase; RED_BLOCK_POST2_AAA; at(RED_BLOCK_POST2_RECON); blocks_RED_BLOCK_POST2_AAA; clone_location;;
phase; RED_BLOCK_POST1_DECORATIONS_1516; at(RED_BLOCK_POST2_RECON); blocks_RED_BLOCK_POST1_DECORATIONS_1516; clone_location;;
phase; RED_BLOCK_POST2_SERVER_INPUT; at(RED_BLOCK_POST2_RECON); blocks_RED_BLOCK_POST2_SERVER_INPUT; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; RAC1(TARGET_TO_WP); RWP11(TARGET_TO_WP);
olink; RWP11(OBJECT_WP_TO_VEHICLE); RAC1(OBJECT_WP_TO_VEHICLE);
tlink; RWP11(TARGET_TO_WP); RWP12(TARGET_TO_WP);
olink; RWP12(OBJECT_WP_TO_VEHICLE); RAC1(OBJECT_WP_TO_VEHICLE);
tlink; RWP12(TARGET_TO_WP); RWP11(TARGET_TO_WP);
tlink; RAC2(TARGET_TO_WP); RWP21(TARGET_TO_WP);
olink; RWP21(OBJECT_WP_TO_VEHICLE); RAC2(OBJECT_WP_TO_VEHICLE);
tlink; RWP21(TARGET_TO_WP); RWP22(TARGET_TO_WP);
olink; RWP22(OBJECT_WP_TO_VEHICLE); RAC2(OBJECT_WP_TO_VEHICLE);
tlink; RWP22(TARGET_TO_WP); RWP21(TARGET_TO_WP);
tlink; GAC1(TARGET_TO_WP); GWP11(TARGET_TO_WP);
olink; GWP11(OBJECT_WP_TO_VEHICLE); GAC1(OBJECT_WP_TO_VEHICLE);
tlink; GWP11(TARGET_TO_WP); GWP12(TARGET_TO_WP);
olink; GWP12(OBJECT_WP_TO_VEHICLE); GAC1(OBJECT_WP_TO_VEHICLE);
tlink; GWP12(TARGET_TO_WP); GWP11(TARGET_TO_WP);
tlink; GAC2(TARGET_TO_WP); GWP21(TARGET_TO_WP);
olink; GWP21(OBJECT_WP_TO_VEHICLE); GAC2(OBJECT_WP_TO_VEHICLE);
tlink; GWP21(TARGET_TO_WP); GWP22(TARGET_TO_WP);
olink; GWP22(OBJECT_WP_TO_VEHICLE); GAC2(OBJECT_WP_TO_VEHICLE);
tlink; GWP22(TARGET_TO_WP); GWP21(TARGET_TO_WP);
tlink; GWP31(TARGET_TO_WP); GWP32(TARGET_TO_WP);
olink; GWP31(OBJECT_WP_TO_VEHICLE); GMC(OBJECT_WP_TO_VEHICLE);
tlink; GWP32(TARGET_TO_WP); GWP31(TARGET_TO_WP);
olink; GWP32(OBJECT_WP_TO_VEHICLE); GMC(OBJECT_WP_TO_VEHICLE);
tlink; RWP31(TARGET_TO_WP); RWP32(TARGET_TO_WP);
olink; RWP31(OBJECT_WP_TO_VEHICLE); RMC(OBJECT_WP_TO_VEHICLE);
tlink; RWP32(TARGET_TO_WP); RWP31(TARGET_TO_WP);
olink; RWP32(OBJECT_WP_TO_VEHICLE); RMC(OBJECT_WP_TO_VEHICLE);
tlink; GMC(TARGET_TO_WP); GWP31(TARGET_TO_WP);
tlink; RMC(TARGET_TO_WP); RWP31(TARGET_TO_WP);
tlink; BLUE_BLOCK_POST1_RECON(block_postSUBblue); BLUE_BLOCK_POSTS_SUB(block_postSUBblue);
tlink; BLUE_BLOCK_POST1_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BLOCK_POST1_AAA(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BLOCK_POST1_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BLOCK_POST1_AAA(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BLOCK_POST1_RECON(block_postSUBred); RED_BLOCK_POSTS_SUB(block_postSUBred);
tlink; RED_BLOCK_POST1_RECON(ACTIVATE_MACHINE_GUNS); RED_BLOCK_POST1_AAA(ACTIVATE_MACHINE_GUNS);
tlink; RED_BLOCK_POST1_RECON(DEACTIVATE_MACHINE_GUNS); RED_BLOCK_POST1_AAA(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BLOCK_POST2_RECON(block_postSUBblue); BLUE_BLOCK_POSTS_SUB(block_postSUBblue);
tlink; BLUE_BLOCK_POST2_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BLOCK_POST2_AAA(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BLOCK_POST2_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BLOCK_POST2_AAA(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BLOCK_POST1_SERVER_INPUT(SERVER_INPUT); BLUE_BLOCK_POST1_RECON(SERVER_INPUT);
tlink; BLUE_BLOCK_POST1_SERVER_INPUT(block_postKILLSUBblue); BLUE_BLOCK_POSTS_SUB(block_postKILLSUBblue);
tlink; BLUE_BLOCK_POST2_SERVER_INPUT(block_postKILLSUBblue); BLUE_BLOCK_POSTS_SUB(block_postKILLSUBblue);
tlink; BLUE_BLOCK_POST2_SERVER_INPUT(SERVER_INPUT); BLUE_BLOCK_POST2_RECON(SERVER_INPUT);
tlink; RED_BLOCK_POST1_SERVER_INPUT(SERVER_INPUT); RED_BLOCK_POST1_RECON(SERVER_INPUT);
tlink; RED_BLOCK_POST1_SERVER_INPUT(block_postKILLSUBred); RED_BLOCK_POSTS_SUB(block_postKILLSUBred);
tlink; RED_BLOCK_POST2_RECON(block_postSUBred); RED_BLOCK_POSTS_SUB(block_postSUBred);
tlink; RED_BLOCK_POST2_RECON(ACTIVATE_MACHINE_GUNS); RED_BLOCK_POST2_AAA(ACTIVATE_MACHINE_GUNS);
tlink; RED_BLOCK_POST2_RECON(DEACTIVATE_MACHINE_GUNS); RED_BLOCK_POST2_AAA(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BLOCK_POST2_SERVER_INPUT(SERVER_INPUT); RED_BLOCK_POST2_RECON(SERVER_INPUT);
tlink; RED_BLOCK_POST2_SERVER_INPUT(block_postKILLSUBred); RED_BLOCK_POSTS_SUB(block_postKILLSUBred);

#
## conditions
#
check; RAC1; location_type(Decoration,Transport);
check; RAC1; coalition(f);
check; RAC1; in_radius(PRIMARY_LINK_PHASE,100000);
check; RAC1; free();
check; RWP11; location_type(Decoration,Transport);
check; RWP11; coalition(f);
check; RWP11; range(PRIMARY_LINK_PHASE,closest_outof,15000);
check; RWP11; free();
check; RAC2; location_type(Decoration,Transport);
check; RAC2; coalition(f);
check; RAC2; in_radius(PRIMARY_LINK_PHASE,100000);
check; RAC2; free();
check; RWP21; location_type(Decoration,Transport);
check; RWP21; coalition(f);
check; RWP21; range(PRIMARY_LINK_PHASE,closest_outof,15000);
check; RWP21; free();
check; GAC1; location_type(Decoration,Transport);
check; GAC1; coalition(e);
check; GAC1; in_radius(PRIMARY_LINK_PHASE,100000);
check; GAC1; free();
check; GWP11; location_type(Decoration,Transport);
check; GWP11; coalition(e);
check; GWP11; range(PRIMARY_LINK_PHASE,closest_outof,15000);
check; GWP11; free();
check; GAC2; location_type(Decoration,Transport);
check; GAC2; coalition(e);
check; GAC2; in_radius(PRIMARY_LINK_PHASE,100000);
check; GAC2; free();
check; GWP21; location_type(Decoration,Transport);
check; GWP21; coalition(e);
check; GWP21; range(PRIMARY_LINK_PHASE,closest_outof,15000);
check; GWP21; free();
check; GWP31; location_type(Decoration,Transport);
check; GWP31; coalition(e);
check; GWP31; range(PRIMARY_LINK_PHASE,closest_outof,15000);
check; GWP31; free();
check; RWP31; location_type(Decoration,Transport);
check; RWP31; coalition(f);
check; RWP31; range(PRIMARY_LINK_PHASE,closest_outof,15000);
check; RWP31; free();
check; GMC; location_type(Decoration,Transport);
check; GMC; coalition(e);
check; GMC; in_radius(PRIMARY_LINK_PHASE,100000);
check; GMC; free();
check; RMC; location_type(Decoration,Transport);
check; RMC; coalition(f);
check; RMC; in_radius(PRIMARY_LINK_PHASE,100000);
check; RMC; free();
check; BLUE_BLOCK_POST1_RECON; free();
check; BLUE_BLOCK_POST1_RECON; in_radius(PRIMARY_LINK_PHASE,120000);
check; BLUE_BLOCK_POST1_RECON; coalition(e);
check; BLUE_BLOCK_POST1_RECON; location_type(GroundObjective,Transport);
check; RED_BLOCK_POST1_RECON; coalition(f);
check; RED_BLOCK_POST1_RECON; free();
check; RED_BLOCK_POST1_RECON; location_type(GroundObjective,Transport);
check; RED_BLOCK_POST1_RECON; in_radius(PRIMARY_LINK_PHASE,150000);
check; BLUE_BLOCK_POST2_RECON; free();
check; BLUE_BLOCK_POST2_RECON; coalition(e);
check; BLUE_BLOCK_POST2_RECON; location_type(GroundObjective,Transport);
check; BLUE_BLOCK_POST2_RECON; range(PRIMARY_LINK_PHASE,closest_outof,40000);
check; RED_BLOCK_POST2_RECON; coalition(f);
check; RED_BLOCK_POST2_RECON; free();
check; RED_BLOCK_POST2_RECON; location_type(GroundObjective,Transport);
check; RED_BLOCK_POST2_RECON; range(PRIMARY_LINK_PHASE,closest_outof,35000);

#
## property actions
#
action; RAC1(VEHICLE_0_TYPE,Model); set_model(APC-arm-car,Allies:APC-arm-car:BA10M);
action; RAC1(VEHICLE_1_TYPE,Model); set_model(Cargo truck,Allies:Cargo truck:GAZ-AA);
action; RAC1(VEHICLE_2_TYPE,Model); set_model(Cargo truck,Allies:Cargo truck:GAZ-AA);
action; RAC1(VEHICLE_3_TYPE,Model); set_model(Cargo truck,Allies:Cargo truck:GAZ-AA);
action; RAC1(VEHICLE_4_TYPE,Model); set_model(Staff car,Allies:Staff car:GAZ-M);
action; RAC1(VEHICLE_5_TYPE,Model); set_model(AAA SP cannon,Allies:AAA SP cannon:gaz-aa-m4-aa);
action; RAC2(VEHICLE_0_TYPE,Model); set_model(APC-arm-car,Allies:APC-arm-car:BA10M);
action; RAC2(VEHICLE_1_TYPE,Model); set_model(Cargo truck,Allies:Cargo truck:GAZ-AA);
action; RAC2(VEHICLE_2_TYPE,Model); set_model(Cargo truck,Allies:Cargo truck:GAZ-AA);
action; RAC2(VEHICLE_3_TYPE,Model); set_model(Cargo truck,Allies:Cargo truck:GAZ-AA);
action; RAC2(VEHICLE_4_TYPE,Model); set_model(Staff car,Allies:Staff car:GAZ-M);
action; RAC2(VEHICLE_5_TYPE,Model); set_model(AAA SP cannon,Allies:AAA SP cannon:gaz-aa-m4-aa);
action; GAC1(VEHICLE_0_TYPE,Model); set_model(Staff car,Axis:Staff car:merc22);
action; GAC1(VEHICLE_1_TYPE,Model); set_model(AAA SP cannon,Axis:AAA SP cannon:SdKfz10-Flak38);
action; GAC1(VEHICLE_2_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:Opel-Blitz);
action; GAC1(VEHICLE_3_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:Opel-Blitz);
action; GAC1(VEHICLE_4_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:ford-G917);
action; GAC1(VEHICLE_5_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:ford-G917);
action; GAC2(VEHICLE_0_TYPE,Model); set_model(Staff car,Axis:Staff car:merc22);
action; GAC2(VEHICLE_1_TYPE,Model); set_model(AAA SP cannon,Axis:AAA SP cannon:SdKfz10-Flak38);
action; GAC2(VEHICLE_2_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:Opel-Blitz);
action; GAC2(VEHICLE_3_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:Opel-Blitz);
action; GAC2(VEHICLE_4_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:ford-G917);
action; GAC2(VEHICLE_5_TYPE,Model); set_model(Cargo truck,Axis:Cargo truck:ford-G917);
action; GMC(VEHICLE_0_TYPE,Model); set_model(Tank,Axis:Tank:Stug37L24);
action; GMC(VEHICLE_1_TYPE,Model); set_model(Tank,Axis:Tank:Stug37L24);
action; GMC(VEHICLE_2_TYPE,Model); set_model(Tank,Axis:Tank:PzIV-G);
action; GMC(VEHICLE_3_TYPE,Model); set_model(Tank,Axis:Tank:PzIV-G);
action; GMC(VEHICLE_4_TYPE,Model); set_model(AAA SP cannon,Axis:AAA SP cannon:SdKfz10-Flak38);
action; GMC(VEHICLE_5_TYPE,Model); set_model(Tank,Axis:Tank:PzIII-L);
action; GMC(VEHICLE_6_TYPE,Model); set_model(Tank,Axis:Tank:PzIII-L);
action; GMC(VEHICLE_7_TYPE,Model); set_model(AAA SP cannon,Axis:AAA SP cannon:SdKfz10-Flak38);
action; RMC(VEHICLE_0_TYPE,Model); set_model(Tank,Allies:Tank:BT7M);
action; RMC(VEHICLE_1_TYPE,Model); set_model(Tank,Allies:Tank:BT7M);
action; RMC(VEHICLE_2_TYPE,Model); set_model(Tank,Allies:Tank:T70);
action; RMC(VEHICLE_3_TYPE,Model); set_model(Tank,Allies:Tank:T70);
action; RMC(VEHICLE_4_TYPE,Model); set_model(AAA SP cannon,Allies:AAA SP cannon:gaz-aa-m4-aa);
action; RMC(VEHICLE_5_TYPE,Model); set_model(Tank,Allies:Tank:T34-76STZ);
action; RMC(VEHICLE_6_TYPE,Model); set_model(Tank,Allies:Tank:T34-76STZ);
action; RMC(VEHICLE_7_TYPE,Model); set_model(AAA SP cannon,Allies:AAA SP cannon:gaz-aa-m4-aa);
action; BLUE_BLOCK_POST1_AAA(MG,AILevel); <empty>();
action; BLUE_BLOCK_POST1_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_BLOCK_POST1_RECON(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_BLOCK_POST1_RECON(RECON_OBJ,Success); set(Success,1);
action; BLUE_BLOCK_POST1_RECON(Tank,Zone); <empty>();
action; BLUE_BLOCK_POST1_RECON(Plane_in,Zone); set(Zone,1750);
action; BLUE_BLOCK_POST1_RECON(Plane_in,YPos); <empty>();
action; BLUE_BLOCK_POST1_RECON(Plane_out,Zone); set(Zone,2000);
action; BLUE_BLOCK_POST1_RECON(Plane_out,YPos); <empty>();
action; RED_BLOCK_POST1_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_BLOCK_POST1_RECON(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_BLOCK_POST1_RECON(RECON_OBJ,Success); set(Success,1);
action; RED_BLOCK_POST1_RECON(Tank,Zone); <empty>();
action; RED_BLOCK_POST1_RECON(Plane_in,Zone); set(Zone,1750);
action; RED_BLOCK_POST1_RECON(Plane_in,YPos); <empty>();
action; RED_BLOCK_POST1_RECON(Plane_out,Zone); set(Zone,2000);
action; RED_BLOCK_POST1_RECON(Plane_out,YPos); <empty>();
action; RED_BLOCK_POST1_AAA(MG,AILevel); <empty>();
action; BLUE_BLOCK_POST2_AAA(MG,AILevel); <empty>();
action; BLUE_BLOCK_POST2_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_BLOCK_POST2_RECON(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_BLOCK_POST2_RECON(RECON_OBJ,Success); set(Success,1);
action; BLUE_BLOCK_POST2_RECON(Tank,Zone); <empty>();
action; BLUE_BLOCK_POST2_RECON(Plane_in,Zone); set(Zone,1750);
action; BLUE_BLOCK_POST2_RECON(Plane_in,YPos); <empty>();
action; BLUE_BLOCK_POST2_RECON(Plane_out,Zone); set(Zone,2000);
action; BLUE_BLOCK_POST2_RECON(Plane_out,YPos); <empty>();
action; RED_BLOCK_POST2_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_BLOCK_POST2_RECON(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_BLOCK_POST2_RECON(RECON_OBJ,Success); set(Success,1);
action; RED_BLOCK_POST2_RECON(Tank,Zone); <empty>();
action; RED_BLOCK_POST2_RECON(Plane_in,Zone); set(Zone,1750);
action; RED_BLOCK_POST2_RECON(Plane_in,YPos); <empty>();
action; RED_BLOCK_POST2_RECON(Plane_out,Zone); set(Zone,2000);
action; RED_BLOCK_POST2_RECON(Plane_out,YPos); <empty>();
action; RED_BLOCK_POST2_AAA(MG,AILevel); <empty>();

#
## unlinks
#

#
## gui helpers
#
gui_helper; RAC1; 1269; 8341;
gui_helper; RWP11; 1615; 8465;
gui_helper; RWP12; 1275; 8594;
gui_helper; RAC2; 1905; 8988;
gui_helper; RWP21; 2291; 9088;
gui_helper; RWP22; 1903; 9218;
gui_helper; GAC1; -2019; 8326;
gui_helper; GWP11; -1600; 8443;
gui_helper; GWP12; -2017; 8558;
gui_helper; GAC2; -2638; 8977;
gui_helper; GWP21; -2236; 9077;
gui_helper; GWP22; -2631; 9180;
gui_helper; GWP31; -2863; 9600;
gui_helper; GWP32; -3294; 9720;
gui_helper; RWP31; 2944; 9678;
gui_helper; RWP32; 2594; 9797;
gui_helper; GMC; -3302; 9506;
gui_helper; RMC; 2570; 9561;
gui_helper; BLUE_BLOCK_POST1; -6239; 7466;
gui_helper; BLUE_BLOCK_POST1_AAA; -5869; 7472;
gui_helper; BLUE_BLOCK_POST1_RECON; -6232; 7256;
gui_helper; BLUE_BLOCK_POSTS_SUB; -5310; 7771;
gui_helper; RED_BLOCK_POST1_RECON; 5127; 7232;
gui_helper; RED_BLOCK_POSTS_SUB; 5983; 7715;
gui_helper; RED_BLOCK_POST1_AAA; 5517; 7448;
gui_helper; RED_BLOCK_POST1_DECORATIONS; 5134; 7437;
gui_helper; BLUE_BLOCK_POST2; -6218; 8329;
gui_helper; BLUE_BLOCK_POST2_AAA; -5839; 8327;
gui_helper; BLUE_BLOCK_POST2_RECON; -6218; 8109;
gui_helper; BLUE_BLOCK_POST1_SERVER_INPUT; -5870; 7256;
gui_helper; BLUE_BLOCK_POST2_SERVER_INPUT; -5845; 8124;
gui_helper; RED_BLOCK_POST1_SERVER_INPUT; 5507; 7230;
gui_helper; RED_BLOCK_POST2_RECON; 5163; 8130;
gui_helper; RED_BLOCK_POST2_AAA; 5535; 8362;
gui_helper; RED_BLOCK_POST1_DECORATIONS_1516; 5165; 8347;
gui_helper; RED_BLOCK_POST2_SERVER_INPUT; 5529; 8133;
gui_helper; check; 1472; 8100;RAC1(location_type)
gui_helper; check; 1469; 8136;RAC1(coalition)
gui_helper; check; 1476; 8211;RAC1(in_radius)
gui_helper; check; 1472; 8170;RAC1(free)
gui_helper; check; 1685; 8321;RWP11(location_type)
gui_helper; check; 1686; 8356;RWP11(coalition)
gui_helper; check; 1684; 8426;RWP11(range)
gui_helper; check; 1684; 8389;RWP11(free)
gui_helper; check; 2099; 8758;RAC2(location_type)
gui_helper; check; 2099; 8792;RAC2(coalition)
gui_helper; check; 2101; 8864;RAC2(in_radius)
gui_helper; check; 2102; 8827;RAC2(free)
gui_helper; check; 2352; 8952;RWP21(location_type)
gui_helper; check; 2351; 8987;RWP21(coalition)
gui_helper; check; 2350; 9060;RWP21(range)
gui_helper; check; 2351; 9022;RWP21(free)
gui_helper; check; -1816; 8107;GAC1(location_type)
gui_helper; check; -1815; 8143;GAC1(coalition)
gui_helper; check; -1808; 8208;GAC1(in_radius)
gui_helper; check; -1813; 8177;GAC1(free)
gui_helper; check; -1533; 8294;GWP11(location_type)
gui_helper; check; -1532; 8329;GWP11(coalition)
gui_helper; check; -1531; 8399;GWP11(range)
gui_helper; check; -1532; 8365;GWP11(free)
gui_helper; check; -2440; 8779;GAC2(location_type)
gui_helper; check; -2439; 8812;GAC2(coalition)
gui_helper; check; -2438; 8873;GAC2(in_radius)
gui_helper; check; -2438; 8843;GAC2(free)
gui_helper; check; -2173; 8948;GWP21(location_type)
gui_helper; check; -2173; 8984;GWP21(coalition)
gui_helper; check; -2170; 9054;GWP21(range)
gui_helper; check; -2172; 9019;GWP21(free)
gui_helper; check; -2710; 9478;GWP31(location_type)
gui_helper; check; -2707; 9511;GWP31(coalition)
gui_helper; check; -2704; 9574;GWP31(range)
gui_helper; check; -2705; 9541;GWP31(free)
gui_helper; check; 3011; 9537;RWP31(location_type)
gui_helper; check; 3011; 9569;RWP31(coalition)
gui_helper; check; 3010; 9639;RWP31(range)
gui_helper; check; 3009; 9602;RWP31(free)
gui_helper; check; -3088; 9250;GMC(location_type)
gui_helper; check; -3089; 9282;GMC(coalition)
gui_helper; check; -3087; 9344;GMC(in_radius)
gui_helper; check; -3088; 9313;GMC(free)
gui_helper; check; 2796; 9308;RMC(location_type)
gui_helper; check; 2795; 9347;RMC(coalition)
gui_helper; check; 2795; 9411;RMC(in_radius)
gui_helper; check; 2795; 9380;RMC(free)
gui_helper; check; -6045; 7185;BLUE_BLOCK_POST1_RECON(free)
gui_helper; check; -6046; 7216;BLUE_BLOCK_POST1_RECON(in_radius)
gui_helper; check; -6044; 7152;BLUE_BLOCK_POST1_RECON(coalition)
gui_helper; check; -6044; 7118;BLUE_BLOCK_POST1_RECON(location_type)
gui_helper; check; 5303; 7120;RED_BLOCK_POST1_RECON(coalition)
gui_helper; check; 5304; 7153;RED_BLOCK_POST1_RECON(free)
gui_helper; check; 5304; 7088;RED_BLOCK_POST1_RECON(location_type)
gui_helper; check; 5306; 7184;RED_BLOCK_POST1_RECON(in_radius)
gui_helper; check; -6031; 8038;BLUE_BLOCK_POST2_RECON(free)
gui_helper; check; -6030; 8005;BLUE_BLOCK_POST2_RECON(coalition)
gui_helper; check; -6030; 7971;BLUE_BLOCK_POST2_RECON(location_type)
gui_helper; check; -6032; 8073;BLUE_BLOCK_POST2_RECON(range)
gui_helper; check; 5339; 8018;RED_BLOCK_POST2_RECON(coalition)
gui_helper; check; 5340; 8051;RED_BLOCK_POST2_RECON(free)
gui_helper; check; 5340; 7986;RED_BLOCK_POST2_RECON(location_type)
gui_helper; check; 5342; 8085;RED_BLOCK_POST2_RECON(range)
gui_helper; Model; 1338; 8111;RAC1; (VEHICLE_0_TYPE);
gui_helper; Model; 1338; 8151;RAC1; (VEHICLE_1_TYPE);
gui_helper; Model; 1338; 8191;RAC1; (VEHICLE_2_TYPE);
gui_helper; Model; 1338; 8231;RAC1; (VEHICLE_3_TYPE);
gui_helper; Model; 1338; 8271;RAC1; (VEHICLE_4_TYPE);
gui_helper; Model; 1338; 8311;RAC1; (VEHICLE_5_TYPE);
gui_helper; Model; 1974; 8758;RAC2; (VEHICLE_0_TYPE);
gui_helper; Model; 1974; 8798;RAC2; (VEHICLE_1_TYPE);
gui_helper; Model; 1974; 8838;RAC2; (VEHICLE_2_TYPE);
gui_helper; Model; 1974; 8878;RAC2; (VEHICLE_3_TYPE);
gui_helper; Model; 1974; 8918;RAC2; (VEHICLE_4_TYPE);
gui_helper; Model; 1974; 8958;RAC2; (VEHICLE_5_TYPE);
gui_helper; Model; -1935; 8094;GAC1; (VEHICLE_0_TYPE);
gui_helper; Model; -1935; 8134;GAC1; (VEHICLE_1_TYPE);
gui_helper; Model; -1935; 8174;GAC1; (VEHICLE_2_TYPE);
gui_helper; Model; -1935; 8214;GAC1; (VEHICLE_3_TYPE);
gui_helper; Model; -1935; 8254;GAC1; (VEHICLE_4_TYPE);
gui_helper; Model; -1935; 8294;GAC1; (VEHICLE_5_TYPE);
gui_helper; Model; -2554; 8745;GAC2; (VEHICLE_0_TYPE);
gui_helper; Model; -2554; 8785;GAC2; (VEHICLE_1_TYPE);
gui_helper; Model; -2554; 8825;GAC2; (VEHICLE_2_TYPE);
gui_helper; Model; -2554; 8865;GAC2; (VEHICLE_3_TYPE);
gui_helper; Model; -2554; 8905;GAC2; (VEHICLE_4_TYPE);
gui_helper; Model; -2554; 8945;GAC2; (VEHICLE_5_TYPE);
gui_helper; Model; -3224; 9256;GMC; (VEHICLE_0_TYPE);
gui_helper; Model; -3221; 9288;GMC; (VEHICLE_1_TYPE);
gui_helper; Model; -3221; 9322;GMC; (VEHICLE_2_TYPE);
gui_helper; Model; -3221; 9356;GMC; (VEHICLE_3_TYPE);
gui_helper; Model; -3221; 9389;GMC; (VEHICLE_4_TYPE);
gui_helper; Model; -3221; 9424;GMC; (VEHICLE_5_TYPE);
gui_helper; Model; -3220; 9458;GMC; (VEHICLE_6_TYPE);
gui_helper; Model; -3220; 9490;GMC; (VEHICLE_7_TYPE);
gui_helper; Model; 2642; 9284;RMC; (VEHICLE_0_TYPE);
gui_helper; Model; 2644; 9323;RMC; (VEHICLE_1_TYPE);
gui_helper; Model; 2644; 9359;RMC; (VEHICLE_2_TYPE);
gui_helper; Model; 2642; 9393;RMC; (VEHICLE_3_TYPE);
gui_helper; Model; 2645; 9429;RMC; (VEHICLE_4_TYPE);
gui_helper; Model; 2647; 9465;RMC; (VEHICLE_5_TYPE);
gui_helper; Model; 2649; 9501;RMC; (VEHICLE_6_TYPE);
gui_helper; Model; 2648; 9536;RMC; (VEHICLE_7_TYPE);
gui_helper; AILevel; -5799; 7451;BLUE_BLOCK_POST1_AAA; (MG);
gui_helper; TaskType; -6168; 7094;BLUE_BLOCK_POST1_RECON; (RECON_OBJ);
gui_helper; Coalition; -6169; 7133;BLUE_BLOCK_POST1_RECON; (RECON_OBJ);
gui_helper; Success; -6168; 7174;BLUE_BLOCK_POST1_RECON; (RECON_OBJ);
gui_helper; Zone; -6168; 7215;BLUE_BLOCK_POST1_RECON; (Tank);
gui_helper; Zone; -5832; 7106;BLUE_BLOCK_POST1_RECON; (Plane_in);
gui_helper; YPos; -5832; 7146;BLUE_BLOCK_POST1_RECON; (Plane_in);
gui_helper; Zone; -5832; 7186;BLUE_BLOCK_POST1_RECON; (Plane_out);
gui_helper; YPos; -5832; 7226;BLUE_BLOCK_POST1_RECON; (Plane_out);
gui_helper; TaskType; 5186; 7077;RED_BLOCK_POST1_RECON; (RECON_OBJ);
gui_helper; Coalition; 5186; 7117;RED_BLOCK_POST1_RECON; (RECON_OBJ);
gui_helper; Success; 5185; 7158;RED_BLOCK_POST1_RECON; (RECON_OBJ);
gui_helper; Zone; 5185; 7195;RED_BLOCK_POST1_RECON; (Tank);
gui_helper; Zone; 5527; 7082;RED_BLOCK_POST1_RECON; (Plane_in);
gui_helper; YPos; 5527; 7122;RED_BLOCK_POST1_RECON; (Plane_in);
gui_helper; Zone; 5527; 7162;RED_BLOCK_POST1_RECON; (Plane_out);
gui_helper; YPos; 5527; 7202;RED_BLOCK_POST1_RECON; (Plane_out);
gui_helper; AILevel; 5574; 7401;RED_BLOCK_POST1_AAA; (MG);
gui_helper; AILevel; -5777; 8305;BLUE_BLOCK_POST2_AAA; (MG);
gui_helper; TaskType; -6154; 7948;BLUE_BLOCK_POST2_RECON; (RECON_OBJ);
gui_helper; Coalition; -6155; 7987;BLUE_BLOCK_POST2_RECON; (RECON_OBJ);
gui_helper; Success; -6154; 8028;BLUE_BLOCK_POST2_RECON; (RECON_OBJ);
gui_helper; Zone; -6154; 8068;BLUE_BLOCK_POST2_RECON; (Tank);
gui_helper; Zone; -5818; 7959;BLUE_BLOCK_POST2_RECON; (Plane_in);
gui_helper; YPos; -5818; 7999;BLUE_BLOCK_POST2_RECON; (Plane_in);
gui_helper; Zone; -5818; 8039;BLUE_BLOCK_POST2_RECON; (Plane_out);
gui_helper; YPos; -5818; 8079;BLUE_BLOCK_POST2_RECON; (Plane_out);
gui_helper; TaskType; 5222; 7975;RED_BLOCK_POST2_RECON; (RECON_OBJ);
gui_helper; Coalition; 5222; 8015;RED_BLOCK_POST2_RECON; (RECON_OBJ);
gui_helper; Success; 5221; 8056;RED_BLOCK_POST2_RECON; (RECON_OBJ);
gui_helper; Zone; 5221; 8093;RED_BLOCK_POST2_RECON; (Tank);
gui_helper; Zone; 5563; 7980;RED_BLOCK_POST2_RECON; (Plane_in);
gui_helper; YPos; 5563; 8020;RED_BLOCK_POST2_RECON; (Plane_in);
gui_helper; Zone; 5563; 8060;RED_BLOCK_POST2_RECON; (Plane_out);
gui_helper; YPos; 5563; 8100;RED_BLOCK_POST2_RECON; (Plane_out);
gui_helper; AILevel; 5599; 8323;RED_BLOCK_POST2_AAA; (MG);
