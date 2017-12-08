import psycopg2


def checkLoginInfo(uname,upass):
#Checks if USN already exists
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='XADMIN')
    cursor=cn.cursor()
    checkIT="SELECT TRACEBACK FROM REGISTER WHERE USRNAM = %(id)s"
    checkDATA={ 'id':uname.lower() }
    cursor.execute(checkIT,checkDATA)
    acknowledgeADMIN = cursor.fetchone()
    try: #check for details
        if upass==acknowledgeADMIN[0]:
            return 1
        else:
            return 0
    except:
        return 0


def fetchAdminName(user):
    #gets admin name
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='XADMIN')
    cursor=cn.cursor()
    getTrace = "SELECT TRACE FROM REGISTER WHERE USRNAM = %(username)s "
    checkDATA={ 'username': user.lower() }
    cursor.execute(getTrace,checkDATA)
    trace = cursor.fetchone()[0]
    m = "SELECT NAME FROM ADMIN_DET WHERE TRACE = %(tr)s"
    n = { 'tr': trace }
    cursor.execute(m,n)
    name = cursor.fetchone()[0]
    return name






