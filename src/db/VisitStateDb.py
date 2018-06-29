#coding=utf-8

from BaseDb import BaseDb

from src.model.Models import *

from src.utils import Utils

class VisitStateDb(BaseDb):

	def tableName(self):
		return "visitstate";

	#操作bookinfo表
	def createTableSql(self):
		return '''
				create table {}(
					lastVisitUrl varchar(256),
					lastVisitBookUrl varchar(256),
					lastBookId varchar(16)
				)
			'''.format(self.tableName());

	def dropTableSql(self):
		return "drop table if exists {}".format(self.tableName());

	def setValue(self, key, value):
		self.executeSql("select * from {}".format(self.tableName()));
		if self.fetchOne() == None:
			self.executeSql('''insert into {} ({}) values ("{}")'''.format(self.tableName(), key, value));
		else:
			self.executeSql('''update {} set {} = "{}"'''.format(self.tableName(), key, value));

	def getValue(self, key):
		self.executeSql('''select * from {}'''.format(self.tableName()));
		ret = self.fetchOne();
		if ret == None:
			return ret;
		else:
			return ret[key];

	#测试代码
	def test(self):
		self.createTable();

		self.setValue("lastVisitUrl", "www.baidu.com1");
		self.setValue("lastVisitBookUrl", "www.baidu.com2");
		self.setValue("lastBookId", "10331");

		Utils.log(self.getValue("lastVisitUrl"));
		Utils.log(self.getValue("lastVisitBookUrl"));
		Utils.log(self.getValue("lastBookId"));

		# self.delete(visitingModel);