import mysql.connector as con
from flask import Flask
from datetime import datetime as dt


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

def insertProduct(path, uploader):
    con = connection()
    cursor = con.cursor()
    cur_time = dt.now().strftime('%s')
    sql = "INSERT INTO katalog (path, user_email, upload_date) VALUES (%s, %s, %s)"
    cursor.execute(sql, (path, uploader, cur_time))
    con.commit()
    return True

def getProducts(limit, offset):
    con = connection()
    cursor = con.cursor(buffered=True, dictionary=True)
    sql = 'select * from katalog limit %s offset %s'
    cursor.execute(sql, (limit, offset))
    result = cursor.fetchall()
    return result
