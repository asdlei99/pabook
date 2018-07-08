#coding=utf-8

#七牛和aws key
class Config:
    shared = None;
    def __init__(self):
        #七牛
        self.qnAK = "qiniu access key";
        self.qnSK = "qiniu secret key";
        self.qnBK = "qiniu bucket name";

        #aws
        self.awsBK = "aw-kaso";

        #mysql
        self.dbUser = "wanghy"
        self.dbPwd = "wang@1234"
        self.dbName = "book"

Config.shared = Config();
