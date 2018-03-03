from __future__ import unicode_literals
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import psycopg2
from django.template import RequestContext
import re
import mechanize
from pyscri import setUpNewStudentData,check_login_details,putmarksintodb,putMarksCustomSem
from pyscri import studoinfo,verificaMail,detFromDB,addi,connDB
from pyscri.teacha import teacha
import csv
import numpy as np
import pandas as pd


def index(request):
    return render(request,'admini/pro.html')

def student(request):
    return render(request,'portal/headtest.html')

def login_redirection_stu(request):
    x_id = request.POST['usn']
    x_id=x_id.upper()
    request.session['cur_usn'] = x_id
    #checkLen = check_login_details.checkForID(x_id)
#    if checkLen == 1:
    x_pass=request.POST['psw']
    conn =psycopg2.connect(dbname='d1v03ol0gs21v5',user='mvsjgtxaoxwmgp',password='7b32ce61d22ce32052e233639448ab315708a2c78884b39932dc9ead1b26ef53',host='ec2-54-235-123-153.compute-1.amazonaws.com',port='5432')
    cursor=conn.cursor()
    checkIT="SELECT USR_PSW FROM student_reg WHERE USR_ID= %(uid)s"
    checkDATA={'uid':x_id}
    cursor.execute(checkIT,checkDATA)
    acknowledgeUSER = cursor.fetchall()
    #print x_pass.strip() == (acknowledgeUSER[0][0]).strip()
    #print x_pass.strip()+">>"+acknowledgeUSER[0][0].strip()
    if x_pass.strip()==(acknowledgeUSER[0][0]).strip():
        return render(request,'portal/temp_red.html',{'name':[x_id]})
    else:
        return render(request,'admini/pro.html') #,{'name':[x_id]})
#        try: #check for non registered users
#            if x_pass==acknowledgeUSER[0][1]:
#                verf_usr=check_login_details.verifica(x_id)
#                if verf_usr == 'Y':
#                    return render(request,'portal/login_redirection_stu.html',{'name':[x_id]})
#                else:
#                    checkIT="SELECT STUD_NAME FROM STUD_DET WHERE STUD_USN= %(susn)s"
#                    checkDATA={'susn':x_id.upper()}
#                    cursor.execute(checkIT,checkDATA)
#                    sFullName=cursor.fetchone()
#                    checkIT="SELECT REGD_MAIL FROM GENKY WHERE USN= %(sn)s"
#                    checkDATA={'sn':x_id.upper()}
#                    cursor.execute(checkIT,checkDATA)
#                    regdMail = cursor.fetchone()
#                    return render(request,'portal/new_reg_verfiy.html',{'datas':[sFullName[0],regdMail[0]]}) #regdMail[0]
#
#            else:
#                return render(request,'portal/headtest_incorrect.html')
#        except:
#            return render(request,'portal/headtest_incorrect.html',{'alert':["Incorrect USN or Password"]})
#    else:
#        return render(request,'portal/headtest_incorrect.html',{'alert':["This ID is not register"]})



#red.html
def red(request):
    current_usn = "pd"
    #current_usn = request.session['cur_usn']
    #name=detFromDB.getName(current_usn)
    #fetched = teacha.fetchFilxPath()
    return render(request,'portal/red.html',{'datas':[[current_usn]]})#[name,len(fetched)]})



def capitalize(name):
    sname=''
    for i in name.split(' '):
        print i
        sname=sname+(i[:1].upper()+i[1:].lower())+" "
    return sname


def temp_red(request):
    subject = ['subject']
    mar = ['mark']
    x_id = request.POST['usn']
    x_id=x_id.upper()
    #request.session['cur_usn'] = x_id
    #http://results.vtu.ac.in/vitaviresultcbcs/index.php
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("http://results.vtu.ac.in/vitaviresultcbcs/index.php")
    br.select_form(nr=0)
    br.form['lns']=x_id
    sub = br.submit()
    soup = BeautifulSoup(sub.read(),"lxml")
    flag=0
    for i in soup.findAll('td'):
        if i.text.strip(' ') == "Student Name":
            flag+=1
        elif flag==1:
            student_name = i.text.strip(" : ")
            flag=0
    student_name = capitalize(student_name)

    for div in soup.findAll('div',{'style':'text-align: left;width: 400px;'}):
        subject.append(div.text)

    i=1
    j=1
    k=6
    l=1
    for div in soup.findAll('div',{'class':'divTableCell'}):
        if i==6:
            if j % k ==0:
                mar.append(div.text)
                k=k+1
                l+=1
            else:
                j+=1
        else:
            i+=1

    finalm = [mar[1]]
    subject.remove("subject")
    for i in xrange(4,len(mar),3):
        if i <=24:
            finalm.append(mar[i])
        else:
            break
    grad = ['g']
    gp = [-1]
    for i in finalm:
        gx=getGrade(int(i))
        grad.append(gx[0])
        gp.append(gx[1])

    sum=0
    grad.remove('g')
    gp.remove(-1)
    for i in range(0,len(gp)):
        if i==1 or i==3:
            sum += gp[i]*3.0
        elif i>=6:
            sum+=gp[i]*2.0
        else:
            sum+=gp[i]*4.0
    return render(request,'portal/temp_red.html',{'datas':[[student_name],subject,grad,str(sum/26)[:4],x_id]})


def getGrade(n):
    if n >= 90 :
        return 'S+',10
    elif n>=80 and n<90:
        return 'S',9
    elif n>=70 and n<80:
        return 'A',8
    elif n>=60 and n<70:
        return 'B',7
    elif n>=50 and n<60:
        return 'C',6
    elif n>=45 and n<50:
        return 'D',5
    elif n>=40 and n<45:
        return 'E',4
    else:
        return 'F',0


def semester_wise(request):
    usn = request.POST['usn']
    df4 = pd.read_csv('https://raw.githubusercontent.com/PriyadharshanSaba/Prototyping-StudentsMarksPredictor-MachineLearning/master/ds/gpa4.csv', sep='\t')
    x4=df4.loc[df4['usn'] == usn]
    df5 = pd.read_csv('https://raw.githubusercontent.com/PriyadharshanSaba/Prototyping-StudentsMarksPredictor-MachineLearning/master/ds/gpa5.csv', sep='\t')
    x5=df5.loc[df5['usn'] == usn]
    print x5['gpa']
    return render(request,'portal/semesters.html',{'datas':[x4['gpa'].values,x5['gpa'].values]})


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
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
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
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
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
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="UPDATE GENKY SET REGD_MAIL = %(rm)s WHERE USN=%(uid)s"
    checkDATA={'rm':regd,'uid':newUSN.upper()}
    cursor.execute(checkIT,checkDATA)
    cn.commit()
    return render(request,'portal/new_reg_verfiy.html',{'datas':[x[0],regd]})


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
    fetched = teacha.fetchFilxPath()
    return render(request,'portal/notes.html',{'datas':fetched})

def profile_settings(request):
    return render(request,'portal/profile_settings.html',{'datas':None})

def errorStudentAcc(request):
    return render(request,'portal/error.html',{'datas':'errorStudentAcc'})

def signOut(request):
    request.session.flush()
    return render(request,'portal/headtest.html')

def loadingRedirecting(request):
    return render(request,'portal/new_reg_verfiy.html')

def changePassword(request):
    db=connDB.connect()
    usn=request.session['cur_usn']
    que="SELECT * FROM studentportal.REGISTER WHERE USR_ID=%(uid)s AND USR_PSW=%(np)s"
    dat={'np':request.POST['curPass'],'uid':usn}
    db[1].execute(que,dat)
    #print "data>>>" + str(cur.fetchone())
    if db[1].fetchone()!=None:
        if request.POST['curPass'] == request.POST['newPass']:
            return render(request,'portal/profile_settings.html',{'datas':1})
        else:
            que="UPDATE studentportal.REGISTER SET USR_PSW=%(np)s WHERE USR_ID=%(uid)s"
            dat={'np':request.POST['newPass'],'uid':usn}
            db[1].execute(que,dat)
            db[0].commit()
            return render(request,'portal/profile_settings.html',{'datas':0})
    else:
        return render(request,'portal/profile_settings.html',{'datas':2})

def changeMail(request):
    db=connDB.connect()
    usn=request.session['cur_usn']
    que="SELECT * FROM studentportal.REGISTER WHERE USR_ID=%(uid)s AND USR_PSW=%(np)s"
    dat={'np':request.POST['entPass'],'uid':usn}
    db[1].execute(que,dat)
    #print "data>>>" + str(cur.fetchone())
    if db[1].fetchone()!=None:
        que="UPDATE studentportal.STUD_DET SET MAIL=%(np)s WHERE STUD_USN=%(uid)s"
        dat={'np':request.POST['newMail'],'uid':usn}
        db[1].execute(que,dat)
        db[0].commit()
        return render(request,'portal/profile_settings.html',{'datas':0})
    else:
        return render(request,'portal/profile_settings.html',{'datas':2})

def static_attend_preRefresh(request):
    usn = request.session['cur_usn']
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
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
    mes=addi.generateMessage_attend(perAt,xnam)
    return render(request,'portal/static_attend_preRefresh.html',{'datas':[fet,ca,ch,cod,xnam,perAt,mes]})






########### MOBILE SITES ############

def red_mob(request):
    return render(request,'portal/mobile/headtest_mobile.html',{'datas':1})

def index_mob(request):
    return render(request,'admini/mobile/index_mobile.html',{'datas':1})


