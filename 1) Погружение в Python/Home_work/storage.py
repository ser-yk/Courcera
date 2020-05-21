"""
Программа хранит ключ-значение в файле формата JSON.
Через командрую страку подаются значения ключа(--key key_1) и значение (--val value_1).
Если передано два значения, то они заносятся в файл. Если только одно, то выводятся значения по ключу.
Если ключ не найдет выводится None.
"""
import os
import tempfile
import argparse
import json

def read_data(path, key, data=None):
    try:  # Пытаюсь прочесть файл
        with open(path, 'r') as file:
            data = json.load(file)
            return data
    except:  # Файл был найден или пустой
        return data

def write_data(path, data, key, val):
    with open(path, 'w') as file:
        if data:  # Обновляем данные для файла
            if key in data:
                data[key].append(val)
            else:
                data.update({key: [val]})
        else:  # Формируем данные для нового файла
            data = {key: [val]}
        # Обновляем файл
        file.write(json.dumps(data, indent=4))

def what_do_i(path, key, val):
    data = read_data(path, key)  # Пытаемся найти файл и ключ в файле
    if val is None:  # Программе передали только ключ, пытаемля найти его значение
        if data and key in data:
            print(*data[key], sep=', ')
        else:
            print(None)
    else:  # Программе передали и ключ и значение, нужно их записать.
        write_data(path, data, key, val)

#  Указываем параметры, которые ждёт программа при запуске из командной строки
parser = argparse.ArgumentParser(description='Input key and value')
parser.add_argument('--key')
parser.add_argument('--val', default=None)
my_namespace = parser.parse_args()

if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    what_do_i(storage_path, my_namespace.key, my_namespace.val)
