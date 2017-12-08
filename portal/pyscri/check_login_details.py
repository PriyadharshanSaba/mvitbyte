import psycopg2


def checkForID(ID):
#Checks USN ID for validation in the login form
    if len(str(ID)) == 10:
        return 1
    else:
        return 0


def checkIfExists(ID):
#Checks if USN already exists
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT USR_ID FROM REGISTER WHERE USR_ID= %(id)s"
    checkDATA={ 'id':ID }
    cursor.execute(checkIT,checkDATA)
    if cursor.fetchone():
        return 1
    else:
        return 0


def verifica(usn):
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT VERF FROM GENKY WHERE USN= %(id)s"
    checkDATA={ 'id':usn }
    try:
        cursor.execute(checkIT,checkDATA)
        fee=cursor.fetchone()
        return fee[0]
    except:
        return 'Y'



