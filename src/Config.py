#coding=utf-8

#七牛和aws key
class Config:
    shared = None;
    def __init__(self):
        self.qnAK = "kEmp3KqS4q-vdXq4ZXfVxeEm7KtpTQJ4EQ3-s0vl";
        self.qnSK = "x9HqUozCeuvCnB0euXLtmNP_oNqlzDqShUh7SsbB";
        self.qnBK = "com-aw";

        self.awsBK = "com-kaso";

Config.shared = Config();