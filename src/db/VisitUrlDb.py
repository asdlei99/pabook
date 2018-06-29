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
					visiting tinyint not null default 0,
					bookId varchar(16)
				)
			'''.format(self.tableName());

	def dropTableSql(self):
		return "drop table if exists {}".format(self.tableName());

	def insertSql(self, model):
		if model.bookId != None:
			return '''insert into {} (url, visiting, bookId) values ("{}", "{}", "{}")'''.format(self.tableName(), model.url, model.visiting, model.bookId);
		else:
			return '''insert into {} (url, visiting) values ("{}", "{}")'''.format(self.tableName(), model.url, model.visiting);

	def updateSql(self, model):
		if model.bookId != None:
			return '''update {} set visiting="{}" where url="{}"'''.format(self.tableName(), model.visiting, model.url);
		else:
			return '''update {} set visiting="{}", bookId="{}" where url="{}"'''.format(self.tableName(), model.visiting, model.bookId, model.url);

	def deleteSql(self, model):
		return '''delete from {} where url="{}"'''.format(self.tableName(), model.url);

	def getVisitingUrl(self):
		self.executeSql("select url from {} where visiting = 1".format(self.tableName()));
		oneRet = self.fetchOne();
		if oneRet == None:
			self.executeSql("select url from {}".format(self.tableName()));
			oneRet = self.fetchOne();
		if oneRet == None:
			return None;
		else:
			return oneRet["url"];

	def deleteVisitUrl(self, url):
		self.executeSql('''delete from {} where url="{}"'''.format(self.tableName(), url));

	#测试代码
	def test(self):
		self.createTable();
		visitingModel = VisitUrlModel("http://www.baidu.com", 0);

		self.insert(visitingModel);

		visitingModel.visiting = 1;

		self.update(visitingModel);

		Utils.log(" -- test visiting url = " + str(self.getVisitingUrl()));

		# self.delete(visitingModel);

class VisitPageUrl(VisitUrlDb):
	def tableName(self):
		return "visitpageurl";