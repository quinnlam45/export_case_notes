from django.db import Error, connection
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
            return 'User not found'
        else:
            pwd_salt_byte = retrieve_salt(user_id)
            pwd_hash_str = return_pwd_hash(pwd, pwd_salt_byte)

            with connection.cursor() as cursor:
                cursor.execute('exec spQLPDUserValidate %s, %s', (user_id, pwd_hash_str))
                # returns user id if successful
                row = cursor.fetchone()
                print(row)
                if row:
                    return 'Login successful'
                else:
                    return 'Login unsuccessful'
    
    except Error as err:
        print(err)
        return 'Login unsuccessful'