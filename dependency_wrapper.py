import dependency_container
import configs
import core
import processing
import rcon


class Ioc:
    def __init__(self):
        self._ioc = dependency_container.DependencyContainer()

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        return self._ioc.config

    @property
    def objects(self) -> configs.Objects:
        """Словарь данных объектов в логах по имени объекта"""
        return self._ioc.objects

    @property
    def objects_controller(self) -> core.ObjectsController:
        """Контроллер объектов в логах"""
        return self._ioc.objects_controller

    @property
    def events_controller(self) -> core.EventsController:
        """Контроллер событий"""
        return self._ioc.events_controller

    @property
    def players_controller(self) -> processing.PlayersController:
        """Контроллер игроков"""
        return self._ioc.players_controller

    @property
    def ground_controller(self) -> processing.GroundController:
        """Контроллер наземки"""
        return self._ioc.ground_controller

    @property
    def campaign_controller(self) -> processing.CampaignController:
        """Контроллер кампании"""
        return self._ioc.campaign_controller

    @property
    def airfields_controller(self) -> processing.AirfieldsController:
        """Контроллер аэродромов"""
        return self._ioc.airfields_controller

    @property
    def divisions_controller(self) -> processing.DivisionsController:
        """Контроллер дивизий"""
        return self._ioc.divisions_controller

    @property
    def grid_controller(self) -> processing.GridController:
        """Контроллер графа"""
        return self._ioc.grid_controller

    @property
    def source_parser(self) -> processing.SourceParser:
        """Парсер исходников миссий"""
        return self._ioc.source_parser

    @property
    def map_painter(self) -> processing.MapPainter:
        """Рисовальщик изображений карты с иконками целей"""
        return self._ioc.map_painter

    @property
    def rcon(self) -> rcon.DServerRcon:
        """Консоль сервера"""
        return self._ioc.rcon

    @property
    def generator(self) -> processing.Generator:
        """Генератор миссий"""
        return self._ioc.generator

    @property
    def storage(self) -> processing.Storage:
        """Объект для работы с БД"""
        return self._ioc.storage
