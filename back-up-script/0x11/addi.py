from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import mysql.connector
import re
import mechanize
import random
import numpy as nu
import random


def generateMessage_attend(attendance,subjects):
    
    str8 = ["Ahoy! Here's a nerd!","Too much attendance isnt good for life!!","Why do you even have to check attendance!?","Aye Aye Nerdy!"]
    str7 = ["You seem to be safe..","Seems like you're on the safer side!!","Nothing to worry, I hope!!","Safe guarded!!"]
    
    
    avg=round(((nu.average(attendance))/10),1)
    min=round(((nu.amin(attendance))/10),1)
    if avg>=8.5:
        if min>=8.2:
            n=random.randint(0,(len(str8)-1))
            return str8[n]
        else:
            n=random.randint(0,(len(str7)-1))
            return str7[n]

    elif avg<8.2 and avg>7.5:
        if min>=7.7:
            n=random.randint(0,(len(str7)-1))
            return str7[n]
        else:
            t = 0
            for o in attendance:
                if round((o/10),1) == min:
                    temp = t
                    break
                else:
                    t = t+1
            substr = subjects[t]
            try:
                substr = substr.split('and')
            except:
                substr = substr
            str7r = ["Seems like you're having trouble in "+substr[0]+"?","You appear to be facing issues from "+substr[0]+"!","Watch out for "+substr[0]+"!","Mind attending more "+substr[0]+" classes?"]
            n=random.randint(0,(len(str7r)-1))
            return str7r[n]
    else:
        t = 0
        for o in attendance:
            if round((o/10),1) == min:
                temp = t
                break
            else:
                t = t+1
        substr = subjects[t]
        try:
            substr = substr.split('and')
        except:
            substr = substr
        str4 = ["Mind attending more "+substr[0]+" classes?","Why dont you attend "+substr[0]+" classes?","Too cool to attend college?","Watch out,mate!","You're attendance freaks me out!!!"]
        n=random.randint(0,(len(str4)-1))
        return str4[n]


def reduceRange(marks1):
    marks1 = list(marks1)
    marks1 = map(float,marks1)
    marks1 = [f/10.0 for f in marks1]
    marks1 = [round(f,2) for f in marks1]
    marks1 = [f*10 for f in marks1]
    marks1 = map(int,marks1)
    for i in range(0,len(marks1)):
        if marks1[i]%4 != 0:
            marks1[i] = 0
    marks1 = set(marks1)
    marks1 = list(marks1)
    marks1.sort()
#    for row in range(0,len(marks1)):
#        marks1[row].sort()
    return marks1





