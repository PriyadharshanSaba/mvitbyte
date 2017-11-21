import mysql.connector
import numpy as nu
import addi

def getName(usn):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT STUD_NAME FROM STUD_DET WHERE STUD_USN= %(uid)s"
    checkDATA={'uid':usn}
    cursor.execute(checkIT,checkDATA)
    name = cursor.fetchone()
    return name


def rangeMarks(branch,uusn):
    started = 0
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT USN FROM SEM4_2017_CBCS15"
    cursor.execute(checkIT)
    fetchedUSNs = cursor.fetchall()
    j=0
    im=0
    jstart = 0
    for i in fetchedUSNs:
        im = im+1
        if i[0][5:7] == branch:
            if j == 0:
                jstart = im-1
                j = j+1
            started = started + 1
        elif i[0][0][5:7] != branch and started != 0:
            break

    checkIT1="SELECT SUB1M,SUB2M,SUB3M,SUB4M,SUB5M,SUB6M,SUB7M,SUB8M FROM SEM4_2017_CBCS15 WHERE USN = %(uid1)s"
    checkDATA1={'uid1':uusn}
    cursor.execute(checkIT1,checkDATA1)
    myMarks1 = cursor.fetchone()
    checkIT2="SELECT SUB1I,SUB2I,SUB3I,SUB4I,SUB5I,SUB6I,SUB7I,SUB8I FROM SEM4_2017_CBCS15 WHERE USN = %(uid1)s"
    checkDATA2={'uid1':uusn}
    cursor.execute(checkIT2,checkDATA2)
    myMarks2 = cursor.fetchone()
    
#myMarks = [yui/10 for yui in myMarks]
#myMarks = [round(yui,1) for yui in myMarks]
#myMarks = map(int,myMarks)

    xmarks = [[None for x in range(0,8)] for m in range(0,started)]

    for i in range(0,started):
        xmarks[i][0] = 0

    ki = 0
    for k in range (jstart,jstart+started):
        xuid = fetchedUSNs[k][0]
        checkITK="SELECT SUB1M,SUB2M,SUB3M,SUB4M,SUB5M,SUB6M,SUB7M,SUB8M FROM SEM4_2017_CBCS15 WHERE USN = %(uid)s"
        checkDATAK={'uid':xuid}
        cursor.execute(checkITK,checkDATAK)
        fetRes = cursor.fetchone()
        for kj in range(0,8):
            xmarks[ki][kj]=fetRes[kj]
        ki = ki + 1
    xmarks = map(list,zip(*xmarks))
    for row in range(0,8):
        xmarks[row] = addi.reduceRange(xmarks[row])

    return xmarks



















#    for k in range(jstart,jstart+started):
#        xuid = fetchedUSNs[k][0]
#        checkITK="SELECT SUB1M,SUB2M,SUB3M,SUB4M,SUB5M,SUB6M,SUB7M,SUB8M FROM SEM4_2017_CBCS15 WHERE USN = %(uid)s"
#        checkDATAK={'uid':xuid}
#        cursor.execute(checkITK,checkDATAK)
#        fetRes = cursor.fetchone()
#        marks1[l] = fetRes[0]
#        marks2[l] = fetRes[1]
#        marks3[l] = fetRes[2]
#        marks4[l] = fetRes[3]
#        marks5[l] = fetRes[4]
#        marks6[l] = fetRes[5]
#        marks7[l] = fetRes[6]
#        marks8[l] = fetRes[7]
#        l = l+1

#    marks1 = addi.reduceRange(marks1)
#    return marks1,marks2,marks3,marks4,marks5,marks6,marks7,marks8





