#coding=utf-8

from BaseDb import BaseDb

from src.model.Models import *

class VisitUrlDb(BaseDb):

	def tableName(self):
		return "visiturl";

	#操作bookinfo表
	def createTableSql(self):
		return '''
				create table {}(
					id int default 0 not null primary key,
					url varchar(256) not null unique key,
					visiting tinyint not null default 0
				)
			'''.format(self.tableName());

	def dropTableSql(self):
		return "drop table if exists {}".format(self.tableName());

	def insertSql(self, model):
		return '''insert into {} (url, visiting) values ("{}", "{}")'''.format(self.tableName(), model.url, model.visiting);

	def updateSql(self, model):
		return '''update {} set visiting="{}" where url="{}"'''.format(self.tableName(), model.visiting, model.url);

	def deleteSql(self, model):
		return '''delete from {} where url="{}"'''.format(self.tableName(), model.url);

	#测试代码
	def test(self):
		self.createTable();
		visitingModel = VisitUrlModel("http://www.baidu.com", 0);

		self.insert(visitingModel);

		visitingModel.visiting = 1;

		self.update(visitingModel);

		# self.delete(visitingModel);

class VisitPageUrl(VisitUrlDb):
	def tableName(self):
		return "visitpageurl";