#coding=utf-8

from BaseDb import BaseDb

from src.model.Models import *

class KeyValueDb(BaseDb):

	def tableName(self):
		return "keyvalue";

	#操作bookinfo表
	def createTableSql(self):
		return '''
				create table if not exists {}(
					tkey varchar(256) not null primary key,
					tvalue varchar(256) not null
				);
			'''.format(self.tableName());

	def dropTableSql(self):
		return "drop table if exists {}".format(self.tableName());

	def get(self, key):
		self.executeSql('''select tvalue from {} where tkey="{}"'''.format(self.tableName(), key));
		oneRet = self.fetchOne();
		if oneRet != None:
			return oneRet["tvalue"];
		return None;

	def set(self, key, value):
		storedValue = self.get(key);
		if storedValue == None:
			if value != None:
				#insert
				self.executeSql('''insert into {} (tkey, tvalue) values ("{}", "{}")'''.format(self.tableName(), key, value));
		else:
			if value == None:
				#delete
				self.executeSql('''delete from {} where tkey = "{}"'''.format(self.tableName(), key));
			else:
				#update
				self.executeSql('''update {} set tvalue="{}" where tkey="{}"'''.format(self.tableName(), value, key));

	#测试代码
	def test(self):
		self.createTable();
		self.set("testkey", None);
		self.set("testkey", "testValue");
		self.set("testkey", "testValue");
		self.set("testkey", None);
		self.set("testkey", "testValue");
		Utils.log(str(self.get("testkey")));
		Utils.log(str(self.get("testkey1")));