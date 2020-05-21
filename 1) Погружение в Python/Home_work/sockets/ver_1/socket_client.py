"""
Version 1.1
confirmed 09.04.2020
"""

import socket


class Client:
    def __init__(self, ip, port, timeout=None):
        self.client_socket = socket.create_connection((ip, port), timeout)
        # self.client_socket.settimeout(timeout)

    def put(self, cmd):
        try:
            self.client_socket.sendall(cmd.encode('utf8'))
        except socket.timeout:
            print("send data timeout")
        except socket.error as ex:
            print('send data error', ex)

    def get(self, cmd):
        try:
            self.client_socket.sendall(cmd.encode('utf8'))
        except socket.timeout:
            print("send data timeout")
        except socket.error as ex:
            print('send data error', ex)

    def work_with(self):
        while True:
            request = str(input())
            cmd, key, value, time = self.separate(request)
            while cmd != 'put' and cmd != 'get':
                request = str(input('Error command! Please input new:\n'))
                cmd, key, value, time = self.separate(request)
            if cmd == 'put':
                self.put(request)
            elif cmd == 'get':
                self.get(request)
            print(self.client_socket.recv(1024).decode())

    @staticmethod
    def separate(request):
        # Метод позволяет определить, что нам передал клиент, разбиваем запрос на переменные.
        # Передаём переменные в work_with_json
        cnt = len(request.split())
        if cnt == 4:
            cmd, key, value, time = request.split()
            return cmd, key, value, time
        elif cnt == 2:
            cmd, key = request.split()
            return cmd, key, None, None

        return None, None, None, None

    def close(self):
        self.client_socket.close()
        print('Disconnect')


start = Client('127.0.0.1', 8001)
start.work_with()
