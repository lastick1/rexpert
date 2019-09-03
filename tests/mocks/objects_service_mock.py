"Мок сервиса работы с объектами"
from services import ObjectsService
from .stubs import pass_


class ObjectsServiceMock(ObjectsService):
    "Мок сервиса работы с объектами"

    def __init__(self, emitter, config, objects):
        super().__init__(emitter, config, objects)
        self.init = pass_
