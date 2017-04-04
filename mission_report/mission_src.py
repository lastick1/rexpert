import re
from pathlib import Path
from mission_report import helpers
import datetime
# https://tproger.ru/translations/regular-expression-python/
server_inputs_re = re.compile(
    '\n\s*MCU_TR_ServerInput'
    '\n\s*\{'
    '\n\s*Index = \d+;'
    '\n\s*Name = "(?P<name>.+\.|.*)";'
    '\n\s*Desc = .*'
    '\n\s*Targets = .*'
    '\n\s*Objects = .*'
    '\n\s*XPos = (?P<XPos>-?\d+\.\d+);'
    '\n\s*YPos = -?\d+\.\d+;'
    '\n\s*ZPos = (?P<ZPos>-?\d+\.\d+);'
    '\n\s*XOri = .*;'
    '\n\s*YOri = .*;'
    '\n\s*ZOri = .*;'
    '\n\s*Enabled = .*;'
    '\n\s*\}')
mission_objectives_re = re.compile(
    '\n\s*MCU_TR_MissionObjective'
    '\n\s*\{'
    '\n\s*Index = \d+;'
    '\n\s*Targets = .*'
    '\n\s*Objects = .*'
    '\n\s*XPos = (?P<XPos>-?\d+\.\d+);'
    '\n\s*YPos = -?\d+\.\d+;'
    '\n\s*ZPos = (?P<ZPos>-?\d+\.\d+);'
    '\n\s*XOri = .*;'
    '\n\s*YOri = .*;'
    '\n\s*ZOri = .*;'
    '\n\s*Enabled = .*;'
    '\n\s*LCName = \d+;'
    '\n\s*LCDesc = \d+;'
    '\n\s*TaskType = (?P<TaskType>\d+);'
    '\n\s*Coalition = (?P<Coalition>\d+);'
    '\n\s*Success = (?P<Success>0|1);'
    '\n\s*IconType = .+;'
    '\n\s*\}')

mission_airfields_re = re.compile(
    'Airfield\n\s*[/\na-zA-Z0-9"=\.\s;\{\}\\\\-]*\n')

mission_airfield_re = re.compile(
    '[/\na-zA-Z0-9"=\.\s;\{\}\\\\-]*'
    '\n\s*Name = "(?P<name>[a-zA-Z0-9\.\s\-]*)";'
    '\n\s*Index = (?P<index>\d+);'
    '\n\s*[/\na-zA-Z0-9"=\.\s;\{\}\\\\-]*'
    '\n\s*XPos = (?P<XPos>-?\d+\.\d+);'
    '\n\s*YPos = -?\d+\.\d+;'
    '\n\s*ZPos = (?P<ZPos>-?\d+\.\d+);')

mission_guimap_re = re.compile(
    'GuiMap = "(?P<guimap>[a-zA-Z\-0-9]*)";'
)

mission_date_re = re.compile(
    'Date = (?P<date>[a-zA-Z\-0-9\.]*);'
)

r"""
.	Один любой символ, кроме новой строки \n.
?	0 или 1 вхождение шаблона слева
+	1 и более вхождений шаблона слева
*	0 и более вхождений шаблона слева
\w	Любая цифра или буква (\W — все, кроме буквы или цифры)
\d	Любая цифра [0-9] (\D — все, кроме цифры)
\s	Любой пробельный символ (\S — любой непробельнй символ)
\b	Граница слова
[..]	Один из символов в скобках ([^..] — любой символ, кроме тех, что в скобках)
\	Экранирование специальных символов (\. означает точку или \+ — знак «плюс»)
^ и $	Начало и конец строки соответственно
{n,m}	От n до m вхождений ({,m} — от 0 до m)
a|b	Соответствует a или b
()	Группирует выражение и возвращает найденный текст
\t, \n, \r	Символ табуляции, новой строки и возврата каретки соответственно"""


target_defs = (
    "_rear_warehouse",
    "_front_warehouse",
    "_block_post",
    "_bridge",
    "_fort",
    "_station",
    "_HQ"
)


objectives_mapping = {
    '14': 'flames',
    '5': 'trucks',
    '6': 'tanks',
    '4': 'arts'
}
coalitions_mapping = {
    '4': {'1': '2', '2': '1'},
    '5': {'1': '2', '2': '1'},
    '6': {'1': '2', '2': '1'}
}


class MissionSrc:
    """
    Класс-парсер исходников миссии
    """
    def __init__(self, src=Path()):
        src_text = src.read_text()
        self.server_inputs = []
        self.mission_objectives = []
        self.airfields_raw = []
        self.airfields = []
        self.guimap = None
        self.date = None

        all_matches = server_inputs_re.findall(src_text)
        # все сервер инпуты в виде словарей
        for m in all_matches:
            self.server_inputs.append({"name": m[0], "XPos": float(m[1]), "ZPos": float(m[2])})
        # все мишн обжективы в виде словарей
        all_matches = mission_objectives_re.findall(src_text)
        for m in all_matches:
            mo = {"obj_type": m[2], "XPos": m[0], "ZPos": m[1], "coalition": m[3], "success": m[4]}
            self.mission_objectives.append(mo)
        # все филды, не разобранные по полям
        all_matches = mission_airfields_re.findall(src_text)
        for m in all_matches:
            self.airfields_raw.append(m)
        # разбор филдов по полям
        for af_str in self.airfields_raw:
            m = mission_airfield_re.match(af_str.strip()).groupdict()
            m["supply"] = False
            if "supply" in af_str:
                m["supply"] = True
            if "Country = 101;" in af_str:
                m["coalition"] = "red"
            elif "Country = 201;" in af_str:
                m["coalition"] = "blue"
            else:
                m["coalition"] = "neutral"
            self.airfields.append(m)
        for m in mission_guimap_re.findall(src_text):
            self.guimap = m
        for m in mission_date_re.findall(src_text):
            self.date = datetime.datetime.strptime(m, '%d.%m.%Y')

    def ground_targets_inputs(self):
        tgts = []
        if len(self.server_inputs):
            for si in self.server_inputs:
                for definition in target_defs:
                    if definition in si["name"]:
                        if "red_" in si["name"]:
                            si["coalition"] = "Red"
                        elif "blue_" in si["name"]:
                            si["coalition"] = "Blue"
                        tgts.append(si)
        return tgts

    def find_by_coords(self, xpos, zpos):
        for si in self.server_inputs:
            if si["XPos"] == xpos and si["ZPos"] == zpos:
                return si
        for mo in self.mission_objectives:
            if mo["XPos"] == xpos and mo["ZPos"] == zpos:
                return mo
        for af in self.airfields:
            if af["XPos"] == xpos and af["ZPos"] == zpos:
                return af

    def red_targets(self):
        tgts = []
        for tgt in self.ground_targets_inputs():
            if tgt["name"].startswith("red_"):
                tgts.append(tgt)
        return tgts

    def blue_targets(self):
        tgts = []
        for tgt in self.ground_targets_inputs():
            if tgt["name"].startswith("blue_"):
                tgts.append(tgt)
        return tgts

    def find_server_input_in_radius(self, xpos, zpos, r):
        p1 = {}
        p2 = {"x": float(xpos), "z": float(zpos)}
        for si in self.server_inputs:
            p1["x"] = float(si["XPos"])
            p1["z"] = float(si["ZPos"])
            if helpers.distance(p1, p2) < r:
                return si

    def find_mission_objective_in_radius(self, xpos, zpos, r, not_obj_type=None):
        p1 = {}
        p2 = {"x": float(xpos), "z": float(zpos)}
        if not_obj_type:
            for mo in self.mission_objectives:
                p1["x"] = float(mo["XPos"])
                p1["z"] = float(mo["ZPos"])
                if helpers.distance(p1, p2) < r:
                    if int(mo["obj_type"]) != not_obj_type:
                        return mo
        else:
            for mo in self.mission_objectives:
                p1["x"] = float(mo["XPos"])
                p1["z"] = float(mo["ZPos"])
                if helpers.distance(p1, p2) < r:
                    return mo

    def find_airfield_in_radius(self, xpos, zpos, r):
        p1 = {}
        p2 = {"x": float(xpos), "z": float(zpos)}
        for af in self.airfields:
            p1["x"] = float(af["XPos"])
            p1["z"] = float(af["ZPos"])
            if helpers.distance(p1, p2) < r:
                return af

    @property
    def icons(self):
        icons = {
            '1': {
                'flames': [],
                'trucks': [],
                'tanks': [],
                'arts': [],
                'warehouses': [],
                'hqs': [],
                'airfields': [],
                'forts': []
            },
            '2': {
                'flames': [],
                'trucks': [],
                'tanks': [],
                'arts': [],
                'warehouses': [],
                'hqs': [],
                'airfields': [],
                'forts': []
            }
        }
        for mo in self.mission_objectives:
            if mo['obj_type'] not in ('4', '5', '6', '14'):
                continue
            if mo['obj_type'] == '14' and mo['success'] == '1':
                icons[mo['coalition']][objectives_mapping[mo['obj_type']]].append(
                    {'x': float(mo['ZPos']), 'z': float(mo['XPos'])})
            else:
                if mo['obj_type'] in coalitions_mapping.keys():
                    coal = coalitions_mapping[mo['obj_type']][mo['coalition']]
                else:
                    coal = mo['coalition']
                icons[coal][objectives_mapping[mo['obj_type']]].append({'x': float(mo['ZPos']), 'z': float(mo['XPos'])})
        for o in self.server_inputs:
            if 'half' in o['name']:
                continue
            if 'red' in o['name']:
                coal = '1'
            elif 'blue' in o['name']:
                coal = '2'
            else:
                continue
            if 'warehouse' in o['name'] and 'red' in o['name']:
                icons[coal]['warehouses'].append({'x': float(o['ZPos']), 'z': float(o['XPos'])})
            elif 'hq' in o['name'] and 'rus' in o['name']:
                icons[coal]['hqs'].append({'x': float(o['ZPos']), 'z': float(o['XPos'])})
            elif 'fort' in o['name'] and 'blue' in o['name']:
                icons[coal]['forts'].append({'x': float(o['ZPos']), 'z': float(o['XPos'])})
        for o in self.airfields:
            if o['coalition'] == 'red':
                coal = '1'
            elif o['coalition'] == 'blue':
                coal = '2'
            else:
                continue
            icons[coal]['airfields'].append({'x': float(o['ZPos']), 'z': float(o['XPos']), 'name': o['name']})
        return icons
