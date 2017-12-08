import csv
import psycopg2



cn = psycopg2.connect(user='root', password='Rocky@2009', database='studentportal')
cursor=cn.cursor()
with open('datasets/CS_IV_SemMarks/cs_blr_iv.csv','r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        try:
            checkIT="INSERT INTO SEM4_2017_CBCS15 VALUES (%(uid)s, %(s1c)s, %(s1i)s, %(s1m)s, %(s2c)s, %(s2i)s, %(s2m)s, %(s3c)s, %(s3i)s, %(s3m)s, %(s4c)s, %(s4i)s, %(s4m)s, %(s5c)s, %(s5i)s, %(s5m)s, %(s6c)s, %(s6i)s, %(s6m)s, %(s7c)s, %(s7i)s, %(s7m)s, %(s8c)s, %(s8i)s, %(s8m)s, %(s1p)s, %(s2p)s, %(s3p)s, %(s4p)s, %(s5p)s, %(s6p)s, %(s7p)s, %(s8p)s)"
            checkDATA={'uid':row[0],'s1c':row[2],'s1i':row[4],'s1m':row[5],'s2c':row[7],'s2i':row[9],'s2m':row[10],'s3c':row[12],'s3i':row[14],'s3m':row[15],'s4c':row[17],'s4i':row[19],'s4m':row[20],'s5c':row[22],'s5i':row[24],'s5m':row[25],'s6c':row[27],'s6i':row[29],'s6m':row[30],'s7c':row[32],'s7i':row[34],'s7m':row[35],'s8c':row[37],'s8i':row[39],'s8m':row[40], 's1p':row[6], 's2p':row[11], 's3p':row[16], 's4p':row[21], 's5p':row[26], 's6p':row[31], 's7p':row[36], 's8p':row[41]}
            cursor.execute(checkIT,checkDATA)
            cn.commit()
        except:
            pass

