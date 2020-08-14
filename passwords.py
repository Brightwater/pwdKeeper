import psycopg2
from cryptography.fernet import Fernet
import time
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
from hashlib import scrypt
from base64 import urlsafe_b64encode

loggedIn = False
user = ""
salt = b'cVC\xc3w\x8f\xeb\xbf\xd2g\x9b\xa2\x86;;b'
salt2 = b"\xbb\x06'=kVd\xe0\xbe\xa7\x8f\x83\x87\xc3%\x84"
try:
    connection = psycopg2.connect(user = "py", password= "", host = "127.0.0.1", port = "5432", database = "pydb")

    cursor = connection.cursor()

    #print(connection.get_dsn_parameters(), "\n")

    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    #print("You are connected to - ", record, "\n")

    cursor.execute("SELECT * FROM pwd;")
    record = cursor.fetchone()
    #print(record)
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to Psql: ", error)
    exit()

# login with the users credentials
def login(uName, unencryptedPassword):
    # Todo add encryption check
    try:
        global loggedIn
        global user

        encryptedPwd = encryptMasterPassword(unencryptedPassword)
        pwd = encryptedPwd.decode()
        #print("PASSWORD: ", pwd)
        sql = """SELECT Login, pwd FROM pwd WHERE Login = %s AND pwd = %s"""
        #cursor.execute(f"SELECT Login, pwd FROM pwd WHERE Login = '{uName}' AND pwd = '{pwd}'")

        cursor.execute(sql, (uName, pwd))
        name, p = cursor.fetchone()
        #print(f"Logging in as: {name}")
        p
        loggedIn = True
        user = name

        return 1
    except (Exception, psycopg2.Error) as error:
        #print("Could not login new user?", error)
        return -1

def addService(username, masterPassword, serviceName, serviceUsername, servicePassword):
    #sql1 = """SELECT cardinality('servies')
    #          FROM pwd
    #          WHERE login = %s"""
    #numServ = cursor.execute(sql1, (username))
    #print(numServ)
    try:
        encryptedPwd = servicePwdEncrypt(servicePassword, masterPassword)
        ep = encryptedPwd.decode()
        print("adding", username, masterPassword, serviceName, serviceUsername, ep)
        sql1 = """UPDATE pwd
            SET services = array_append(services, %s)
            WHERE login = %s"""
        sql2 = """UPDATE pwd
            SET usernames = array_append(usernames, %s)
            WHERE login = %s"""
        sql3 = """UPDATE pwd
            SET passwords = array_append(passwords, %s)
            WHERE login = %s"""      
        cursor.execute(sql1, (serviceName, username,))
        cursor.execute(sql2, (serviceUsername, username,))
        cursor.execute(sql3, (ep, username,))
        connection.commit()
        print("SHould have been a success")
        return 1
    except:
        return -1

def listAllServices(username):
    sql = """SELECT services
             FROM pwd
             WHERE login = %s"""
    cursor.execute(sql, (username,))
    services = cursor.fetchone()

    return services

def getServiceCredentials(username, serviceName, masterPassword):
    sql = """SELECT usernames, services, passwords
             FROM pwd
             WHERE login = %s"""

    cursor.execute(sql, (username,))
    res = cursor.fetchall()[0]
    
    i = 0
    found = False
    for s in res[1]:
        if serviceName in s:
            found = True
            break
        i+=1    
    
    if not found:
        return -1, serviceName

    servicePassword = res[2][i].encode()

    decryptedPwd = pwdDecrypt(servicePassword, masterPassword)
    if decryptedPwd is None:
        return 0, None

    string = f"service: {res[1][i]}\nusername: {res[0][i]}\npassword: {decryptedPwd}"
    string2 = f"<b>{res[1][i]}</b><p>Username: {res[0][i]}<br>Password: {decryptedPwd}</p>"
    return string, string2

def newUser(username, unencryptedPassword):
    encryptedPwd = encryptMasterPassword(unencryptedPassword).decode()

    sql = """INSERT INTO pwd(login, pwd)
             VALUES(%s, %s);"""

    try:
        cursor.execute(sql, (username, encryptedPwd,))
        connection.commit()
        return f"Created user: {username}"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return -1



def validateLogin():
    if loggedIn:
        print(f"Currently logged in as: {user}")
        return True
    else:
        print("Not logged in")
        return False
        
def encryptMasterPassword(password):
    pe = password.encode()

    # create PBKDF2HMAC key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt2,
        iterations=100000,
        backend=default_backend()
    )
    
    # encode p using key
    key = base64.urlsafe_b64encode(kdf.derive(pe))

    return(key)

# encrypt given password with seed main password
#   f = {"pwd to encrypt", "key(main pwd)"}
def servicePwdEncrypt(p, k):
    encryptedPwd = ""

    pe = k.encode()

    # create PBKDF2HMAC key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    # encode p using key
    key = base64.urlsafe_b64encode(kdf.derive(pe))
    f = Fernet(key)
    token = f.encrypt(p.encode())

    encryptedPwd = token
    
    return(encryptedPwd)
    

def pwdDecrypt(encryptedPwd, k):
    try:
        pe = k.encode()

        # create PBKDF2HMAC key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        # encode p using key
        key = base64.urlsafe_b64encode(kdf.derive(pe))
        f = Fernet(key)
        
        
        decryptedPwd = f.decrypt(encryptedPwd).decode()

        return decryptedPwd
    except Exception as error:
        print(error)
        pass

def disconnect():
    if(connection):
        cursor.close()
        connection.close()
        print("Psql connection is closed")
    else:
        print("?")
