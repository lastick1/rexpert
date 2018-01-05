import datetime
DATE_FORMAT = '%d.%m.%Y'


class Campaign:
    def __init__(self):
        """Класс кампании, хранящий текущее состояние игрового процесса"""
        self.date = datetime.datetime.now()  # TODO заглушка
