#coding=utf-8

#七牛和aws key
class Config:
    shared = None;
    def __init__(self):
        self.qnAK = "qiniu access key";
        self.qnSK = "qiniu secret key";
        self.qnBK = "qiniu bucket name";

        #aws bucket name
        self.awsBK = "com-kaso";

Config.shared = Config();