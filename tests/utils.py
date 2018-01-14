"""Полезные функции для тестирования"""
import shutil
import pathlib
import processing


def get_nodes_keys(nodes: list) -> set:
    """Получить ключи узлов из списка узлов"""
    return set(z.key for z in nodes)


def get_polygons_keys(nodes: list) -> tuple:
    """Получить ключи узлов в списке многоугольников"""
    return tuple(set(z.key for z in x) for x in nodes)


def get_nodes(points: list) -> list:
    """Получить узлы из точек (нейтральные)"""
    nodes = []
    key = 0
    for point in points:
        nodes.append(processing.Node(key=key, text=key, pos=point.to_dict(), color='#FFFFFF'))
        key += 1
    return nodes


def get_nodes_by_keys(keys: list, grid: processing.Grid) -> list:
    """Получить ключи узлов из списка узлов"""
    return list(grid.node(key) for key in keys)


def clean_directory(directory: str):
    """Очистить директорию"""
    folder = pathlib.Path(directory)
    if folder.exists():
        shutil.rmtree(directory)
        folder.mkdir(parents=True)
