"""Контейнер зависимостей"""
import pathlib
import configs
import core
import processing
import storage
import rcon


class DependencyContainer:  # pylint: disable=R0902
    """Тривиальная реализация, но вроде работает"""
    def __init__(self):
        self._config: configs.Config = None
        self._objects: configs.Objects = None
        self._objects_controller: core.ObjectsController = None
        self._events_controller: core.EventsController = None
        self._players_controller: processing.PlayersController = None
        self._ground_controller: processing.GroundController = None
        self._campaign_controller: processing.CampaignController = None
        self._airfields_controller: processing.AirfieldsController = None
        self._divisions_controller: processing.DivisionsController = None
        self._warehouses_controller: processing.WarehouseController = None
        self._grid_controller: processing.GridController = None
        self._aircraft_vendor: processing.AircraftVendor = None
        self._source_parser: processing.SourceParser = None
        self._map_painter: processing.MapPainter = None
        self._rcon: rcon.DServerRcon = None
        self._generator: processing.Generator = None
        self._storage: storage.Storage = None

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        if not self._config:
            self._config = configs.Config(pathlib.Path('./configs/main.json'))
        return self._config

    @property
    def objects(self) -> configs.Objects:
        """Словарь данных объектов в логах по имени объекта"""
        if not self._objects:
            self._objects = configs.Objects()
        return self._objects

    @property
    def objects_controller(self) -> core.ObjectsController:
        """Контроллер объектов в логах"""
        if not self._objects_controller:
            self._objects_controller = core.ObjectsController(self)
        return self._objects_controller

    @property
    def events_controller(self) -> core.EventsController:
        """Контроллер событий"""
        if not self._events_controller:
            self._events_controller = core.EventsController(self)
        return self._events_controller

    @property
    def players_controller(self) -> processing.PlayersController:
        """Контроллер игроков"""
        if not self._players_controller:
            self._players_controller = processing.PlayersController(self)
        return self._players_controller

    @property
    def ground_controller(self) -> processing.GroundController:
        """Контроллер наземных целей"""
        if not self._ground_controller:
            self._ground_controller = processing.GroundController(self)
        return self._ground_controller

    @property
    def campaign_controller(self) -> processing.CampaignController:
        """Контроллер кампании"""
        if not self._campaign_controller:
            self._campaign_controller = processing.CampaignController(self)
        return self._campaign_controller

    @property
    def airfields_controller(self) -> processing.AirfieldsController:
        """Контроллер аэродромов"""
        if not self._airfields_controller:
            self._airfields_controller = processing.AirfieldsController(self)
        return self._airfields_controller

    @property
    def divisions_controller(self) -> processing.DivisionsController:
        """Контроллер дивизий"""
        if not self._divisions_controller:
            self._divisions_controller = processing.DivisionsController(self)
        return self._divisions_controller

    @property
    def warehouses_controller(self) -> processing.WarehouseController:
        """Контроллер складов"""
        if not self._warehouses_controller:
            self._warehouses_controller = processing.WarehouseController(self)
        return self._warehouses_controller

    @property
    def grid_controller(self) -> processing.GridController:
        """Контроллер графа"""
        if not self._grid_controller:
            self._grid_controller = processing.GridController(self.config)
        return self._grid_controller

    @property
    def aircraft_vendor(self):
        """Поставщик самолётов на аэродромы"""
        if not self._aircraft_vendor:
            self._aircraft_vendor = processing.AircraftVendor(self.config.planes, self.config.gameplay)
        return self._aircraft_vendor

    @property
    def source_parser(self) -> processing.SourceParser:
        """Парсер исходников миссий"""
        if not self._source_parser:
            self._source_parser = processing.SourceParser(self.config)
        return self._source_parser

    @property
    def map_painter(self) -> processing.MapPainter:
        """Рисовальщик изображений карты с иконками целей"""
        if not self._map_painter:
            self._map_painter = processing.MapPainter(self)
        return self._map_painter

    @property
    def rcon(self) -> rcon.DServerRcon:
        """Консоль сервера"""
        if not self._rcon:
            self._rcon = rcon.DServerRcon(self.config.main.rcon_ip, self.config.main.rcon_port)
        return self._rcon

    @property
    def generator(self) -> processing.Generator:
        """Генератор миссий"""
        if not self._generator:
            self._generator = processing.Generator(self.config)
        return self._generator

    @property
    def storage(self) -> storage.Storage:
        """Объект для работы с БД"""
        if not self._storage:
            self._storage = storage.Storage(self.config.main)
        return self._storage
