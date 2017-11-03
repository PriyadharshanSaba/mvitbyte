import requests
import mechanize
from bs4 import BeautifulSoup
import csv


subCode=[None]*10
subName=[None]*10
subInternal=[None]*10
subExternal=[None]*10
subPass=[None]*10


br = mechanize.Browser()
br.set_handle_robots(False)
#login_usn = raw_input()

hashcheck=0
check_notnull=False
br_i = 0



def getBranch(x):
    branch_list = ['CS','IS','EE','EC','ME','BT','CV']
    return branch_list[x]



for usn_i in range(1,10):
    if usn_i<10:
        fusn_i="00"+str(usn_i)
    elif usn_i>=10 and usn_i<100:
        fusn_i="0"+str(usn_i)
    elif usn_i>=100:
        fusn_i=str(usn_i)
    if br_i > 6 :
        break

    branch = getBranch(br_i)
    uid="1MV15"+str(branch)+str(fusn_i)
    br.open("http://results.vtu.ac.in/cbcs_17/index.php")
    br.select_form(nr=0)
    try:
        br_i = br_i + 1
        br.form['usn'] = uid
        sub = br.submit()
        soup = BeautifulSoup(sub.read(),"lxml")
        for i in soup.findAll('td'):
            print i.text

        for td in soup.findAll('td',{'style':'padding-left:15px;text-transform:uppercase'}):
            student_usn = td.text[3:].upper()
            if student_usn!=None and hashcheck<5:
                hashcheck=0
                check_notnull=True

            elif hashcheck>=5:
                break
            
            else:
                hashcheck=hashcheck+1
                check_notnull=False

        if check_notnull==True:
            for td in soup.findAll('td',{'style':'padding-left:15px'}):
                student_name = td.text[2:].upper()
                print student_name
            
            for td in soup.findAll('table',{'class':'table table-bordered'}):
                mark_meta=td.text.split("\n")
                try:
                    for mar_i in range(0,8):
                        subCode[mar_i]=mark_meta[((mar_i+1)*10)+3]
                        subName[mar_i]=mark_meta[((mar_i+1)*10)+4]
                        subInternal[mar_i]=int(mark_meta[((mar_i+1)*10)+5])
                        subExternal[mar_i]=int(mark_meta[((mar_i+1)*10)+6])
                        subPass[mar_i]=mark_meta[((mar_i+1)*10)+8]
                    with open('cs_blr_iv.csv', 'a') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
                        spamwriter.writerow([student_usn,student_name,subCode[0],subName[0],subInternal[0],subExternal[0],subPass[0],subCode[1],subName[1],subInternal[1],subExternal[1],subPass[1],subCode[2],subName[2],subInternal[2],subExternal[2],subPass[2],subCode[3],subName[3],subInternal[3],subExternal[3],subPass[3],subCode[4],subName[4],subInternal[4],subExternal[4],subPass[4],subCode[5],subName[5],subInternal[5],subExternal[5],subPass[5],subCode[6],subName[6],subInternal[6],subExternal[6],subPass[6],subCode[7],subName[7],subInternal[7],subExternal[7],subPass[7],subCode[8],subName[8],subInternal[8],subExternal[8],subPass[8]])
                except:
                    break
    except:
        break

