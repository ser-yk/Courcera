"""
Version 1.3
confirmed 13.04.2020
Третья версия является ассинхронной
 """

import asyncio
import json


class EchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        # print('Connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        request = data.decode()
        ans = self.work_with_json(request)
        # print('Data received: {!r}'.format(request))

        # print('Send: {!r}'.format(ans))
        self.transport.write(f'{ans}\n\n'.encode('utf8'))

        # print('Close the client socket:', self.peername)
        # self.transport.close()

    def work_with_json(self, request):
        """Функция для записи данных в файл"""
        try:
            data = json.load(open('server_data_7.json', 'r'))
        except:
            data = {}

        cmd, key, value, time = self.separate(request)
        # Записавыеновые данные в JSON
        if cmd == 'put':
            return self.put_data(data, key, value, time)
        # Формируем ответ клиенту на запрос данных, возвращаем хранящиеся данные
        elif cmd == 'get':
            return self.get_data(data, key)
        else:
            return 'error\nwrong command'

    @ staticmethod
    def put_data(data, key, value, time):
        # Записываем нове данные в файл
        with open('server_data_7.json', 'w') as f:

            # Ключ уже есть в словаре
            if key in data:
                # Если последний timestamp был меньше секунды назад, перезаписываем данные на более поздние
                for item in reversed(range(len(data[key]))):
                    if time - data[key][item][1] < 1:
                        data[key].pop(item)
                        # data[key].append((value, time))
                data[key].append((value, time))


            # Кюч необходимо добавить в словарь
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
            return f'{answer}'
        # От нас хотят все значения, которые хранятся на сервере в JSON
        elif key == '*':
            for item in data:
                for metric in data[item]:
                    answer += f'\n{item} {metric[0]} {metric[1]}'
            return f'{answer}'
        # Если неверный ключ, возвращаем просто окей
        else:
            return answer

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


def run_server(host, port):
    # asyncio.run(main(host, port))
    # Костыль чтобы перезаписать файл на тестерировочном сервере курсеры
    f = open('server_data_7.json', 'w')
    f.close()
    
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        EchoServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()



# run_server('127.0.0.1', 8001)

