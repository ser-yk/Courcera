"""
Version 1.2
confirmed 11.04.2020
"""
import socket
import time


class ClientError(socket.error):
    pass


class Client:
    def __init__(self, ip, port, timeout=None):
        self.client_socket = socket.create_connection((ip, port), timeout)

    def put(self, key, value, timestamp=None):
        data = f'put {key} {value} {timestamp or int(time.time())}\n'
        self.client_socket.send(data.encode('utf8'))
        status, data = self.client_socket.recv(1024).decode().split('\n', 1)
        if status == 'error':
            raise ClientError

    def get(self, key):
        self.client_socket.send(f'get {key}\n'.encode('utf8'))
        revc = self.client_socket.recv(1024).decode()
        status, data = revc.split('\n', 1)
        # Сервер вернул ОК, что значит, что такого ключа нет
        # Возвращаем пустой список
        if status == "ok" and len(data) < 3:
            return {}
        elif status == 'ok' and data:
            dic = self.format_data(revc)
            if dic:
                return dic
            else:
                raise ClientError
        else:
            raise ClientError
        # Ключ был успешно найден, формируем словарь из полученной строки для вывода на экран

    @staticmethod
    def format_data(r_data):
        # Формируем словарь из полученной строки от сервера
        try:
            data = r_data.strip().split('\n')[1:]
            data_dict = {}
            for item in data:
                key, value, timestamp = item.split()
                if key in data_dict:
                    data_dict[key].append((int(timestamp), float(value)))
                    data_dict[key].sort(key=lambda x: x[0])
                else:
                    data_dict[key] = [(int(timestamp), float(value))]

            return data_dict
        except (ValueError, TypeError):
            raise ClientError

    def close(self):
        self.client_socket.close()


client = Client("127.0.0.1", 8001, timeout=15)
client.put("palm.cpu", 0.5, timestamp=1150864247)
client.put("palm.cpu", 2.0, timestamp=1150864248)
client.put("palm.cpu", 0.5, timestamp=1150864248)
client.put("eardrum.cpu", 3, timestamp=1150864250)
client.put("eardrum.cpu", 4, timestamp=1150864251)
client.put("eardrum.memory", 4200000)
print(client.get("*"), '\n')
print(client.get("palm.cpu"), '\n')
print(client.get('sdfkjhsdf'), 'It was wrong key',  '\n')
# client.put('jhjhhj', 'hgggh', 'jhhj')