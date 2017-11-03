# -*- coding: utf-8 -*-
#from utils.utils import YourClassOrFunction

from __future__ import unicode_literals
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import mysql.connector
from django.template import RequestContext
import re
import mechanize
from pyscri import setUpNewStudentData,check_login_details,putmarksintodb,putMarksCustomSem
from pyscri import studoinfo,verificaMail
import csv


def index(request):
    return render(request,'portal/headtest.html')


def login_redirection_stu(request):
    x_id = request.POST['usn']
    x_id=x_id.upper()
    request.session['cur_usn'] = x_id
    checkLen = check_login_details.checkForID(x_id)
    if checkLen == 1:
        x_pass=request.POST['psw']
        cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
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
    return render(request,'portal/red.html',{'name':[current_usn]})


def getAttendance(request):
    uusn = request.session['cur_usn']
    x= studoinfo.setMarks(uusn)
    return render(request,'portal/attend.html',{'datas':[x]})   #x=( , ,[],[])


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
    return render(request,'portal/putmarks.html',{'datas':[marks,subject_names]})


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
        setUpNewStudentData.verifiHit(usn)
        return render(request,'portal/welcome_page.html')
    else:
        return render(request,'portal/error.html',{'datas':kgen})


def errorStudentAcc(request):
    return render(request,'portal/error.html',{'datas':'errorStudentAcc'})


def signOut(request):
    request.session.flush()
    return render(request,'portal/headtest.html')

def loadingRedirecting(request):
    return render(request,'portal/new_reg_verfiy.html')
