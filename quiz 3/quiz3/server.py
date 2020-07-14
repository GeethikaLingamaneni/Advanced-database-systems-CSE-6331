import os
from flask import Flask,redirect,render_template,request
import pypyodbc
import time
import random
import urllib
import datetime
import json
import redis
import pickle
import hashlib

app = Flask(__name__)

server = 'geethikasqlserver.database.windows.net'
database = 'adbdb'
username = 'geethika'
password = 'Lin@2598'
driver= '{ODBC Driver 17 for SQL Server}'
myHostname = "geethika.redis.cache.windows.net"
myPassword = "vhtZjHKFEu5OAKtsPOtoSpwMYfhw+Ol8retvR+fdFgE="

r = redis.Redis(host='geethika.redis.cache.windows.net',
        port=6379, db=0, password='vhtZjHKFEu5OAKtsPOtoSpwMYfhw+Ol8retvR+fdFgE=')


def q7(code=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    cursor.execute("SELECT  ti.entity,ti.year, ti.NumberTerroristIncidents from sp join ti on sp.code=ti.code where sp.code='"+str(code)+"'")
    rows1 = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('seventh.html',r=rows1,t=exectime)


@app.route('/seventh', methods=['GET'])
def ques7():
    code = request.args.get('code', '')
    return q7(code)



def q8(val1=None,val2=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    cursor.execute("SELECT  ti.entity,ti.year,ti.NumberTerroristIncidents from ti join sp on sp.code=ti.code and ti.year BETWEEN '"+str(val1)+"' AND '"+str(val2)+"'")
    rows = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('eight.html',r=rows,t=exectime)

@app.route('/eighth', methods=['GET'])
def ques8():
    val1 = request.args.get('val1', '')
    val2 = request.args.get('val2', '')
    return q8(val1,val2)




def q9(va1=None,va2=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    cursor.execute("SELECT count(ti.NumberTerroristIncidents) from ti join sp on sp.code=ti.code where sp.prevalence BETWEEN '"+str(va1)+"' AND '"+str(va2)+"'")
    rows1 = cursor.fetchall()
    cursor.execute("Select ti.entity,ti.year,ti.NumberTerroristIncidents from ti join sp on sp.code=ti.code where sp.prevalence BETWEEN '"+str(va1)+"' AND '"+str(va2)+"'")
    rows2 = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('nine.html',r=rows1,l=rows2,t=exectime)


@app.route('/nine', methods=['GET'])
def ques9():
    va1 = request.args.get('va1', '')
    va2 = request.args.get('va2', '')
    return q9(va1,va2)







def q108(val1=None,val2=None,num2=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num2)):
      cursor.execute("SELECT  ti.entity,ti.year, ti.NumberTerroristIncidents from sp join ti on sp.code=ti.code and ti.year BETWEEN '"+str(val1)+"' AND '"+str(val2)+"'")
      rows1 = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('eight.html',r=rows1,t=exectime)


@app.route('/tena', methods=['GET'])
def ques108():
    val1 = request.args.get('val1', '')
    val2 = request.args.get('val2', '')
    num2 = request.args.get('num2', '')
    return q108(val1,val2,num2)





def q109(va3=None,va4=None,numa=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(numa)):
      cursor.execute("SELECT count(ti.NumberTerroristIncidents) from ti join sp on sp.code=ti.code where sp.prevalence BETWEEN '"+str(va3)+"' AND '"+str(va4)+"'")
      rows1 = cursor.fetchall()
      cursor.execute("Select ti.entity,ti.year,ti.NumberTerroristIncidents from ti join sp on sp.code=ti.code where sp.prevalence BETWEEN '"+str(va3)+"' AND '"+str(va4)+"'")
      rows2 = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('nine.html',r=rows1,l=rows2,t=exectime)


@app.route('/ninea', methods=['GET'])
def ques109():
    va3 = request.args.get('va3', '')
    va4 = request.args.get('va4', '')
    numa = request.args.get('numa', '')
    return q109(va3,va4,numa)



def q118(value1=None,value2=None,num3=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num3)):
      success=("SELECT  ti.entity,ti.year, ti.NumberTerroristIncidents from sp join ti on sp.code=ti.code and ti.year BETWEEN '"+str(value1)+"' AND '"+str(value2)+"'")
      hash = hashlib.sha224(success.encode('utf-8')).hexdigest()
      key = "redis_cache:" + hash
      if (r.get(key)):
           print("redis cached")
      else:
           # Do MySQL query   
           cursor.execute(success)
           data = cursor.fetchall()
           rows1 = []
           for j in data:
                rows1.append(str(j))  
           # Put data into cache for 1 hour
           r.set(key, pickle.dumps(list(rows1)) )
           r.expire(key, 36)

    end = time.time()
    exectime = end - start
    return render_template('eight.html',r=rows1,t=exectime)


@app.route('/elevena', methods=['GET'])
def ques118():
    value1 = request.args.get('value1', '')
    value2 = request.args.get('value2', '')
    num3 = request.args.get('num3', '')
    return q118(value1,value2,num3)



def q119(va5=None,va6=None,numb=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(numb)):
      success1=("SELECT count(ti.NumberTerroristIncidents) from ti join sp on sp.code=ti.code where sp.prevalence BETWEEN '"+str(va5)+"' AND '"+str(va6)+"'")
      success2=("Select ti.entity,ti.year,ti.NumberTerroristIncidents from ti join sp on sp.code=ti.code where sp.prevalence BETWEEN '"+str(va5)+"' AND '"+str(va6)+"'")
      hash = hashlib.sha224(success1.encode('utf-8')).hexdigest()
      key = "redis_cache:" + hash
      if (r.get(key)):
           print("redis cached")
      else:
           # Do MySQL query   
           cursor.execute(success1)
           rows1 = cursor.fetchall()
           cursor.execute(success2)
           rows2 = cursor.fetchall()
           rows1= []
           #for j in rows1:
               # rows1.append(str(j))  
           # Put data into cache for 1 hour
           r.set(key, pickle.dumps(list(rows1)) )
           r.expire(key, 36)
    end = time.time()
    exectime = end - start
    return render_template('nine.html',t=exectime)


@app.route('/nineb', methods=['GET'])
def ques119():
    va5 = request.args.get('va5', '')
    va6 = request.args.get('va6', '')
    numb = request.args.get('numb', '')
    return q119(va5,va6,numb)





      
port = os.getenv('PORT', '8000')
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=int(port))