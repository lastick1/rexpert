# from time import sleep
from datetime import datetime
import threading
import rcon
import db
import campaign
import business
from pathlib import Path
import gen
date_format = 'missionReport(%Y-%m-%d_%H-%M-%S)'

connector = db.PGConnector


def log_this(msg, m_name):
    with Path('./logs/timing_log_' + m_name + '.txt').open(
            mode='a', encoding='utf-8') as f:
        f.write(msg)
        f.write('\n')


class Processor:
    def __init__(self, commander):
        """ Класс контроля за обработкой
        :type commander: rcon.Commander """
        self.campaign = campaign.Campaign()
        self.commander = commander
        self.business = dict()
        self.threads = dict()
        self.missions = dict()
        self.last_mission = None
        self.filter_int = 0

    def _process(self, m_name, logs):
        """ Обработка логов """
        self.commander.update_current_mission(m_name)
        if not self.last_mission:
            self.last_mission = m_name
        else:
            if datetime.strptime(m_name, date_format) > datetime.strptime(self.last_mission, date_format):
                self.last_mission = m_name
        if m_name not in self.missions.keys():
            # если миссия новая, то создаём её
            self.missions[m_name] = campaign.Mission(m_name, connector.get_objects_dict())
        # обновление миссии новыми логами
        self.missions[m_name].update(logs)
        if datetime.strptime(m_name, date_format) < datetime.strptime(self.last_mission, date_format):
            self.missions[m_name].complete()
        # отправка сервер инпутов об уничтоженных наземных целях
        if not self.missions[m_name].is_ended:
            connector.Missions.save_score(m_name, self.missions[m_name].score)
            self.commander.process_commands(self.missions[m_name].commands)  # команды инфо счёта и инпуты захвата
            self.commander.process_commands(self.missions[m_name].g_report.killed_commands)

        # бизнес-логика
        if m_name not in self.business.keys():
            self.business[m_name] = business.Business(m_name)
        self.business[m_name].update(
            self.missions[m_name].m_report.sorties,
            self.missions[m_name].is_ended,
            self.missions[m_name].tvd_name
        )
        # отправка сервер инпутов с чатом и киками
        if not self.missions[m_name].is_ended:
            self.commander.process_commands(self.business[m_name].commands)

        u = self.campaign.update(self.missions[m_name])
        if u:
            # если требуется обновить следующую миссию
            if m_name not in self.threads.keys():
                self.threads[m_name] = threading.Thread(args=(u[0], u[1]), target=gen.Generator.make_mission)
                self.threads[m_name].start()
            else:
                self.threads[m_name].join()
                self.threads[m_name] = threading.Thread(args=(u[0], u[1]), target=gen.Generator.make_mission)
                self.threads[m_name].start()

    def consume(self, m_name, logs):
        """ Обработать новые логи миссии """
        self._process(m_name, logs)

    def notify(self, m_name):
        """ Уведомить о приходе нового лог-файла миссии """
        last_atype = 0
        if m_name in self.missions.keys():
            last_atype = self.missions[m_name].last_atype
        logs = connector.Missions.select_mission_log_atypes(m_name, last_atype=last_atype)
        self.consume(m_name, logs)
