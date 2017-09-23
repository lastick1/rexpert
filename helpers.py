""" Полезные методы """
from pathlib import Path
import os

def compile_log(folder: str, report: str, dest: str):
    """ Собрать лог по порядку из папки в один файл
    :param folder: Папка
    :param report: паттерн имени лога, который собрать
    :param dest: целевой файл
    """
    folder = Path(folder)
    with Path(dest).open(mode='w') as destination:
        files = list(str(x) for x in folder.glob(report))
        for file in sorted(files, key=os.path.getmtime):
            with Path(file).open() as stream:
                destination.writelines(stream.readlines())
