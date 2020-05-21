import requests
import time

def calc_age(uid):
    # Получаем id на случай если ввели user_name
    access_token = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
    params_1 = {'user_ids': uid, 'v': 5.103, 'access_token': access_token}
    user_info = requests.get('https://api.vk.com/method/users.get', params=params_1)
    id = user_info.json()["response"][0]['id']
    print('VK id', id)

    # Делаем запром на друзей
    params_2 = {'user_id': id, 'v': 5.103, 'access_token': access_token, 'fields': 'bdate'}
    friends_info = requests.get("https://api.vk.com/method/friends.get", params_2)

    if "error" in friends_info.json():
        return False, friends_info.json()["error"]["error_msg"]

    # Фильтруем и обрабатываем данные
    cnt = dict()
    for friend in friends_info.json()['response']['items']:
        if 'bdate' in friend:
            if len(friend['bdate']) > 5:
                years_old = int(time.strftime('%Y')) - int(friend['bdate'].split('.')[2])
                # if years_old > 90:
                #     print(friend)
                if years_old in cnt:
                    cnt[years_old] += 1
                else:
                    cnt[years_old] = 1

    return True, sorted(cnt.items(), key=lambda v: (v[1], -v[0]), reverse=True)


if __name__ == '__main__':
    status, res = calc_age('chernov2010')
    print(res)

    if status:
        k = 0
        for y, q in res:
            k += y / q

        print('Коэффицент:', k / len(res))

    # natalie.dudko