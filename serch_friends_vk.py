import json
from urllib.parse import urlencode
import requests

AOUTH_URL = 'https://oauth.vk.com/authorize'
APP_ID = 6020082
V = '5.64'
access_token = 'c78734ff3baaa06843486680400c4fb75a1bcfe674ea2729e3e2432148f6348fbfce7d8ea48307ba758a1'
params = dict()

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends',
    'v': V
}


def get_friend_list(user_id='4058867'):
    count = input('Введите ограничение для списка друзей: ')
    user_id = input('Введите id пользователя, списки друзей друзей которого хотите посмотреть: ')

    params = {
        'user_id': user_id,
        'count': count,
        'access_token': access_token
    }
    response = requests.get('https://api.vk.com/method/friends.get', params)
    user_ids_list = response.json()['response']
    return user_id, user_ids_list


def get_friends_list_execute(user_ids_list, count=3):
    req_url = 'https://api.vk.com/method/execute'
    inner_code = ',\n'.join(
        ['"%d": API.friends.get({"user_id": %d, "count": %d})' % (i, i, count) for i in user_ids_list])
    req_code = 'return {%s};' % inner_code
    req_data = {
        'code': req_code,
        'access_token': access_token
    }
    response = requests.get('?'.join((req_url, urlencode(req_data))))
    return response.json()['response']


def spt_lst_by_25_elem(user_ids_list):
    return list(user_ids_list[(i * 25):(i * 25 + 25)] for i in range(len(user_ids_list) // 25 + 1))


def main():
    user_id, user_ids_list = get_friend_list()
    with open('full_list.txt', 'w') as f:
        f.write('%s\n' % user_id)
    lst_of_users_lists = spt_lst_by_25_elem(user_ids_list)

    full_list_of_lists = dict()
    count = int(input('Введите ограничение для списка друзей друзей: '))
    for users_short_list in lst_of_users_lists:
        short_dict = get_friends_list_execute(users_short_list, count)
        full_list_of_lists.update(short_dict)

    with open('full_list.txt', 'a') as f:
        json.dump(full_list_of_lists, f, indent=4)
    print(len(full_list_of_lists))


if __name__ == '__main__':
    main()
