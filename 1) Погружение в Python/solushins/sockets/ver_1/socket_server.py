"""
Version 1.1
confirmed 09.04.2020
 """

import socket
import json


class WrongCmd:
    pass


class Server:
    def __init__(self, ip='', port=8001, timeout=None):
        self.timeout = timeout
        self.server_socket = socket.socket()
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        self.connect()

    def connect(self):
        while True:
            self.conn, self.addr = self.server_socket.accept()
            self.conn.settimeout(self.timeout)
            print('Connected', self.addr)
            self.waiting()

    def waiting(self):
        while True:
            try:
                rev_data = self.conn.recv(1024)
                # self.conn.send('Something\n'.encode('utf8'))
            except socket.timeout:
                self.conn.send('error\n'.encode('utf8'))
                print("close connection by timeout")
                break

            if not rev_data:
                self.conn.send('error\n'.encode('utf8'))
            else:
                self.answer(rev_data)

    def answer(self, rev_data):
        request = rev_data.decode()
        try:
            ans = self.work_with_json(request)
            return self.conn.sendall(f'{ans}\n'.encode('utf8'))
        except WrongCmd:
            print('Error work json file or data')
            return self.conn.sendall('Error command\n'.encode('utf8'))

    def work_with_json(self, request):
        """Функция для записи данных в файл"""
        try:
            data = json.load(open('server_data.json', 'r'))
        except:
            data = {}

        cmd, key, value, time = self.separate(request)
        if cmd == 'put':
            with open('server_data.json', 'w') as f:
                if key in data:
                    data[key].append((value, time))
                else:
                    data[key] = [(value, time)]
                json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
                return "Data was added"
        elif cmd == 'get':
            if key in data and key != '*':
                return data[key]
            elif key == '*':
                return data
            else:
                return 'Wrong key'
        else:
            return "Error. Some problems with file or data"

    @staticmethod
    def separate(request):
        # Метод позволяет определить, что нам передал клиент, разбиваем запрос на переменные.
        # Передаём переменные в work_with_json
        cnt = len(request.split())
        if cnt == 4:
            cmd, key, value, time = request.split()
            return cmd, key, float(value), int(time)
        elif cnt == 2:
            cmd, key = request.split()
            return cmd, key, None, None
        # Если что-то не так, то возвращаем пустые значения, в принимающей функции будет выкинуто исключение
        return None, None, None, None

    def close(self):
        self.server_socket.close()
        print('Disconnect')


start = Server()
