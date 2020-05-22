import requests
import json

with open('55.txt') as f:
  num = f.readline().strip()

  while num:
    r = requests.get(f'http://numbersapi.com/{num}/math?json=true')
    j = json.loads(r.text)

    if j['found']:
      print('Interesting')
    else:
      print('Boring')

    num = f.readline().strip()