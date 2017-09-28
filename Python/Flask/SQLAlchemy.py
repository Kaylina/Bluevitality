# code=UTF-8
# 数据库连接demo 使用SQLALCHEMY

from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=\
	'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

# 程序使用数据库，并且获得所有功能
db=SQLAlchemy(app)


# 定义模型
class Role(db.Model):
	# 定义表名
	__tablename__='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	users=db.relationship('User',backref='role')
	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),unique=True,index=True)
	role_id=db.Column(db.Integer,db.ForeignKet('roles.id'))
	
	def __repr__(self):
		return '<User %r>' %self.username