"""Модуль взаимодействия с консолью DServer"""
from socket import socket, AF_INET, SOCK_STREAM


class DServerRcon:
    """Взаимеодействие с сервером Ил-2 Штурмовик: Битва за Сталинград
    через Server Remote Console - 'RCon'"""

    def __init__(self, tcp_ip: str, tcp_port: str, buffer_size: int = 1024):
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(500)
        self.connected = False
        self.authed = False
        self.response_list = []

    def __del__(self):
        self.socket.close()

    def __rcon_send_raw_command(self, command: str = 'mystatus'):
        """Отправка команды на сервер 'as is', может вызывать ошибки"""
        if not self.connected:
            raise NameError('Not connected')

        # формирование пакета
        command_len = len(command) + 1
        pack_l = command_len.to_bytes(2, byteorder='little')
        pack_m = command.encode(encoding='utf-8')
        pack_z = (0).to_bytes(1, byteorder='little')
        packet = pack_l + pack_m + pack_z

        # отправка пакета
        try:
            self.socket.send(packet)
        except:  # pylint: disable=W0702
            self.connected = False
            raise

        # получение ответа
        resp = self.socket.recv(self.buffer_size)
        self.response_list.append((resp, command))
        return str(resp[2:-1], encoding="ascii")

    def connect(self):
        """Подключиться к консоли"""
        if not hasattr(self, 'tcp_ip') or not hasattr(self, 'tcp_port') \
        or not hasattr(self, 'buffer_size') or not hasattr(self, 'socket'):
            raise NameError('Not initialized')

        self.socket.settimeout(500)
        if not self.connected:
            try:
                self.authed = False
                self.socket.connect((self.tcp_ip, self.tcp_port))
                self.connected = True
            except:
                self.connected = False
                self.authed = False

    def reconnect(self):
        """Переподключение к консоли"""
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
        """Авторизация в консоли для дополнительных команд"""
        if not self.connected:
            return False

        resp = self.__rcon_send_raw_command("auth {0} {1}".format(user, password))

        if len(resp):  # pylint: disable=C1801
            if resp[-1] == "1":
                self.authed = True
                return True
            else:
                # self.AUTHED = False
                return False
        elif isinstance(resp, bytes) and len(resp) == 0:  # pylint: disable=C1801
            self.authed = True
            return True
        else:
            # self.AUTHED = False
            return False

    def server_status(self):
        """Статус сервера (типа пинг)"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("serverstatus")
        return resp

    def player_list(self):
        """Получение списка игроков (тяжёлая команда)"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("getplayerlist")
        return resp

    def chatmsg(self, roomtype, identifier, message):
        """Отправка сообщения в чат сервера"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command(
            "chatmsg {0} {1} {2}".format(roomtype, identifier, message))
        return resp

    def info_message(self, message):
        """Сообщение всем пользователям"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("chatmsg 0 0 {}".format(message))
        return resp

    def private_message(self, account_id: str, message: str):
        """Сообщение конкретному пользователю"""
        if not self.connected:
            raise NameError("Not connected")
        return self.chatmsg(3, account_id, message)

    def allies_message(self, message):
        """Сообщение команде союзников"""
        if not self.connected:
            raise NameError("Not connected")
        return self.chatmsg(2, 1, message)

    def axis_message(self, message):
        """Сообщение команде люфтваффе"""
        if not self.connected:
            raise NameError("Not connected")
        return self.chatmsg(2, 2, message)

    def kick(self, name):
        """Кик пользователя"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("kick name {0}".format(name))
        return resp

    def ban(self, name):
        """Бан пользователя на 7 дней"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("ban name {0}".format(name))
        return resp

    def banuser(self, name):
        """Бан пользователя на 15 минут"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("banuser playerid {0}".format(name))
        return resp

    def server_input(self, server_input):
        """Отправка сервер-инпута в логику миссии"""
        if not self.connected:
            raise NameError("Not connected")
        resp = self.__rcon_send_raw_command("serverinput {0}".format(server_input))
        return resp
