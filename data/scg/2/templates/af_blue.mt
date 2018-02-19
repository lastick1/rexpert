# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_WINDSOCK_357; main(scg\2\blocks_quickmission\windsock.group);
blocks_set; blocks_BF1_358; main(scg\2\blocks_quickmission\ground\blue_field.group);

#
## geo params
#
phase; WINDSOCK_357; random(BF1_358); blocks_WINDSOCK_357; clone_location;;
phase; BF1_358; random(<DELETED>); blocks_BF1_358; clone_location;;

#
## cases & switches
#

#
## gate links
#

#
## conditions
#
check; WINDSOCK_357; location_type(Decoration,Windsock);
check; WINDSOCK_357; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; WINDSOCK_357; free();
check; BF1_358; location_type(Decoration,Parking);
check; BF1_358; coalition(e);
check; BF1_358; range(PRIMARY_LINK_PHASE,closest_outof,1);

#
## property actions
#

#
## unlinks
#

#
## gui helpers
#
gui_helper; WINDSOCK_357; -1600; -280;
gui_helper; check; -1546; -88;WINDSOCK_357(location_type)
gui_helper; check; -1549; -49;WINDSOCK_357(range)
gui_helper; check; -1549; -9;WINDSOCK_357(free)
gui_helper; BF1_358; -1779; 75;
gui_helper; check; -1760; 251;BF1_358(location_type)
gui_helper; check; -1761; 287;BF1_358(coalition)
gui_helper; check; -1762; 324;BF1_358(range)
