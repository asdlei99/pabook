#coding=utf-8

import urlparse

from src.parser import BookId

from src.db.BookinfoDb import BookinfoDb
from src.db.ChapterDb import ChapterDb
from src.db.VisitUrlDb import *
from src.db.KeyValueDb import *

from src.utils import Utils

import os

class Config:
    shared = None;
    #参数检查
    def checkInput(self):
        if not Utils.isValidUrl(self.rootUrl):
            raise Exception("rootUrl is not valid");
        elif not Utils.isValidStr(self.outPath):
            raise Exception("outPath is not valid");
        elif not Utils.isValidStr(self.charset):
            raise Exception("charset is not valid");

    def __init__(self, url, output, charset, parser, type, storge, aescode = None):
        self.rootUrl = url;

        urlParseResult = urlparse.urlsplit(url);
        self.scheme = urlParseResult.scheme;
        self.host = urlParseResult.netloc;

        self.outPath = output;
        self.tmpPath = output + os.sep + ".tmp";
        if not Utils.createDir(self.tmpPath):
            raise Exception("--创建tmpdir失败");
        self.charset = charset;

        self.parser = parser;
        self.parseType = type;

        self.storge = storge;

        self.aescode = aescode;
        self.checkInput();

        self.bookDb = BookinfoDb();
        self.visitUrlDb = VisitUrlDb();
        self.visitBookUrlDb = VisitBookUrlDb();
        self.kvDb = KeyValueDb();

        BookId.init(self.kvDb);

        from src.utils import Log
        Log.setOutPath(output);
