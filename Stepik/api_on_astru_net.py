import requests
import json

def get_token():
    client_id = '07ebd1b8a990662a188f'
    client_secret = '917f0db42bef167eb8b12984081ccbe1'

    # инициируем запрос на получение токена
    r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                      data={"client_id": client_id, "client_secret": client_secret})

    # разбираем ответ сервера
    j = json.loads(r.text)
    # достаем токен
    token = j["token"]
    return token

def get_info(storege, id, token):
    try:
        # создаем заголовок, содержащий наш токен
        headers = {"X-Xapp-Token": token}
        # инициируем запрос с заголовком
        r = requests.get(f"https://api.artsy.net/api/artists/{id}", headers=headers)
        r.encoding = 'utf-8'
        # разбираем ответ сервера
        j = json.loads(r.text)
        storege[j['sortable_name']] = j['birthday']
    except:
        return

my_store = dict()
with open(r"dataset_24476_4.txt") as f:
    token = get_token()
    while id:
        id = f.readline().strip()
        get_info(my_store, id, token)

for name, year in sorted(my_store.items(), key=lambda x: (x[1], x[0])):
    print(name)