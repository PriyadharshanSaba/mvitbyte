import mysql.connector

def connect():
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    return cn,cursor
