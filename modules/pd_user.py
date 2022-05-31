from django.db import Error, connection
import bcrypt

def return_pwd_hash(pwd, pwd_salt):
    byte_pwd = pwd.encode('utf-8')
    hash = bcrypt.hashpw(byte_pwd, pwd_salt)

    return hash

def add_pd_user(username, pwd):
    # check if user exists
    try:
        pwd_salt = bcrypt.gensalt()
        pwd_hash = return_pwd_hash(pwd, pwd_salt)
        pwd_salt_str = pwd_salt.decode('utf-8')

        cursor = connection.cursor()
        params = (username, pwd_hash, pwd_salt_str)
        sql_exec = """\
        DECLARE @resultMessage NVARCHAR(250);
        EXEC spQLAddPDUser @Username=%s, @Pwd=%s, @PwdSalt=%s, @responseMessage=@resultMessage OUTPUT;
        SELECT @resultMessage AS Output;
        """
        cursor.execute(sql_exec, params)
        rows = cursor.fetchall()
        print(rows)
        sp_output_message = rows[0][0]

        return sp_output_message
    
    except Error as err:
        print(err)
        return f'Cannot create {username} login'
    finally:
        connection.close()

def verify_pd_user(username, pwd):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT TOP 1 UserID', params)
        pwd_salt = bcrypt.gensalt()
        pwd_hash = return_pwd_hash(pwd, pwd_salt)
        pwd_salt_str = pwd_salt.decode('utf-8')

        params = (username, pwd_hash, pwd_salt_str)

        return 'User created successfully'
    
    except Error as err:
        print(err)
        return f'Cannot create {username} login'
    finally:
        connection.close()