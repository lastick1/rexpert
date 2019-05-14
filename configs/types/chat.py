"Описание настроек чата"


class Chat:
    "Класс настроек чата"
    def __init__(self, cfg: dict):
        self.warehouse_notification_interval = cfg['warehouse_notification_interval']
        self.points_notification_interval = cfg['points_notification_interval']
