#coding=utf-8

from src.db import Db

from src.model import *

from src.utils import Utils

from src.utils import Log

class BaseDb(object):
    def __init__(self):
        Log.D("init class " + str(self.__class__));
        self.db = Db.instance;
        self.createTable();

    def __del__(self):
        if Utils != None:
            Log.D("dealloc class " + str(self.__class__));

    def executeSql(self, sql):
        self.db.executeSql(sql);

    def fetchOne(self):
        return self.db.fetchOne();

    def fetchAll(self):
        return self.db.fetchAll();

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

