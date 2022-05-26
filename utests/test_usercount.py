import unittest
from unittest.mock import MagicMock, patch, Mock
from main.rest import *

class MyTestCase(unittest.TestCase):

    ## This is not working, we need to create app to test this
    ## raise RuntimeError(_app_ctx_err_msg)
    ##RuntimeError: Working outside of application context.
    @unittest.skip("skipping for now")
    @patch('main.models.User')
    def tsomething(self, inst):
        inst.query.filter_by(authenticated=1).count.return_value = 99
        inst.query.count.return_value = 100
        #print (check_total_employee())
        #self.assertEqual(True, False)

    @unittest.skip("skipping for now")
    @patch('main.rest.check_total_employee')
    def test_something2(self, mock_emp):
        mock_emp.all_count = 99
        mock_emp.auth_count = 991

        print(check_total_employee())
        # self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
