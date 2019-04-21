import mysql.connector as con
from flask import Flask


def connection():
    db = con.connect(host='localhost', user='root', passwd='janganlupa', database='pms')
    return db

def authenticate(email, passwd):
    con = connection()
    cursor = con.cursor()
    cursor.execute('select email, password from user where (email=%s and password=%s)', (email, passwd))
    cursor.fetchone()
    if cursor.rowcount == 1:
        return True
    else:
        return False
