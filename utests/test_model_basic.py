import unittest
from main.models import User
from datetime import datetime, timedelta, timezone

class MyTestCase(unittest.TestCase):

    email = "mymail@mm.cc"
    passwd = "password123"

    @classmethod
    def setUpClass(cls):
        cls.usr = User(cls.email,cls.passwd)


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        testid = self.id().split('.')[-1]
        print("running mytests: ", testid)
        testname = self.shortDescription()
        print("running mytests: ", testname)
        if testid == "test_role":
            self.usr = User('kss@awesome.com', 'integration-tests', "Admin")

    def test_get_email(self):
        print (self.usr.get_email())

    #@unittest.skip("skipping for now")
    def test_registeredtime(self):
        #print (self.usr.registered_on)
        #print(datetime.now())
        #print(self.usr.to_json())

        self.assertAlmostEqual(self.usr.registered_on, datetime.now(),
            delta=timedelta(seconds=40))

    #@unittest.skip("skipping for now")
    def test_hashedpass(self):
        '''hashed pass test'''
        print(self.usr.hashed_password)
        print (self.usr.is_correct_password("pasword"))
        self.assertTrue(self.usr.is_correct_password("password123"))

   # @unittest.skip("skipping for now")
    def test_role(self):
        print (self.usr.role)
        self.assertEqual('Admin', self.usr.role)
        #pass

    #@unittest.skip("skipping for now")
    def test_json_resp(self):
        print (len(self.usr.to_json()))
        print (self.usr.to_json()['email'])
        self.assertEqual(self.email, self.usr.email)

if __name__ == '__main__':
    unittest.main()
