# Коммандер Random Expert
##### Версия 'Divisions'
**В процессе:**

* Покрытие тестами нового функционала
* Новая обработка логов, уход от использования классов il2_stats
* Переделка генератора для внедрения будущих изменений
* Рефакторинг кода. Тестируемость старых классов.
* Переход на использование MongoDB для хранения информации о гаражах

**В планах:**

* Механизм дивизий, смотреть описание в секретной лаборатории
* Хранение графа кампании в файле



##### MongoDB
* На ветке divisions используется [MongoDB](https://www.mongodb.com/download-center?jmp=nav#community)
* Ей для запуска надо указать папку для хранения базы данных
* Стандартный порт: 27017
* [Настройка на запуск как Windows Service](https://stackoverflow.com/questions/2438055/how-to-run-mongodb-as-windows-service)
* Для удобства (GUI) можно использовать [Robo 3T](https://robomongo.org)
* В этой базе данные хранятся в коллекциях json-объектов (коллекции документов)
* Чтобы найти конкретный документ в коллекции, надо в find указать объект-запрос вида: {"Имя_свойства": "Значение_свойства"}
* В Robomongo (*Robo 3T*) документы редактируются как текстовые объекты: ПКМ по документу коллекции -> Edit Document



##### Известные особенности логов DServer
* Не важно, как игрок покинул с сервера - у его бота должен быть атайп деинициализации
