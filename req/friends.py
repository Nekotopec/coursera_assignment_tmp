import requests
import pprint
import operator
import datetime
import sys
ACCESS_TOKEN = 'b9281814b9281814b928181458b9454676bb928b9281814e48916ee51f863048d5d9fe2'
YEAR = datetime.date.today().year


def calc_age(uid):
    user_id = requests.get(
        'https://api.vk.com/method/users.get?v=5.71&access_token={}&user_ids={}'.format(ACCESS_TOKEN, uid)).json()
    user_id = user_id['response'][0]['id']
    friends_list = requests.get(
        'https://api.vk.com/method/friends.get?v=5.71&access_token={}&user_id={}&fields=bdate'.format(ACCESS_TOKEN, user_id)).json()
    if 'response' not in friends_list:
        print('Error: permission denied')
        return

    real_friends_list = friends_list['response']['items']
    my_counting = dict()
    for friend in real_friends_list:
        if 'bdate' in friend and len(friend['bdate']) > 5:
            old = YEAR - int(friend['bdate'][-4:])
            if old in my_counting:
                my_counting[old] += 1
            else:
                my_counting[old] = 1
    my_counting = my_counting.items()
    my_counting = sorted(my_counting, key=operator.itemgetter(1), reverse=True)
    return my_counting


if __name__ == '__main__':
    object1 = sys.argv[1]
    res = calc_age(object1)
    if res is not None:
        pprint.pprint(res)
        print(f'{object1}')
        for i in res:
            print(f'Возраст:{i[0]} - {i[1]} друзей')
