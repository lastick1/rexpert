"""Регулярные выражения для извлечения данных из исходников миссий"""
import re
# https://tproger.ru/translations/regular-expression-python/
SERVER_INPUT_RE = re.compile(
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
MISSION_OBJECTIVE_RE = re.compile(
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

AIRFIELD_RE = re.compile(
    'Airfield\n\s*[/\na-zA-Z0-9"=\.\s;\{\}\\\\-]*\n')

AIRFIELD_DATA_RE = re.compile(
    '[/\na-zA-Z0-9"=\.\s;\{\}\\\\-]*'
    '\n\s*Name = "(?P<name>[a-zA-Z0-9\.\s\-]*)";'
    '\n\s*Index = (?P<index>\d+);'
    '\n\s*[/\na-zA-Z0-9"=\.\s;\{\}\\\\-]*'
    '\n\s*XPos = (?P<XPos>-?\d+\.\d+);'
    '\n\s*YPos = -?\d+\.\d+;'
    '\n\s*ZPos = (?P<ZPos>-?\d+\.\d+);')

GUIMAP_RE = re.compile(
    'GuiMap = "(?P<guimap>[a-zA-Z\-0-9]*)";'
)

MISSION_DATE_RE = re.compile(
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
