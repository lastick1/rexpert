"Объёкты, встречаемые в логах"
import codecs

class Object:
    "Класс объекта из логов"
    def __init__(self, cls: str, log_name: str, playable: str, name: str, name_ru: str):
        self.cls = cls
        self.log_name = log_name
        self.playable = bool(int(playable))
        self.name = name
        self.name_ru = name_ru.replace('\n', '').replace('\r', '')

class Objects(dict):
    "Словарь объёктов"
    def __init__(self):
        with codecs.open(r'.\configs\objects.csv', encoding='utf-8') as stream:
            lines = stream.readlines()
        tmp = list(Object(*x.split(',')) for x in lines[1:])
        data = list((x.log_name, x) for x in tmp)
        super().__init__(data)
