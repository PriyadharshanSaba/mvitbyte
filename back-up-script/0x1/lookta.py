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
from pyscri.teacha.FILx import fileDATA



def teacherlog(request):
    return render(request,'ta/headtest_ta.html')


def teacherHome(request):
    try:
        staff_id = request.POST['staffid']
        staff_id=staff_id.upper()
        request.session['cur_usn'] = staff_id
        staff_pass=request.POST['psw']
        request.session['session_pass'] = staff_pass
    except:
        staff_id=request.session['cur_usn']
        staff_pass=request.session['session_pass']
    cn = mysql.connector.connect(user='root', password='Rocky@2009', database='TEACHA')
    cursor=cn.cursor()
    checkIT="SELECT USERNAME FROM REGISTER WHERE STAFFID= %(uid)s AND PASS=%(pass)s"
    checkDATA={'uid':staff_id,'pass':staff_pass}
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
#return render(request,'ta/parsing_error.html', {'datas':[staff_id,staff_pass]})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        filxNam = request.POST['filxname']
        #yes = fileDATA.checkIfExists(myfile.name)
        yes = 0
        if yes != 1:
            fs = FileSystemStorage(location='media/')
            #filename = fs.save(myfile.name, myfile)
            fext = (myfile.name).split('.')
            fext = fext[len(fext) - 1]
            filxNam = str(filxNam)+"."+str(fext)
            filename = fs.save(filxNam, myfile)
            uploaded_file_url = fs.url(filename)
            fileDATA.filePathIntoDB(filename,uploaded_file_url)
            return render(request, 'ta/home_ta.html', {'datas':[[request.session['cur_user']]]})
    return render(request, 'ta/parsing_error.html')


def deleteNodes(request):
    fetched = fileDATA.fetchFilxPath()
    request.session['file_list_length'] = len(fetched)
        # if len(fetched) == 0:
        #return render(request, 'ta/delNotesMod.html',{'datas':[request.session['cur_user']]})
    return render(request, 'ta/delNotesMod.html', {'datas':fetched})


def deleteRequest(request):
    len = request.session['file_list_length']
    file_name_list = request.POST.getlist('files')
    x =fileDATA.deleteFiles(file_name_list)
    return render(request, 'ta/delRequest.html',{'datas':[file_name_list,len,x]})

def notes(request):
    fetched = fileDATA.fetchFilxPath()
    return render(request, 'ta/notes_ta.html',{'datas':fetched})


def upload_form(request):
    x = fileDATA.fetchFilxPath()
    return render(request, 'ta/upload_files.html',{'datas':len(x)})

def succs(request):
    return render(request,'ta/succs.html')

def error(request):
    return render(request,'ta/parsing_error.html')

def goBack(request):
    return render(request,'ta/headtest_ta.html')


