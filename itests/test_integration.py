import unittest
from main import create_app, db
from main.models import User
from unittest.mock import MagicMock, patch, Mock
from main.rest import *


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._app = create_app('flask_test.cfg')
        cls.testing_client = cls._app.test_client()
        cls._app.app_context().push()
        #with cls._app.app_context():
        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        #with cls._app.app_context():
        db.drop_all()

    def setUp(self):
        testid = self.id().split('.')[-1]
        print("running mytests: ", testid)
        testname = self.shortDescription()
        if testid == "test_401":
            user1 = User(email='ksd@awesome.cas', plaintext_password='integration-tests')
            db.session.add(user1)
            db.session.commit()

    @unittest.skip("skipping for now")
    def test_401(self):
        response = self.testing_client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    @unittest.skip("skipping for now")
    def test_register(self):
        data = {'email':'kind@my.cm', 'password':'kind'}
        response = self.testing_client.post('/register', data=json.dumps(data), headers={"content-type":"application/json"}, follow_redirects=True)
        print (response.data)
        #self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        user1 = User(email='userid@awesome.com', plaintext_password='integration-tests')
        db.session.add(user1)
        db.session.commit()
        print(user1.get_one_user(1))


    @unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_mock(self, mock_u):
        u1 = User("sa@aa.s", "ksks")
        u2 = User("sa3@aa.s", "ksks")
        EXPECTED = dict()
        EXPECTED['d'] = [u1, u2]
        print (EXPECTED['d'])
        mock_u.query.all.return_value = EXPECTED['d']
        response = self.testing_client.get('/allusers')

        print(response.data)
        # self.assertEqual(True, False)

    @unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_count(self, mock_u):
        #d = [2]
        mock_u.query.count.return_value = 100
        response = self.testing_client.get('/allusercount')
        print(response.data)

    @unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_auth_count(self, mock_u):
        d = [2]
        mock_u.query.filter_by(authenticated=1).count.return_value = 99
        response = self.testing_client.get('/authuserscount')
        print(response.data)

    @unittest.skip("skipping for now")
    @patch('main.models.User')
    def test_checkusers(self, mock_u):
        mock_u.query.count.return_value = 100
        mock_u.query.filter_by(authenticated=1).count.return_value = 99
        response = self.testing_client.get('/checkusers')
        print(response.data)


if __name__ == '__main__':
    unittest.main()
