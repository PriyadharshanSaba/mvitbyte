import smtplib

def verfMail(otp,toAdd,name):
    fromaddr = 'studentportal.info7@gmail.com'
    pasw='dbmsproject@2017'
    toaddrs = str(toAdd)
    content="Hello, "+str(name)+"\n Your code is : "+otp
    msg = "\r\n".join(["From:" + fromaddr,"To:" + toaddrs,"Subject: Verification Code","",content])
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(fromaddr,pasw)
    mail.sendmail(fromaddr,toaddrs,msg)
    mail.close()
    return


