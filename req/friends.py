import requests
import pprint
import operator
import datetime
import sys
ACCESS_TOKEN = 'b9281814b9281814b928181458b9454676bb928b9281814e48916ee51f863048d5d9fe2'
YEAR = datetime.date.today().year


class UserVK:

    """ This class contain user's description."""

    ACCESS_TOKEN = 'b9281814b9281814b928181458b9454676bb928b9281814e48916ee51f863048d5d9fe2'

    def __init__(self, uid):
        self.uid = uid
        self.user_id = self._user_id_getter()
        self.friend_list = self._friend_list_getter()

    def _user_id_getter(self):
        user_id = requests.get(
            'https://api.vk.com/method/users.get?v=5.71&access_token={}&user_ids={}'.format(ACCESS_TOKEN, self.uid)).json()
        user_id = user_id['response'][0]['id']
        return user_id

    def _friend_list_getter(self):
        friends_list = requests.get(
            'https://api.vk.com/method/friends.get?v=5.71&access_token={}&user_id={}&fields=bdate'.format(ACCESS_TOKEN, self.user_id)).json()
        if 'response' not in friends_list:
            print('Error: permission denied')
            return 'permission denied'
        clear_friend_list = friends_list['response']['items']
        return clear_friend_list


class Counter:
    """ Class for counting of some users attributes."""

    def counter(self, obj):
        """This method make a dictionary that contains age and number of users.
            return dict = {age : number}
        """
        my_counting = dict()
        for friend in obj.friend_list:
            if 'bdate' in friend and len(friend['bdate']) > 5:
                old = YEAR - int(friend['bdate'][-4:])
                if old in my_counting:
                    my_counting[old] += 1
                else:
                    my_counting[old] = 1
        return my_counting


class Sorter:
    """ Class for sorting of users attributes"""

    def sort_friend_list(self, ditcionary):
        """ This method will sort User's friendlist descending by age in descending order."""
        my_counting = ditcionary.items()
        my_counting = sorted(
            my_counting, key=operator.itemgetter(1), reverse=True)
        return my_counting


if __name__ == '__main__':
    object1 = sys.argv[1]
    user = UserVK(object1)
    counter = Counter()
    sorter = Sorter()
    counter.counter(user)
    res = sorter.sort_friend_list(counter.counter(user))
    if res is not None:
        print(f'{object1}')
        for i in res:
            print(f'Возраст:{i[0]} - {i[1]} друзей')
