"""Контейнер зависимостей"""
import pathlib
import configs
import core
import processing
import rcon


class DependencyContainer:
    def __init__(self):
        self._config = None
        self._objects = None
        self._objects_controller = None
        self._events_controller = None
        self._players_controller = None
        self._ground_controller = None
        self._campaign_controller = None
        self._airfields_controller = None
        self._grid_controller = None
        self._rcon = None
        self._generator = None
        self._storage = None

    @property
    def config(self) -> configs.Config:
        """Конфигурация приложения"""
        if not self._config:
            self._config = configs.Config(pathlib.Path('./configs/conf.ini'))
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
        if not self.events_controller:
            self._events_controller = core.EventsController(self)
        return self.events_controller

    @property
    def players_controller(self):
        """Контроллер игроков"""
        if not self._players_controller:
            self._players_controller = processing.PlayersController(self)
        return self._players_controller

    @property
    def ground_controller(self) -> processing.GroundController:
        """Контроллер наземки"""
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
    def grid_controller(self) -> processing.GridController:
        """Контроллер графа"""
        if not self._grid_controller:
            self._grid_controller = processing.GridController(self.config)
        return self._grid_controller

    @property
    def rcon(self):
        """Консоль сервера"""
        if not self._rcon:
            self._rcon = rcon.DServerRcon(self.config.main.rcon_ip, self.config.main.rcon_port)
        return self._rcon

    @property
    def storage(self) -> processing.Storage:
        """Объект для работы с БД"""
        if not self._storage:
            self._storage = processing.Storage(self.config.main)
        return self._storage

    @property
    def generator(self) -> processing.Generator:
        """Генератор миссий"""
        if not self._generator:
            self._generator = processing.Generator(self.config)
        return self._generator
