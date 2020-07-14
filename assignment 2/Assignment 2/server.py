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
    
def largest():
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Select "mag","time","place"  from EARTHQ where "mag" is not NULL order by "mag" DESC limit 5'
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(db2conn)
    return render_template('largest.html',r=rows)
    
@app.route('/largest5', methods=['POST'])
def large():
    return largest()

def greaterthan3(datefrom=None, dateto=None):
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='select "mag","time","place" from EARTHQ where "mag">3 and ("time" between ? and ?)'
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, datefrom)
        ibm_db.bind_param(stmt, 2, dateto)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('largest.html',r=rows)
    

@app.route('/quakesinjune1-8', methods=['GET'])
def greater():
    datefrom = request.args.get('datefrom', '')
    dateto = request.args.get('dateto', '')
    return greaterthan3(datefrom, dateto)



def recent3days(rangefrom=None, rangeto=None, datefromritch=None, datetoritch=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
       
        sql='select count(*) from EARTHQ where ("mag" BETWEEN ? AND ?) AND ("time" between ? AND ?)'
        #Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, rangefrom)
        ibm_db.bind_param(stmt, 2, rangeto)
        ibm_db.bind_param(stmt, 3, datefromritch)
        ibm_db.bind_param(stmt, 4, datetoritch)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn) 
    return render_template('count.html', r=rows)
    

@app.route('/quakesrange', methods=['GET'])
def rangeq():
    datefromritch = request.args.get('datefromritch', '')
    datetoritch = request.args.get('datetoritch', '')
    rangefrom = request.args.get('rangefrom', '')
    rangeto = request.args.get('rangeto', '')
    
    return recent3days(rangefrom, rangeto, datefromritch, datetoritch)	



def arlington():
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='SELECT "mag","time","place" FROM EARTHQ WHERE acos(sin(0.0175*32.7357) * sin(0.0175*"latitude") + cos(0.0175*32.7357) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* -97.1081)) )* 6371 < 500'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('largest.html',r=rows)


 
@app.route('/within500kmofA', methods=['POST'])
def nearer():
    return arlington()


def dallas():
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='SELECT "mag","time","place"  FROM EARTHQ WHERE acos(sin(0.0175*32.7767) * sin(0.0175*"latitude") + cos(0.0175*32.7767) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* -97.1081))) * 6371 < 200 order by "mag" desc LIMIT 1'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('largest.html',r=rows)



@app.route('/within200kmofDallas', methods=['GET'])
def near():
    return dallas()


def new():
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='SELECT count(*) FROM EARTHQ WHERE acos(sin(0.0175*32.7767) * sin(0.0175*"latitude") + cos(0.0175*32.7767) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* (-97.1081)))) * 6371 < 1000'
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        sql1='SELECT count(*) FROM EARTHQ WHERE acos(sin(0.0175*61) * sin(0.0175*"latitude") + cos(0.0175*61) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* (-150)))) * 6371 < 1000'
        stmt = ibm_db.prepare(db2conn,sql1)
        ibm_db.execute(stmt)
        rowsa=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rowsa.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('both.html',r=rows,l=rowsa)

@app.route('/newsearch', methods=['GET'])
def newarea():
    return new()


 
 
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

      
port = os.getenv('PORT', '8000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

