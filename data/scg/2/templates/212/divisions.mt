# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_SERVER_SET; main(scg\2\blocks_quickmission\ref_point.group);
blocks_set; blocks_BLUE_FRONT_AF_1; main(scg\2\blocks_quickmission\airfields_blue\!x180747z128910.group);
blocks_set; blocks_BLUE_FRONT_AF_2; main(scg\2\blocks_quickmission\airfields_blue\!x180747z128910.group);
blocks_set; blocks_BLUE_FRONT_AF_3; main(scg\2\blocks_quickmission\airfields_blue\!x180747z128910.group);
blocks_set; blocks_RED_FRONT_AF_1; main(scg\2\blocks_quickmission\airfields_red\!x119961z143087.group);
blocks_set; blocks_RED_FRONT_AF_2; main(scg\2\blocks_quickmission\airfields_red\!x119961z143087.group);
blocks_set; blocks_RED_FRONT_AF_3; main(scg\2\blocks_quickmission\airfields_red\!x119961z143087.group);
blocks_set; blocks_BLUE_REAR_AF; main(scg\2\blocks_quickmission\airfields_blue\!x180747z128910.group);
blocks_set; blocks_BLUE_REAR_AF_REFERENCE; main(scg\2\blocks_quickmission\ref_point.group);
blocks_set; blocks_RED_REAR_AF_REFERENCE; main(scg\2\blocks_quickmission\ref_point.group);
blocks_set; blocks_RED_REAR_AF; main(scg\2\blocks_quickmission\airfields_red\!x119961z143087.group);
blocks_set; blocks_FL_ICONS; main(scg\2\blocks_quickmission\icons\fl_icon.group);

#
## geo params
#
phase; SERVER_SET; server_setpos(); blocks_SERVER_SET; ;;
phase; BLUE_FRONT_AF_1; random(SERVER_SET); blocks_BLUE_FRONT_AF_1; clone_location;scg\2\blocks_quickmission\airfields_blue;
phase; BLUE_FRONT_AF_2; random(BLUE_FRONT_AF_1); blocks_BLUE_FRONT_AF_2; clone_location;scg\2\blocks_quickmission\airfields_blue;
phase; BLUE_FRONT_AF_3; random(BLUE_FRONT_AF_2); blocks_BLUE_FRONT_AF_3; clone_location;scg\2\blocks_quickmission\airfields_blue;
phase; RED_FRONT_AF_1; random(SERVER_SET); blocks_RED_FRONT_AF_1; clone_location;scg\2\blocks_quickmission\airfields_red;
phase; RED_FRONT_AF_2; random(RED_FRONT_AF_1); blocks_RED_FRONT_AF_2; clone_location;scg\2\blocks_quickmission\airfields_red;
phase; RED_FRONT_AF_3; random(RED_FRONT_AF_2); blocks_RED_FRONT_AF_3; clone_location;scg\2\blocks_quickmission\airfields_red;
phase; BLUE_REAR_AF; random(BLUE_REAR_AF_REFERENCE); blocks_BLUE_REAR_AF; clone_location;scg\2\blocks_quickmission\airfields_blue;
phase; BLUE_REAR_AF_REFERENCE; random(SERVER_SET); blocks_BLUE_REAR_AF_REFERENCE; clone_location;;
phase; RED_REAR_AF_REFERENCE; random(SERVER_SET); blocks_RED_REAR_AF_REFERENCE; clone_location;;
phase; RED_REAR_AF; random(RED_REAR_AF_REFERENCE); blocks_RED_REAR_AF; clone_location;scg\2\blocks_quickmission\airfields_red;
phase; FL_ICONS; at(SERVER_SET); blocks_FL_ICONS; clone_location;;

#
## cases & switches
#

#
## gate links
#

#
## conditions
#
check; BLUE_FRONT_AF_1; free();
check; BLUE_FRONT_AF_1; coalition(e);
check; BLUE_FRONT_AF_1; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; BLUE_FRONT_AF_1; location_type(Decoration,Parking);
check; BLUE_FRONT_AF_2; free();
check; BLUE_FRONT_AF_2; coalition(e);
check; BLUE_FRONT_AF_2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; BLUE_FRONT_AF_2; location_type(Decoration,Parking);
check; BLUE_FRONT_AF_3; free();
check; BLUE_FRONT_AF_3; coalition(e);
check; BLUE_FRONT_AF_3; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; BLUE_FRONT_AF_3; location_type(Decoration,Parking);
check; RED_FRONT_AF_1; location_type(Decoration,Parking);
check; RED_FRONT_AF_1; free();
check; RED_FRONT_AF_1; coalition(f);
check; RED_FRONT_AF_1; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; RED_FRONT_AF_2; location_type(Decoration,Parking);
check; RED_FRONT_AF_2; free();
check; RED_FRONT_AF_2; coalition(f);
check; RED_FRONT_AF_2; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; RED_FRONT_AF_3; location_type(Decoration,Parking);
check; RED_FRONT_AF_3; free();
check; RED_FRONT_AF_3; coalition(f);
check; RED_FRONT_AF_3; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; BLUE_REAR_AF_REFERENCE; coalition(e);
check; BLUE_REAR_AF_REFERENCE; location_type(Airfield,GrassField);
check; BLUE_REAR_AF_REFERENCE; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; BLUE_REAR_AF; in_radius(PRIMARY_LINK_PHASE,100);
check; BLUE_REAR_AF; location_type(Decoration,Parking);
check; RED_REAR_AF_REFERENCE; location_type(Airfield,GrassField);
check; RED_REAR_AF_REFERENCE; coalition(f);
check; RED_REAR_AF_REFERENCE; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; RED_REAR_AF; in_radius(PRIMARY_LINK_PHASE,100);
check; RED_REAR_AF; location_type(Decoration,Parking);

#
## property actions
#

#
## unlinks
#

#
## gui helpers
#
gui_helper; SERVER_SET; 697; 295;
gui_helper; BLUE_FRONT_AF_1; 2037; 285;
gui_helper; BLUE_FRONT_AF_2; 2065; -153;
gui_helper; BLUE_FRONT_AF_3; 2073; -585;
gui_helper; RED_FRONT_AF_1; -648; 303;
gui_helper; RED_FRONT_AF_2; -811; -218;
gui_helper; RED_FRONT_AF_3; -962; -705;
gui_helper; BLUE_REAR_AF; 1447; 1027;
gui_helper; BLUE_REAR_AF_REFERENCE; 1442; 712;
gui_helper; RED_REAR_AF_REFERENCE; 58; 726;
gui_helper; RED_REAR_AF; 57; 1089;
gui_helper; FL_ICONS; 730; 3;
gui_helper; check; 2260; 379;BLUE_FRONT_AF_1(free)
gui_helper; check; 2261; 344;BLUE_FRONT_AF_1(coalition)
gui_helper; check; 2259; 417;BLUE_FRONT_AF_1(range)
gui_helper; check; 2260; 305;BLUE_FRONT_AF_1(location_type)
gui_helper; check; 2288; -59;BLUE_FRONT_AF_2(free)
gui_helper; check; 2289; -94;BLUE_FRONT_AF_2(coalition)
gui_helper; check; 2287; -21;BLUE_FRONT_AF_2(range)
gui_helper; check; 2288; -133;BLUE_FRONT_AF_2(location_type)
gui_helper; check; 2296; -491;BLUE_FRONT_AF_3(free)
gui_helper; check; 2297; -526;BLUE_FRONT_AF_3(coalition)
gui_helper; check; 2295; -453;BLUE_FRONT_AF_3(range)
gui_helper; check; 2296; -565;BLUE_FRONT_AF_3(location_type)
gui_helper; check; -416; 317;RED_FRONT_AF_1(location_type)
gui_helper; check; -414; 359;RED_FRONT_AF_1(free)
gui_helper; check; -415; 398;RED_FRONT_AF_1(coalition)
gui_helper; check; -414; 435;RED_FRONT_AF_1(range)
gui_helper; check; -579; -204;RED_FRONT_AF_2(location_type)
gui_helper; check; -577; -162;RED_FRONT_AF_2(free)
gui_helper; check; -578; -123;RED_FRONT_AF_2(coalition)
gui_helper; check; -577; -86;RED_FRONT_AF_2(range)
gui_helper; check; -730; -691;RED_FRONT_AF_3(location_type)
gui_helper; check; -728; -649;RED_FRONT_AF_3(free)
gui_helper; check; -729; -610;RED_FRONT_AF_3(coalition)
gui_helper; check; -728; -573;RED_FRONT_AF_3(range)
gui_helper; check; 1681; 780;BLUE_REAR_AF_REFERENCE(coalition)
gui_helper; check; 1679; 734;BLUE_REAR_AF_REFERENCE(location_type)
gui_helper; check; 1679; 824;BLUE_REAR_AF_REFERENCE(range)
gui_helper; check; 1692; 1131;BLUE_REAR_AF(in_radius)
gui_helper; check; 1689; 1046;BLUE_REAR_AF(location_type)
gui_helper; check; 326; 797;RED_REAR_AF_REFERENCE(location_type)
gui_helper; check; 328; 748;RED_REAR_AF_REFERENCE(coalition)
gui_helper; check; 328; 846;RED_REAR_AF_REFERENCE(range)
gui_helper; check; 295; 1209;RED_REAR_AF(in_radius)
gui_helper; check; 286; 1109;RED_REAR_AF(location_type)
