import mysql.connector as con
from flask import Flask
from datetime import datetime as dt
import os


def connection():
    db = con.connect(host='localhost', user='root', passwd='janganlupa', database='pms')
    return db

def authenticate(email, passwd):
    con = connection()
    cursor = con.cursor()
    cursor.execute('select email, password from user where (email=%s and password=%s)', (email, passwd))
    cursor.fetchone()
    return  cursor.rowcount == 1


def insertProduct(path, uploader):
    con = connection()
    cursor = con.cursor()
    cur_time = dt.now().strftime('%s')
    sql = "INSERT INTO katalog (path, user_email, upload_date) VALUES (%s, %s, %s)"
    cursor.execute(sql, (path, uploader, cur_time))
    con.commit()
    cursor.close()
    return True

def getProducts(limit, offset, condition=None):
    con = connection()
    cursor = con.cursor(buffered=True, dictionary=True)
    sql = 'select * from katalog '
    if condition:
        sql+=' where {}={}'.format(condition['column'], condition['operand'])
    sql+= ' limit %s offset %s'
    cursor.execute(sql, (limit, offset))
    result = cursor.fetchall()
    cursor.close()
    return result

def delProduct(id, app):
    con = connection()
    filename = getProducts(1,0, {'column':'id', 'operand':id} )[0]['path']
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.getcwd()) + '/' + filename)
    cursor = con.cursor(buffered=True, dictionary=True)
    sql = 'delete from katalog where id = %s'
    cursor.execute(sql, (id, ))
    con.commit()
    result = cursor.rowcount
    cursor.close()
    return result == 1
