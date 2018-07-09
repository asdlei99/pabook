#coding=utf-8

from BaseDb import BaseDb

from src.model import *

class ChapterDb(BaseDb):
    def __init__(self, bookId):
        self.bookId = bookId;
        if bookId == None:
            raise Exception(" bookId is None")
        super(ChapterDb, self).__init__();

    def tableName(self):
        return "chapter_" + str(self.bookId);

    #操作bookinfo表
    def createTableSql(self):
        return '''
                create table if not exists {}(
                    id int not null auto_increment primary key,
                    title varchar(64) not null,
                    downUrl varchar(256) not null,
                    uniqueKey varchar(32) not null unique key,
                    downloaded tinyint default 0
                );
            '''.format(self.tableName());

    def dropTableSql(self):
        return "drop table if exists {}".format(self.tableName());

    def insertSql(self, model):
        return '''insert into {} (title, downUrl, uniqueKey) values ("{}", "{}", "{}")'''.format(self.tableName(), model.title, model.downUrl, model.uniqueKey);

    def updateSql(self, model):
        return '''update {} set title="{}", downUrl="{}" where uniqueKey="{}"'''.format(self.tableName(), model.title, model.downUrl, model.uniqueKey);

    def deleteSql(self, model):
        return '''delete from {} where uniqueKey="{}"'''.format(self.tableName(), model.uniqueKey);

    def setSectionInfoModel(self, sectionModel):
        succ = True;
        values = "";
        l = len(sectionModel.chapters);
        for i in range(0, l):
            c = sectionModel.chapters[i];
            values += '''("{}", "{}", "{}")'''.format(c.title, c.downUrl, c.uniqueKey);
            if i < l - 1:
                values += ","
        self.executeSql('''insert into {} (title, downUrl, uniqueKey) values {}'''.format(self.tableName(), values));

    def getSectionInfoModel(self):
        self.executeSql('''select * from {}'''.format(self.tableName()));
        allRet = self.fetchAll();
        if allRet != None:
            chapters = [];
            for one in allRet:
                chapterModel = ChapterModel();
                chapterModel.applyDict(one);
                chapters.append(chapterModel);
            sectionInfoModel = SectionInfoModel();
            sectionInfoModel.chpaters = chapters;
            return sectionInfoModel;
        return None;

    def setDownloaded(self, uniqueKey, succ):
        self.executeSql('''update {} set downloaded = "{}" where uniqueKey = "{}"'''.format(self.tableName(), succ, uniqueKey));

    #测试代码
    def test(self):
        self.createTable();
        chapterModel = ChapterModel("http://www.baidu.com", "第一章 堕落的天才", "sadasdaks;kfewokflkslf");

        # self.bookInfoDelete(bookInfoModel);
        self.insert(chapterModel);

        chapterModel.title = "第一章 堕落的天才（改）";

        self.update(chapterModel);

        self.delete(chapterModel);