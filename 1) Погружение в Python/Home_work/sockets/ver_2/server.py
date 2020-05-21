"""
Version 1.2
confirmed 11.04.2020
 """

import socket
import json


class WrongCmd:
    pass


class Server:
    def __init__(self, ip='', port=8888, timeout=None):
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
            self.close()
            break

    def waiting(self):
        # Ждём ообщения от клиента
        while True:
            try:
                rev_data = self.conn.recv(1024)
            except (socket.timeout, ConnectionAbortedError):
                break

            if not rev_data:
                self.conn.send('error\n'.encode('utf8'))
            else:
                self.answer(rev_data)

    def answer(self, rev_data):
        # Этот метод формирует ответ и отвечает клиенту на его запрос
        request = rev_data.decode()
        ans = self.work_with_json(request)
        print('Status: ', ans, '---------')
        return self.conn.send(f'{ans}\n\n'.encode('utf8'))

        # Возможно нужно удалить т.к. исключения обработаны в возвращающей функции separate
        # В случае не валидных значний от клиента ans расняется error
        # except WrongCmd:
        #     print('Error work json file or data')
        #     return self.conn.send('error\n\n'.encode('utf8'))

    def work_with_json(self, request):
        """Функция для записи данных в файл"""
        try:
            data = json.load(open('server_data.json', 'r'))
        except:
            data = {}

        cmd, key, value, time = self.separate(request)
        print('!', cmd, key, value, time)
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - ')
        # Записавыеновые данные в JSON
        if cmd == 'put':
            return self.put_data(data, key, value, time)
        # Формируем ответ клиенту на запрос данных, возвращаем хранящиеся данные
        elif cmd == 'get':
            return self.get_data(data, key)
        else:
            return 'error\nwrong command'

    @staticmethod
    def put_data(data, key, value, time):
        # Записываем нове данные в файл
        with open('server_data.json', 'w') as f:
            # Ключ уже есть в словаре
            if key in data:
                data[key].append((value, time))
            # Кюч необходимо обавить в словарь
            else:
                data[key] = [(value, time)]
            json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
            return 'ok'

    @staticmethod
    def get_data(data, key):
        # От нас хотят значения по определённому ключу
        answer = 'ok'
        if key in data and key != '*':
            for metric in data[key]:
                answer += f'\n{key} {metric[0]} {metric[1]}'
            # return "dfdfkj lkjkj"
            return f'{answer}'
        # От нас хотят все значения, которые хранятся на сервере в JSON
        elif key == '*':
            for item in data:
                for metric in data[item]:
                    answer += f'\n{item} {metric[0]} {metric[1]}'
            return f'{answer}'
        # Если неверный ключ, возвращаем просто окей
        else:
            return 'ok'

    @staticmethod
    def separate(request):
        # Метод позволяет определить, что нам передал клиент, разбиваем запрос на переменные.
        # В итоге возвращем четыре переменные в work_with_json, либо пустые значения
        try:
            cnt = len(request.strip().split())
            if cnt == 4:
                cmd, key, value, time = request.split()
                return cmd, key, float(value), int(time)
            elif cnt == 2:
                cmd, key = request.split()
                return cmd, key, None, None
            # Если что-то не так, то возвращаем пустые значения, в принимающей функции будет выкинуто исключение
            return None, None, None, None
        # Если невалидные данные, то возвращаем пустые значения, в принимающей функции будет выкинуто исключение
        except ValueError:
            return None, None, None, None

    def close(self):
        self.server_socket.close()
        print('\nDisconnect\n\n'.upper())


start = Server()
