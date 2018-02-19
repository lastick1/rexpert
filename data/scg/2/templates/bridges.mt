# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_BLUE_BRIDGE1_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_bridge_blue.group);
blocks_set; blocks_BLUE_BRIDGES_SUB; main(scg\1\blocks_quickmission\bridge_sub.group);
blocks_set; blocks_RED_BRIDGE1_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_bridge_red.group);
blocks_set; blocks_RED_BRIDGES_SUB; main(scg\1\blocks_quickmission\bridge_sub.group);
blocks_set; blocks_BLUE_BRIDGE1_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\blue_bridge1.group);
blocks_set; blocks_BLUE_BRIDGE2_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_bridge_blue.group);
blocks_set; blocks_BLUE_BRIDGE2_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\blue_bridge2.group);
blocks_set; blocks_RED_BRIDGE1_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\red_bridge1.group);
blocks_set; blocks_RED_BRIDGE2_RECON; main(scg\1\blocks_quickmission\ground\recon\recon_bridge_red.group);
blocks_set; blocks_RED_BRIDGE2_SERVER_INPUT; main(scg\1\blocks_quickmission\inputs\red_bridge2.group);
blocks_set; blocks_RED_BRIDGE1_MACHINE_GUN1; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_RED_BRIDGE1_MACHINE_GUN2; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_RED_BRIDGE2_MACHINE_GUN1; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_RED_BRIDGE2_MACHINE_GUN2; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_BLUE_BRIDGE2_MACHINE_GUN1; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_BLUE_BRIDGE2_MACHINE_GUN2; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_BLUE_BRIDGE1_MACHINE_GUN1; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);
blocks_set; blocks_BLUE_BRIDGE1_MACHINE_GUN2; main(scg\1\blocks_quickmission\ground\aaa\small\smart_machine_gun_no_spawner.group);

#
## geo params
#
phase; BLUE_BRIDGE1_RECON; random(<EMPTY>); blocks_BLUE_BRIDGE1_RECON; clone_location;;
phase; BLUE_BRIDGES_SUB; at(BLUE_BRIDGE1_RECON); blocks_BLUE_BRIDGES_SUB; clone_location;;
phase; RED_BRIDGE1_RECON; random(<EMPTY>); blocks_RED_BRIDGE1_RECON; clone_location;;
phase; RED_BRIDGES_SUB; at(RED_BRIDGE1_RECON); blocks_RED_BRIDGES_SUB; clone_location;;
phase; BLUE_BRIDGE1_SERVER_INPUT; at(BLUE_BRIDGE1_RECON); blocks_BLUE_BRIDGE1_SERVER_INPUT; clone_location;;
phase; BLUE_BRIDGE2_RECON; random(BLUE_BRIDGE1_RECON); blocks_BLUE_BRIDGE2_RECON; clone_location;;
phase; BLUE_BRIDGE2_SERVER_INPUT; at(BLUE_BRIDGE2_RECON); blocks_BLUE_BRIDGE2_SERVER_INPUT; clone_location;;
phase; RED_BRIDGE1_SERVER_INPUT; at(RED_BRIDGE1_RECON); blocks_RED_BRIDGE1_SERVER_INPUT; clone_location;;
phase; RED_BRIDGE2_RECON; random(RED_BRIDGE1_RECON); blocks_RED_BRIDGE2_RECON; clone_location;;
phase; RED_BRIDGE2_SERVER_INPUT; at(RED_BRIDGE2_RECON); blocks_RED_BRIDGE2_SERVER_INPUT; clone_location;;
phase; RED_BRIDGE1_MACHINE_GUN1; random(RED_BRIDGE1_RECON); blocks_RED_BRIDGE1_MACHINE_GUN1; clone_location;;
phase; RED_BRIDGE1_MACHINE_GUN2; random(RED_BRIDGE1_RECON); blocks_RED_BRIDGE1_MACHINE_GUN2; clone_location;;
phase; RED_BRIDGE2_MACHINE_GUN1; random(RED_BRIDGE2_RECON); blocks_RED_BRIDGE2_MACHINE_GUN1; clone_location;;
phase; RED_BRIDGE2_MACHINE_GUN2; random(RED_BRIDGE2_RECON); blocks_RED_BRIDGE2_MACHINE_GUN2; clone_location;;
phase; BLUE_BRIDGE2_MACHINE_GUN1; random(BLUE_BRIDGE2_RECON); blocks_BLUE_BRIDGE2_MACHINE_GUN1; clone_location;;
phase; BLUE_BRIDGE2_MACHINE_GUN2; random(BLUE_BRIDGE2_RECON); blocks_BLUE_BRIDGE2_MACHINE_GUN2; clone_location;;
phase; BLUE_BRIDGE1_MACHINE_GUN1; random(BLUE_BRIDGE1_RECON); blocks_BLUE_BRIDGE1_MACHINE_GUN1; clone_location;;
phase; BLUE_BRIDGE1_MACHINE_GUN2; random(BLUE_BRIDGE1_RECON); blocks_BLUE_BRIDGE1_MACHINE_GUN2; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; BLUE_BRIDGE1_RECON(bridgeSUBblue); BLUE_BRIDGES_SUB(bridgeSUBblue);
tlink; BLUE_BRIDGE1_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BRIDGE1_MACHINE_GUN1(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE1_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BRIDGE1_MACHINE_GUN1(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE1_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BRIDGE1_MACHINE_GUN2(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE1_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BRIDGE1_MACHINE_GUN2(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE1_RECON(bridgeSUBred); RED_BRIDGES_SUB(bridgeSUBred);
tlink; RED_BRIDGE1_RECON(ACTIVATE_MACHINE_GUNS); RED_BRIDGE1_MACHINE_GUN1(ACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE1_RECON(DEACTIVATE_MACHINE_GUNS); RED_BRIDGE1_MACHINE_GUN1(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE1_RECON(ACTIVATE_MACHINE_GUNS); RED_BRIDGE1_MACHINE_GUN2(ACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE1_RECON(DEACTIVATE_MACHINE_GUNS); RED_BRIDGE1_MACHINE_GUN2(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE1_SERVER_INPUT(bridgeKILLSUBblue); BLUE_BRIDGES_SUB(bridgeKILLSUBblue);
tlink; BLUE_BRIDGE1_SERVER_INPUT(SERVER_INPUT); BLUE_BRIDGE1_RECON(SERVER_INPUT);
tlink; BLUE_BRIDGE2_RECON(bridgeSUBblue); BLUE_BRIDGES_SUB(bridgeSUBblue);
tlink; BLUE_BRIDGE2_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BRIDGE2_MACHINE_GUN1(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE2_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BRIDGE2_MACHINE_GUN1(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE2_RECON(ACTIVATE_MACHINE_GUNS); BLUE_BRIDGE2_MACHINE_GUN2(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE2_RECON(DEACTIVATE_MACHINE_GUNS); BLUE_BRIDGE2_MACHINE_GUN2(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_BRIDGE2_SERVER_INPUT(SERVER_INPUT); BLUE_BRIDGE2_RECON(SERVER_INPUT);
tlink; BLUE_BRIDGE2_SERVER_INPUT(bridgeKILLSUBblue); BLUE_BRIDGES_SUB(bridgeKILLSUBblue);
tlink; RED_BRIDGE1_SERVER_INPUT(SERVER_INPUT); RED_BRIDGE1_RECON(SERVER_INPUT);
tlink; RED_BRIDGE1_SERVER_INPUT(bridgeKILLSUBred); RED_BRIDGES_SUB(bridgeKILLSUBred);
tlink; RED_BRIDGE2_RECON(bridgeSUBred); RED_BRIDGES_SUB(bridgeSUBred);
tlink; RED_BRIDGE2_RECON(ACTIVATE_MACHINE_GUNS); RED_BRIDGE2_MACHINE_GUN1(ACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE2_RECON(DEACTIVATE_MACHINE_GUNS); RED_BRIDGE2_MACHINE_GUN1(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE2_RECON(ACTIVATE_MACHINE_GUNS); RED_BRIDGE2_MACHINE_GUN2(ACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE2_RECON(DEACTIVATE_MACHINE_GUNS); RED_BRIDGE2_MACHINE_GUN2(DEACTIVATE_MACHINE_GUNS);
tlink; RED_BRIDGE2_SERVER_INPUT(bridgeKILLSUBred); RED_BRIDGES_SUB(bridgeKILLSUBred);
tlink; RED_BRIDGE2_SERVER_INPUT(SERVER_INPUT); RED_BRIDGE2_RECON(SERVER_INPUT);

#
## conditions
#
check; BLUE_BRIDGE1_RECON; location_type(Decoration,Bridge);
check; BLUE_BRIDGE1_RECON; coalition(e);
check; BLUE_BRIDGE1_RECON; free();
check; BLUE_BRIDGE1_RECON; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_BRIDGE1_RECON; in_radius(PRIMARY_LINK_PHASE,120000);
check; RED_BRIDGE1_RECON; location_type(Decoration,Bridge);
check; RED_BRIDGE1_RECON; free();
check; RED_BRIDGE1_RECON; coalition(f);
check; BLUE_BRIDGE2_RECON; location_type(Decoration,Bridge);
check; BLUE_BRIDGE2_RECON; coalition(e);
check; BLUE_BRIDGE2_RECON; free();
check; BLUE_BRIDGE2_RECON; range(PRIMARY_LINK_PHASE,closest_outof,40000);
check; RED_BRIDGE2_RECON; location_type(Decoration,Bridge);
check; RED_BRIDGE2_RECON; free();
check; RED_BRIDGE2_RECON; coalition(f);
check; RED_BRIDGE2_RECON; range(PRIMARY_LINK_PHASE,closest_outof,35000);
check; RED_BRIDGE1_MACHINE_GUN1; free();
check; RED_BRIDGE1_MACHINE_GUN1; coalition(f);
check; RED_BRIDGE1_MACHINE_GUN1; location_type(Decoration,AAAPosition);
check; RED_BRIDGE1_MACHINE_GUN1; in_radius(PRIMARY_LINK_PHASE,1000);
check; RED_BRIDGE1_MACHINE_GUN2; free();
check; RED_BRIDGE1_MACHINE_GUN2; coalition(f);
check; RED_BRIDGE1_MACHINE_GUN2; location_type(Decoration,AAAPosition);
check; RED_BRIDGE1_MACHINE_GUN2; in_radius(PRIMARY_LINK_PHASE,1000);
check; RED_BRIDGE2_MACHINE_GUN1; free();
check; RED_BRIDGE2_MACHINE_GUN1; coalition(f);
check; RED_BRIDGE2_MACHINE_GUN1; location_type(Decoration,AAAPosition);
check; RED_BRIDGE2_MACHINE_GUN1; in_radius(PRIMARY_LINK_PHASE,1000);
check; RED_BRIDGE2_MACHINE_GUN2; free();
check; RED_BRIDGE2_MACHINE_GUN2; coalition(f);
check; RED_BRIDGE2_MACHINE_GUN2; location_type(Decoration,AAAPosition);
check; RED_BRIDGE2_MACHINE_GUN2; in_radius(PRIMARY_LINK_PHASE,1000);
check; BLUE_BRIDGE2_MACHINE_GUN1; free();
check; BLUE_BRIDGE2_MACHINE_GUN1; coalition(e);
check; BLUE_BRIDGE2_MACHINE_GUN1; location_type(Decoration,AAAPosition);
check; BLUE_BRIDGE2_MACHINE_GUN1; in_radius(PRIMARY_LINK_PHASE,1000);
check; BLUE_BRIDGE2_MACHINE_GUN2; free();
check; BLUE_BRIDGE2_MACHINE_GUN2; coalition(e);
check; BLUE_BRIDGE2_MACHINE_GUN2; location_type(Decoration,AAAPosition);
check; BLUE_BRIDGE2_MACHINE_GUN2; in_radius(PRIMARY_LINK_PHASE,1000);
check; BLUE_BRIDGE1_MACHINE_GUN1; free();
check; BLUE_BRIDGE1_MACHINE_GUN1; coalition(e);
check; BLUE_BRIDGE1_MACHINE_GUN1; location_type(Decoration,AAAPosition);
check; BLUE_BRIDGE1_MACHINE_GUN1; in_radius(PRIMARY_LINK_PHASE,1000);
check; BLUE_BRIDGE1_MACHINE_GUN2; free();
check; BLUE_BRIDGE1_MACHINE_GUN2; coalition(e);
check; BLUE_BRIDGE1_MACHINE_GUN2; location_type(Decoration,AAAPosition);
check; BLUE_BRIDGE1_MACHINE_GUN2; in_radius(PRIMARY_LINK_PHASE,1000);

#
## property actions
#
action; BLUE_BRIDGE1_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_BRIDGE1_RECON(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_BRIDGE1_RECON(RECON_OBJ,Success); set(Success,1);
action; BLUE_BRIDGE1_RECON(Tank,Zone); <empty>();
action; BLUE_BRIDGE1_RECON(Plane_in,Zone); <empty>();
action; BLUE_BRIDGE1_RECON(Plane_in,YPos); <empty>();
action; BLUE_BRIDGE1_RECON(Plane_out,Zone); <empty>();
action; BLUE_BRIDGE1_RECON(Plane_out,YPos); <empty>();
action; RED_BRIDGE1_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_BRIDGE1_RECON(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_BRIDGE1_RECON(RECON_OBJ,Success); set(Success,1);
action; RED_BRIDGE1_RECON(Tank,Zone); <empty>();
action; RED_BRIDGE1_RECON(Plane_in,Zone); <empty>();
action; RED_BRIDGE1_RECON(Plane_in,YPos); <empty>();
action; RED_BRIDGE1_RECON(Plane_out,Zone); <empty>();
action; RED_BRIDGE1_RECON(Plane_out,YPos); <empty>();
action; BLUE_BRIDGE2_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; BLUE_BRIDGE2_RECON(RECON_OBJ,Coalition); set(Coalition,1);
action; BLUE_BRIDGE2_RECON(RECON_OBJ,Success); set(Success,1);
action; BLUE_BRIDGE2_RECON(Tank,Zone); <empty>();
action; BLUE_BRIDGE2_RECON(Plane_in,Zone); <empty>();
action; BLUE_BRIDGE2_RECON(Plane_in,YPos); <empty>();
action; BLUE_BRIDGE2_RECON(Plane_out,Zone); <empty>();
action; BLUE_BRIDGE2_RECON(Plane_out,YPos); <empty>();
action; RED_BRIDGE2_RECON(RECON_OBJ,TaskType); set(TaskType,7);
action; RED_BRIDGE2_RECON(RECON_OBJ,Coalition); set(Coalition,2);
action; RED_BRIDGE2_RECON(RECON_OBJ,Success); set(Success,1);
action; RED_BRIDGE2_RECON(Tank,Zone); <empty>();
action; RED_BRIDGE2_RECON(Plane_in,Zone); <empty>();
action; RED_BRIDGE2_RECON(Plane_in,YPos); <empty>();
action; RED_BRIDGE2_RECON(Plane_out,Zone); <empty>();
action; RED_BRIDGE2_RECON(Plane_out,YPos); <empty>();
action; RED_BRIDGE1_MACHINE_GUN1(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random friendly);
action; RED_BRIDGE1_MACHINE_GUN1(AAA_SMALL_TYPE,Country); set_country(friendly);
action; RED_BRIDGE1_MACHINE_GUN2(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random friendly);
action; RED_BRIDGE1_MACHINE_GUN2(AAA_SMALL_TYPE,Country); set_country(friendly);
action; RED_BRIDGE2_MACHINE_GUN1(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random friendly);
action; RED_BRIDGE2_MACHINE_GUN1(AAA_SMALL_TYPE,Country); set_country(friendly);
action; RED_BRIDGE2_MACHINE_GUN2(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random friendly);
action; RED_BRIDGE2_MACHINE_GUN2(AAA_SMALL_TYPE,Country); set_country(friendly);
action; BLUE_BRIDGE2_MACHINE_GUN1(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random enemy);
action; BLUE_BRIDGE2_MACHINE_GUN1(AAA_SMALL_TYPE,Country); set_country(enemy);
action; BLUE_BRIDGE2_MACHINE_GUN2(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random enemy);
action; BLUE_BRIDGE2_MACHINE_GUN2(AAA_SMALL_TYPE,Country); set_country(enemy);
action; BLUE_BRIDGE1_MACHINE_GUN1(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random enemy);
action; BLUE_BRIDGE1_MACHINE_GUN1(AAA_SMALL_TYPE,Country); set_country(enemy);
action; BLUE_BRIDGE1_MACHINE_GUN2(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,random enemy);
action; BLUE_BRIDGE1_MACHINE_GUN2(AAA_SMALL_TYPE,Country); set_country(enemy);

#
## unlinks
#

#
## gui helpers
#
gui_helper; BLUE_BRIDGE1_RECON; -4030; 4282;
gui_helper; BLUE_BRIDGES_SUB; -3173; 3937;
gui_helper; RED_BRIDGE1_RECON; -349; 4339;
gui_helper; RED_BRIDGES_SUB; -1046; 3969;
gui_helper; BLUE_BRIDGE1_SERVER_INPUT; -4028; 4517;
gui_helper; BLUE_BRIDGE2_RECON; -3233; 4533;
gui_helper; BLUE_BRIDGE2_SERVER_INPUT; -3237; 4773;
gui_helper; RED_BRIDGE1_SERVER_INPUT; -343; 4573;
gui_helper; RED_BRIDGE2_RECON; -1394; 4516;
gui_helper; RED_BRIDGE2_SERVER_INPUT; -1414; 4735;
gui_helper; RED_BRIDGE1_MACHINE_GUN1; -318; 4914;
gui_helper; RED_BRIDGE1_MACHINE_GUN2; -314; 5256;
gui_helper; RED_BRIDGE2_MACHINE_GUN1; -1351; 5091;
gui_helper; RED_BRIDGE2_MACHINE_GUN2; -1347; 5433;
gui_helper; BLUE_BRIDGE2_MACHINE_GUN1; -3193; 5114;
gui_helper; BLUE_BRIDGE2_MACHINE_GUN2; -3189; 5456;
gui_helper; BLUE_BRIDGE1_MACHINE_GUN1; -4041; 4870;
gui_helper; BLUE_BRIDGE1_MACHINE_GUN2; -4037; 5212;
gui_helper; check; -3835; 4138;BLUE_BRIDGE1_RECON(location_type)
gui_helper; check; -3835; 4171;BLUE_BRIDGE1_RECON(coalition)
gui_helper; check; -3837; 4205;BLUE_BRIDGE1_RECON(free)
gui_helper; check; -3839; 4236;BLUE_BRIDGE1_RECON(in_radius)
gui_helper; check; -158; 4309;RED_BRIDGE1_RECON(in_radius)
gui_helper; check; -158; 4209;RED_BRIDGE1_RECON(location_type)
gui_helper; check; -160; 4273;RED_BRIDGE1_RECON(free)
gui_helper; check; -159; 4240;RED_BRIDGE1_RECON(coalition)
gui_helper; check; -3038; 4389;BLUE_BRIDGE2_RECON(location_type)
gui_helper; check; -3038; 4422;BLUE_BRIDGE2_RECON(coalition)
gui_helper; check; -3040; 4456;BLUE_BRIDGE2_RECON(free)
gui_helper; check; -3039; 4494;BLUE_BRIDGE2_RECON(range)
gui_helper; check; -1203; 4386;RED_BRIDGE2_RECON(location_type)
gui_helper; check; -1203; 4448;RED_BRIDGE2_RECON(free)
gui_helper; check; -1204; 4419;RED_BRIDGE2_RECON(coalition)
gui_helper; check; -1202; 4479;RED_BRIDGE2_RECON(range)
gui_helper; check; -129; 4851;RED_BRIDGE1_MACHINE_GUN1(free)
gui_helper; check; -129; 4818;RED_BRIDGE1_MACHINE_GUN1(coalition)
gui_helper; check; -128; 4784;RED_BRIDGE1_MACHINE_GUN1(location_type)
gui_helper; check; -127; 4885;RED_BRIDGE1_MACHINE_GUN1(in_radius)
gui_helper; check; -130; 5193;RED_BRIDGE1_MACHINE_GUN2(free)
gui_helper; check; -130; 5160;RED_BRIDGE1_MACHINE_GUN2(coalition)
gui_helper; check; -129; 5126;RED_BRIDGE1_MACHINE_GUN2(location_type)
gui_helper; check; -128; 5227;RED_BRIDGE1_MACHINE_GUN2(in_radius)
gui_helper; check; -1162; 5028;RED_BRIDGE2_MACHINE_GUN1(free)
gui_helper; check; -1162; 4995;RED_BRIDGE2_MACHINE_GUN1(coalition)
gui_helper; check; -1161; 4961;RED_BRIDGE2_MACHINE_GUN1(location_type)
gui_helper; check; -1160; 5062;RED_BRIDGE2_MACHINE_GUN1(in_radius)
gui_helper; check; -1163; 5370;RED_BRIDGE2_MACHINE_GUN2(free)
gui_helper; check; -1163; 5337;RED_BRIDGE2_MACHINE_GUN2(coalition)
gui_helper; check; -1162; 5303;RED_BRIDGE2_MACHINE_GUN2(location_type)
gui_helper; check; -1161; 5404;RED_BRIDGE2_MACHINE_GUN2(in_radius)
gui_helper; check; -3004; 5051;BLUE_BRIDGE2_MACHINE_GUN1(free)
gui_helper; check; -3004; 5018;BLUE_BRIDGE2_MACHINE_GUN1(coalition)
gui_helper; check; -3003; 4984;BLUE_BRIDGE2_MACHINE_GUN1(location_type)
gui_helper; check; -3002; 5085;BLUE_BRIDGE2_MACHINE_GUN1(in_radius)
gui_helper; check; -3005; 5393;BLUE_BRIDGE2_MACHINE_GUN2(free)
gui_helper; check; -3005; 5360;BLUE_BRIDGE2_MACHINE_GUN2(coalition)
gui_helper; check; -3004; 5326;BLUE_BRIDGE2_MACHINE_GUN2(location_type)
gui_helper; check; -3003; 5427;BLUE_BRIDGE2_MACHINE_GUN2(in_radius)
gui_helper; check; -3852; 4807;BLUE_BRIDGE1_MACHINE_GUN1(free)
gui_helper; check; -3852; 4774;BLUE_BRIDGE1_MACHINE_GUN1(coalition)
gui_helper; check; -3851; 4740;BLUE_BRIDGE1_MACHINE_GUN1(location_type)
gui_helper; check; -3850; 4841;BLUE_BRIDGE1_MACHINE_GUN1(in_radius)
gui_helper; check; -3853; 5149;BLUE_BRIDGE1_MACHINE_GUN2(free)
gui_helper; check; -3853; 5116;BLUE_BRIDGE1_MACHINE_GUN2(coalition)
gui_helper; check; -3852; 5082;BLUE_BRIDGE1_MACHINE_GUN2(location_type)
gui_helper; check; -3851; 5183;BLUE_BRIDGE1_MACHINE_GUN2(in_radius)
gui_helper; TaskType; -3965; 4124;BLUE_BRIDGE1_RECON; (RECON_OBJ);
gui_helper; Coalition; -3965; 4164;BLUE_BRIDGE1_RECON; (RECON_OBJ);
gui_helper; Success; -3965; 4204;BLUE_BRIDGE1_RECON; (RECON_OBJ);
gui_helper; Zone; -3964; 4250;BLUE_BRIDGE1_RECON; (Tank);
gui_helper; Zone; -3635; 4129;BLUE_BRIDGE1_RECON; (Plane_in);
gui_helper; YPos; -3635; 4169;BLUE_BRIDGE1_RECON; (Plane_in);
gui_helper; Zone; -3635; 4209;BLUE_BRIDGE1_RECON; (Plane_out);
gui_helper; YPos; -3635; 4249;BLUE_BRIDGE1_RECON; (Plane_out);
gui_helper; TaskType; -277; 4184;RED_BRIDGE1_RECON; (RECON_OBJ);
gui_helper; Coalition; -277; 4224;RED_BRIDGE1_RECON; (RECON_OBJ);
gui_helper; Success; -277; 4264;RED_BRIDGE1_RECON; (RECON_OBJ);
gui_helper; Zone; -283; 4304;RED_BRIDGE1_RECON; (Tank);
gui_helper; Zone; 51; 4189;RED_BRIDGE1_RECON; (Plane_in);
gui_helper; YPos; 51; 4229;RED_BRIDGE1_RECON; (Plane_in);
gui_helper; Zone; 51; 4269;RED_BRIDGE1_RECON; (Plane_out);
gui_helper; YPos; 51; 4309;RED_BRIDGE1_RECON; (Plane_out);
gui_helper; TaskType; -3172; 4374;BLUE_BRIDGE2_RECON; (RECON_OBJ);
gui_helper; Coalition; -3172; 4414;BLUE_BRIDGE2_RECON; (RECON_OBJ);
gui_helper; Success; -3172; 4454;BLUE_BRIDGE2_RECON; (RECON_OBJ);
gui_helper; Zone; -3171; 4500;BLUE_BRIDGE2_RECON; (Tank);
gui_helper; Zone; -2833; 4383;BLUE_BRIDGE2_RECON; (Plane_in);
gui_helper; YPos; -2833; 4423;BLUE_BRIDGE2_RECON; (Plane_in);
gui_helper; Zone; -2833; 4463;BLUE_BRIDGE2_RECON; (Plane_out);
gui_helper; YPos; -2833; 4503;BLUE_BRIDGE2_RECON; (Plane_out);
gui_helper; TaskType; -1327; 4362;RED_BRIDGE2_RECON; (RECON_OBJ);
gui_helper; Coalition; -1327; 4402;RED_BRIDGE2_RECON; (RECON_OBJ);
gui_helper; Success; -1327; 4442;RED_BRIDGE2_RECON; (RECON_OBJ);
gui_helper; Zone; -1328; 4481;RED_BRIDGE2_RECON; (Tank);
gui_helper; Zone; -994; 4366;RED_BRIDGE2_RECON; (Plane_in);
gui_helper; YPos; -994; 4406;RED_BRIDGE2_RECON; (Plane_in);
gui_helper; Zone; -994; 4446;RED_BRIDGE2_RECON; (Plane_out);
gui_helper; YPos; -994; 4486;RED_BRIDGE2_RECON; (Plane_out);
gui_helper; Model; -253; 4814;RED_BRIDGE1_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Country; -253; 4854;RED_BRIDGE1_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Model; -254; 5156;RED_BRIDGE1_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Country; -254; 5196;RED_BRIDGE1_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Model; -1286; 4991;RED_BRIDGE2_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Country; -1286; 5031;RED_BRIDGE2_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Model; -1287; 5333;RED_BRIDGE2_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Country; -1287; 5373;RED_BRIDGE2_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Model; -3128; 5014;BLUE_BRIDGE2_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Country; -3128; 5054;BLUE_BRIDGE2_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Model; -3129; 5356;BLUE_BRIDGE2_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Country; -3129; 5396;BLUE_BRIDGE2_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Model; -3976; 4770;BLUE_BRIDGE1_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Country; -3976; 4810;BLUE_BRIDGE1_MACHINE_GUN1; (AAA_SMALL_TYPE);
gui_helper; Model; -3977; 5112;BLUE_BRIDGE1_MACHINE_GUN2; (AAA_SMALL_TYPE);
gui_helper; Country; -3977; 5152;BLUE_BRIDGE1_MACHINE_GUN2; (AAA_SMALL_TYPE);
