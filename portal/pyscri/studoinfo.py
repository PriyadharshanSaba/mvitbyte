from __future__ import unicode_literals
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import psycopg2
import re
import mechanize

global num
global name

def setMarks(usn):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("http://45.112.202.150:9084/SISloginform")
    br.select_form(nr=0)
    login_usn = usn
    br.form['txtUserName']=login_usn
    br.form['txtPassword']=login_usn
    sub = br.submit()
    op=br.open("http://45.112.202.150:9084/SISWelcome.jsp")
    soup = BeautifulSoup(op.read(),"lxml")
    i=1
    for font in soup.findAll('font',{'size':3}):
        if i==2:
            name=str(font.text)
        elif i==24:
            num = str(font.text)
            num = num.split()
            num=num[0]
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
    
    subject_chlist = [None]*6
    i=0
    j=0
    for td in soup.findAll('td',{'width':'9%'}):
        if j>2 and j%2==0:
            subject_chlist[i]=td.text
            i=i+1
        j=j+1
    
    subject_calist = [None]*6
    i=0
    j=0
    for td in soup.findAll('td',{'width':'8%'}):
        if j>1:
            subject_calist[i]=td.text
            i=i+1
        j=j+1
    
    subject_attends = [None]*6
    i=0
    j=0
    for td in soup.findAll('td',{'width':'18%'}):
        if j>0:
            subject_attends[i]=td.text
            
            i=i+1
        j=j+1
    for i in range(0,len(subject_codelist)):
        if subject_codelist[i] == None:
            subject_codelist[i] = 0
    for i in range(0,len(subject_attends)):
        if subject_attends[i] == None:
            subject_attends[i] = 0
    #    insertionTODatabase(usn,num,subject_codelist,subject_attends)
    return name,num,subject_codelist,subject_attends



def subcodeToSubname(code):
    nam = [0 for l in xrange(0,6)]
    cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
    cursor=cn.cursor()
    checkIT="SELECT SUB_NAME FROM SUB_DET WHERE SUB_CODE=%(sc)s"
    for i in range (0,6):
        try:
            cp = code[i].split()
            strcode = str(cp[0])
            checkDATA={'sc':strcode}
            cursor.execute(checkIT,checkDATA)
            nam[i] = cursor.fetchone()
        except:
            nam[i] = "Nothing"

    return nam



