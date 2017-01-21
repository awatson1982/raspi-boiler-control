import psycopg2
from passlib.hash import sha512_crypt
from get_props import prop
import logging


logtype = prop('logtype')
if logtype == 'file':
    logFile = prop('loglocation')
    logging.basicConfig(format='%(asctime)s: %(message)s ',filename=logFile, filemode='a', level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)


def get_password(userid):
    userid = userid.upper()
    logging.debug('get password for %s' % userid)
    conn_string = prop('database')
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    sql =   """
            select password from users where userid = %(userid)s
            """
    cursor.execute(sql, {'userid':userid})
    row = cursor.fetchone()
    if row is not None:
        dbpassword = row[0]
        logging.debug('db password hash %s' % dbpassword)
        return dbpassword
    else:
        logging.debug('No details found for user')
        return None

def check_password(password, userid):
    logging.debug('username/password to check is %s/%s' % (userid, password))
    dbpassword = get_password(userid)
    if dbpassword is not None:
        if sha512_crypt.verify(password, dbpassword):
            logging.debug('password correct')
            return True
        else:
            logging.debug('password incorrect')
            return False
    else:
        return False

def hash_password(password):
    logging.debug('hash password')
    hashed_password = sha512_crypt.encrypt(password)
    logging.debug('hashed password = %s' % hashed_password)
    return hashed_password

