from datetime import datetime
from django.db import Error, connection
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
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

def record_login_time(username):
    time_now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute('UPDATE tblQLPDUser SET LastLogin=%s WHERE Username=%s', [time_now, username])

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
                cursor.execute('EXEC spQLPDUserValidate %s, %s', (user_id, pwd_hash_str))
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
                user = User.objects.get(username=username)
                print(f'retrieved user: {user}')
            except User.DoesNotExist:
                # add user to django user db
                user = User(username=username)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.using('users').get(pk=user_id)
        except User.DoesNotExist:
            return None

def get_all_users():
    user_dict = {'user_rows':[]}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT UserID, Username, (CASE WHEN UserType = 1 THEN 'Admin' ELSE 'User' END) Usertype, LastLogin FROM tblQLPDUser")
            row = cursor.fetchone()
            while row:
                user_dict['user_rows'].append(row)
                row = cursor.fetchone()
        return user_dict
    except:
        user_dict['user_message'] = 'Error retrieving users'
        return user_dict

def delete_django_user(username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return 'Deleted django user'
    except User.DoesNotExist:
        return 'Django user does not exist'

def delete_user(username):
    user_id = lookup_userID(username)
    if user_id != None:
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM tblQLPDUser WHERE UserID=%s',[user_id])
            result = delete_django_user(username)
            return f'User {username} deleted'
        except:
            return 'Error deleting user'
    else:
        return 'User not found'

def check_user_is_admin(username):
    user_id = lookup_userID(username)
    if user_id != None:
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT UserType FROM tblQLPDUser WHERE UserID=%s',[user_id])
                returned_user_type = cursor.fetchone()

                if returned_user_type[0] == 1:
                    return True
                else:
                    return False
        except:
            print('Admin check error')
            return False
    else:
        print('User not found')
        return False

def update_user_pwd(username, pwd):
    try:
        # check if user exists
        user_id = lookup_userID(username)

        if user_id != None:
            new_pwd_salt = bcrypt.gensalt()
            pwd_hash_str = return_pwd_hash(pwd, new_pwd_salt)
            pwd_salt_str = new_pwd_salt.decode('utf-8')

            with connection.cursor() as cursor:
                params = (pwd_hash_str, pwd_salt_str, user_id)
                cursor.execute('UPDATE tblQLPDUser SET Pwd=%s, PwdSalt=%s WHERE UserID=%s', params)

                return 'User updated successfully'
        else:
            return 'User not found'
    except Error as err:
        print(err)
        return f'Cannot update user {username}'