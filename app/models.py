from app import db
from sqlalchemy import func,distinct,or_

class Host(db.Model):
	__tablename__ = 'host'
	hid = db.Column('hid',db.Integer, primary_key=True)
	


class Servers(db.Model):
	__tablename__ = 'servers'
	sid = db.Column('sid',db.Integer,primary_key=True)  
	servername = db.Column('servername',db.String)
	ipaddress = db.Column('ipaddress',db.String)
	serverkey = db.Column('serverkey',db.String)
	status = db.Column('status',db.Boolean)
	
	def __repr__(self):
		return 'Servers {}'.format(self.servername)

        def update(self):
                db.session.commit()

        def save(self):
                db.session.add(self)
                self.update()

        def remove(self):
                db.session.delete(self)
                self.update()

        @staticmethod
        def getAllservers():
                return Servers.query.all()

	@staticmethod
	def getServerById(queryid):
		return Servers.query.filter_by(sid=queryid).all()


class Users(db.Model):
	__tablename__ = 'users'
	uid = db.Column('uid',db.Integer,primary_key=True)
	username = db.Column('username',db.String)
	groupid =  db.Column(db.Integer,db.ForeignKey('groups.gid'))
	serverid =  db.Column('serverid',db.Integer)
	status = db.Column('status',db.Boolean)

	def __repr__(self):
		return 'Users {}'.format(self.username)

        def update(self):
                db.session.commit()

        def save(self):
                db.session.add(self)
                self.update()

        def remove(self):
                db.session.delete(self)
                self.update()

        @staticmethod
        def getAllUsers():
                return Users.query.all()

	@staticmethod
	def getUsersByServerId(serverid):
		return Users.query.filter(serverid==serverid).all()

class Groups(db.Model):
	__table__name = 'groups'
	gid = db.Column('gid',db.Integer,primary_key=True)
	groupname = db.Column('groupname',db.String)
	services = db.Column('services',db.String)
	defaultservice = db.Column('defaultservice',db.String)
	parent = db.Column('parent',db.String)
	member = db.Column('member',db.String)
	status = db.Column('status',db.Boolean)
	aclid = db.Column(db.Integer,db.ForeignKey('acl.aid'))
	logintype = db.Column('logintype',db.String)
	serverid = db.Column('serverid',db.Integer)
	remarks = db.Column('remarks',db.String)
	users = db.relationship('Users',backref='users',lazy=True)

	def __repr__(self):
		return 'Groups {}'.format(self.groups)

        def update(self):
                db.session.commit()

        def save(self):
                db.session.add(self)
                self.update()

        def remove(self):
                db.session.delete(self)
                self.update()

        @staticmethod
        def getAllGroups():
                return Groups.query.all()


	@staticmethod
	def getAGroupByServerId(serverid):
		return Groups.query.filter_by(serverid=serverid).all()

class Acl(db.Model):
	__table__name = 'acl'
	aid = db.Column('aid',db.Integer,primary_key=True)
	aclname = db.Column('aclname',db.String)
	serverid = db.Column('serverid',db.String)
	permit = db.Column('permit',db.String)
	status = db.Column('status',db.Boolean)

	groups = db.relationship('Groups',backref='groups',lazy=True)

	def __repr__(self):
		return 'Acls {}'.format(self.aclname)

        def update(self):
                db.session.commit()

        def save(self):
                db.session.add(self)
                self.update()

        def remove(self):
                db.session.delete(self)
                self.update()

        @staticmethod
        def getAllAcls():
                return Acl.query.all()

	@staticmethod
	def getAclByServerId(serverid):
		return Acl.query.filter_by(serverid=serverid).all()
