import requests
from requests.auth import HTTPBasicAuth

url = r'https://datasend.webpython.graders.eldf.ru/'
r1 = requests.post(url + r'submissions/1/', auth=HTTPBasicAuth('alladin', 'opensesame'))

d = r1.json()
password = d['password']
path = d['path']
login = d['login']
instructions = d['instructions'].encode('utf8').decode()

print(f'{login}\n{password}\n{path}]n{instructions}\n')

r2 = requests.put(url + path, auth=HTTPBasicAuth(login, password))
print(r2.text)
