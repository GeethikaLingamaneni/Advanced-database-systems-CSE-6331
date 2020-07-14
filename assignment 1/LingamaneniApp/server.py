
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
    
def demo(name=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Select * from PEOPLE where "Name"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
            print(rows)
        ibm_db.close(db2conn)
    return render_template('ppl.html', r=rows)
	
	
# handle database request and query people information
def salarysearch():
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Select * from PEOPLE where "Salary"<99000'
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
    return render_template('salary.html', r=rows)
	
def removePerson(name=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Delete from PEOPLE where "Name"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rows=[]
        # close database connection
        ibm_db.close(db2conn)
    return render_template('removeppl.html')

# handle database request and query people information
def updatekeyword(nameToUpdateKeyword=None, keyword=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Update PEOPLE set "Keywords"=? where "Name"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, keyword)
        ibm_db.bind_param(stmt, 2, nameToUpdateKeyword)
        ibm_db.execute(stmt)
        rows=[]
        
        # close database connection
        ibm_db.close(db2conn)
    return render_template('updateppl.html')	
	
def updatesalary(nameToUpdate=None, salary=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Update PEOPLE set "Salary"=? where "Name"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, salary)
        ibm_db.bind_param(stmt, 2, nameToUpdate)
        ibm_db.execute(stmt)
        rows=[]
        # close database connection
        ibm_db.close(db2conn)
    return render_template('updateppl.html')		

def updatepicture(nameToUpdatePic=None, picture=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='Update PEOPLE set "Picture"=? where "Name"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, picture)
        ibm_db.bind_param(stmt, 2, nameToUpdatePic)
        ibm_db.execute(stmt)
        rows=[]
        # close database connection
        ibm_db.close(db2conn)
    return render_template('updateppl.html')


# main page to dump some environment information
@app.route('/')
def index():
   return render_template('index.html', app=appenv)


@app.route('/search', methods=['GET'])
def searchroute():
    name = request.args.get('name', '')
    return demo(name)

@app.route('/searchlessthan99000', methods=['POST'])
def searchsalary():
    return salarysearch()

@app.route('/remove', methods=['GET'])
def remove():
    name = request.args.get('nameToRemove', '')
    return removePerson(name)	
	
@app.route('/updatekeyword', methods=['GET'])
def updatekey():
    nameToUpdateKeyword = request.args.get('nameToUpdateKeyword', '')
    keyword = request.args.get('newkeyword', '')
    return updatekeyword(nameToUpdateKeyword, keyword)	

@app.route('/updatesalary', methods=['GET'])
def updatesalarys():
    nameToUpdate = request.args.get('nameToUpdate', '')
    salary = request.args.get('newSalary', '')
    return updatesalary(nameToUpdate, salary)		
	
@app.route('/updatepicture', methods=['GET'])
def updatepictures():
    nameToUpdatePic= request.args.get('nameToUpdatePic', '')
    picture = request.args.get('newPicture', '')
    return updatepicture(nameToUpdatePic, picture)		
	
@app.route('/demo/<name>')
def demoroute(name=None):
    return demo(name)

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
