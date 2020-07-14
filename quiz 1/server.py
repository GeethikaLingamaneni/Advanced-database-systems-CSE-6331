import os
from flask import Flask,redirect,render_template,request
import urllib
import datetime
import json
import ibm_db

app = Flask(__name__)

# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
   db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
   db2cred = db2info["credentials"]
   appenv = json.loads(os.environ['VCAP_APPLICATION'])
else:
    raise ValueError('Expected cloud environment')
    
def room(minim=None, max=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Select * from NAMES where "Room">=? and "Room"<=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, minim)
        ibm_db.bind_param(stmt, 2, max)
        ibm_db.execute(stmt)
        rows=[]
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('rooms.html',r=rows)
    
@app.route('/roomrange', methods=['GET'])
def rangesearchs():
    minim = request.args.get('minim', '')
    max = request.args.get('max', '')
    return room(minim, max)

    
 
def updatenames(idToUpdate=None, newName=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
       
        sql='Update NAMES set "Name"=? where "ID"=?'
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, newName)
        ibm_db.bind_param(stmt, 2, idToUpdate)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
  
        # close database connection
        ibm_db.close(db2conn)
    return render_template('update.html',r=rows)	 
 
@app.route('/updatename', methods=['GET'])
def update():
    idToUpdate = request.args.get('idToUpdate', '')
    newName = request.args.get('newName', '')
    return updatenames(idToUpdate, newName)	

@app.route('/')
def index():
   return render_template('index.html', app=appenv)

 
@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
	return render_template('404.html',title='404')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
	return render_template('500.html',title='500')



def updatevalue(min=None):
    if(min.isdigit()):
        if(int(min)%2==0):
            ci='even'
        else:
            ci='odd'
    else:
        ci='unknown'
    return render_template('value.html',text=min,r=ci)
    
@app.route('/updatevalue', methods=['GET'])
def value():
    min = request.args.get('min', '')
    return updatevalue(min)
      
port = os.getenv('PORT', '8000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

