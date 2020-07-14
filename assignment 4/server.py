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
	
def disdata(rangefrom1=None,rangeto1=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    success="SELECT depth,mag from edata where mag between '"+str(rangefrom1)+"' and '"+str(rangeto1)+"' "
    cursor.execute(success)
    rows = cursor.fetchall()
    depth=[]
    mag=[]
    for row in rows:
            depth.append(row['depth'])
            mag.append(row['mag'])
    X = np.array(list(zip(depth, mag)))
    kmeans = KMeans(n_clusters = int(8))
    kmeans.fit(X)
    centroid = kmeans.cluster_centers_
    labels = kmeans.labels_
    imga=BytesIO()
    all = [[]] * 8
    for i in range(len(X)):

        # print(index)
        # print(X[i], labels[i])

            colors = ["b.", "r.", "g.", "w.", "y.", "c.", "m.", "k."]
            for i in range(len(X)):
               plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=3)
               
            plt.scatter(centroid[:, 0], centroid[:, 1], marker="x", s=150, linewidths=5, zorder=10)
            
            plt.savefig(imga, format='png')
            imga.seek(0)

            plot_url = base64.b64encode(imga.getvalue()).decode()
            plt.show()
            plt.clf()
           
            break 
           
    return render_template('success.html', plot_url=plot_url)
   
    #return render_template('success.html', name = 'new_plot', url ='plot.png')     
    #return render_template('success.html', name = plt.show())	

@app.route('/displaydata', methods=['GET'])
def display():
    rangefrom1 = (request.args.get('rangefrom1',''))
    rangeto1 =(request.args.get('rangeto1',''))
    return disdata(rangefrom1,rangeto1) 


def piechart(rangefrom=None,rangeto=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    partition= float((float(rangeto)-float(rangefrom))/5)
    print(partition)
    sizes=[]
    labels=[]
    imgb=BytesIO()
    lower = float(rangefrom)
    upper=0
    imgb=BytesIO()
    for i in range(0,int(5)):
          upper= lower+partition
          success="SELECT count(*) from edata where mag between '"+str(lower)+"'and '"+str(upper)+"'"
          cursor.execute(success)
          result_set = cursor.fetchall()
          print(result_set)
          for row in result_set:
              sizes.append(row[0])
              labels.append('magrange'+str(round(lower,2))+' and '+str(round(upper,2)))
          lower=upper
    print(labels)
    print(sizes)
    colors = ['gold', 'lightcoral','yellowgreen','blue','lightblue']
    explode = (0.1, 0, 0)
    plt.pie(sizes,labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig(imgb, format='png')
    imgb.seek(0)
    plot_url = base64.b64encode(imgb.getvalue()).decode()
    plt.show()
    plt.clf()
    return render_template('success2.html', plot_url=plot_url)
   
@app.route('/pie', methods=['GET'])
def piec():
    rangefrom = str(request.args.get('rangefrom',''))
    rangeto =str(request.args.get('rangeto',''))
    return piechart(rangefrom,rangeto)


def barchart(rangefrom1=None,rangeto1=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:geethikasqlserver.database.windows.net,1433;Database=adbdb;Uid=geethika;Pwd=Lin@2598;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    partition= float((float(rangeto1)-float(rangefrom1))/5)
    print(partition)
    performance=[]
    labels=[]
    lower = float(rangefrom1)
    upper=0
    imgc=BytesIO()
    for i in range(0,int(5)):
          upper= lower+partition
          success="SELECT count(*) from edata where mag between '"+str(lower)+"'and '"+str(upper)+"'"
          cursor.execute(success)
          result_set = cursor.fetchall()
          print(result_set)
          rows=[]
          for row in result_set:
              performance.append(row[0])
              labels.append(''+str(round(lower,2))+' to '+str(round(upper,2)))
          lower=upper
    print(labels)
    y_pos = np.arange(len(labels))
    plt.bar(y_pos, performance, align='center', alpha=0.5,color='brown')
    plt.xticks(y_pos, labels)
    plt.ylabel('Count')
    plt.title('Mag range')
    plt.savefig(imgc, format='png')
    imgc.seek(0)
    plot_url = base64.b64encode(imgc.getvalue()).decode()
    plt.show()
    plt.clf()
    return render_template('success3.html', plot_url=plot_url)	

@app.route('/bar', methods=['GET'])
def barc():
    rangefrom1 = (request.args.get('rangefrom1',''))
    rangeto1 =(request.args.get('rangeto1',''))
   
    return barchart(rangefrom1,rangeto1) 	






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