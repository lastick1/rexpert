def get_aircraft_mod(aircraft, mod_id):
    try:
        return aircraft_mods[aircraft][mod_id]
    except KeyError:
        return None


aircraft_mods = {
    'bf 110 e-2': {
        1: 'Armored windscreen and headrest',
        2: 'Additional armor',
        3: '12 x SC50',
        4: '2 x SC500',
        5: '1 x SC1000'
    },
    'bf 109 e-7': {
        1: '4 x SC50',
        2: '1 x SC250',
        3: 'Armored windscreen',
        4: 'Removed headrest',
        5: 'Additional armor'
    },
    'il-2 mod.1941': {
        1: '2 x 23mm',
        2: '6 x FAB-50/100',
        3: '2 x FAB-250',
        4: '8 x RBS-82',
        5: '8 x ROFS-132'
    },
    'he 111 h-6': {
        1: 'Bottom 20mm',
        2: 'Nose 20mm',
        3: '2 x SC1000',
        4: '2 x SC1800',
        5: 'SC2500'
    },
    'bf 109 f-2': {
        1: '20mm',
        2: '4 x SC50',
        3: '1 x SC250',
        4: 'Armored windscreen',
        5: 'Removed headrest'
    },
    'il-2 mod.1942': {
        1: '2 x 23mm',
        2: '2 x 37mm',
        3: '2 x FAB-250',
        4: '8 x RBS-82/ROFS-132',
        5: 'Gunner turret'
    },
    'ju 87 d-3': {
        1: 'Siren',
        2: 'SC1800',
        3: 'Additional armor',
        4: 'MG containers',
        5: '2 x 37mm'
    },
    'bf 109 f-4': {
        1: '2 x 15mm',
        2: '4 x SC50',
        3: '1 x SC250',
        4: 'Armored windscreen',
        5: 'Removed headrest',
        6: '2 x 20mm'
    },
    'pe-2 ser.87': {
        1: '10 x FAB-100',
        2: '4 x FAB-250',
        3: '2 x FAB-500',
        4: '10 x ROS-132',
        5: 'Turret'
    },
    'lagg-3 ser.29': {
        1: '23mm',
        2: '37mm',
        3: '2 x FAB-50',
        4: '2 x FAB-100',
        5: '6 x ROS-82'
    },
    'bf 109 g-2': {
        1: '2 x 20mm',
        2: '4 x SC50',
        3: '1 x SC250',
        4: 'Armored headrest',
        5: 'Removed headrest'
    },
    'mc.202 ser.viii': {
        1: 'Armored windscreen',
        2: '2 x 50-T',
        3: '2 x 100-T',
        4: '2 x 7.7mm',
        5: '2 x 20mm'
    },
    'mig-3 ser.24': {
        1: '6 x ROS-82',
        2: '2 x FAB-50/100',
        3: '2 x 12.7 (wings)',
        4: '2 x 12.7 (nose)',
        5: '2 x 20mm'
    },
    'yak-1 ser.69': {
        1: '2 x ROS-82',
        2: '6 x ROS-82',
        3: '2 x FAB-50',
        4: '2 x FAB-100',
        5: 'RPK-10'
    },
    'fw 190 a-3': {
        1: '4 x SC50',
        2: '1 x SC250',
        3: '1 x SC500',
        4: '2 x 20mm (120)',
        5: '2 x 20mm (180)'
    },
    'i-16 type 24': {
        1: '4 x ROS-82',
        2: '6 x ROS-82',
        3: '2 x FAB-50/100',
        4: 'Windscreen',
        5: '2 x 20mm'
    },
    'la-5 ser.8': {
        1: '2 x FAB-50',
        2: '2 x FAB-100',
        3: 'RPK-10',
        4: 'Windscreen',
        5: 'Special ammo loadout'
    },
    'ju 88 a-4': {
        1: '6 x SC250',
        2: '4 x SC500',
        3: 'SC1000',
        4: 'SC1800',
        5: '44 x SC50'
    },
    'pe-2 ser.35': {
        1: '10 x FAB-100',
        2: '4 x FAB-250',
        3: '2 x FAB-500',
        4: '10 x ROS-132',
        5: 'RPK-2'
    },
    'p-40e-1': {
        1: '4 x 12.7mm',
        2: 'Additional ammo',
        3: '4 x ROS-82',
        4: '1 x FAB-250',
        5: '1 x FAB-500'
    },
    'ju 52 3mg4e': {
        1: 'unknown 1',
        2: 'unknown 2',
        3: 'unknown 3',
        4: 'unknown 4',
        5: 'unknown 5'
    }
}
