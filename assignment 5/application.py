import os
from flask import Flask,redirect,render_template,request
import pymssql
import time
import random
import urllib
import datetime
import json
import redis
import pickle
import hashlib
import random
import urllib
import datetime
import json
import pickle
import hashlib
import shutil
import csv
import sys


application = Flask(__name__)


r = redis.Redis(host='adb5.i11iaw.ng.0001.use2.cache.amazonaws.com',
        port=6379, db=0, password='vhtZjHKFEu5OAKtsPOtoSpwMYfhw+Ol8retvR+fdFgE=')
   



def largest():
    dbconn = pymssql.connect(server='adbdb.ccqiv46tukii.us-east-2.rds.amazonaws.com', port=1433, user='geethika', password='geethika', database='adbdb')
    #dbconn = pymssql.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()


    cursor.execute("select top (5) mag,time,place from edata order by mag desc")
    rows = cursor.fetchall()
    return render_template('largest.html',r=rows)

@application.route("/largest5", methods=['POST'])
def large():
    return largest()


def greaterthan3():
    dbconn = pymssql.connect(server='adbdb.ccqiv46tukii.us-east-2.rds.amazonaws.com', port=1433, user='geethika', password='geethika', database='adbdb')
    #dbconn = pymssql.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()

    cursor.execute("Select mag,time,place from edata where mag>3 and (TIME between '2020-06-01' and '2020-06-08')")
    rows = cursor.fetchall()
    return render_template('largest.html',r=rows)

@application.route("/quakesinjune1-8", methods=['POST'])
def greater():
    return greaterthan3()




def recent3days(rangefrom=None,rangeto=None):
    dbconn = pymssql.connect(server='adbdb.ccqiv46tukii.us-east-2.rds.amazonaws.com', port=1433, user='geethika', password='geethika', database='adbdb')
    #dbconn = pymssql.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()


    cursor.execute("Select count(*) from edata where( mag BETWEEN " + rangefrom +" AND " + rangeto + ") AND (TIME between '2020-06-11' and '2020-06-13')")
    rows = cursor.fetchone()
    return render_template('count.html',r=rows)


@application.route("/quakesrange", methods=['GET'])
def rangeq():
    rangefrom = request.args.get('rangefrom', '')
    rangeto = request.args.get('rangeto', '')
    return recent3days(rangefrom, rangeto)	



def arlington():
    dbconn = pymssql.connect(server='adbdb.ccqiv46tukii.us-east-2.rds.amazonaws.com', port=1433, user='geethika', password='geethika', database='adbdb')
    #dbconn = pymssql.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()


    cursor.execute("Select mag,time,place from edata where acos(sin((3.14/180)*32.7357) * sin((3.14/180)*latitude) + cos((3.14/180)*32.7357) * cos((3.14/180)*latitude) * cos((3.14/180)*longitude - ((3.14/180)*(-97.1081)))) * 6371 < 500")
    rows = cursor.fetchall()
    return render_template('largest.html',r=rows)


@application.route("/within500kmofA", methods=['POST'])
def nearer():
    return arlington()



def dallas():
    dbconn = pymssql.connect(server='adbdb.ccqiv46tukii.us-east-2.rds.amazonaws.com', port=1433, user='geethika', password='geethika', database='adbdb')
    #dbconn = pymssql.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()


    cursor.execute("Select top(1) mag,time,place from edata where acos(sin((3.14/180)*32.8) * sin((3.14/180)*latitude) + cos((3.14/180)*32.8) * cos((3.14/180)*latitude) * cos((3.14/180)*longitude - ((3.14/180)*(-96.8)))) * 6371 < 200")
    rows = cursor.fetchall()
    return render_template('largest.html',r=rows)

@application.route("/within200kmofDallas", methods=['POST'])
def near():
    return dallas()



def new():
    dbconn = pymssql.connect(server='adbdb.ccqiv46tukii.us-east-2.rds.amazonaws.com', port=1433, user='geethika', password='geethika', database='adbdb')
    #dbconn = pymssql.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()

    cursor.execute("SELECT count(*) FROM edata WHERE acos(sin((3.14/180)*32.8) * sin((3.14/180)*latitude) + cos((3.14/180)*32.8) * cos((3.14/180)*latitude) * cos((3.14/180)*longitude - ((3.14/180)*(-96.8)))) * 6371 < 1000" )
    rows = cursor.fetchone()
    cursor.execute("SELECT count(*) FROM edata WHERE acos(sin((3.14/180)*61) * sin((3.14/180)*latitude) + cos((3.14/180)*61) * cos((3.14/180)*latitude) * cos((3.14/180)*longitude - ((3.14/180)*(-150)))) * 6371 < 1000" )
    rowsa = cursor.fetchone()
    return render_template('both.html',r=rows,l=rowsa)

@application.route("/newsearch", methods=['POST'])
def newarea():
    return new()




@application.route("/")
def index():
   return render_template('index.html')

 
@application.errorhandler(404)
@application.route("/error404")
def page_not_found(error):
	return render_template('404.html',title='404')

@application.errorhandler(500)
@application.route("/error500")
def requests_error(error):
	return render_template('500.html',title='500')






if __name__ == "__main__":
	application.run()