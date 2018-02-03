"""Полезные функции"""

import pathlib
import os
import imageio


def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""

    class Convert:  # pylint: disable=R0903
        """Конвертер функции сравнения в функцию ключа"""
        def __init__(self, obj, *args):  # pylint: disable=W0613
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return Convert


def compile_log(folder: str, report: str, dest: str):
    """ Собрать лог по порядку из папки в один файл
    :param folder: Папка
    :param report: паттерн имени лога, который собрать
    :param dest: целевой файл
    """
    folder = pathlib.Path(folder)
    with pathlib.Path(dest).open(mode='w') as destination:
        files = list(str(x) for x in folder.glob(report))
        for file in sorted(files, key=os.path.getmtime):
            with pathlib.Path(file).open() as stream:
                destination.writelines(stream.readlines())


def compile_gif(folder: str):
    """Собрать картинки в gif-анимацию в заданной папке"""
    folder = pathlib.Path(folder)
    files = list(str(x) for x in folder.glob('*.png'))
    with imageio.get_writer('./movie.gif', mode='I', duration=1) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)


def compile_ldf(folder: str, dest: str):
    """Объединить файлы LDF из папки в указанный файл"""
    folder = pathlib.Path(folder)
    files = list(pathlib.Path(x) for x in folder.glob('*.ldf'))
    text = ''
    for file in files:
        with file.open(encoding='utf-8') as stream:
            read = stream.read()[29:-13]
            text += read
    text = '#1CGS Location Database file\n{}\n#end of file'.format(text)
    pathlib.Path(dest).write_text(text, encoding='utf-8')
