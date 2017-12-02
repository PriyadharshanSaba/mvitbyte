from __future__ import unicode_literals
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import mysql.connector
from django.template import RequestContext
import re
import mechanize
from pyscri import setUpNewStudentData,check_login_details,putmarksintodb,putMarksCustomSem
from pyscri import studoinfo,verificaMail,detFromDB,addi
from pyscri.teacha.FILx import fileDATA
import csv
import numpy


def index(request):
    return render(request,'portal/headtest.html')

def login_redirection_stu(request):
    x_id = request.POST['usn']
    x_id=x_id.upper()
    request.session['cur_usn'] = x_id
    checkLen = check_login_details.checkForID(x_id)
    if checkLen == 1:
        x_pass=request.POST['psw']
        cn =mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
        cursor=cn.cursor()
        checkIT="SELECT USR_ID, USR_PSW FROM REGISTER WHERE USR_ID= %(uid)s"
        checkDATA={'uid':x_id.upper()}
        cursor.execute(checkIT,checkDATA)
        acknowledgeUSER = cursor.fetchall()
        try: #check for non registered users
            if x_pass==acknowledgeUSER[0][1]:
                verf_usr=check_login_details.verifica(x_id)
                if verf_usr == 'Y':
                    return render(request,'portal/login_redirection_stu.html',{'name':[x_id]})
                else:
                    checkIT="SELECT STUD_NAME FROM STUD_DET WHERE STUD_USN= %(susn)s"
                    checkDATA={'susn':x_id.upper()}
                    cursor.execute(checkIT,checkDATA)
                    sFullName=cursor.fetchone()
                    checkIT="SELECT REGD_MAIL FROM GENKY WHERE USN= %(sn)s"
                    checkDATA={'sn':x_id.upper()}
                    cursor.execute(checkIT,checkDATA)
                    regdMail = cursor.fetchone()
                    return render(request,'portal/new_reg_verfiy.html',{'datas':[sFullName[0],regdMail[0]]}) #regdMail[0]

            else:
                return render(request,'portal/headtest_incorrect.html')
        except:
            return render(request,'portal/headtest_incorrect.html',{'alert':["Incorrect USN or Password"]})
    else:
        return render(request,'portal/headtest_incorrect.html',{'alert':["This ID is not register"]})



#red.html
def red(request):
    current_usn = request.session['cur_usn']
    name=detFromDB.getName(current_usn)
    fetched = fileDATA.fetchFilxPath()
    return render(request,'portal/red.html',{'datas':[name,len(fetched)]})


def getAttendance(request):
    uusn = request.session['cur_usn']
    x= studoinfo.setMarks(uusn)
    co = [None]*6
    for i in range(0,6):
        co[i] = x[2][i]
    xnam=studoinfo.subcodeToSubname(co)
    perAt=map(float,x[3])
    mes=addi.generateMessage_attend(perAt,xnam)
    return render(request,'portal/attend.html',{'datas':[x,xnam,mes]})   #x=( , ,[],[])


def attendanceFromDBMS(request):
    usn = request.session['cur_usn']
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT * FROM ATTENDS WHERE USN_ID = %(uid)s"
    checkDATA={'uid':usn}
    cursor.execute(checkIT,checkDATA)
    fet = cursor.fetchone()
    ch = [0 for chi in range(0,6)]
    ca = [0 for chi in range(0,6)]
    cod = [0 for chi in range(0,6)]
    j=0
    for i in range (1,18,3):
        if fet[i+1] == None or fet[i+2] == None or fet[i] == None:
            cod[j] = 0
            ca[j] = 0
            ch[j] = 0
        else:
            cod[j] = fet[i]
            ca[j] = fet[i+1]
            ch[j] = fet[i+2]
        j = j+1
    cat=map(float,ca)
    cheld=map(float,ch)
    perAt=(numpy.round((numpy.divide(cat,cheld)),4))*100
    xnam=studoinfo.subcodeToSubname(cod)
    return render(request,'portal/attend_preRefresh.html',{'datas':[fet,ca,ch,cod,xnam,perAt]})   #x=( , ,[],[])


#testmod.html   |   newRegMod
def registerNewStudent(request):
    new_usrID = request.POST['newusn']
    new_usrID=new_usrID.upper()
    request.session['new_user_ID']=new_usrID
    checkLen = check_login_details.checkForID(new_usrID)
    if checkLen == 1:
        check = check_login_details.checkIfExists(new_usrID)
        if check == 0:
            new_usrPass =request.POST['newpasw']
            request.session['newuserspass']=new_usrPass
            return render(request,'portal/loadingRedirecting.html')
        else:
            return render(request,'portal/headtest_exists.html')
    else:
        return render(request,'portal/headtest_incorrect.html')


def headtestExists(request):
    #User already exists
    return render(request,'portal/headtest_exists.html')


def putmar(request):
    uusn = request.session['cur_usn']
    marks = putmarksintodb.getmar(uusn)
    subject_names= putmarksintodb.getSubNam(marks)
    cod = [None]*8
    intern = [None]*8
    extern = [None]*8
    finmar = [None]*8
    j = 0
    for i in range(1,24,3):
        cod[j]=marks[i]
        intern[j]=marks[i+1]
        extern[j]=marks[i+2]
        j=j+1
    finmar=numpy.add(intern,extern)
    sortedArr = numpy.sort(finmar)
    if sortedArr[0] != 0:
        xarr = [None]*(len(sortedArr)+1)
        xarr[0] = 0
        for i in range (1,(len(sortedArr)+1)):
            xarr[i] = sortedArr[i-1]
    else:
        xarr=sortedArr
    rangeMarks0x0 = detFromDB.rangeMarks(uusn[5:7],uusn)
    rangeMarks0x1 = rangeMarks0x0[0]
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkITK="SELECT SUB1M,SUB2M,SUB3M,SUB4M,SUB5M,SUB6M,SUB7M,SUB8M FROM SEM4_2017_CBCS15 WHERE USN = %(uid0)s"
    checkDATAK={'uid0':uusn}
    cursor.execute(checkITK,checkDATAK)
    m1 = cursor.fetchone()
    checkIT2="SELECT SUB1I,SUB2I,SUB3I,SUB4I,SUB5I,SUB6I,SUB7I,SUB8I FROM SEM4_2017_CBCS15 WHERE USN = %(uid1)s"
    checkDATA2={'uid1':uusn}
    cursor.execute(checkIT2,checkDATA2)
    m2 = cursor.fetchone()
    myMarks = list(numpy.add(m1,m2))
    #myMarks = rangeMarks0x0[1]
    graphi = 0
    graph_X_Axis = [None]*8
    #label = [0 for li in range(0,8)]
    for xaxis in range(0,8):
        #label[graphi] = ["." for lj in range(0,len(rangeMarks[graphi]))]
        graph_X_Axis[graphi] = len(rangeMarks0x1)
        graphi = graphi + 1
    return render(request,'portal/putmarks.html',{'datas':[cod,subject_names,finmar.tolist(),intern,extern,xarr,rangeMarks0x1,graph_X_Axis,myMarks]}) #8


def welcomeRedirect(request):
    return render(request,'portal/welcome_page.html')


def welcomeNewRege(request):
    newUSN=request.session['new_user_ID']
    request.session['cur_usn'] = newUSN
    newPASSWORD=request.session['newuserspass']
        #try:
    setUpNewStudentData.insertIntoRegister(newUSN,newPASSWORD)
    x=setUpNewStudentData.fetchAndInsert(newUSN)    #[student_name,mail_id,num1,num2,num3]
    putMarksCustomSem.main_func(newUSN[-3:],newUSN[-3:],"s4")
    oxo=setUpNewStudentData.generateMail(newUSN)
    mai=verificaMail.verfMail(oxo,x[1],x[0])
    temp = str(x[1])
    temp=temp.split("@")
    reg = temp[0]
    regd=reg[0]
    for r in range(1,len(temp[0])):
        if r>=3 and r<((len(temp[0]))-2):
            regd=regd+'*'
        else:
            regd=regd+str(reg[r])
    regd=regd+"@"+temp[1]
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="UPDATE GENKY SET REGD_MAIL = %(rm)s WHERE USN=%(uid)s"
    checkDATA={'rm':regd,'uid':newUSN.upper()}
    cursor.execute(checkIT,checkDATA)
    cn.commit()
    return render(request,'portal/new_reg_verfiy.html',{'datas':[x[0],regd]})
#    except:
#        try:
#            setUpNewStudentData.deletePrior(newUSN)
#            return render(request,'portal/error.html',{'datas':'deletePrior'})
#        except:
#            return render(request,'portal/error.html')


def verifyUser(request):
    return render(request,'portal/verification_page.html')

def verification(request):
    #kgen=request.session['otp_key']
    usn=request.session['cur_usn']
    EntKey = request.POST['otp']
    kgen = setUpNewStudentData.verifyCode(usn)
    if EntKey == kgen:
        setUpNewStudentData.verifiHit2(usn)
        name=detFromDB.getName(usn)
        return render(request,'portal/red.html',{'datas':[name]})
    else:
        return render(request,'portal/error.html',{'datas':kgen})


def notes(request):
    fetched = fileDATA.fetchFilxPath()
    return render(request,'portal/notes.html',{'datas':fetched})

def profile_settings(request):
    return render(request,'portal/profile_settings.html')

def errorStudentAcc(request):
    return render(request,'portal/error.html',{'datas':'errorStudentAcc'})

def signOut(request):
    request.session.flush()
    return render(request,'portal/headtest.html')

def loadingRedirecting(request):
    return render(request,'portal/new_reg_verfiy.html')
