import smtplib

def verfMail(otp,toAdd,name):
    fromaddr = 'studentportal.info7@gmail.com'
    pasw='dbmsproject@2017'
    toaddrs = str(toAdd)
    content="Hello, "+str(name)+"\nYour code is : "+otp+"\n\n\n\nThis is a testing being done in our shitty DBMS project. Feel free to click the delete button. \n\n\n\nYour freindly neighbourhood,\nPD"
    msg = "\r\n".join(["From:" + fromaddr,"To:" + toaddrs,"Subject: Verification Code","",content])
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(fromaddr,pasw)
    mail.sendmail(fromaddr,toaddrs,msg)
    mail.close()
    return


