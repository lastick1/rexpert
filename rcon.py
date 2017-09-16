""" Модуль взаимодействия с консолью DServer """
import threading
from time import sleep
from pathlib import Path
import queue
import datetime
from enum import Enum
from socket import socket, AF_INET, SOCK_STREAM
# import time


class RconCommunicator:
    """ Communicate with IL-2 Battle of Stalingrad dedicated server
    through Server Remote Console - 'RCon' """

    def __init__(self, tcp_ip, tcp_port, buffer_size=1024):
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(500)
        self.connected = False
        if self.tcp_ip and self.tcp_port:
            try:
                self.socket.connect((self.tcp_ip, self.tcp_port))
                self.connected = True
            finally:
                self.authed = False
                self.response_list = []

    def __rcon_send_raw_command(self, command: str = 'mystatus'):
        """Sends command 'as is', may cause errors"""
        if not hasattr(self, 'tcp_ip') or not hasattr(self, 'tcp_port') \
        or not hasattr(self, 'buffer_size') or not hasattr(self, 'socket'):
            raise NameError("RconCommunicator NotInitialized")

        if not self.connected:
            return None
        # формируем пакет
        command_len = len(command) + 1
        pack_l = command_len.to_bytes(2, byteorder='little')
        pack_m = command.encode(encoding='utf-8')
        pack_z = (0).to_bytes(1, byteorder='little')
        packet = pack_l + pack_m + pack_z

        # добавить проверку, установлено ли соединение
        # отправляем пакет
        try:
            self.socket.send(packet)
        except: #pylint: disable=W0702
            self.connected = False
            return None
        resp = self.socket.recv(self.buffer_size)
        self.response_list.append((resp, command))
        return str(resp[2:-1], encoding="ascii")

    def reconnect(self):
        """ Переподключение к консоли """
        self.socket.close()
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(500)
        self.connected = False
        try:
            self.socket.connect((self.tcp_ip, self.tcp_port))
            self.connected = True
        finally:
            self.authed = False

    def auth(self, user, password):
        """Authenticate communicator. Gives more permission if true"""
        if not self.connected:
            return False

        resp = self.__rcon_send_raw_command("auth {0} {1}".format(user, password))

        if len(resp):  #pylint: disable=C1801
            if resp[-1] == "1":
                self.authed = True
                return True
            else:
                # self.AUTHED = False
                return False
        elif isinstance(resp, bytes) and len(resp) == 0:  #pylint: disable=C1801
            self.authed = True
            return True
        else:
            # self.AUTHED = False
            return False

    def server_status(self):
        """ Статус сервера (типа пинг) """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("serverstatus")
        return resp

    def player_list(self):
        """ Получение списка игроков (тяжёлая команда) """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("getplayerlist")
        return resp

    def chatmsg(self, roomtype, identifier, message):
        """ Отправка сообщения в чат сервера """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command(
            "chatmsg {0} {1} {2}".format(roomtype, identifier, message))
        return resp

    def info_message(self, message):
        """ Сообщение всем пользователям """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("chatmsg 0 0 {}".format(message))
        return resp

    def private_message(self, account_id, message):
        """ Сообщение конкретному пользователю """
        if not self.connected:
            raise NameError("Not connected")
        return self.chatmsg(3, account_id, message)

    def allies_message(self, message):
        """ Сообщение команде союзников """
        if not self.connected:
            raise NameError("Not connected")
        return self.chatmsg(2, 1, message)

    def axis_message(self, message):
        """ Сообщение команде люфтваффе """
        if not self.connected:
            raise NameError("Not connected")
        return self.chatmsg(2, 2, message)

    def kick(self, name):
        """ Кик пользователя """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("kick name {0}".format(name))
        return resp

    def ban(self, name):
        """ Бан пользователя на 7 дней """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("ban name {0}".format(name))
        return resp

    def banuser(self, name):
        """ Бан пользователя на 15 минут """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("banuser playerid {0}".format(name))
        return resp

    def server_input(self, server_input):
        """ Отправка сервер-инпута в логику миссии """
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("serverinput {0}".format(server_input))
        return resp


class CommandType(Enum):
    """ Тип команды """
    none = 0
    message = 1
    kick = 2
    s_input = 3
    ban = 4
    info = 5


class Command:
    """ Команда, передаваемая серверу """
    def __init__(
            self,
            mission_name: str,
            tik: int = 0,
            cmd_type: CommandType = CommandType.none,
            account_id: str = '',
            subject: str = '',
            reason: str = ''):
        """
        :param tik: тик
        :param cmd_type: тип команды
        :param mission_name: имя миссии
        :param subject: тело команды (сообщение, ник)
        :param reason: причина отправки команды
        """
        self.tik = tik
        self.cmd_type = cmd_type
        self.account_id = account_id
        self.mission_name = mission_name
        self.text = subject
        self.reason = reason
        self.now = datetime.datetime.now()
        self.is_sent = False

    @property
    def m_start(self):
        """ Начало миссии """
        if self.mission_name:
            return datetime.datetime.strptime(self.mission_name, 'missionReport(%Y-%m-%d_%H-%M-%S)')
        return datetime.datetime.now()

    @property
    def time_passed(self):
        """ Время с начала миссии """
        return self.now - self.m_start

    def __eq__(self, other):
        if self.tik == other.tik \
                and self.mission_name == other.mission_name \
                and self.cmd_type == other.cmd_type \
                and self.text == other.text:
            return True
        return False


class Commander:
    """ Класс, передающий команды/сообщения на сервер и игрокам """
    def __init__(self, config):
        self.commands_pool = dict()
        self._process = Commander._Process(config)

    def stop(self):
        """ Остановка работы """
        self._process.running = False
        self._process.join()

    class _Process(threading.Thread):
        """ Синлтон """
        def __init__(self, config):
            if not config:
                return
            threading.Thread.__init__(self)
            self.queue = queue.Queue()
            self.current_mission = None
            self.running = True
            self.offline_mode = config.offline_mode
            self.console_cmd_output = config.console_cmd_output
            self.console_chat_output = config.console_chat_output
            self.test_mode = config.test_mode
            if config.offline_mode:
                self._console = None
            else:
                self._console = RconCommunicator(config.rcon_ip, config.rcon_port)
                self._console.auth(config.rcon_login, config.rcon_password)
            self.start()

        def run(self):
            if self.offline_mode:
                print('Console Commander started in offline mode')
            else:
                print('Console Commander started')
            while self.running:
                if not self.queue.empty():
                    with Path('./logs/commands_'+self.current_mission+'.txt').absolute().open(
                        mode='a', encoding='utf-8') as cmndr_log:
                        cmd = self.queue.get()
                        if not self.offline_mode:
                            if cmd.mission_name == self.current_mission:
                                status = 'status'
                                if cmd.cmd_type == CommandType.s_input:
                                    status = self._console.server_input(cmd.text)
                                    line = '{} {} {} {}'.format(
                                        cmd.now.strftime("[%H:%M:%S]"),
                                        status,
                                        cmd.text,
                                        cmd.reason)
                                    if self.console_cmd_output:
                                        print(line)
                                    cmndr_log.write('{} \n'.format(line))
                                    sleep(30)
                                elif cmd.cmd_type == CommandType.kick:
                                    if not self.test_mode:
                                        status = self._console.kick(cmd.text)
                                    line = '{} {} {} KICK [{}] - {}'.format(
                                        cmd.now.strftime("[%H:%M:%S]"),
                                        status,
                                        cmd.account_id,
                                        cmd.text,
                                        cmd.reason)
                                    if self.console_cmd_output:
                                        print(line)
                                    cmndr_log.write('{} \n'.format(line))
                                elif cmd.cmd_type == CommandType.ban:
                                    if not self.test_mode:
                                        status = self._console.banuser(cmd.account_id)
                                    line = '{} {} {} BAN [{}] - {}'.format(
                                        cmd.now.strftime("[%H:%M:%S]"),
                                        status,
                                        cmd.account_id,
                                        cmd.text,
                                        cmd.reason)
                                    if self.console_cmd_output:
                                        print(line)
                                    cmndr_log.write('{} \n'.format(line))
                                elif cmd.cmd_type == CommandType.message:
                                    status = self._console.private_message(cmd.account_id, cmd.text)
                                    if self.console_chat_output:
                                        print(cmd.now.strftime("[%H:%M:%S]"), end=' ')
                                        print("{} MSG [{}]: {}".format(
                                            status, cmd.account_id, cmd.text))
                                elif cmd.cmd_type == CommandType.info:
                                    status = self._console.info_message(cmd.text)
                                    if self.console_chat_output:
                                        print(cmd.now.strftime("[%H:%M:%S]"), end=' ')
                                        print("{} MSG [{}]: {}".format(
                                            status, cmd.account_id, cmd.text))
                                cmd.is_sent = True
                            else:
                                print("[{}] {} not processed: {} {}".format(
                                    cmd.mission_name, cmd.cmd_type, cmd.text, cmd.account_id))
            print('Console Commander stopped')

    def process_commands(self, commands: list):
        """ Обработать список команд (отправить) """
        for cmd in commands:
            if cmd.mission_name not in self.commands_pool:
                self.commands_pool[cmd.mission_name] = []
            if cmd not in self.commands_pool[cmd.mission_name]:
                self.commands_pool[cmd.mission_name].append(cmd)
                self._process.queue.put(cmd)

    def update_current_mission(self, mission_name):
        """ Обновить текущую миссию """
        self._process.current_mission = mission_name

    def message(self, account_id: str, text: str, reason: str = 'info message'):
        """ Отправить сообщение """
        commands = list()
        commands.append(Command(
            '',
            cmd_type=CommandType.message,
            account_id=account_id,
            subject=text,
            reason=reason
        ))
        self.process_commands(commands)
