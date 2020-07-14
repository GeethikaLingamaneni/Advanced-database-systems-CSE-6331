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
   
def randrange(rangefrom=None,rangeto=None,num=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num)):
        mag= round(random.uniform(rangefrom, rangeto),1)
        success="SELECT * from edata where mag>'"+str(mag)+"'"
        hash = hashlib.sha224(success.encode('utf-8')).hexdigest()
        key = "redis_cache:" + hash
        if (r.get(key)):
           print("redis cached")
        else:
           # Do MySQL query   
           cursor.execute(success)
           data = cursor.fetchall()
           rows = []
           for j in data:
                rows.append(str(j))  
           # Put data into cache for 1 hour
           r.set(key, pickle.dumps(list(rows)) )
           r.expire(key, 36)
        cursor.execute(success)
    end = time.time()
    exectime = end - start
    return render_template('count.html', t=exectime)

@app.route('/multiplerun', methods=['GET'])
def randquery():
    rangefrom = float(request.args.get('rangefrom',''))
    rangeto = float(request.args.get('rangeto',''))
    num = request.args.get('num','')
    return randrange(rangefrom,rangeto,num) 
	
def disdata(rangefrom1=None,rangeto1=None,num1=None):
    dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num1)):
        mag= round(random.uniform(rangefrom1, rangeto1),1)
        success="SELECT * from edata where mag>'"+str(mag)+"'"
        cursor.execute(success)
        rows = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('count.html', t=exectime,ci=rows)

@app.route('/displaydata', methods=['GET'])
def display():
    rangefrom1 = float(request.args.get('rangefrom1',''))
    rangeto1 = float(request.args.get('rangeto1',''))
    num1 = request.args.get('num1','')
    return disdata(rangefrom1,rangeto1,num1) 

def datad(num2=None):
    dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num2)):
        success2="Delete top(2)PERCENT from edata COMMIT;"
        cursor.execute(success2)
        success="SELECT count(*) from edata;"
        cursor.execute(success)
        rows = cursor.fetchall()
        end = time.time()   
    exectime = end - start
    return render_template('count2.html', t=exectime,r=rows)

@app.route('/ddata', methods=['GET'])
def displayd():
    num2 = request.args.get('num2','')
    return datad(num2) 


def rrange(num3=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num3)):
        success2="Delete top(2)PERCENT from edata COMMIT;"
        cursor.execute(success2)
        success="SELECT count(*)  from edata;"
        hash = hashlib.sha224(success.encode('utf-8')).hexdigest()
        key = "redis_cache:" + hash
        if (r.get(key)):
           print("redis cached")
           rows=[]
        else:
           # Do MySQL query   
           cursor.execute(success)
           data = cursor.fetchall()
           rows = []
           for j in data:
                rows.append(str(j))  
           # Put data into cache for 1 hour
           r.set(key, pickle.dumps(list(rows)) )
           r.expire(key, 36)
        cursor.execute(success)    
    end = time.time()
    exectime = end - start
    return render_template('count2.html', t=exectime,r=rows)

@app.route('/mdata', methods=['GET'])
def rquery():
    num3 = request.args.get('num3','')
    return rrange(num3) 



@app.route('/')
def hello_world():
  return render_template('index.html')


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
	return render_template('404.html',title='404')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
	return render_template('500.html',title='500')


    
port = os.getenv('PORT', '8000')
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=int(port))