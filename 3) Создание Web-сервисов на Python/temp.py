# import pymysql.cursors
#
# con = pymysql.connect(host='localhost',
#                                   user='root',
#                                   password='qazwsx2320',
#                                   db='cars',
#                                   charset='utf8mb4',
#                                   cursorclass=pymysql.cursors.DictCursor)
#
# with con.cursor() as connection:
#     connection.execute('Show tables')
#     tab = connection.fetchone()
#     print(tab)

import requests

r = requests.get('http://numbersapi.com/31/math?json=true')
print(r.status_code, r.content)






