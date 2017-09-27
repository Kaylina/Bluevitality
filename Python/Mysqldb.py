import MySQLdb

conn = MySQLdb.connect("localhost","root","","test")

cur = conn.cursor()

def insert(username,password):
	sql = "insert into user (username,password) values ('%s','%s')" %(username,password)
	cur.execute(sql)
	conn.commit()
	conn.close()

def isExisted(username,password):
	#sql="select * from user where username ='%s' and password ='%s'" %(username,password)
	sql="select * from user where username ="+username+" and password ="+password

	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

'''
username = 1
password = 1 or 1 = 1

select * from user where username = 1 and password =1 or 1 = 1
'''
