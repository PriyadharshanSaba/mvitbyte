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
from pyscri import check_admin_login,putMarksCustomSem
import csv
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pyscri.teacha import teacha
from pyscri.admin import connDB



def teacherlog(request):
    return render(request,'ta/headtest_ta.html',{'datas':None})


def teacherHome(request):
    try:
        staff_nam = request.POST['staffnam']
        staff_nam=staff_nam.upper()
        request.session['cur_usn'] = staff_nam
        staff_pass=request.POST['psw']
        request.session['session_pass'] = staff_pass
    except:
        staff_nam=request.session['cur_usn']
        staff_pass=request.session['session_pass']
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='TEACHA')
    cursor=cn.cursor()
    checkIT="SELECT USERNAME FROM REGISTER WHERE USERNAME= %(uid)s AND PASS=%(pass)s"
    checkDATA={'uid':teacha.namCap(staff_nam),'pass':staff_pass}
    cursor.execute(checkIT,checkDATA)
    try:
        log = cursor.fetchone()
        request.session['cur_user'] = log
        if log != None:
            return render(request,'ta/home_ta.html',{'datas':[[log]]})
        else:
            return render(request,'ta/parsing_error.html')
    except:
        return render(request,'ta/parsing_error.html')

        #except:
#return render(request,'ta/parsing_error.html', {'datas':[staff_nam,staff_pass]})


def newReg(request):
    db = connDB.DBConnection()
    staff_nam = request.POST['teachaName']
    request.session['teacher_name']=staff_nam
    que="SELECT MAX(STAFFID) FROM TEACHA.REGISTER"
    db[1].execute(que)
    c=db[1].fetchone()
    if c[0] == None:
        cx=0;
    else:
        cx=int(c[0])

    if request.POST['teachGender'] == '10':
        gend="Mr. "
    elif request.POST['teachGender'] == '11':
        gend="Ms. "
    else:
        gend="Mx. "
    
    ce=teacha.checkExisting(gend+staff_nam)
    if ce==0:
        que = "INSERT INTO TEACHA.REGISTER VALUES (%(id)s,%(nam)s,%(pass)s)"
        checkDATA={'id':(cx+1),'nam':gend+teacha.namCap(staff_nam), 'pass':request.POST['teachaNewpasw']}
        db[1].execute(que,checkDATA)
        db[0].commit()
        que = "INSERT INTO TEACHA.TEACHA_DET VALUES (%(id)s,%(mail)s,%(ph)s,%(gd)s)"
        checkDATA={'id':cx+1,'mail':request.POST['teachaMail'],'ph':request.POST['teachaPh'],'gd':gend}
        db[1].execute(que,checkDATA)
        db[0].commit()
        return render(request,'ta/temptest.html',{'datas':gend+teacha.namCap(staff_nam)})
    else:
        return render(request,'ta/headtest_ta.html',{'exists':1})



def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        filxNam = request.POST['filxname']
        #yes = teacha.checkIfExists(myfile.name)
        yes = 0
        if yes != 1:
            fs = FileSystemStorage(location='media/')
            #filename = fs.save(myfile.name, myfile)
            fext = (myfile.name).split('.')
            fext = fext[len(fext) - 1]
            filxNam = str(filxNam)+"."+str(fext)
            filename = fs.save(filxNam, myfile)
            uploaded_file_url = fs.url(filename)
            teacha.filePathIntoDB(filename,uploaded_file_url)
            return render(request, 'ta/home_ta.html', {'datas':[[request.session['cur_user']]]})
    return render(request, 'ta/parsing_error.html')


def deleteNodes(request):
    fetched = teacha.fetchFilxPath()
    request.session['file_list_length'] = len(fetched)
        # if len(fetched) == 0:
        #return render(request, 'ta/delNotesMod.html',{'datas':[request.session['cur_user']]})
    return render(request, 'ta/delNotesMod.html', {'datas':fetched})


def deleteRequest(request):
    len = request.session['file_list_length']
    file_name_list = request.POST.getlist('files')
    x =teacha.deleteFiles(file_name_list)
    return render(request, 'ta/delRequest.html',{'datas':[file_name_list,len,x]})

def notes(request):
    fetched = teacha.fetchFilxPath()
    return render(request, 'ta/notes_ta.html',{'datas':fetched})


def upload_form(request):
    x = teacha.fetchFilxPath()
    return render(request, 'ta/upload_files.html',{'datas':len(x)})


def succs(request):
    return render(request,'ta/succs.html')

def error(request):
    return render(request,'ta/parsing_error.html')

def goBack(request):
    return render(request,'ta/headtest_ta.html')



