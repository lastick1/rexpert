# Коммандер Random Expert

## Версия 'Divisions'

Планы и прогресс можно посмотреть по issues в текущем GitHub репозитории

### Базовая логика игрового процесса

* Самолёты на аэродромах конечны
* Посадка допускается на любом аэродроме на своей территории, включая недоступные для взлёта в миссии

#### Главная цель миссии - захватить один из аэродромов противника, набрав 13 очков захвата

##### В каждой миссии у сторон есть следующие цели для уничтожения

|Тип цели|Количество|Очки захвата|Идут в следующую миссию|
| --- | :---: | --- | --- |
|Фронтовой аэродром| 3 | 1 | Нет |
|Укрепрайон| 3 | 3 | Да |
|Артиллерийская позиция| 3 | 2 | Нет |
|Тыловой склад| 2 | 4 | Да |
|Танковое наступление| 2 | -1 у противника | Нет |

Захватывается тот аэродром, на котором меньше всего самолётов к концу миссии

#### Дополнительно

* У сторон есть по 2 дополнительных тыловых аэродрома для получения пополнения самолётов.
* В конце миссии самолёты с тыловых аэродромов автоматически пополняют парк фронтовых аэродромов
* Один раз в игровой месяц приходит поставка самолётов, распределяемая по всем аэродромам на карте

## Сборка, настройка и запуск проекта

1. Установить статистику il2_stats от =FB=Vaal
1. Установить зависимости, выполнив install.bat в корне репозитория.
1. Установить и запустить MongoDB
1. Скопировать папку data/scg в папку игры, чтобы scg также была в <папка_с_игрой>/data
1. Скопировать папку missiongen в папку bin игры
1. Настроить конфигурационный файл main.json. Рекомендуется использовать IDE для его редактирования, чтобы работали подсказки к настройкам. Описание настроек по спецификации [json-schema](https://json-schema.org/) есть в файле ./data/schemas/main.json.
1. Инициализировать кампанию, выполнив `python runme.py initialize`
1. Настроить SDS для DServer, чтобы в нём были миссии result1 и result2, идущие по кругу. Оставить хотя бы 3-минутный отсчёт конца миссии, чтобы коммандер успевал сгенерировать следующую миссию.
1. Настроить консоль сервера (RCon). Не забывать указать настройки подключения и для коммандера в main.json.
1. Очистить папку с логами DServer.
1. Запустить DServer, дождаться загрузки миссии.
1. Запустить коммандер, выполнив `python runme.py run`

### Известные особенности логов DServer

* Не важно, как игрок покинул с сервера - у его бота должен быть атайп деинициализации
* В конце раунда (Max time for round, tdmRoundTime в SDS) в лог выдаётся атайп 19

## Спецификация

### Конфиги (configs)

#### .py файлы менять настоятельно не рекомендуется

В папке **configs** хранится конфигурация коммандера в json, xgml, txt и csv файлах

* main.json - основной файл настроек коммандера
* ban_list_permanent.txt - список навсегда забаненных пользователей
* mgen.json - настройки генерации ТВД и генерации миссий
* gameplay.json - настройки игровых параметров на сервере
* planes.json - настройки распределения и генерации самолётов на аэродромах (лочки, скины)
* stats_custom.json - настройки интеграции со статистикой
* draw_settings.json - настройки отрисовки карт на сайте
* dfpr.json - данные настроек генерации миссий, подставляемые в шаблон в соответствии с ТВД
* objects.csv - все игровые объекты (для обновления брать из статы =FB=vaal)

### MongoDB

* В версии divisions используется [MongoDB](https://www.mongodb.com/download-center?jmp=nav#community)
* Ей для запуска надо указать папку для хранения базы данных
* Стандартный порт: 27017
* [Настройка на запуск как Windows Service](https://stackoverflow.com/questions/2438055/how-to-run-mongodb-as-windows-service)
> D:\mongodb\bin>mongod --dbpath=D:\mongodb --logpath=D:\mongodb\log.txt --install
* Для удобства (GUI) можно использовать [Robo 3T](https://robomongo.org)
* В этой БД данные хранятся в коллекциях json-объектов (коллекции документов)
* Чтобы найти конкретный документ в коллекции, надо в find указать объект-запрос вида: {"Имя_свойства": "Значение_свойства"}
* В Robomongo (*Robo 3T*) документы редактируются как текстовые объекты: ПКМ по документу коллекции -> Edit Document

### Генерация

Для контроля версий шаблонов миссий и баз локаций эти данные сохранены в папке data в проекте. При обновлении следует скопировать файлы в соответствующие папки и закоммитить изменения. Сохранять бэкапы не нужно, всё хранит контроль версий.

Сервер генерирует координатные группы для каждого аэродрома, описанного в moscow_fields.csv, stalin_fields.csv и kuban_fields.csv файлах. Координатная группа представляет из себя MCU аэродрома с объектным и целевым input триггером на него, которые должны соединяться с логикой, задаваемой в отдельной группе.

Субтитры аэродромов будут генерироваться по шаблонной группе: необходимо создать группу с субтитрами, где вместо имени аэродрома прописать !AFNAME!. Это будет служить меткой, куда при генерации будет подставлено наименование аэродрома.

Генератор (MissionGen.exe) должен запускаться в каталоге с игрой, т.к. он использует её структуру при выдаче миссии. По-умолчанию он складывает генерируемые миссии в data/Missions с именем result.Mission.
Ресурсы для генерации тоже должны быть в каталоге с игрой (data/scg). Иначе генератор не может найти зависимости и не работает.