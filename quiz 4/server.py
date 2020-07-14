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
from io import BytesIO
import base64
import hashlib
import  math
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
plt.rcParams['figure.figsize'] = (6,4)
plt.style.use('ggplot')
import base64


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



#############################################################################################################





#########################################################################################################




#########################################################################################################

def scatterplotq4(c=None,yrf=None,yrt=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    success="SELECT Smokers,Year from s where Year between '"+str(yrf)+"'and '"+str(yrt)+"' and Entity = '"+str(c)+"'"
    cursor.execute(success)
    result_set = cursor.fetchall()
    sizes=[]
    labels = []
    for row in result_set:
        sizes.append(row[0])
        labels.append(row[1])
    print(labels)
    print(sizes)
    plt.scatter(labels,sizes,color="blue",alpha=0.5,marker="*")
    plt.xticks(labels)
    plt.xlabel("Years")
    plt.ylabel("Smokers")
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()  
    plt.show()
    plt.clf()
    return render_template('success3.html',plot_url=plot_url) 



def barchartq4(c=None,yrf=None,yrt=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    success="SELECT Smokers,Year from s where Year between '"+str(yrf)+"'and '"+str(yrt)+"' and Entity = '"+str(c)+"'"
    cursor.execute(success)
    result_set = cursor.fetchall()
    sizes=[]
    labels = []
    for row in result_set:
        sizes.append(row[0])
        labels.append(row[1])
    print(labels)
    print(sizes)
    y_pos = np.arange(len(labels))
    fig, ax = plt.subplots()    
    width = 0.75 # the width of the bars 
    ax.barh(y_pos, sizes, width, color=('green'))
    ax.set_yticks(y_pos+width/2)
    ax.set_yticklabels(labels, minor=False)
    #plt.bar(y_pos, performance, color=('gold', 'yellowgreen', 'lightcoral','blue','red'),align='center', alpha=0.5)
    #plt.xticks(y_pos, objects)
    plt.ylabel('Years')
    plt.xlabel('Smokers')
    for i, v in enumerate(sizes):
        ax.text(v + 3, i + .25, str(v), color='black', fontweight='bold')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.show()
    plt.clf()
    return render_template('success2.html',plot_url=plot_url)


def piechartq4(c=None,yrf=None, yrt=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    success="SELECT Smokers,Year from s where Year between '"+str(yrf)+"'and '"+str(yrt)+"' and Entity = '"+str(c)+"'"
    cursor.execute(success)
    result_set = cursor.fetchall()
    sizes=[]
    labels = []
    for row in result_set:
        sizes.append(row[0])
        labels.append(row[1])
    print(labels)
    print(sizes)
    colors = ['gold', 'yellowgreen', 'lightcoral','blue','red','brown']
    plt.pie(sizes,labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.show()
    plt.clf()
    return render_template('success.html',plot_url=plot_url)
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


@app.route('/q45', methods=['GET'])
def q45():
    c = request.args.get('cou','')
    a = request.args.get('yrf','')
    b = request.args.get('yrt','')
    return piechartq4(c,a,b) 

@app.route('/q46', methods=['GET'])
def q46():
    c = request.args.get('cou6','')
    a = request.args.get('yrf6','')
    b = request.args.get('yrt6','')
    return barchartq4(c,a,b) 

@app.route('/q47', methods=['GET'])
def q47():
    c = request.args.get('cou7','')
    a = request.args.get('yrf7','')
    b = request.args.get('yrt7','')
    return scatterplotq4(c,a,b) 




port = os.getenv('PORT', '8000')
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=int(port))