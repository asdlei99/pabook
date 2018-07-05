#coding=utf-8

from optparse import OptionParser

from src.parser.YbduParser import YbduParser

from src.storge.FileStorge import FileStorge

import os

import urlparse

from src.storge.Storge import *

from src.utils import Utils

from src.Config import Config

from src.utils import Log

class Prepare:
    def __parseOptions(self):
        parser = OptionParser();
        parser.add_option("-r", "--url", dest="url", help="download web url");#download url
        parser.add_option("-o", "--output", dest="output", help="output dir");#输出文件夹路径
        parser.add_option("-p", "--parser", dest="parser", help="parser name");#解析器类名
        parser.add_option("-c", "--charset", default="utf-8", dest="charset", help="sit charset");#内容读取charset
        parser.add_option("-s", "--storge", dest="storge", help="file storge type");#文件存储类名 Storge的子类
        parser.add_option("-a", "--aescode", dest="aescode", help="aes encode pwd");#文件加密密码
        parser.add_option("-t", "--type", dest="type", default="all", help="download type 'all' or 'single'")
        (options, args) = parser.parse_args();

        if not options.url:
            parser.error(" need --url");
        
        if not options.output or not Utils.createDir(options.output):
            parser.error(" need --output");

        if not options.parser or len(options.parser) == 0:
            parser.error(" need --parser");

        if not options.storge or len(options.storge) == 0:
            parser.error(" need --storge");

        if not options.type or len(options.type) == 0 or (options.type != "all" and options.type != "single"):
            parser.error(" need --type 'single' or 'all'");

        storgeInstance = eval(options.storge + '("%s")' % (options.output));

        if storgeInstance == None:
            parser.error(" need --storge");

        urlParseResult = urlparse.urlsplit(options.url);
        if not urlParseResult or not Utils.isValidStr(urlParseResult.scheme) or not Utils.isValidStr(urlParseResult.netloc):
            parser.error(" need --rooturl");

        return {
            "url": options.url,
            "output": options.output,
            "charset": options.charset,
            "parser": options.parser,
            "storge": storgeInstance,
            "aescode": options.aescode,
            "type": options.type
        };

    def __init__(self):
        self.onPrepare();

    def createConfig(self):
        Config.shared = Config(**self.__parseOptions());

    def createParser(self):
        #创建parser
        parser = eval(Config.shared.parser + "()");

        if not parser: 
            raise "parser cant init";

        if Config.shared.parseType == "all":
            parser.execute();
        else:
            parser.downloadBook(Config.shared.rootUrl);

    def onPrepare(self):
        self.createConfig();
        # self.test();
        self.createParser()

    def test(self):
        Log.test();


