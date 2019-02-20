from flask import abort,jsonify,request,render_template,session,redirect,url_for,escape
from ldaputils import add_user,search_user,modify_user,delete_user,all_user,search_usermail,check_pass
from app import app
from utils import *
from app.models import Servers,Users,Acl,Groups
from app.generator import *
import requests
import json
'''LOGIN'''
'''
@app.route('/')
def index():

	if 'username' in session:
		#return redirect(url_for('welcome'))
		return checkUser(session['username'])[0][1]['mail']
			
	return render_template("login.html")
'''
@app.route('/login',methods=['POST'])                                                                                                                               
def login():                                                                                                                                                             
        data = request.form                                                                                                                                              
        exchangeusername = data['username']                                                                                                                              
        exchangepassword = data['password']                                                                                                                              
                                                                                                                                                                         
        headers = { 'authorization': "Basic ZGEzOWEzZWU1ZTZiNGIwZDMyNTViZmVmOTU2MDE4OTBhZmQ4MDcwOTpw" }                                                                  
        payload = { "username":exchangeusername,"password":exchangepassword }                                                                                            
        r =  requests.post(APIURL,data=payload,headers=headers)                                                                                                          
        if r.status_code == 200:                                                                                                                                         
                result = r.json()                                                                                                                                        
                if result.get('status_code') == 200:                                                                                                                     
                        fetchData = result.get('data')                                                                                                                   
                        session['username'] = fetchData.get('samaccountname')                                                                                            
                        session['name'] = fetchData.get('displayname')                                                                                                   
                        session['department'] = fetchData.get('department')                                                                                              
                                                                                                                                                                         
			return redirect(url_for('welcome'))
                else:                                                                                                                                                    
                        return redirect(url_for('index',message="Invalid Login"))                                                                                        
@app.route('/logout')                                                                                                                                                    
def logout():                                                                                                                                                            
    # remove the username from the session if it's there                                                                                                                 
    session.pop('username', None)                                                                                                                                        
    return redirect(url_for('index'))                                                                                                                                    
                                                                                                                                                                         
                                         
@app.route('/welcome')
def welcome():
	if 'username' not in session:
		return redirect(url_for('index'))

	else:
		result = search_usermail(session['username'])
		if result:
			return result[0][1]['gidNumber']

	return "Welcome "+session["username"]

@app.route('/api/users',methods=["GET"])
def alluser():
	response = [ {
			"username": d[1]['cn'],
			"gid":d[1]['gidNumber'],
			"mail":d[1]['mail']
			} for d in all_user()]
	return jsonify(response)

@app.route('/api/users/<username>/search',methods=["GET"])
def usersearch(username):
	return jsonify(search_user(username)[0][1])


@app.route('/api/users/<username>/delete',methods=["DELETE"])
def userdelete(username):
	return jsonify(search_user(username)[0][1])

@app.route('/api/users/add',methods=["POST"])
def useradd():
	if not request.get_json() or ("username" not in request.get_json() \
		and "usermail" not in request.get_json() and "userpassword" not in request.get_json()):
		abort(400)

	data = request.get_json()
	username = data.get('username')
	userpassword = data.get("userpassword")
	usermail = data.get("usermail")

	result = add_user(str(username),str(usermail),str(userpassword))
	return jsonify(result[0])

@app.route('/api/users/changePassword',methods=["PUT"])
def changePass():
	if not request.get_json() or ("username" not in request.get_json() \
		and "pass" not in request.get_json()):
		abort(400)

	data = request.get_json()
	username = data.get('username')
	password = data.get('pass')

	result = modify_user(str(username),str(password))
	return jsonify(result[0]) 

@app.route('/api/users/<username>/validate',methods=["POST"])
def validatePassword(username):
	if not request.get_json() or ("password" not in request.get_json()):
		abort(400)

	data =  request.get_json()
	password = data.get('password')
	result = check_pass(username,password) 
	return jsonify(result)


@app.route('/api/tacservers',methods=['GET'])
def getServers():
	response = [ 
		  { "sid" : x.sid,
		    "servername" : x.servername,
		    "ipaddress" : x.ipaddress,
		    "serverkey" : x.serverkey,
		    "status" : x.status} for x in Servers.getAllservers() ]

	return jsonify(response)


@app.route('/api/tacusers',methods=['GET'])
def getTacUsers():
	response = [ 
		  { "uid" : x.uid,
		    "username" : x.username,
		    "groupid" : x.groupid,
		    "serverid" : x.serverid,
		    "groupname" : x.users.groupname,
		    "status" : x.status} for x in Users.getAllUsers() ]

	return jsonify(response)


@app.route('/api/tacacl',methods=['GET'])
def getTacACL():
	response = [ 
		  { "aid" : x.aid,
		    "aclname" : x.aclname,
		    "serverid" : x.serverid,
		    "permit" : x.permit,
		    "status" : x.status} for x in Acl.getAllAcls() ]

	return jsonify(response)


@app.route('/api/tacgroups',methods=['GET'])
def getTacGroups():
	response = [ 
		  { "gid" : x.gid,
		    "groupname" : x.groupname,
		    "serverid" : x.serverid,
		    "services" : x.services,
		    "parent" : x.parent,
		    "member" : x.member,
		    "aclid" : x.aclid,
		    "logintype" : x.logintype,
		    "remarks" : x.remarks,
		    "status" : x.status} for x in Groups.getAllGroups() ]

	return jsonify(response)


@app.route('/api/tac/generate',methods=['POST'])
def genTac():
	if not request.get_json() or ('serverid' not in request.get_json()):
		abort(400)

	data = request.get_json()
	serverid = data.get('serverid')

	generateTemplate(serverid)
	with ("1/tac_plus.txt","r") as f:
		tacacsfile = f.readlines()


	return render_template('template.html',content=tacacsfile)


@app.route('/api/test',methods=['PUT'])
def testPut():
	if not request.get_json():
		abort(400)

	data = request.get_json()
	return jsonify(data)

