# Коммандер Random Expert

## Версия 'Divisions'

**В процессе:**

* Хранение графа кампании в файле
* Учёт самолётов на аэродромах
* Рефакторинг кода. Тестируемость старых классов.
* Механизм дивизий, смотреть описание в секретной лаборатории
* Новая обработка логов

**В планах:**

* Учёт повреждений аэродромов
* Захват аэродромов
* Запуск DServer из-под коммандера
  C:\DServer\Normal\bin\game\normal.exe C:\DServer\Normal\data\normal.sds
* Grid.IsValidForGeneration()

**Готово:**

* Распределение самолётов на старте по приоритетным тыловым филдам
* Сборка файла миссии
* Управление аэродромами
* Обновление папки ТВД (scg/1, scg/2)
* Генерация базы локаций
  * Определение прифронтовой территории по треугольникам
  * Сборка файла базы локаций
  * Генерация базы локаций (покраска)
* Генерация координатных групп субтитров
* Генерация координатных групп аэродромов (плейнсетов с анлоками)
* Уход от использования классов il2_stats
* Переход на использование MongoDB для хранения информации о гаражах
* Граф построен так, что каждая значимая точка (филд) внутри многоугольника из нейтральных точек
* Покрытие тестами нового функционала

### Известные особенности логов DServer

* Не важно, как игрок покинул с сервера - у его бота должен быть атайп деинициализации

## Описание концепции сервера [Документ](https://docs.google.com/document/d/19wJ2J6eMQ3f0qdcpgRliBeUqO_iSqaKN_KV1izEkhKU/edit#)

* У всех филдов накапливается урон от миссии к миссии. Пополняются только активные в миссии аэродромы.
* Захват филда возможен только во время его присутствия в миссии.
* Самолёты на аэродромах в миссии конечны. Допускается посадка на неактивные аэродромы. При этом самолёт поступает на неактивный аэродром.
* Самолёты на аэродромах переходят из миссии в миссию с учётом пополнения.
* В миссии у сторон по 3 фронтовых филда и 1 тыловой.
* Филд - это сложная цель, которую невозможно выбить за одну миссию, если он изначально цел. Если филд выбили на 50%(?), то он становится доступным для захвата путём посадки самолётов на него.

### Ангар/модификации

* Самолёты для одного игрока не ограничены. Всегда можно взлетать, если самолёты есть на аэродроме.
* Игроки имеют ограничение модификаций. При неудачном вылете игрок теряет столько модификаций, сколько было на его самолёте.
* Модификации пополняются за результативные вылеты: любой вылет с нанесённым противнику уроном даёт +1 модификацию.

## Спецификация

### Конфиги (configs)

#### .py файлы менять настоятельно не рекомендуется

В папке **configs** хранится конфигурация коммандера в ini, txt, xgml, json и csv файлах

* conf.ini - основной файл настроек коммандера
* ban_list_permanent.txt - список навсегда забаненных пользователей
* missiongen.json - настройки генерации ТВД и генерации миссий
* gameplay.json - настройки игровых параметров на сервере
* planes.json - настройки распределения и генерации самолётов на аэродромах (лочки, скины)
* stats_custom.json - настройки интеграции со статистикой
* draw_settings.json - настройки отрисовки карт на сайте
* dfpr.json - данные настроек генерации миссий, подставляемые в шаблон в соответствии с ТВД
* c_start.json - начальное состояние кампании (текущий твд и даты в твд)
* defaultparams_template.dat - шаблон файла настроек генерации миссий
* objects.csv - все игровые объекты (для обновления брать из статы =FB=vaal)

### MongoDB

* На ветке divisions используется [MongoDB](https://www.mongodb.com/download-center?jmp=nav#community)
* Ей для запуска надо указать папку для хранения базы данных
* Стандартный порт: 27017
* [Настройка на запуск как Windows Service](https://stackoverflow.com/questions/2438055/how-to-run-mongodb-as-windows-service)
* Для удобства (GUI) можно использовать [Robo 3T](https://robomongo.org)
* В этой базе данные хранятся в коллекциях json-объектов (коллекции документов)
* Чтобы найти конкретный документ в коллекции, надо в find указать объект-запрос вида: {"Имя_свойства": "Значение_свойства"}
* В Robomongo (*Robo 3T*) документы редактируются как текстовые объекты: ПКМ по документу коллекции -> Edit Document

### Генерация

Для контроля версий шаблонов миссий и баз локаций эти данные сохранены в папке data в проекте. При обновлении следует скопировать файлы в соответствующие папки и закоммитить изменения. Сохранять бэкапы не нужно, всё хранит контроль версий.

Сервер генерирует координатные группы для каждого аэродрома, описанного в moscow_fields.csv, stalin_fields.csv и kuban_fields.csv файлах. Координатная группа представляет из себя MCU аэродрома с объектным и целевым input триггером на него, которые должны соединяться с логикой, задаваемой в отдельной группе.

Субтитры аэродромов будут генерироваться по шаблонной группе: необходимо создать группу с субтитрами, где вместо имени аэродрома прописать !AFNAME!. Это будет служить меткой, куда при генерации будет подставлено наименование аэродрома.
