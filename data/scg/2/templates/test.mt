# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_PHASE_1; main(scg\2\blocks_quickmission\scenario\counter.group);
blocks_set; blocks_PHASE_4; main(scg\2\blocks_quickmission\node_subtitle.group);
blocks_set; blocks_PHASE_12; main(scg\2\blocks_quickmission\scenario\multiplier_x12.group);

#
## geo params
#
phase; PHASE_1; server_setpos(); blocks_PHASE_1; ;;
phase; PHASE_4; random(PHASE_1); blocks_PHASE_4; clone_location;;
phase; PHASE_12; random(PHASE_1); blocks_PHASE_12; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; PHASE_12(COUNTER); PHASE_4(NODE_EVENT_BLUE);

#
## conditions
#

#
## property actions
#
action; PHASE_1(MAIN,Counter); <empty>();
action; PHASE_1(TANKS_DEATH_DELAY,Time); <empty>();

#
## unlinks
#

#
## gui helpers
#
gui_helper; PHASE_1; -3863; -1167;
gui_helper; PHASE_4; -3239; -1201;
gui_helper; PHASE_12; -3742; -1531;
gui_helper; Counter; -3789; -1241;PHASE_1; (MAIN);
gui_helper; Time; -3789; -1201;PHASE_1; (TANKS_DEATH_DELAY);
