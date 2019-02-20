from app import app
from utils import *
from app.models import Servers,Users,Acl,Groups
from templates import *

def generateTemplate(serverid):
	serverKey = Servers.getServerById(serverid)[0].serverkey
	template = TEMPLATEPATH.format(serverid)
	with open(template,'w') as f:
		f.write(defaultHeading(serverKey,"S"))
		f.write('\n{0}'.format(commentGen("GROUPS")))
		for x in Groups.getAGroupByServerId(serverid):

			if x.remarks:
				f.write('\n{0}'.format(commentGen(x.remarks)))
			aclname = ''
			if x.aclid:
				aclname = x.groups.aclname
			f.write(group(x.groupname,x.defaultservice,x.services,x.parent,x.member,aclname,x.logintype,x.remarks))
			f.write('\n')
		f.write(userHeading())
		f.write('\n{0}'.format(commentGen("USERSLIST")))
		for d in Users.getUsersByServerId(serverid):
			f.write(users(d.username,d.users.groupname))

			


	
