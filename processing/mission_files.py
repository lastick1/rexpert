"""Работа с файлами миссий"""
import subprocess
import time
import os

from datetime import datetime
from pathlib import Path


class MissionFiles:
    """Класс миссии в файловой системе, для перемещения и переименования файлов миссии"""
    def __init__(self, mission_file: Path, game_folder: Path, resaver_folder: Path):
        tmp = mission_file.absolute()
        self.files = {
            'Mission': tmp,
            'msnbin': Path(''.join(str(tmp).split('.')[:-1]) + '.msnbin'),
            'list': Path(''.join(str(tmp).split('.')[:-1]) + '.list'),
            'eng': Path(''.join(str(tmp).split('.')[:-1]) + '.eng'),
            'fra': Path(''.join(str(tmp).split('.')[:-1]) + '.fra'),
            'rus': Path(''.join(str(tmp).split('.')[:-1]) + '.rus'),
            'ger': Path(''.join(str(tmp).split('.')[:-1]) + '.ger'),
            'pol': Path(''.join(str(tmp).split('.')[:-1]) + '.pol'),
            'spa': Path(''.join(str(tmp).split('.')[:-1]) + '.spa')
        }
        self.resaver_folder = resaver_folder
        self.game_folder = game_folder

    def _replace(self, dst):
        """ Перемещение файлов миссии в указанную папку с заменой """
        for file_ext in self.files:
            tmp = Path(str(dst) + '.' + file_ext)
            self.files[file_ext].replace(tmp)
            self.files[file_ext] = tmp

    def move_to_dogfight(self, name: str):
        """ Перемещение файлов миссии в папку Multiplayer/Dogfight с заменой
        :param name: Имя файлов миссии"""
        # меняем в лист-файле пути к файлам локализации
        content = self.files['list'].read_text(encoding='utf-8').replace('missions/', 'multiplayer/dogfight/')
        content = content.replace('result', name)
        self.files['list'].write_text(content, encoding='utf-8')
        # вычисляем путь к папке data
        d = os.path.dirname(str(self.files['Mission']))
        while d.split(sep='\\')[-1] != 'data':
            d = str(Path(d).joinpath(os.pardir).resolve())
        # переносим файлы с заменой
        self._replace(Path(d).joinpath('.\\Multiplayer\\Dogfight\\' + name))

    def resave(self):
        now = str(datetime.now()).replace(":", "-").replace(" ", "_")
        resaver_folder = str(self.resaver_folder)
        data_folder = str(self.game_folder.joinpath(r'.\data'))
        with open(resaver_folder + r"\resaver_log_" + now + ".txt", "w") as resaver_log:
            args = [
                str(self.resaver_folder) + r"\MissionResaver.exe",
                "-d",
                data_folder,
                "-f",
                str(self.files['Mission'])
            ]
            resaver = subprocess.Popen(args, cwd=str(resaver_folder), stdout=resaver_log)
            resaver.wait()
            time.sleep(0.5)

    def detach_src(self):
        """ Переименование файла исходника миссии с заменой, чтобы он не был использован DServer """
        p = Path(os.path.splitext(str(self.files['Mission']))[0] + '_src.Mission')
        self.files['Mission'].replace(p)
        self.files['Mission'] = p

    # TODO сделать вместо detach - zip архив
    def zip_src(self):
        raise NotImplementedError
