#coding=utf-8

import urlparse

from src.utils import Utils

import os

#七牛和aws key
class Config:
    shared = None;
    def __init__(self):
        '''
        基本参数
        ------------
        '''
        #要爬的网站根目录
        self.url = "https://www.ybdu.com";
        #如果有输出，输出路径
        self.outPath = "./out";
        #解析器名称
        #目前就一个 YbduParser，如果爬其他站，需要实现新的Parser子类
        self.parserName = "YbduParser";
        #Storge名称
        #保存文件方法
        #FileStorge表示存本地
        #QiniuStorge表示存七牛云
        #AWSStorge表示存AWS
        self.storgeName = "FileStorge";
        #charset
        self.charset = "utf-8";
        #aes code
        #如果设为None表示即将存储的内容不加密
        #如果为非None字符串，表示存储内容将加密，字符串的内容为加密使用的code
        self.aesCode = "helloworld";
        #type
        # all 表示爬全站
        # single 表示爬单本小说
        self.parseType = "all"
        '''
        Storge
        ------------
        '''
        #七牛
        self.qnAK = "qiniu access key";
        self.qnSK = "qiniu secret key";
        self.qnBK = "qiniu bucket name";

        #aws
        self.awsBK = "aw-kaso";

        '''
        DataBase
        ------------
        '''
        #mysql
        self.dbUser = "wanghy";
        self.dbPwd = "wang@1234";
        self.dbName = "book";

        self.logLevel = "";

    def error(self, msg):
        raise Exception(msg);

    #检查参数是否正确
    def check(self):
        #url
        urlParseResult = urlparse.urlsplit(self.url);
        if urlParseResult == None:
            self.error("Config.url配置错误");
        self.scheme = urlParseResult.scheme;
        self.host = urlParseResult.netloc;
        if not Utils.isValidStr(self.scheme) or not Utils.isValidStr(self.host):
            self.error("Config.url配置错误");

        #outPath
        if not Utils.isValidStr(self.outPath):
            self.error("Config.outPath配置错误");
        if not os.path.isdir(self.outPath):
            if not Utils.createDir(self.outPath):
                self.error("Config.outPath配置错误");

        from src.utils import Log
        Log.setOutPath(self.outPath);

        self.tmpPath = self.outPath + os.sep + ".tmp";
        if not os.path.isdir(self.tmpPath):
            if not Utils.createDir(self.tmpPath):
                self.error("Config.outPath配置错误");

        #parser
        if self.parserName != "YbduParser":
            self.error("Config.parserName配置错误");

        #storge
        if self.storgeName != "FileStorge" and self.storgeName != "QiniuStorge" and self.storgeName != "AWSStorge":
            self.error("Config.storgeName配置错误");

        if self.storgeName == "QiniuStorge":
            if not Utils.isValidStr(self.qnAK) or not Utils.isValidStr(self.qnSK) or not Utils.isValidStr(self.qnBK):
                self.error("未配置七牛云的 access key，secret key，bucketname");
        elif self.storgeName == "AWSStorge":
            if not Utils.isValidStr(self.awsBK):
                self.error("未配置AWS的bucketname");

        #aescode
        if self.aesCode != None and not Utils.isValidStr(self.aesCode):
            self.error("Config.aesCode配置错误");

        #parserType
        if self.parseType != "all" and self.parseType != "single":
            self.error("Config.parsetType配置错误");

        #数据库
        if not Utils.isValidStr(self.dbUser) or not Utils.isValidStr(self.dbPwd) or not Utils.isValidStr(self.dbName):
            self.error("未配置mysql的用户名，密码或数据库名称");

Config.shared = Config();
Config.shared.check();
