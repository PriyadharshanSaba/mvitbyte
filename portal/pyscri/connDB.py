import psycopg2

def connect():
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    return cn,cursor
