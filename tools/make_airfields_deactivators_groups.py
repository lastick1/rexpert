"""Генерация координатных групп для отключения аэродромов"""
from __future__ import annotations
import sys
import pathlib
import os


AIRFIELD_DEACTIVATOR_GROUP_FORMAT = """MCU_H_ReferencePoint
{{
  Index = 7;
  Name = "Helper Reference Point";
  Desc = "";
  Targets = [];
  Objects = [];
  XPos = 0.000;
  YPos = 0.000;
  ZPos = 0.000;
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Forward = 11;
  Backward = 11;
  Left = 11;
  Right = 11;
}}

MCU_TR_ServerInput
{{
  Index = 8;
  Name = "REXPERT_DEACT_{0}";
  Desc = "";
  Targets = [27];
  Objects = [];
  XPos = -5.000;
  YPos = 17.795;
  ZPos = -5.000;
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Enabled = 1;
}}

MCU_CMD_Behaviour
{{
  Index = 23;
  Name = "NEUT";
  Desc = "";
  Targets = [];
  Objects = [25];
  XPos = -10.000;
  YPos = 17.795;
  ZPos = -10.000;
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Filter = 16;
  Vulnerable = 1;
  Engageable = 1;
  LimitAmmo = 1;
  RepairFriendlies = 0;
  RehealFriendlies = 0;
  RearmFriendlies = 0;
  RefuelFriendlies = 0;
  AILevel = 3;
  Country = 0;
  FloatParam = 0;
}}

MCU_H_Output
{{
  Index = 25;
  Name = "AF_MCU_OBJECT";
  Desc = "";
  Targets = [];
  Objects = [];
  XPos = -10.000;
  YPos = 17.795;
  ZPos = 0.000;
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
}}

MCU_Timer
{{
  Index = 27;
  Name = "t5s";
  Desc = "";
  Targets = [28,23];
  Objects = [];
  XPos = -5.000;
  YPos = 17.795;
  ZPos = -10.000;
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
  Time = 5;
  Random = 100;
}}

MCU_Deactivate
{{
  Index = 28;
  Name = "Trigger Deactivate";
  Desc = "";
  Targets = [27];
  Objects = [];
  XPos = 0.000;
  YPos = 17.795;
  ZPos = -10.000;
  XOri = 0.00;
  YOri = 0.00;
  ZOri = 0.00;
}}

"""


def main(airfields_csv: str, folder: str):
    """Сгенерировать координатные группы с Translator:ServerInput для отключения аэродромов"""
    rows = pathlib.Path(airfields_csv).read_text().split('\n')
    for row in rows:
        if row:
            name, x, z, orientation = row.split(';')
            input_name = name.replace(' ', '_').replace('.', '_')
            data = AIRFIELD_DEACTIVATOR_GROUP_FORMAT.format(input_name)
            filename = f'!x{x}z{z}.Group'
            group_file = pathlib.Path(os.path.abspath(os.path.join(folder, filename)))
            group_file.write_text(data, 'utf-8')
            print(f'Group for {input_name} created')


if __name__ == '__main__':
    try:
        # pylint может ложно-положительно срабатывать https://github.com/PyCQA/pylint/issues/2778
        main(*sys.argv[1:])
    except Exception as exception:
        print(exception)
