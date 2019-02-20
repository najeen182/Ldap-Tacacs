import md5
from passlib.hash import ldap_md5_crypt

TEMPLATEPATH="{0}/tac_plus.conf"
TEMPLATETEXTPATH="{0}/tac_plus.txt"
def convertPassword(password):

    newpassword = md5.new(password).digest()
    newpassword = ldap_md5_crypt.encrypt(password)
    return newpassword 
    #return "{{CRYPT}}{0}".format(newpassword.encode('base64'))
    #return "{{md5}}{0}".format(newpassword.encode('base64'))

def verifyPassword(password,hashvalue):
    valid = ldap_md5_crypt.verify(password,hashvalue)
    return valid

def allowUsers(groupid):
	gid = [19004]
	if groupid in gid:
		return True

	return False
