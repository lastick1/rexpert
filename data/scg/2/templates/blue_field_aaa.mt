# neoqb RoF mission template file [text dump]

#
## block sets
#
blocks_set; blocks_BLUE-ATTACK-AF-1; main(scg\2\blocks_quickmission\airfields_blue\!x100505z156297.group);
blocks_set; blocks_LARGE_CANNON_85_882; main(scg\2\blocks_quickmission\ground\aaa\big\smart_large_cannon.group);
blocks_set; blocks_MEDIUM_CANNON_86_883; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON2_87_884; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON3_88_885; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON4_89_886; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON5_90_887; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON6_91_888; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_SMALL_CANNON_92_889; main(scg\2\blocks_quickmission\ground\aaa\small\smart_machine_gun.group);
blocks_set; blocks_SMALL_CANNON2_93_890; main(scg\2\blocks_quickmission\ground\aaa\small\smart_machine_gun.group);
blocks_set; blocks_BLUE_SMART_CHECKZONE_891; main(scg\2\blocks_quickmission\smart_blue_checkzone.group);
blocks_set; blocks_MEDIUM_CANNON_86_883_180; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON2_87_884_181; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);
blocks_set; blocks_MEDIUM_CANNON6_91_888_192; main(scg\2\blocks_quickmission\ground\aaa\med\smart_auto_cannon.group);

#
## geo params
#
phase; BLUE-ATTACK-AF-1; random(<EMPTY>); blocks_BLUE-ATTACK-AF-1; clone_location;scg\2\blocks_quickmission\airfields_blue;
phase; LARGE_CANNON_85_882; random(BLUE_SMART_CHECKZONE_891); blocks_LARGE_CANNON_85_882; clone_location;;
phase; MEDIUM_CANNON_86_883; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON_86_883; clone_location;;
phase; MEDIUM_CANNON2_87_884; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON2_87_884; clone_location;;
phase; MEDIUM_CANNON3_88_885; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON3_88_885; clone_location;;
phase; MEDIUM_CANNON4_89_886; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON4_89_886; clone_location;;
phase; MEDIUM_CANNON5_90_887; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON5_90_887; clone_location;;
phase; MEDIUM_CANNON6_91_888; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON6_91_888; clone_location;;
phase; SMALL_CANNON_92_889; random(BLUE_SMART_CHECKZONE_891); blocks_SMALL_CANNON_92_889; clone_location;;
phase; SMALL_CANNON2_93_890; random(BLUE_SMART_CHECKZONE_891); blocks_SMALL_CANNON2_93_890; clone_location;;
phase; BLUE_SMART_CHECKZONE_891; at(BLUE-ATTACK-AF-1); blocks_BLUE_SMART_CHECKZONE_891; clone_location;;
phase; MEDIUM_CANNON_86_883_180; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON_86_883_180; clone_location;;
phase; MEDIUM_CANNON2_87_884_181; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON2_87_884_181; clone_location;;
phase; MEDIUM_CANNON6_91_888_192; random(BLUE_SMART_CHECKZONE_891); blocks_MEDIUM_CANNON6_91_888_192; clone_location;;

#
## cases & switches
#

#
## gate links
#
tlink; BLUE-ATTACK-AF-1(AAA_OFF); BLUE_SMART_CHECKZONE_891(AAA_OFF);
tlink; BLUE-ATTACK-AF-1(AAA_ON); BLUE_SMART_CHECKZONE_891(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); SMALL_CANNON2_93_890(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); SMALL_CANNON_92_889(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON6_91_888(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON5_90_887(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON4_89_886(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON3_88_885(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON2_87_884(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON_86_883(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); LARGE_CANNON_85_882(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON_86_883_180(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON2_87_884_181(AAA_ON);
tlink; BLUE-ATTACK-AF-1(AAA_ON); MEDIUM_CANNON6_91_888_192(AAA_ON);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_LARGE_CANNONS); LARGE_CANNON_85_882(ACTIVATE_LARGE_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_LARGE_CANNONS); LARGE_CANNON_85_882(DEACTIVATE_LARGE_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON_86_883(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON_86_883(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2_87_884(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2_87_884(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON3_88_885(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON3_88_885(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON4_89_886(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON4_89_886(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON5_90_887(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON5_90_887(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON6_91_888(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON6_91_888(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_MACHINE_GUNS); SMALL_CANNON_92_889(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_MACHINE_GUNS); SMALL_CANNON_92_889(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_MACHINE_GUNS); SMALL_CANNON2_93_890(ACTIVATE_MACHINE_GUNS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_MACHINE_GUNS); SMALL_CANNON2_93_890(DEACTIVATE_MACHINE_GUNS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON_86_883_180(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON_86_883_180(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2_87_884_181(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON2_87_884_181(DEACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(ACTIVATE_AUTO_CANNONS); MEDIUM_CANNON6_91_888_192(ACTIVATE_AUTO_CANNONS);
tlink; BLUE_SMART_CHECKZONE_891(DEACTIVATE_AUTO_CANNONS); MEDIUM_CANNON6_91_888_192(DEACTIVATE_AUTO_CANNONS);

#
## conditions
#
check; BLUE-ATTACK-AF-1; coalition(e);
check; BLUE-ATTACK-AF-1; location_type(Decoration,Parking);
check; BLUE-ATTACK-AF-1; free();
check; BLUE-ATTACK-AF-1; in_radius(PRIMARY_LINK_PHASE,60000);
check; LARGE_CANNON_85_882; location_type(Decoration,AAAPosition);
check; LARGE_CANNON_85_882; free();
check; LARGE_CANNON_85_882; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON_86_883; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON_86_883; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON_86_883; free();
check; MEDIUM_CANNON2_87_884; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON2_87_884; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON2_87_884; free();
check; MEDIUM_CANNON3_88_885; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON3_88_885; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON3_88_885; free();
check; MEDIUM_CANNON4_89_886; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON4_89_886; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON4_89_886; free();
check; MEDIUM_CANNON5_90_887; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON5_90_887; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON5_90_887; free();
check; MEDIUM_CANNON6_91_888; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON6_91_888; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON6_91_888; free();
check; SMALL_CANNON_92_889; location_type(Decoration,AAAPosition);
check; SMALL_CANNON_92_889; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMALL_CANNON_92_889; free();
check; SMALL_CANNON2_93_890; location_type(Decoration,AAAPosition);
check; SMALL_CANNON2_93_890; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; SMALL_CANNON2_93_890; free();
check; MEDIUM_CANNON_86_883_180; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON_86_883_180; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON_86_883_180; free();
check; MEDIUM_CANNON2_87_884_181; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON2_87_884_181; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON2_87_884_181; free();
check; MEDIUM_CANNON6_91_888_192; location_type(Decoration,AAAPosition);
check; MEDIUM_CANNON6_91_888_192; range(PRIMARY_LINK_PHASE,closest_outof,1);
check; MEDIUM_CANNON6_91_888_192; free();

#
## property actions
#
action; BLUE-ATTACK-AF-1(Repair,Time); set(Time,4500);
action; LARGE_CANNON_85_882(AAA_BIG_TYPE,Model); set_model(AAA HVY static cannon,random enemy);
action; LARGE_CANNON_85_882(AAA_BIG_TYPE,Country); set_country(enemy);
action; LARGE_CANNON_85_882(AAA_BIG_TYPE,AILevel); set(AILevel,3);
action; MEDIUM_CANNON_86_883(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON_86_883(AAA_MED_TYPE,Country); set_country(enemy);
action; MEDIUM_CANNON2_87_884(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON2_87_884(AAA_MED_TYPE,Country); set_country(enemy);
action; MEDIUM_CANNON3_88_885(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON3_88_885(AAA_MED_TYPE,Country); set_country(enemy);
action; MEDIUM_CANNON4_89_886(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON4_89_886(AAA_MED_TYPE,Country); set_country(enemy);
action; MEDIUM_CANNON5_90_887(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON5_90_887(AAA_MED_TYPE,Country); set_country(enemy);
action; MEDIUM_CANNON6_91_888(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON6_91_888(AAA_MED_TYPE,Country); set_country(enemy);
action; SMALL_CANNON_92_889(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Axis:AAA machinegun:mg34-aa);
action; SMALL_CANNON_92_889(AAA_SMALL_TYPE,Country); set_country(enemy);
action; SMALL_CANNON_92_889(AAA_SMALL_TYPE,AILevel); set(AILevel,3);
action; SMALL_CANNON2_93_890(AAA_SMALL_TYPE,Model); set_model(AAA machinegun,Axis:AAA machinegun:mg34-aa);
action; SMALL_CANNON2_93_890(AAA_SMALL_TYPE,Country); set_country(enemy);
action; SMALL_CANNON2_93_890(AAA_SMALL_TYPE,AILevel); set(AILevel,3);
action; BLUE_SMART_CHECKZONE_891(AUTO_CANNONS,Time); <empty>();
action; BLUE_SMART_CHECKZONE_891(Inner Zone,Zone); <empty>();
action; BLUE_SMART_CHECKZONE_891(MACHINE_GUNS,Time); <empty>();
action; BLUE_SMART_CHECKZONE_891(Outer Zone,Zone); <empty>();
action; MEDIUM_CANNON_86_883_180(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON_86_883_180(AAA_MED_TYPE,Country); set_country(enemy);
action; MEDIUM_CANNON2_87_884_181(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON2_87_884_181(AAA_MED_TYPE,Country); set_country(enemy);
action; MEDIUM_CANNON6_91_888_192(AAA_MED_TYPE,Model); set_model(AAA LT static cannon,random enemy);
action; MEDIUM_CANNON6_91_888_192(AAA_MED_TYPE,Country); set_country(enemy);

#
## unlinks
#

#
## gui helpers
#
gui_helper; BLUE-ATTACK-AF-1; 3446; -2204;
gui_helper; LARGE_CANNON_85_882; 4614; -4718;
gui_helper; MEDIUM_CANNON_86_883; 4616; -4303;
gui_helper; MEDIUM_CANNON2_87_884; 5183; -4312;
gui_helper; MEDIUM_CANNON3_88_885; 4635; -3475;
gui_helper; MEDIUM_CANNON4_89_886; 5168; -3501;
gui_helper; MEDIUM_CANNON5_90_887; 4646; -3048;
gui_helper; MEDIUM_CANNON6_91_888; 5159; -3053;
gui_helper; SMALL_CANNON_92_889; 4637; -2143;
gui_helper; SMALL_CANNON2_93_890; 5162; -2599;
gui_helper; BLUE_SMART_CHECKZONE_891; 3834; -2484;
gui_helper; MEDIUM_CANNON_86_883_180; 4607; -3913;
gui_helper; MEDIUM_CANNON2_87_884_181; 5174; -3922;
gui_helper; MEDIUM_CANNON6_91_888_192; 4645; -2617;
gui_helper; check; 3004; -2152;BLUE-ATTACK-AF-1(coalition)
gui_helper; check; 3082; -2151;BLUE-ATTACK-AF-1(location_type)
gui_helper; check; 3102; -1950;BLUE-ATTACK-AF-1(free)
gui_helper; check; 3011; -1951;BLUE-ATTACK-AF-1(in_radius)
gui_helper; check; 4635; -4544;LARGE_CANNON_85_882(location_type)
gui_helper; check; 4632; -4504;LARGE_CANNON_85_882(free)
gui_helper; check; 4632; -4467;LARGE_CANNON_85_882(range)
gui_helper; check; 4636; -4127;MEDIUM_CANNON_86_883(location_type)
gui_helper; check; 4633; -4087;MEDIUM_CANNON_86_883(range)
gui_helper; check; 4634; -4052;MEDIUM_CANNON_86_883(free)
gui_helper; check; 5203; -4136;MEDIUM_CANNON2_87_884(location_type)
gui_helper; check; 5192; -4089;MEDIUM_CANNON2_87_884(range)
gui_helper; check; 5193; -4054;MEDIUM_CANNON2_87_884(free)
gui_helper; check; 4655; -3299;MEDIUM_CANNON3_88_885(location_type)
gui_helper; check; 4651; -3261;MEDIUM_CANNON3_88_885(range)
gui_helper; check; 4652; -3226;MEDIUM_CANNON3_88_885(free)
gui_helper; check; 5188; -3325;MEDIUM_CANNON4_89_886(location_type)
gui_helper; check; 5188; -3282;MEDIUM_CANNON4_89_886(range)
gui_helper; check; 5189; -3247;MEDIUM_CANNON4_89_886(free)
gui_helper; check; 4666; -2872;MEDIUM_CANNON5_90_887(location_type)
gui_helper; check; 4665; -2837;MEDIUM_CANNON5_90_887(range)
gui_helper; check; 4666; -2802;MEDIUM_CANNON5_90_887(free)
gui_helper; check; 5179; -2877;MEDIUM_CANNON6_91_888(location_type)
gui_helper; check; 5172; -2837;MEDIUM_CANNON6_91_888(range)
gui_helper; check; 5173; -2802;MEDIUM_CANNON6_91_888(free)
gui_helper; check; 4664; -1972;SMALL_CANNON_92_889(location_type)
gui_helper; check; 4660; -1936;SMALL_CANNON_92_889(range)
gui_helper; check; 4659; -1902;SMALL_CANNON_92_889(free)
gui_helper; check; 5189; -2430;SMALL_CANNON2_93_890(location_type)
gui_helper; check; 5191; -2389;SMALL_CANNON2_93_890(range)
gui_helper; check; 5190; -2355;SMALL_CANNON2_93_890(free)
gui_helper; check; 4627; -3737;MEDIUM_CANNON_86_883_180(location_type)
gui_helper; check; 4624; -3697;MEDIUM_CANNON_86_883_180(range)
gui_helper; check; 4625; -3662;MEDIUM_CANNON_86_883_180(free)
gui_helper; check; 5194; -3746;MEDIUM_CANNON2_87_884_181(location_type)
gui_helper; check; 5183; -3699;MEDIUM_CANNON2_87_884_181(range)
gui_helper; check; 5184; -3664;MEDIUM_CANNON2_87_884_181(free)
gui_helper; check; 4665; -2441;MEDIUM_CANNON6_91_888_192(location_type)
gui_helper; check; 4658; -2401;MEDIUM_CANNON6_91_888_192(range)
gui_helper; check; 4659; -2366;MEDIUM_CANNON6_91_888_192(free)
gui_helper; Time; 3031; -2220;BLUE-ATTACK-AF-1; (Repair);
gui_helper; Model; 4692; -4785;LARGE_CANNON_85_882; (AAA_BIG_TYPE);
gui_helper; Country; 4692; -4745;LARGE_CANNON_85_882; (AAA_BIG_TYPE);
gui_helper; AILevel; 4691; -4823;LARGE_CANNON_85_882; (AAA_BIG_TYPE);
gui_helper; Model; 4694; -4370;MEDIUM_CANNON_86_883; (AAA_MED_TYPE);
gui_helper; Country; 4694; -4330;MEDIUM_CANNON_86_883; (AAA_MED_TYPE);
gui_helper; Model; 5261; -4379;MEDIUM_CANNON2_87_884; (AAA_MED_TYPE);
gui_helper; Country; 5261; -4339;MEDIUM_CANNON2_87_884; (AAA_MED_TYPE);
gui_helper; Model; 4713; -3542;MEDIUM_CANNON3_88_885; (AAA_MED_TYPE);
gui_helper; Country; 4713; -3502;MEDIUM_CANNON3_88_885; (AAA_MED_TYPE);
gui_helper; Model; 5246; -3568;MEDIUM_CANNON4_89_886; (AAA_MED_TYPE);
gui_helper; Country; 5246; -3528;MEDIUM_CANNON4_89_886; (AAA_MED_TYPE);
gui_helper; Model; 4724; -3115;MEDIUM_CANNON5_90_887; (AAA_MED_TYPE);
gui_helper; Country; 4724; -3075;MEDIUM_CANNON5_90_887; (AAA_MED_TYPE);
gui_helper; Model; 5237; -3120;MEDIUM_CANNON6_91_888; (AAA_MED_TYPE);
gui_helper; Country; 5237; -3080;MEDIUM_CANNON6_91_888; (AAA_MED_TYPE);
gui_helper; Model; 4713; -2208;SMALL_CANNON_92_889; (AAA_SMALL_TYPE);
gui_helper; Country; 4713; -2168;SMALL_CANNON_92_889; (AAA_SMALL_TYPE);
gui_helper; AILevel; 4711; -2242;SMALL_CANNON_92_889; (AAA_SMALL_TYPE);
gui_helper; Model; 5238; -2666;SMALL_CANNON2_93_890; (AAA_SMALL_TYPE);
gui_helper; Country; 5238; -2626;SMALL_CANNON2_93_890; (AAA_SMALL_TYPE);
gui_helper; AILevel; 5238; -2703;SMALL_CANNON2_93_890; (AAA_SMALL_TYPE);
gui_helper; Time; 3951; -2687;BLUE_SMART_CHECKZONE_891; (AUTO_CANNONS);
gui_helper; Zone; 3951; -2647;BLUE_SMART_CHECKZONE_891; (Inner Zone);
gui_helper; Time; 3951; -2607;BLUE_SMART_CHECKZONE_891; (MACHINE_GUNS);
gui_helper; Zone; 3951; -2567;BLUE_SMART_CHECKZONE_891; (Outer Zone);
gui_helper; Model; 4685; -3980;MEDIUM_CANNON_86_883_180; (AAA_MED_TYPE);
gui_helper; Country; 4685; -3940;MEDIUM_CANNON_86_883_180; (AAA_MED_TYPE);
gui_helper; Model; 5252; -3989;MEDIUM_CANNON2_87_884_181; (AAA_MED_TYPE);
gui_helper; Country; 5252; -3949;MEDIUM_CANNON2_87_884_181; (AAA_MED_TYPE);
gui_helper; Model; 4723; -2684;MEDIUM_CANNON6_91_888_192; (AAA_MED_TYPE);
gui_helper; Country; 4723; -2644;MEDIUM_CANNON6_91_888_192; (AAA_MED_TYPE);
