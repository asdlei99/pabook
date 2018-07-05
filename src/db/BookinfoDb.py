#coding=utf-8

from BaseDb import BaseDb

from src.model.Models import *

from src.utils import Log

class BookinfoDb(BaseDb):

    def tableName(self):
        return "bookinfo";

    #操作bookinfo表
    def createTableSql(self):
        return '''
            create table if not exists {}(
                id int not null auto_increment primary key,
                bookId varchar(16) not null unique key,
                uniqueKey varchar(32) not null unique key,
                title varchar(32) not null,
                author varchar(8) not null ,
                category varchar(32) not null,
                des varchar(300) not null,
                bookImg varchar(256),
                downBookUrl varchar(256) unique key,
                downMuluUrl varchar(256) unique key,
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
                weekRecommendCount int default 0,
                downloadStatus int default -1
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
        self.executeSql('''select * from {} where uniqueKey = "{}"'''.format(self.tableName(), bookUniqueKey));
        return self.fetchOne() != None;

    def isAlreadyDownloadWithBookUrl(self, downBookUrl):
        self.executeSql('''select * from {} where downBookUrl = "{}"'''.format(self.tableName(), downBookUrl))
        oneRet = self.fetchOne();
        if oneRet == None:
            return False;
        elif oneRet["downloadStatus"] == BookDownloadStatus.Completed:
            return True;
        else:
            return False;

    def setDownloadStautsForBookUrl(self, downBookUrl, downloadStatus):
        self.executeSql('''update {} set downloadStatus="{}" where downBookUrl = "{}"'''.format(self.tableName(), downloadStatus, downBookUrl))

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

    def getBookinfo(self, downBookUrl):
        self.executeSql('''select * from {} where downBookUrl = "{}"'''.format(self.tableName(), downBookUrl));
        oneRet = self.fetchOne();
        if oneRet != None:
            bookInfo = BookInfoModel();
            bookInfo.applyDict(oneRet);
            return bookInfo;
        return None;

    def getAllBookinfo(self):
        self.executeSql('''select * from {}'''.format(self.tableName()));
        ret = self.fetchAll();
        if ret != None:
            bookinfos = [];
            for one in ret:
                bookInfo = BookInfoModel();
                bookInfo.applyDict(one);
                bookinfos.append(bookInfo);
            return bookinfos;
        return None;

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

        Log.D(" --- toDict = " + str(bookInfoModel.toDict(True)));

        # self.bookInfoDelete(bookInfoModel);
        self.insert(bookInfoModel);

        bookInfoModel.title = "武动乾坤";
        bookInfoModel.setUniqueKey();

        self.update(bookInfoModel);