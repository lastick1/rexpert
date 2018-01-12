# Конфигурация коммандера Random Expert

## conf.ini - основной файл настроек коммандера

### Секция PROGRAM - ключевые настройки

offline_mode = false (или true - включена или нет работа с RCon)
test_mode = false (или true - тестовый режим - отключает кик)
debug_mode = false (или true - режим отладки)
console_cmd_output = true (или false - дублировать отправку команд в консоль)
console_chat_output = true (или false - дублировать отправку чата в консоль)
minimal_chat_interval = 120 (целое число - интервал отправки сообщений в чат и задержка отправки после serverInput)
draw_edges = false (или true - отображать ребра графа на карте)
draw_nodes = false (или true - отображать узлы графа на карте)
draw_nodes_text = true (или false - отображать текст на узлах графа на карте - неактуально)
draw_influences = false (или true - генерировать Translator:InfluenceArea для каждого аэродрома - неактуально)

game_folder = .\tmp (корневая папка игры)
graph_files_folder = .\tmp (папка с файлами графа - неактуально)
maps_archive_folder = .\tmp (папка для сохранения истории сгенерированных изображений карты)
icons_folder = .\tmp (папка с иконками)
stats_folder = .\tmp (папка статистики =FB=vaal)

### Секция MISSIONGEN

campaign_missions = 181
use_resaver = false
generate_missions = true
special_influences = false
mission_gen_folder = .\tmp
resaver_folder = .\tmp

### Секция RCON - настройки подключения к консоли RCon

rcon_ip = localhost
rcon_port = 8991
rcon_login = myemail@mailprovider.domen
rcon_password = mypassword

### Секция STATS - настройки подключения к базе данных статистики =FB=vaal

user = il2_stats
database = il2_stats
host = 127.0.0.1
port = 5555
password =  il2_stats

### Секция MONGO - настройки подключения к MongoDB

host = localhost
port = 27017
database = test_rexpert

### Секция DSERVER

logs_directory = .\tmp
arch_directory = .\tmp
chat_directory = .\tmp

### Секция NEW_STATS

logs_directory = .\tmp
zips_directory = .\tmp
msrc_directory = .\tmp

## gameplay.json - игровые настройки коммандера (не сервера)

mission_time - длительность миссии в формате 02:30:00 (часы, минуты, секунды)
airfield_radius - радиус аэродрома 
