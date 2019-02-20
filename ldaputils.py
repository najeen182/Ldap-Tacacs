import ldap
import ldap.modlist
import json
import os

from utils import convertPassword,verifyPassword,domainname

#from configldap import IP,USERNAME,PASSWORD,LDAP_BASE
with open(os.getcwd()+'/config.json', 'r') as f:
    d = json.load(f)

def ldapConnection():
    con = ldap.initialize('ldap://{0}'.format(d.get('IP')))
    con.simple_bind_s(d.get('USERNAME'),d.get('PASSWORD'))
    return con

def search_user(filtername):
    query = "(uid={0})".format(filtername)
    result = ldapConnection().search_s(d.get('LDAP_BASE'),ldap.SCOPE_SUBTREE,query)
    return result

def search_usermail(exchangeid):
    query = "(mail={0}@{1})".format(exchangeid,domainname)
    result = ldapConnection().search_s(d.get('LDAP_BASE'),ldap.SCOPE_SUBTREE,query)
    return result

def all_user():
    query = "(uid=*)"
    result = ldapConnection().search_s(d.get('LDAP_BASE'),ldap.SCOPE_SUBTREE,query)
    return result

def add_user(username,usermail,userpassword):
    dn = "uid={0},ou={1},{2}".format(username,str(d.get('OU')),str(d.get('LDAP_BASE')))
    homedirectory = "/home/{0}".format(username)
    modlist = {
                "objectClass" : ["person","organizationalPerson","inetOrgPerson","posixAccount","top","shadowAccount"],
                "uid" : [username],
                "cn" : [username],
                "gidnumber": [str(d.get('GROUPID'))],
                "homedirectory": [homedirectory],
                "loginshell": [str(d.get('LOGINSHELL'))],
                "mail": [usermail],
                "shadowlastchange": ["17316"],
                "shadowmax": ["99999"],
                "shadowmin": [str(d.get('SHADOWMIN'))],
                "shadowwarning":[str(d.get('SHADOWWARNING'))],
                "sn":[username],
                "uidnumber": ["10000"],
                "userpassword": [convertPassword(userpassword)]
                }
    #return ldap.modlist.addModlist(modlist)
    result = ldapConnection().add_s(dn, ldap.modlist.addModlist(modlist))
    return result

def modify_user(username,password):
    dn = "uid={0},ou={1},{2}".format(username,str(d.get('OU')),str(d.get('LDAP_BASE')))
    old_value = {"userPassword":str(search_user(username)[0][1]['userPassword'][0])}
    new_value = { "userPassword" : [convertPassword(password)]}

    modlist = ldap.modlist.modifyModlist(old_value,new_value)
    result = ldapConnection().modify_s(dn,modlist)
    return result

def check_pass(username,password):
    dn = "uid={0},ou={1},{2}".format(username,str(d.get('OU')),str(d.get('LDAP_BASE')))
    old_value = {"userPassword":str(search_user(username)[0][1]['userPassword'][0])}
    return old_value
    validatepassword = verifyPassword(password,old_value)
    return validatepassword 

def delete_user(username):
    
    dn = "uid={0},ou={1},{2}".format(username,str(d.get('OU')),str(d.get('LDAP_BASE')))
    result = ldapConnection().delete_s(dn)
    return result
