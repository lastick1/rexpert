import threading
from time import sleep
from pathlib import Path
import queue
from cfg import MainCfg
import datetime
from enum import Enum
import socket
# import time


class RconCommunicator:
    """ Communicate with IL-2 Battle of Stalingrad dedicated server
    through Server Remote Console - 'RCon' """

    def __init__(self, tcp_ip, tcp_port, buffer_size=1024):
        self.TCP_IP = tcp_ip
        self.TCP_PORT = tcp_port
        self.BUFFER_SIZE = buffer_size
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.settimeout(500)
        self.CONNECTED = False
        if self.TCP_IP and self.TCP_PORT:
            try:
                self.SOCKET.connect((self.TCP_IP, self.TCP_PORT))
                self.CONNECTED = True
            finally:
                self.AUTHED = False
                self.RESPONSE_LIST = []

    def __rcon_send_raw_command(self, command='mystatus'):
        """Sends command 'as is', may cause errors"""
        if not hasattr(self, 'TCP_IP') \
                or not hasattr(self, 'TCP_PORT') \
                or not hasattr(self, 'BUFFER_SIZE') \
                or not hasattr(self, 'SOCKET'):
            raise NameError("RconCommunicator NotInitialized")
        if type(command) is not str:
            raise NameError("type(command) is not str")

        if not self.CONNECTED:
            return None
        # формируем пакет
        cl = len(command) + 1
        pack_l = cl.to_bytes(2, byteorder='little')
        pack_m = command.encode(encoding='utf-8')
        pack_z = (0).to_bytes(1, byteorder='little')
        packet = pack_l + pack_m + pack_z

        # добавить проверку, установлено ли соединение
        # отправляем пакет
        try:
            self.SOCKET.send(packet)
        except:
            self.CONNECTED = False
            return None
        resp = self.SOCKET.recv(self.BUFFER_SIZE)
        self.RESPONSE_LIST.append((resp, command))
        return str(resp[2:-1], encoding="ascii")

    def reconnect(self):
        self.SOCKET.close()
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.settimeout(500)
        self.CONNECTED = False
        try:
            self.SOCKET.connect((self.TCP_IP, self.TCP_PORT))
            self.CONNECTED = True
        finally:
            self.AUTHED = False

    def auth(self, user, password):
        """Authenticate communicator. Gives more permission if true"""
        if not self.CONNECTED:
            return False

        resp = self.__rcon_send_raw_command("auth {0} {1}".format(user, password))

        if len(resp):
            if resp[-1] == "1":
                self.AUTHED = True
                return True
            else:
                # self.AUTHED = False
                return False
        elif type(resp) is bytes and len(resp) == 0:
            self.AUTHED = True
            return True
        else:
            # self.AUTHED = False
            return False

    def server_status(self):
        if not self.CONNECTED:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("serverstatus")
        return resp

    def player_list(self):
        if not self.CONNECTED:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("getplayerlist")
        return resp

    def chatmsg(self, roomtype, id, message):
        if not self.CONNECTED:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("chatmsg {0} {1} {2}".format(roomtype, id, message))
        return resp

    def private_message(self, account_id, message):
        if not self.CONNECTED:
            raise NameError("Not connected")
        return self.chatmsg(3, account_id, message)

    def allies_message(self, message):
        if not self.CONNECTED:
            raise NameError("Not connected")
        return self.chatmsg(2, 1, message)

    def axis_message(self, message):
        if not self.CONNECTED:
            raise NameError("Not connected")
        return self.chatmsg(2, 2, message)

    def kick(self, name):
        if not self.CONNECTED:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("kick name {0}".format(name))
        return resp

    def ban(self, name):
        if not self.CONNECTED:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("ban name {0}".format(name))
        return resp

    def banuser(self, name):
        if not self.CONNECTED:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("banuser playerid {0}".format(name))
        return resp

    def server_input(self, server_input):
        if not self.CONNECTED:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("serverinput {0}".format(server_input))
        return resp

    pass  # class


class CommandType(Enum):
    none = 0
    message = 1
    kick = 2
    s_input = 3
    ban = 4


class Command:
    def __init__(self, mission_name, tik=0, cmd_type=CommandType.none, account_id='', subject='', reason=''):
        """
        Класс команды, передаваемой серверу
        :param tik: int
        :param mission_name: str
        :param subject: str
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
        if len(self.mission_name):
            return datetime.datetime.strptime(self.mission_name, 'missionReport(%Y-%m-%d_%H-%M-%S)')
        return datetime.datetime.now()

    @property
    def t(self):
        return self.now - self.m_start

    def __eq__(self, other):
        if self.tik == other.tik \
                and self.mission_name == other.mission_name \
                and self.cmd_type == other.cmd_type \
                and self.text == other.text:
            return True
        return False


class Commander:
    def __init__(self):
        """
        Класс, передающий команды/сообщения на сервер и игрокам
        """
        self.commands_pool = dict()
        self._process = Commander.__Process()

    def stop(self):
        self._process.running = False
        self._process.join()

    class __Process(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.queue = queue.Queue()
            self.current_mission = None
            self.running = True
            if MainCfg.offline_mode:
                self._console = None
            else:
                self._console = RconCommunicator(MainCfg.rcon_ip, MainCfg.rcon_port)
                self._console.auth(MainCfg.rcon_login, MainCfg.rcon_password)
            self.start()

        def run(self):
            if MainCfg.offline_mode:
                print('Console Commander started in offline mode')
            else:
                print('Console Commander started')
            while self.running:
                if not self.queue.empty():
                    with Path('./logs/commands_'+self.current_mission+'.txt').absolute().open(
                            mode='a', encoding='utf-8') as cmndr_log:
                        cmd = self.queue.get()
                        if not MainCfg.offline_mode:
                            if cmd.mission_name == self.current_mission:
                                status = 'status'
                                if cmd.cmd_type == CommandType.s_input:
                                    status = self._console.server_input(cmd.text)
                                    line = '{} {} {}'.format(cmd.now.strftime("[%H:%M:%S]"), status, cmd.text)
                                    if MainCfg.console_cmd_output:
                                        print(line)
                                    cmndr_log.write('{} \n'.format(line))
                                    sleep(30)
                                elif cmd.cmd_type == CommandType.kick:
                                    if not MainCfg.test_mode:
                                        status = self._console.kick(cmd.text)
                                    line = '{} {} {} KICK [{}] - {}'.format(
                                        cmd.now.strftime("[%H:%M:%S]"), status, cmd.account_id, cmd.text, cmd.reason)
                                    if MainCfg.console_cmd_output:
                                        print(line)
                                    cmndr_log.write('{} \n'.format(line))
                                elif cmd.cmd_type == CommandType.ban:
                                    if not MainCfg.test_mode:
                                        status = self._console.banuser(cmd.account_id)
                                    line = '{} {} {} BAN [{}] - {}'.format(
                                        cmd.now.strftime("[%H:%M:%S]"), status, cmd.account_id, cmd.text, cmd.reason)
                                    if MainCfg.console_cmd_output:
                                        print(line)
                                    cmndr_log.write('{} \n'.format(line))
                                elif cmd.cmd_type == CommandType.message:
                                    status = self._console.private_message(cmd.account_id, cmd.text)
                                    if MainCfg.console_chat_output:
                                        print(cmd.now.strftime("[%H:%M:%S]"), end=' ')
                                        print("{} MSG [{}]: {}".format(status, cmd.account_id, cmd.text))
                                cmd.is_sent = True
                            else:
                                print("[{}] {} not processed: {} {}".format(
                                    cmd.mission_name, cmd.cmd_type, cmd.text, cmd.account_id))
            print('Console Commander stopped')

    def process_commands(self, commands):
        for cmd in commands:
            if cmd.mission_name not in self.commands_pool:
                self.commands_pool[cmd.mission_name] = []
            if cmd not in self.commands_pool[cmd.mission_name]:
                self.commands_pool[cmd.mission_name].append(cmd)
                self._process.queue.put(cmd)

    def update_current_mission(self, mission_name):
        self._process.current_mission = mission_name
