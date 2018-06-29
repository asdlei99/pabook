#coding=utf-8

from BaseDb import BaseDb

from src.model.Models import *

class BookinfoDb(BaseDb):
	def __init__(self):
		super(BookinfoDb, self).__init__();
		self._tableName = "bookinfo";

	def tableName(self):
		return self._tableName;

	#操作bookinfo表
	def createTableSql(self):
		return '''
			create table if not exists {}(
				id int auto_increment primary key,
				bookId varchar(16) not null unique key,
				uniqueKey varchar(32) not null unique key,
				title varchar(32) not null,
				author varchar(8) not null ,
				category varchar(32) not null,
				des varchar(300) not null,
				bookImg varchar(256),
				downBookUrl varchar(256),
				downMuluUrl varchar(256),
				wordsCount int default 0,
				updateTime int default 0,
				chapterCount int default 0,
				status int default 0,
				clickCount int default 0,
				monthClickCount int default 0,
				weekClickCount int default 0,
				collectionCount int default 0,
				recommendCount int default 0,
				monthRecommendCount int default 0,
				weekRecommendCount int default 0
			);
			'''.format(self.tableName());

	def dropTableSql(self):
		return "drop table if exists {}".format(self.tableName());

	def updateSql(self, bookInfoModel):
		bookInfoDict = bookInfoModel.toDict(True);
		attrCount = len(bookInfoDict);
		sql = "update {} set ".format(self.tableName());
		bi = 0;
		for bk, bv in bookInfoDict.items():
			needDouhao = bi < attrCount - 1;
			sql += str(bk) + " = '" + str(bv) + "'" + (needDouhao and "," or "");
			bi += 1;

		return sql;

	def isExistsWithKey(self, bookUniqueKey):
		if self.executeSql('''select * from {} where uniqueKey = "{}"'''.format(self.tableName(), bookUniqueKey)):
			return self.fetchOne() != None;
		else:
			return False;

	def isExistsWithDownUrl(self, downUrl):
		if self.executeSql('''select * from {} where downBookUrl = "{}"'''.format(self.tableName(), downUrl)):
			oneRet = self.fetchOne();
			if oneRet == None:
				return False;
			elif oneRet["downloadStatus"] == BookDownloadStatus.Success:
				return True;
			else:
				return False;
		else:
			return False;

	def deleteSql(self, bookInfoModel):
		return '''delete from {} where uniqueKey = "{}"'''.format(self.tableName(), bookInfoModel.uniqueKey);

	def insertSql(self, bookInfoModel):
		bookInfoDict = bookInfoModel.toDict(True);
		attrCount = len(bookInfoDict);
		mapValues = "";
		mapKeys = "";
		bi = 0;
		for bk, bv in bookInfoDict.items():
			needDouhao = bi < attrCount - 1;
			mapKeys += bk + (needDouhao and "," or "");
			mapValues += "\"{" + bk + "}\"" + (needDouhao and "," or "");
			bi += 1;

		return '''insert into {} ({}) values ({})'''.format(self.tableName(), mapKeys, mapValues).format(**bookInfoDict);

	#测试代码
	def test(self):
		self.createTable();
		bookInfoModel = BookInfoModel();
		bookInfoModel.bookId = "123456";
		bookInfoModel.title = "斗破苍穹";
		bookInfoModel.author = "天蚕土豆";
		bookInfoModel.category = "玄幻";
		bookInfoModel.des = "斗气大法";
		bookInfoModel.setUniqueKey();

		Utils.log(" --- toDict = " + str(bookInfoModel.toDict(True)));

		# self.bookInfoDelete(bookInfoModel);
		self.insert(bookInfoModel);

		bookInfoModel.title = "武动乾坤";
		bookInfoModel.setUniqueKey();

		self.update(bookInfoModel);