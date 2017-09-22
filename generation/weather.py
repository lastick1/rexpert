from random import randint


class WeatherPreset:
    def __init__(self, preset):
        self.preset = preset
        self.turbulences = [0, 0]
        if type(preset['Turbulence']) == list:
            self.turbulences = preset['Turbulence']
        self.cloudlevels = [preset['CloudLevel'][0], preset['CloudLevel'][1]]
        self.cloudheights = [preset['CloudHeight'], preset['CloudHeight']]
        if type(preset['CloudHeight']) == list:
            if len(preset['CloudHeight']) == 2:
                self.cloudheights = [preset['CloudHeight'][0], preset['CloudHeight'][1]]
            else:
                self.cloudheights = [preset['CloudHeight'][0], preset['CloudHeight'][0]]

    @property
    def turbulence(self):
        return randint(self.turbulences[0], self.turbulences[1])

    @property
    def cloudlevel(self):
        return randint(self.cloudlevels[0], self.cloudlevels[1])

    @property
    def cloudheight(self):
        return randint(self.cloudheights[0], self.cloudheights[1])

# WType config sets
presets = [
    {
        'CloudConfig': r"winter\00_Clear_00\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_01\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_02\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_03\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_04\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_05\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_06\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_07\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_08\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\00_Clear_09\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_00\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_01\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 500],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_02\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 700],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_03\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 500],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_04\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 600],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_05\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_06\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 600],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_07\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 700],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_08\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\01_Light_09\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_00\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': 1000,
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_01\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_02\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_03\sky.ini",
        'CloudLevel': [900, 4301],
        'CloudHeight': [300, 700],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_04\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_05\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_06\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [400, 850],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_07\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_08\sky.ini",
        'CloudLevel': [900, 4101],
        'CloudHeight': [400, 900],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\02_Medium_09\sky.ini",
        'CloudLevel': [900, 3801],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\03_Heavy_00\sky.ini",
        'CloudLevel': [900, 3301],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\03_Heavy_03\sky.ini",
        'CloudLevel': [900, 3301],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\03_Heavy_06\sky.ini",
        'CloudLevel': [900, 3101],
        'CloudHeight': [700, 1400],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\03_Heavy_08\sky.ini",
        'CloudLevel': [900, 3401],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"winter\04_Overcast_05\sky.ini",
        'CloudLevel': [3000, 5401],
        'CloudHeight': [200, 500],
        'Turbulence': 0,
        'PrecLevel': 100,
        'PrecType': 2
    },
    {
        'CloudConfig': r"summer\00_Clear_00\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_01\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_02\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_03\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_04\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_05\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_06\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_07\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_08\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\00_Clear_09\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': 200,
        'Turbulence': 0,
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_00\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_01\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 500],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_02\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 700],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_03\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 500],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_04\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 600],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_05\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_06\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 600],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_07\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [300, 700],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_08\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\01_Light_09\sky.ini",
        'CloudLevel': [900, 5001],
        'CloudHeight': [400, 800],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_00\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_01\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_02\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_03\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [300, 700],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_04\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_05\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_06\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [400, 850],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_07\sky.ini",
        'CloudLevel': [900, 4001],
        'CloudHeight': [500, 1000],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_08\sky.ini",
        'CloudLevel': [900, 4101],
        'CloudHeight': [400, 900],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\02_Medium_09\sky.ini",
        'CloudLevel': [900, 3801],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\03_Heavy_00\sky.ini",
        'CloudLevel': [900, 3401],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\03_Heavy_01\sky.ini",
        'CloudLevel': [900, 3501],
        'CloudHeight': [600, 1300],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\03_Heavy_05\sky.ini",
        'CloudLevel': [900, 3601],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\03_Heavy_06\sky.ini",
        'CloudLevel': [900, 3401],
        'CloudHeight': [700, 1400],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\03_Heavy_08\sky.ini",
        'CloudLevel': [900, 3601],
        'CloudHeight': [600, 1200],
        'Turbulence': [0, 1],
        'PrecLevel': 10,
        'PrecType': 0
    },
    {
        'CloudConfig': r"summer\04_Overcast_07\sky.ini",
        'CloudLevel': [3000, 5401],
        'CloudHeight': [200, 600],
        'Turbulence': 0,
        'PrecLevel': 100,
        'PrecType': 1
    }
]
