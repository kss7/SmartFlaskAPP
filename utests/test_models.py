import unittest
from unittest.mock import MagicMock, patch, Mock
from main.models import *


class MyTestCase(unittest.TestCase):

    #@unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_4_auth_count(self, mock_user):
        mock_user.query.filter_by(authenticated=1).count.return_value = 992
        mock_user.query.count.return_value = 9901
        count = User.get_auth_user_count()
        print((count))
        self.assertEqual(992, count)

    #@unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_3_user_count(self, mock_user):
        #u1 = User("sa@aa.s", "ksks")
        mock_user.query.count.return_value = 232
        print (User.get_all_users_count())
        self.assertEqual(232, User.get_all_users_count())

   # @unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_1_get_all_users(self, mock_u):
        u1 = User("sa@aa.s", "ksks")
        u2 = User("sa3@aa.s", "ksks")
        #EXPECTED = dict()
        EXPECTED = [u1, u2]
        print(EXPECTED)
        mock_u.query.all.return_value = EXPECTED
        data = User.get_all_users()
        print (data)
        self.assertEqual(data, EXPECTED)

    #@unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_user(self, mock_user):
        u1 = User("Sonio@aa.s", "ksks")
        mock_user.query.all.return_value = [u1]
        print(User.get_all_users()[0].get_email())
        #print(User.get_user_by_email('kumar@aa.s')) ## will not work properly as its not returning user object,
        # https://medium.com/python-pandemonium/surrender-python-mocking-i-have-you-now-5805e91cfbf4


    @patch('main.models.User')
    def test_2_get_user_by_email(self, mock_user):
        u1 = User("kumar135@aa.s", "ksks", "Admin")
        mock_user.query.filter_by(User.email=="123").first.return_value = [u1]
        print(User.get_user_by_email('kumar@aa.s')[0].get_email())
        print(User.get_user_by_email('kumar@aa.s')[0].get_role())
        print(User.get_user_by_email('kumar@aa.s')[0])
        print (u1.email)
        print (u1)
        self.assertEqual(u1,User.get_user_by_email('kumar@aa.s')[0] )

    @unittest.skip("skipping as it'll NOT work, try integration tests")
    @patch('main.models.User')
    def test_get_user_by_id(self, mock_user):
        u1 = User("Iduser@aa.s", "ksks")
        mock_user.query.get(id=1).return_value = [u1]
        print(User.get_one_user(id)[0])

if __name__ == '__main__':
    unittest.main()
