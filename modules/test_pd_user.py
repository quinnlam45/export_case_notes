import unittest
import io
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta, timezone
import calendar
import time
import jwt
from openpyxl import Workbook
from pd_user import *

class TestPdUser(unittest.TestCase):

    def test_create_pwd_hash(self):
        expected_hash = b'$2b$12$AGqycWsrTYXQg0s.C2riUe5V8lqWZMGyryOUx9Sx3Xh2cPh/ZMsZu'
        pwd = 'password'
        pwd_salt = b'$2b$12$AGqycWsrTYXQg0s.C2riUe'
        hash = create_pwd_hash(pwd, pwd_salt)
        self.assertEqual(expected_hash, hash)
    
    def test_create_auth_token(self):
        test_secret_key = 'secret-key-test'
        expiry_datetime = datetime.now(timezone.utc) + timedelta(minutes=5)
        unix_timestamp = calendar.timegm(expiry_datetime.utctimetuple())
        expected_payload = {
            'sub': 1,
            'name': 'user1',
            'exp': unix_timestamp,
            }
        auth_token = create_auth_token(expected_payload['name'], expected_payload['sub'], expected_payload['exp'], test_key=test_secret_key)
        decoded = jwt.decode(auth_token, test_secret_key, algorithms="HS256")
        print(decoded)
        self.assertEqual(expected_payload, decoded)