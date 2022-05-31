import unittest
import io
from tempfile import NamedTemporaryFile
from openpyxl import Workbook
from pd_user import *

class TestPdUser(unittest.TestCase):

    def test_create_pwd_hash(self):
        expected_hash = b'$2b$12$AGqycWsrTYXQg0s.C2riUe5V8lqWZMGyryOUx9Sx3Xh2cPh/ZMsZu'
        pwd = 'password'
        pwd_salt = b'$2b$12$AGqycWsrTYXQg0s.C2riUe'
        hash = create_pwd_hash(pwd, pwd_salt)
        self.assertEqual(expected_hash, hash)
