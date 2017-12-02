import csv
import mysql.connector


def putmar(usn):
    marks = [[0 for l in xrange(3)] for m in xrange(9)]
    with open(r'portal/static/datasets/CS_IV_SemMarks/CS_IV_SemMarks.csv','r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0]==usn:
                name = row[1]
                usnid = row[0]
                y = 0
                for i in xrange(2,42,5):
                    sub_code = row[i]
                    sub_name = row[i+1]
                    sub_mar = row[i+3]
                    marks[y][0]=row[i]
                    marks[y][1]=row[i+1]
                    marks[y][2]=row[i+3]
                    y=y+1
        return marks

def getmar(usn):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT * FROM SEMIV WHERE USN = %(u)s"
    checkDATA={ 'u':usn.upper() }
    try:
        cursor.execute(checkIT,checkDATA)
        x=cursor.fetchone()
        cn.commit()
        return x
    except:
        return "None"


def getSubNam(code):
    sub_nam= [None]*8
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    j=0
    for i in xrange (1,24,3):
        checkIT="SELECT SUB_NAME FROM SUB_DET WHERE SUB_CODE = %(sc)s"
        checkDATA={ 'sc':code[i] }
        cursor.execute(checkIT,checkDATA)
        sub_nam[j] =cursor.fetchone()
        j=j+1
    return sub_nam


