#/usr/bin/python
#-*- coding:utf-8 -*-
import time
import MySQLdb

class sqlHelper:

	
	def __init__(self,SqlServer,User,Password,DataBase,Charset):
		self.host = SqlServer
		self.user = User
		self.password = Password
		self.db = DataBase
		self.charset = Charset
		self.result = []
		try:
			self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,use_unicode=True,charset=self.charset)
		except MySQLdb.Error as e:
			print "连接数据库出错"+str(e)
		else:
			self.cur = self.conn.cursor()
			self.cur.execute("SET NAMES 'utf8'")
	

		#执行sql语句，如果为select返回tuple结果,其余返回空
	def DoSql(self,Sql):		
		try:
			self.cur.execute(Sql)
		except MySQLdb.Error as e:
			print "执行"+str(Sql)+"语句时候出错:"+str(e)
		else:
			self.result = self.cur.fetchall()	

	def GetResult(self):
		return self.result

	def CloseSqlHelper(self):
		self.cur.close()
		self.conn.close()	
	
	def Commit(self):
		self.conn.commit()		
            
