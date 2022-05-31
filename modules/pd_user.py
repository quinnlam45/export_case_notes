from django.db import Error, connection
import bcrypt

def return_pwd_hash(pwd, pwd_salt):
    byte_pwd = pwd.encode('utf-8')
    hash = bcrypt.hashpw(byte_pwd, pwd_salt)

    return hash

def lookup_userID(username):
    cursor = connection.cursor()
    cursor.execute('SELECT TOP 1 UserID FROM tblQLPDUser WHERE Username=%s', [username])
    row = cursor.fetchone()
    if row:
        user_check_result = row[0]
        return user_check_result
    else:
        return None

def add_pd_user(username, pwd):
    # check if user exists
    try:
        exists_result = lookup_userID(username)
        if exists_result == None:
            pwd_salt = bcrypt.gensalt()
            pwd_hash = return_pwd_hash(pwd, pwd_salt)
            pwd_salt_str = pwd_salt.decode('utf-8')

            cursor = connection.cursor()
            params = (username, pwd_hash, pwd_salt_str)
            cursor.execute('EXEC spQLAddPDUser @Username=%s, @Pwd=%s, @PwdSalt=%s', params)

            return 'User added successfully'
        else:
            return 'User exists'
    except Error as err:
        print(err)
        return f'Cannot create {username} login'
    finally:
        connection.close()

def verify_pd_user(username, pwd):
    try:
        user_check_result = lookup_userID(username)

        if user_check_result == None:
            return 'User does not exist'
        else:
            cursor = connection.cursor()
            cursor.execute('SELECT Pwd, PwdSalt UserID WHERE UserID=%s', user_check_result)
            user_info = namedtuplefetchall(cursor)
            pwd_salt = user_info[0].PwdSalt
            pwd_hash = return_pwd_hash(pwd, pwd_salt)

            return 'Login successful'
    
    except Error as err:
        print(err)
        return f'Cannot create {username} login'
    finally:
        connection.close()