# -*- coding: utf-8 -*-
import MySQLdb

#简陋的SQL封装

class MysqlHandle:

	#初始化构造函数
	#user 		string 		用户名
	#passwd 	string	 	密码
	#db			string		数据库名字
	#host		string		服务器名
	#port		int 		端口
	#charset	string		字符集
	def __init__(self,user="root",passwd="",db="ca2014",host="localhost",port=3306,charset="utf8"):
		self.user = user
		self.passwd = passwd
		self.db = db
		self.host = host
		self.port = port
		self.charset = charset
		print self
		self.conn = MySQLdb.connect (host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset,port=self.port)
		self.cur = self.conn.cursor()

	#执行数据库语句
	#sql 	string	数据库语句
	#return bool	执行是否成功
	def execute_sql(self,sql):
		try:
			self.cur.execute(sql)
			self.conn.commit()
			return True
		except Exception as e:
			print e
			print "error"
			return False

	#关闭连接
	def close_sql(self):
		self.cur.close()
		self.conn.close()
