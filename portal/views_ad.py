# -*- coding: utf-8 -*-
#from utils.utils import YourClassOrFunction

from __future__ import unicode_literals
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
#import psycopg2
import psycopg2
from django.template import RequestContext
import re
import mechanize
from pyscri import check_admin_login,putMarksCustomSem
import csv


def adminiHome(request):
    return render(request,'admini/headtest_admini.html')

def product(request):
    return render(request,'admini/pro.html')


def forgotLoginDetails(request):
    return render(request,'admini/ad.html')


def loginHome(request):
    username = request.session['cur_admin']
    admin_user = check_admin_login.fetchAdminName(username)
    return render(request,'admini/home_ad.html',{'admin':[admin_user]})


def marksDash(request):
    return render(request,'admini/enterMarks.html')

def okay(request):
    startUsn = request.POST['startUSN']
    endUsn = request.POST['endUSN']
    sem = request.session['semester']
    putMarksCustomSem.main_func(startUsn,endUsn,sem)
    return render(request,'admini/dbokay.html')

def testing(request):
    sem=request.POST['sem']
    request.session['semester']=sem
    return render(request, 'admini/temptest.html' ,{'testing':[sem]})


def login_redirection(request):
    admin_name=request.POST['adminNAME']
    admin_pass=request.POST['adminPSW']
    request.session['cur_admin']= admin_name
    checkDetails = check_admin_login.checkLoginInfo(admin_name.lower(),admin_pass)
    if checkDetails == 1:
        return render(request,'admini/login_redirection.html')
    else:
        return render(request,'admini/headtest_admini_incorrect.html')

def aboutAdm(request):
    return render(request,'admini/about.html')

