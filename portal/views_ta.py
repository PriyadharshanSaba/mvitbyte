# -*- coding: utf-8 -*-
#from utils.utils import YourClassOrFunction

from __future__ import unicode_literals
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import psycopg2
from django.template import RequestContext
import re
import mechanize
from pyscri import check_admin_login,putMarksCustomSem,connDB
import csv
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pyscri.teacha import teacha,verificaMail




def teacherlog(request):
    return render(request,'ta/headtest_ta.html',{'datas':None})


def teacherHome(request):
    try:
        staff_nam = request.POST['staffname']
        staff_nam=staff_nam.upper()
        request.session['cur_usn'] = staff_nam.upper()
        staff_pass=request.POST['psw']
        request.session['session_pass'] = staff_pass
    except:
        staff_nam=request.session['cur_usn']
        staff_pass=request.session['session_pass']
    db=teacha.DBConnection();
    checkIT="SELECT TOKEN FROM TEACHA.REGISTER WHERE USERNAME= %(uid)s AND PASS=%(pass)s"
    checkDATA={'uid':staff_nam,'pass':staff_pass}
    db[1].execute(checkIT,checkDATA)
    try:
        log = db[1].fetchone()
        request.session['cur_user'] = log
        checkIT="SELECT SALUT,USERNAME FROM TEACHA.TEACHA_DET WHERE USERNAME= %(uid)s"
        checkDATA={'uid':teacha.namCap(staff_nam)}
        db[1].execute(checkIT,checkDATA)
        sal= db[1].fetchone()
        return render(request,'ta/home_ta.html',{'datas':[sal[0],sal[1]]})
    except:
        return render(request,'ta/headtest_ta.html',{'exist':2})


def newReg(request):
    newUser = request.POST['teachaName']
    db=teacha.DBConnection();
    ce = teacha.checkExisting(newUser)
    teachaPh = 1
        #if teacha.checkPHONE(request.POST['teachaPh'])==1:
    if teachaPh ==1:
        if teacha.checkMAIL(request.POST['teachaMail'])==1:
            sg= request.POST['teachaGender']
            if sg == '10':
                gend="Mr."
            elif sg=='11':
                gend="Ms."
            else:
                gend="Mx."
            inse="SELECT MAX(TOKEN) FROM TEACHA.REGISTER"
            db[1].execute(inse)
            token=db[1].fetchone()[0]
            if token == None:
                token=1
            else:
                token= token+ 1
            if ce==0:
                inse ="INSERT INTO TEACHA.REGISTER VALUES (%(un)s,%(p)s,%(to)s)"
                idat = {'un': newUser.upper(),'p':request.POST['teachaNewpasw'],'to':token}
                db[1].execute(inse,idat)
                db[0].commit()
                inse="INSERT INTO TEACHA.TEACHA_DET VALUES (%(m)s,%(p)s,%(sal)s,%(usr)s,%(to)s)"
                idat={'m':request.POST['teachaMail'],'p':teachaPh,'sal':gend,'usr':teacha.namCap(newUser),'to':token}
                db[1].execute(inse,idat)
                db[0].commit()
                #verificaMail.verfMail('000',newUser,request.POST['teachaMail'])
                return render(request,'ta/headtest_ta.html')
            else:
                return render(request,'ta/headtest_ta.html',{'exist':1})

        else:
            return render(request,'ta/headtest_ta.html',{'exist':3})
    else:
        return render(request,'ta/headtest_ta.html',{'exist':4})





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

def profile_settings(request):
    return render(request,'ta/profile_settings_ta.html',{'datas':None})

def changePassword(request):
    db=connDB.connect()
    que="SELECT * FROM TEACHA.REGISTER WHERE USERNAME=%(uid)s AND PASS=%(np)s"
    dat={'np':request.POST['curPass'],'uid':request.session['cur_usn']}
    db[1].execute(que,dat)
    if db[1].fetchone()!=None:
        if request.POST['curPass'] == request.POST['newPass']:
            return render(request,'ta/profile_settings_ta.html',{'datas':1})
        else:
            que="UPDATE TEACHA.REGISTER SET PASS=%(np)s WHERE USERNAME=%(uid)s"
            dat={'np':request.POST['newPass'],'uid':request.session['cur_usn']}
            db[1].execute(que,dat)
            db[0].commit()
            return render(request,'ta/profile_settings_ta.html',{'datas':0})
    else:
        return render(request,'ta/profile_settings_ta.html',{'datas':2})

def changeMail(request):
    db=connDB.connect()
    que="SELECT * FROM TEACHA.REGISTER WHERE USERNAME=%(uid)s AND PASS=%(np)s"
    dat={'np':request.POST['entPass'],'uid':request.session['cur_usn']}
    db[1].execute(que,dat)
    if db[1].fetchone()!=None:
        que="UPDATE TEACHA.TEACHA_DET SET MAIL=%(np)s WHERE USERNAME=%(uid)s"
        dat={'np':request.POST['newMail'],'uid':request.session['cur_usn']}
        db[1].execute(que,dat)
        db[0].commit()
        return render(request,'ta/profile_settings_ta.html',{'datas':0})
    else:
        return render(request,'ta/profile_settings_ta.html',{'datas':2})



