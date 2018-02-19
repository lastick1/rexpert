# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_RF1_383; main(scg\2\blocks_quickmission\ground\red_field.group);
blocks_set; blocks_WINDSOCK_331_384; main(scg\2\blocks_quickmission\windsock.group);

#
## geo params
#
phase; RF1_383; random(<DELETED>); blocks_RF1_383; clone_location;;
phase; WINDSOCK_331_384; random(RF1_383); blocks_WINDSOCK_331_384; clone_location;;

#
## cases & switches
#

#
## gate links
#

#
## conditions
#
check; RF1_383; location_type(Decoration,Parking);
check; RF1_383; coalition(f);
check; RF1_383; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; WINDSOCK_331_384; location_type(Decoration,Windsock);
check; WINDSOCK_331_384; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; WINDSOCK_331_384; free();

#
## property actions
#

#
## unlinks
#

#
## gui helpers
#
gui_helper; RF1_383; 3077; 434;
gui_helper; check; 3099; 608;RF1_383(location_type)
gui_helper; check; 3102; 650;RF1_383(coalition)
gui_helper; check; 3104; 690;RF1_383(range)
gui_helper; WINDSOCK_331_384; 3238; 68;
gui_helper; check; 3292; 260;WINDSOCK_331_384(location_type)
gui_helper; check; 3289; 299;WINDSOCK_331_384(range)
gui_helper; check; 3289; 339;WINDSOCK_331_384(free)
