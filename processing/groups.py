"""Манипуляции с файлами групп"""
import shutil
import os
import pathlib

import configs

from .formats import ref_point_helper_format
from .mcu import FrontLineIcon, InfluenceArea


class Group:
    """Класс групп-файлов, из которых генератор по шаблону собирает миссию"""
    def __init__(self, group_file: pathlib.Path):
        tmp = group_file.absolute()
        self.files = {
            'Group': tmp,
            'eng': pathlib.Path(''.join(str(tmp).split('.')[:-1]) + '.eng'),
            'fra': pathlib.Path(''.join(str(tmp).split('.')[:-1]) + '.fra'),
            'rus': pathlib.Path(''.join(str(tmp).split('.')[:-1]) + '.rus'),
            'ger': pathlib.Path(''.join(str(tmp).split('.')[:-1]) + '.ger'),
            'pol': pathlib.Path(''.join(str(tmp).split('.')[:-1]) + '.pol'),
            'spa': pathlib.Path(''.join(str(tmp).split('.')[:-1]) + '.spa')
        }

    def clone_to(self, folder):
        """Копирование файлов группы в указанную папку"""
        dest = str(folder)
        for file_ext in self.files:
            self.files[file_ext] = pathlib.Path(shutil.copy(str(self.files[file_ext]), dest))

    def rename(self, dst):
        """Смена имён файлов на dst"""
        dst_path = os.path.dirname(str(self.files['Group'])) + '\\' + dst
        for file_ext in self.files:
            tmp = pathlib.Path(dst_path + '.' + file_ext)
            if tmp.exists():
                os.remove(str(tmp))
            self.files[file_ext].rename(tmp)
            self.files[file_ext] = tmp

    def replace_content(self, src, dst):
        """Замена src в содержимом файлов группы на dst"""
        for file_ext in self.files:
            if file_ext == 'Group':
                content = self.files[file_ext].read_text(encoding='utf-8').replace(src, dst)
                self.files[file_ext].write_text(content, encoding='utf-8')
            else:
                content = self.files[file_ext].read_text(encoding='utf-16-le').replace(src, dst)
                self.files[file_ext].write_text(content, encoding='utf-16-le')


class FrontLineGroup(Group):
    """Класс группы линии фронта"""
    def __init__(self, line: list, areas: dict, group_file: pathlib.Path, ref_point: dict):
        """
        :param line: линия фронта (снизу вверх)
        :param areas: зоны влияния (словарь многоугольников по странам)
        """
        super().__init__(group_file)
        self.icons = []
        self.influences = []
        self._loc_text = None
        i = 2
        for point in line:
            self.icons.append(FrontLineIcon(i, point, target=i+1))
            i += 1
        self.icons[len(self.icons)-1].target = None
        for country in areas.keys():
            for boundary in areas[country]:
                self.influences.append(
                    InfluenceArea(boundary.x, boundary.z, i, boundary.polygon, country))
                i += 1
        self.ref_point_text = ref_point_helper_format.format(i, ref_point['x'], ref_point['z'])

    def make(self):
        """ Записать файлы группы (включая локализацию) """
        for file_ext in self.files:
            if file_ext == 'Group':
                text = ''
                for icon in self.icons:
                    text += str(icon)
                for area in self.influences:
                    text += str(area)
                text += self.ref_point_text
                self.files[file_ext].write_text(text, encoding='utf-8')
            else:
                # файлы локализации нужны, чтобы уменьшить вероятные проблемы (фризы)
                file = pathlib.Path(self.files[file_ext])
                content = '{}\n{}'.format('\ufeff', self.loc_text)
                if file.exists():
                    file.write_text(content, encoding='utf-16-le')

    @property
    def loc_text(self):
        """ Текст файлов локализации (пустые строки) """
        if self._loc_text:
            return self._loc_text
        self._loc_text = ''
        for icon in self.icons:
            self._loc_text += '{}:\n{}:\n'.format(icon.lc_name, icon.lc_desc)
        return self._loc_text


class AirfieldGroup(Group):
    """Группа аэродрома"""
    def __init__(self, mcu_text: str, group_file: pathlib.Path):
        super().__init__(group_file)
        self.mcu_text = mcu_text

    def make(self):
        """Записать файлы группы"""
        for file_ext in self.files:
            if file_ext == 'Group':
                self.files[file_ext].write_text(self.mcu_text, encoding='utf-8')
            else:
                # файлы локализации нужны, чтобы уменьшить вероятные проблемы (фризы)
                pathlib.Path(self.files[file_ext]).write_text('', encoding='utf-16-le')
