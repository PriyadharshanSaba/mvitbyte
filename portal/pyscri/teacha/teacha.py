import mysql.connector
import os
import os.path

def DBConnection():
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    return cn,cursor

def filePathIntoDB(nam,path):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='TEACHA')
    cursor=cn.cursor()
    checkIT="INSERT INTO FILX VALUES(%(n)s,%(p)s)"
    checkDATA={'n':nam,'p':path}
    cursor.execute(checkIT,checkDATA)
    cn.commit()
    return

def checkIfExists(nam):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='TEACHA')
    cursor=cn.cursor()
    checkIT="SELECT * FROM FILX WHERE FILNAME = %(n)s"
    checkDATA={'n':nam}
    cursor.execute(checkIT,checkDATA)
    log = cursor.fetchone()
    if log != None:
        flag = 1
    else:
        flag = 0
    return flag


def fetchFilxPath():
    cn =mysql.connector.connect(user='root', password='Rocky@2009', database='TEACHA')
    cursor=cn.cursor()
    checkIT="SELECT FILNAME,PATH FROM FILX"
    cursor.execute(checkIT)
    return cursor.fetchall()


def deleteFiles(file_names):
    root_pth = os.path.dirname(os.path.realpath(__file__))
    root_pth = root_pth.split("/portal/")[0]
    cn =mysql.connector.connect(user='root', password='Rocky@2009', database='TEACHA')
    cursor=cn.cursor()
    checkIT="SELECT PATH FROM FILX WHERE FILNAME= %(n)s"
    checkDB = "DELETE FROM FILX WHERE FILNAME= %(n)s"
    for fn in file_names:
        checkDATA={'n':fn}
        cursor.execute(checkIT,checkDATA)
        fg = cursor.fetchone()
        fpath = str(root_pth) + str(fg[0])
        cursor.execute(checkDB,checkDATA)
        cn.commit()
        os.remove(str(fpath))
    return "okay"


def namCap(name):
    spli = name.split(" ")
    name=""
    for i in spli:
        name+= i[0].upper()+i[1:]+" "
    return name

def checkExisting(name):
    name = namCap(name)
    db =DBConnection()
    que = "SELECT * FROM TEACHA.REGISTER WHERE USERNAME=%(n)s"
    checkDATA={'n':name}
    db[1].execute(que,checkDATA)
    x = db[1].fetchone()
    if x==None:
        return 0
    else:
        return 1






