from urllib.parse import urlencode
import requests
import time
from pprint import pprint

AOUTH_URL = 'https://oauth.vk.com/authorize'
APP_ID = 6020082
V = '5.64'
access_token = '6d54a571d3c2c1371a7e2bc5c2e0299ed1788fadd707e0d25c41aa0d5041743135d9d46114f9e426e53cd'
params = dict()

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends',
    'v': V
}

def get_friend_list(user_id='4058867'):
    if user_id:
        params = {
            'user_id': user_id,
            'count': 25
            # 'access_token': access_token
        }
    time.sleep(0.5)
    try:
        response = requests.get('https://api.vk.com/method/friends.get', params)
    except Exception as e:
        # pprint(e)
        pprint(response)

    pprint(response.json()['response'])
    return user_id, response.json()['response']


def main():
    user_id, friends_list = get_friend_list()
    print('?'.join((AOUTH_URL, urlencode(auth_data))))
    # full_friends_dict = dict((get_friend_list(user_id) for user_id in friends_list))
    # pprint(full_friends_dict)


if __name__ == '__main__':
    main()
