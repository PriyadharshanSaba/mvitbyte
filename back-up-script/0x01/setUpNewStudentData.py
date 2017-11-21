#Fetches Student details to insert into DataBase
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import mysql.connector
import re
import mechanize
import random
import smtplib


def fetchAndInsert(usn_id):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("http://45.112.202.150:9084/SISloginform")
    br.select_form(nr=0)
    login_usn = usn_id
    br.form['txtUserName']=login_usn
    br.form['txtPassword']=login_usn
    sub = br.submit()
    op=br.open("http://45.112.202.150:9084/SISWelcome.jsp")
    soup = BeautifulSoup(op.read(),"lxml")
    i=1
    num1= "Null"
    num2= "Null"
    num3= "Null"
    for font in soup.findAll('font',{'size':3}):
        if i==2:
            student_name = font.text
            #student_name=student_name.upper()
        elif i==24:
            num = str(font.text)
            #num = num.split()
            try:
                num = num.split(",")
                num1=num[0].split(" ")
                for c in range(0,len(num1)):
                    if len(num1[c])==0 or num1[c]=='\r\n':
                        pass
                    else:
                        num1=num1[c]
                        break
            except:
                num1="Null"
            
            try:
                num2=num[1]
            except:
                num2="Null"
            
            try:
                num3=num[2]
            except:
                num3="Null"
                    
        elif i==26:
            email=str(font.text)
            email=email.split(" ")
            for z in range(0,len(email)):
                if len(email[z])==0 or email[z]=='\r\n':
                    pass
                else:
                    mail_id=email[z]
                    break
        i=i+1
                        
    op_attends=br.open("http://45.112.202.150:9084/acdStdAttViewHndlr?txtAction=ListPage&txtSubAction=ViewList")
    soup = BeautifulSoup(op_attends.read(),"lxml")
    #subject_namelist = [None]*6
    subject_codelist = [None]*6
    i=0
    j=0
    for td in soup.findAll('td',{'width':'53%'}):
        if j>0:
            temp=td.text.split("   ")
            temp=temp[0].split(" - ")
            #subject_namelist[i]=temp[1]
            subject_codelist[i]=temp[0]
            i=i+1
        j=j+1

    subject_chlist = [None]*10
    i=0
    j=0
    for td in soup.findAll('td',{'width':'9%'}):
        if j>2 and j%2==0:
            subject_chlist[i]=td.text
            i=i+1
        j=j+1

    subject_calist = [None]*10
    i=0
    j=0
    for td in soup.findAll('td',{'width':'8%'}):
        if j>1:
            subject_calist[i]=td.text
            i=i+1
        j=j+1

    subject_attends = [None]*10
    i=0
    j=0
    for td in soup.findAll('td',{'width':'18%'}):
        if j>0:
            subject_attends[i]=td.text
            i=i+1
        j=j+1
    #return name,num,subject_codelist,subject_attends

    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    insert_userDAT="INSERT INTO STUD_DET VALUES (%(uid)s,%(uname)s,%(uphone1)s,%(uphone2)s,%(uphone3)s,%(umail)s)"
    usr_DATA={'uid':usn_id,'uname':student_name,'uphone1':num1,'uphone2':num2,'uphone3':num3,'umail':mail_id}
    cursor.execute(insert_userDAT,usr_DATA)
    cn.commit()
    setmarks="INSERT INTO ATTENDS VALUES (%(uusn)s,%(s1)s,%(s1ca)s,%(s1ch)s,%(s2)s,%(s2ca)s,%(s2ch)s,%(s3)s,%(s3ca)s,%(s3ch)s,%(s4)s,%(s4ca)s,%(s4ch)s,%(s5)s,%(s5ca)s,%(s5ch)s,%(s6)s,%(s6ca)s,%(s6ch)s);"
    marDATA={'uusn':usn_id,'s1':subject_codelist[0],'s1ca':subject_calist[0],'s1ch':subject_chlist[0],'s2':subject_codelist[1],'s2ca':subject_calist[1],'s2ch':subject_chlist[1],'s3':subject_codelist[2],'s3ca':subject_calist[2],'s3ch':subject_chlist[2],'s4':subject_codelist[3],'s4ca':subject_calist[3],'s4ch':subject_chlist[3],'s5':subject_codelist[4],'s5ca':subject_calist[4],'s5ch':subject_chlist[4],'s6':subject_codelist[5],'s6ca':subject_calist[5],'s6ch':subject_chlist[5]}
    cursor.execute(setmarks,marDATA)
    cn.commit()
    return student_name,mail_id,num1,num2,num3


def insertIntoRegister(usn,password):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    insert_userDAT="INSERT INTO REGISTER VALUES (%(uid)s,%(uname)s);"
    usr_DATA={'uid':usn,'uname':password}
    cursor.execute(insert_userDAT,usr_DATA)
    cn.commit()
    return

def deletePrior(usn):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    insert_userDAT="DELETE FROM REGISTER WHERE USR_ID = %(u)s"
    usr_DATA={'u':usn.upper()}
    cursor.execute(insert_userDAT,usr_DATA)
    cn.commit()
    return


def verifyCode(usn):    #from DB
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT GKEY FROM GENKY WHERE USN = %(uid)s"
    checkDATA={'uid':usn }
    cursor.execute(checkIT,checkDATA)
    otp = cursor.fetchone()
    return otp[0]

def verifiHit(usn):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="UPDATE GENKY SET VERF = (%(ver)s) WHERE USN=%(uid)s"
    checkDATA={'ver':'X','uid':usn}
    cursor.execute(checkIT,checkDATA)
    cn.commit()
    return


def generateMail(usn):
    xo = random.randint(1000,9999)
    ran = str(xo)
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="INSERT INTO GENKY (USN,GKEY,VERF) VALUES (%(uid)s,%(key)s,%(ver)s)"
    checkDATA={'uid':usn,'key':ran,'ver':'N'}
    cursor.execute(checkIT,checkDATA)
    cn.commit()
    return ran

def verifiHit2(usn):
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="DELETE FROM GENKY WHERE USN = %(uid)s "
    checkDATA={'uid':usn.upper() }
    cursor.execute(checkIT,checkDATA)
    cn.commit()
    return
