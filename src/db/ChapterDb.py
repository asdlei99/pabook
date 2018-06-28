#coding=utf-8

from BaseDb import BaseDb

from src.model.Models import *

class ChapterDb(BaseDb):
	def __init__(self, bookId):
		super(ChapterDb, self).__init__();
		self.bookId = bookId;
		if bookId == None:
			raise Exception(" bookId is None")
		self.tableName = "chapter_" + str(self.bookId);

	#操作bookinfo表
	def createTableSql(self):
		return '''
				create table {}(
					id int default 0 not null primary key,
					title varchar(64) not null,
					downUrl varchar(256) not null,
					uniqueKey varchar(32) not null
				)
			'''.format(self.tableName);

	def dropTableSql(self):
		return "drop table if exists {}".format(self.tableName);

	def insertSql(self, model):
		return '''insert into {} (title, downUrl, uniqueKey) values ("{}", "{}", "{}")'''.format(self.tableName, model.title, model.downUrl, model.uniqueKey);

	def updateSql(self, model):
		return '''update {} set title="{}", downUrl="{}" where uniqueKey="{}"'''.format(self.tableName, model.title, model.downUrl, model.uniqueKey);

	def deleteSql(self, model):
		return '''delete from {} where uniqueKey="{}"'''.format(self.tableName, model.uniqueKey);

	#测试代码
	def test(self):
		self.createTable();
		chapterModel = ChapterModel("http://www.baidu.com", "第一章 堕落的天才", "sadasdaks;kfewokflkslf");

		# self.bookInfoDelete(bookInfoModel);
		self.insert(chapterModel);

		chapterModel.title = "第一章 堕落的天才（改）";

		self.update(chapterModel);

		self.delete(chapterModel);