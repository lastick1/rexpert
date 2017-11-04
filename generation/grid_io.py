"""Спецификация по чтению и записи графа"""
import abc


class GridIO(metaclass=abc.ABCMeta):
    """Абстрактный класс чтения-записи графа"""

    @abc.abstractmethod
    def parse(self) -> None:
        """Считать файл с графом"""

    @abc.abstractmethod
    def save_file(self, path: str, nodes: list, edges: list) -> None:
        """Записать граф в файл"""

    @abc.abstractmethod
    def serialize(self, nodes: dict, edges: list) -> str:
        """Сохранить граф для записи"""

    @property
    @abc.abstractmethod
    def nodes(self) -> dict:
        """Узлы считанного графа"""

    @property
    @abc.abstractmethod
    def edges(self) -> list:
        """Рёбра считанного графа списком из пар (ключ, ключ)"""
