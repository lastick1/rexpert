prices = {
    "aaa_heavy": 50,
    "aaa_light": 50,
    "aaa_mg": 50,
    "aircraft_gunner": 0,
    "aircraft_heavy": 0,
    "aircraft_light": 0,
    "aircraft_medium": 0,
    "aircraft_pilot": 0,
    "aircraft_static": 20,
    "aircraft_transport": 200,
    "aircraft_turret": 0,
    "airfield": 5,
    "armoured_vehicle": 15,
    "artillery_field": 50,
    "artillery_howitzer": 50,
    "artillery_rocket": 50,
    "bomb": 0,
    "bridge": 100,
    "bullet": 0,
    "car": 15,
    "explosion": 0,
    "flare": 0,
    "industrial": 6,
    "locomotive": 60,
    "machine_gunner": 25,
    "parachute": 0,
    "rocket": 0,
    "searchlight": 20,
    "shell": 0,
    "ship": 80,
    "tank_driver": 0,
    "tank_heavy": 240,
    "tank_medium": 120,
    "tank_light": 60,
    "tank_turret": 0,
    "trash": 1,
    "truck": 15,
    "vehicle_crew": 0,
    "vehicle_static": 12,
    "vehicle_turret": 0,
    "wagon": 25,
}


def get_object_price(obj):
    if obj.cls in (
        "vehicle_crew",
        "vehicle_turret",
        "tank_driver",
        "shell",
        "rocket",
        "parachute",
        "flare",
        "explosion",
        "bomb"
    ):
        print(obj.cls, "found with 0 price:", obj.log_name)
    return get_price_by_cls(obj.cls)


def get_price_by_cls(cls):
    return prices[cls]
