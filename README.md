# Коммандер Random Expert
##### Версия 'Divisions'
**В процессе:**

* Генерация базы локаций
    * Вычисление прифронтовых прямоугольников и/или определение прифронтовой территории по треугольникам
    * Покраска локаций и сборка файла базы локаций
* Покрытие тестами нового функционала
* Переделка генератора для внедрения будущих изменений
* Новая обработка логов
* Рефакторинг кода. Тестируемость старых классов.
* Хранение графа кампании в файле

**В планах:**

* Grid.IsValidForGeneration()
* Сборка файла миссии
* Механизм дивизий, смотреть описание в секретной лаборатории

**Готово:**

* Уход от использования классов il2_stats
* Переход на использование MongoDB для хранения информации о гаражах
* Граф построен так, что каждая значимая точка (филд) внутри многоугольника из нейтральных точек

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

## Описание концепции сервера [Документ](https://docs.google.com/document/d/19wJ2J6eMQ3f0qdcpgRliBeUqO_iSqaKN_KV1izEkhKU/edit#)

* У всех филдов накапливается урон от миссии к миссии. Пополняются только активные в миссии аэродромы.
* Захват филда возможен только во время его присутствия в миссии.
* Самолёты на аэродромах в миссии конечны. Допускается посадка на неактивные аэродромы. При этом самолёт поступает на неактивный аэродром.
* Самолёты на аэродромах переходят из миссии в миссию с учётом пополнения.
* Управление выбором филдов на следующую миссию осуществляется через уничтожение прифронтовых целей. Эти цели - "ковырятельные".
* В миссии у сторон по 2 фронтовых филда и 2 тыловых. Оба тыловых выбираются по правилу артиллерийской вилки.
* Филд - это сложная цель, которую невозможно выбить за одну миссию, если он изначально цел. Если филд выбили на 50%(?), то он становится доступным для захвата путём посадки самолётов на него.

### Ангар/модификации

* Самолёты для одного игрока не ограничены. Всегда можно взлетать, если самолёты есть на аэродроме.
* Игроки имеют ограничение модификаций. При неудачном вылете игрок теряет столько модификаций, сколько было на его самолёте.
* Модификации пополняются за результативные вылеты: любой вылет с нанесённым противнику уроном даёт +1 модификацию.