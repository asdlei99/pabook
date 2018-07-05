#coding=utf-8

from BaseDb import BaseDb

from src.model.Models import *

from src.utils import Log

class VisitUrlDb(BaseDb):

	def tableName(self):
		return "visiturl";

	#操作bookinfo表
	def createTableSql(self):
		return '''
				create table if not exists {}(
					id int not null auto_increment primary key,
					url varchar(256) not null unique key,
					bookId varchar(16),
					status tinyint default 0
				);
			'''.format(self.tableName());

	def dropTableSql(self):
		return "drop table if exists {}".format(self.tableName());

	def deleteUrl(self, url):
		self.executeSql('''delete from {} where url="{}"'''.format(self.tableName(), url));

	def insertUrl(self, url):
		self.executeSql('''insert into {} (url) values ("{}")'''.format(self.tableName(), url));

	def getOneUrl(self):
		self.executeSql('''select url from {} where status = 0 limit 1'''.format(self.tableName()));
		ret = self.fetchOne();
		if ret != None:
			return ret["url"];
		return None;

	def isExistsUrl(self, url):
		self.executeSql('''select * from {} where url = "{}" and status = 0'''.format(self.tableName(), url));
		return self.fetchOne() != None;

	def setVisited(self, url):
		self.executeSql('''update {} set status = 1 where url="{}"'''.format(self.tableName(), url));

	#测试代码
	def test(self):
		self.createTable();
		visitingModel = VisitUrlModel("http://www.baidu.com", 0);

		self.insert(visitingModel);

		visitingModel.visiting = 1;

		self.update(visitingModel);

		Log.D(" -- test visiting url = " + str(self.getVisitingUrl()));

		# self.delete(visitingModel);

class VisitBookUrlDb(VisitUrlDb):
	def tableName(self):
		return "visitbookurl";