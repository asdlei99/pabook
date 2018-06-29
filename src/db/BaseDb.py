#coding=utf-8

from src.db import Db

from src.model import *

class BaseDb(object):
	def __init__(self):
		self.db = Db.instance;

	def executeSql(self, sql):
		self.db.executeSql(sql);

	def fetchOne(self):
		return self.db.fetchOne();

	#创建表
	def createTable(self):
		self.executeSql(self.createTableSql());

	#删除表
	def dropTable(self):
		self.executeSql(self.dropTableSql());

	#插入
	def insert(self, model):
		self.executeSql(self.insertSql(model));

	#修改
	def update(self, model):
		self.executeSql(self.updateSql(model));

	#删除
	def delete(self, model):
		self.executeSql(self.deleteSql(model));

	#============
	def createTableSql(self):
		raise Exception("子类实现");
	def dropTableSql(self):
		raise Exception("子类实现");
	def insertSql(self, model):
		raise Exception("子类实现");
	def updateSql(self, model):
		raise Exception("子类实现");
	def deleteSql(self, model):
		raise Exception("子类实现");
	def tableName(self):
		raise Exception("子类实现");

