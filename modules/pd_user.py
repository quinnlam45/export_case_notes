from datetime import datetime, timedelta
from django.db import Error, connection
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import jwt
import bcrypt

def return_pwd_hash(pwd, pwd_salt):
    byte_pwd = pwd.encode('utf-8')
    hash = bcrypt.hashpw(byte_pwd, pwd_salt)
    hash_str = hash.decode('utf-8')

    return hash_str

def lookup_userID(username):
    with connection.cursor() as cursor:
        cursor.execute('SELECT TOP 1 UserID FROM tblQLPDUser WHERE Username=%s', [username])
        row = cursor.fetchone()
        if row:
            user_check_result = row[0]
            return user_check_result
        else:
            return None

def retrieve_salt(user_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT PwdSalt FROM tblQLPDUser WHERE UserID=%s', [user_id])
        user_info = cursor.fetchone()
        pwd_salt_str = user_info[0]
        pwd_salt_byte = pwd_salt_str.encode('utf-8')

        return pwd_salt_byte

def create_auth_token(username, user_id, expiration=None, test_key=None):
    token_expiration_date = datetime.utcnow() + timedelta(minutes=5)
    payload_data = {
        'sub': user_id,
        'name': username,
        'exp': expiration or token_expiration_date,
        }

    key = test_key or settings.SECRET_KEY

    try:
        auth_token = jwt.encode(
            payload_data,
            key,
            algorithm='HS256'
            )
        print(auth_token)

        return auth_token

    except Error as err:
        print(err)

def add_pd_user(username, pwd):
    try:
        # check if user exists
        exists_result = lookup_userID(username)

        if exists_result == None:
            pwd_salt = bcrypt.gensalt()
            pwd_hash_str = return_pwd_hash(pwd, pwd_salt)
            pwd_salt_str = pwd_salt.decode('utf-8')

            with connection.cursor() as cursor:
                params = (username, pwd_hash_str, pwd_salt_str)
                cursor.execute('EXEC spQLPDUserAdd @username=%s, @pwdHashStr=%s, @pwdSalt=%s', params)

                return 'User added successfully'
        else:
            return 'User exists'
    except Error as err:
        print(err)
        return f'Cannot create {username} login'

def verify_pd_user(username, pwd):
    try:
        user_id = lookup_userID(username)

        if user_id == None:
            print('User not found')
            return False
        else:
            pwd_salt_byte = retrieve_salt(user_id)
            pwd_hash_str = return_pwd_hash(pwd, pwd_salt_byte)

            with connection.cursor() as cursor:
                cursor.execute('exec spQLPDUserValidate %s, %s', (user_id, pwd_hash_str))
                # returns user id if successful
                returned_user_id = cursor.fetchone()

                if returned_user_id:
                    print('User found')
                    return returned_user_id[0]
                else:
                    print(f'Could not validate user: {username}')
                    return False
    
    except Error as err:
        print(err)
        return False

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        verify_user_result = verify_pd_user(username, password)

        if verify_user_result:
            try:
                user = User.objects.using('users').get(username=username)
                print(f'retrieved user: {user}')
            except User.DoesNotExist:
                user = User(username=username)
                user.save(using='users')
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.using('users').get(pk=user_id)
        except User.DoesNotExist:
            return None