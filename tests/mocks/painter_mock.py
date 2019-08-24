"Заглушка отрисовщика карт"
from processing import MapPainter


class PainterMock(MapPainter):
    "Заглушка отрисовщика карт"

    def __init__(self):
        super().__init__(None)

    def update_map(self):
        pass
