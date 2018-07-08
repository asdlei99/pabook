#coding=utf-8

from src.utils import Utils
import os, sys

import re

import BookCategories

import urlparse

from src.model import *

from src.db.BookinfoDb import BookinfoDb
from src.db.ChapterDb import ChapterDb
from src.db.VisitUrlDb import *
from src.db.KeyValueDb import *

from src.utils.Aes import Aes

import BookId

from src.Options import Options

from src.utils import Log

class Parser:

    #构造函数
    def __init__(self):
        cfg = Options.shared;

        self.rootUrl = cfg.rootUrl;

        self.scheme = cfg.scheme;
        self.host = cfg.host;

        self.outPath = cfg.outPath;
        self.tmpPath = cfg.tmpPath;
        self.charset = cfg.charset;
        self.aescode = cfg.aescode;

        self.sectionDownloadSuccCount = 0;
        self.sectionDownloadFailedCount = 0;

        self.bookDb = cfg.bookDb;
        self.visitUrlDb = cfg.visitUrlDb;
        self.visitBookUrlDb = cfg.visitBookUrlDb;
        self.kvDb = cfg.kvDb;

        self.storge = cfg.storge;

        Log.D("[I] Parser.inited");

    #析构函数
    def __del__(self):
        Log.D("[I] Parser dealloc");

    #测试
    def test(self):
        pat = r".+?/xiazai/\d+/\d+/?$";
        Log.D(re.compile(pat).match("https://www.ybdu.com/xiazai/15/15360/"));
        sys.exit(1);

    #入口函数
    def execute(self):
        # self.test();
        #如果在数据库中能找到visitUrl，说明程序已经运行过了，可以从数据库中恢复现场
        Log.I("[I] onExecute()");

        #检查是否有visiting的book
        visitingBookUrl = self.visitingBookUrl();
        if visitingBookUrl != None:
            self.downloadBook(visitingBookUrl);

        #检查是否有visiting的url
        visitingUrl = self.visitingUrl();
        if visitingUrl != None:
            self.visit(visitUrl);

        #否则从root开始搜索
        visitUrl = self.nextVisitUrl();
        self.visit(visitUrl);

        Log.I("[I] willVisitNext");
        #处理下一个
        while True:
            visitUrl = self.nextVisitUrl();
            if visitUrl != None:
                self.visit(visitUrl);
            else:
                break;

        Log.I("[I] willVisitNextPageUrl");
        #网页遍历完成
        while True:
            bookUrl = self.nextPageUrl();
            if bookUrl != None:
                self.downloadBook(bookUrl);
            else:
                break;
        Log.I("------parse finished------");

    #开始搜索某个url
    #将url页内包含的所有url都记录下来
    #将url页内包含所有的书页都记录并下载下来
    def visit(self, url):
        Log.I("[I] on visit() " + str(url));
        self.setVisitingUrl(url);
        soup = Utils.soupUrl(url);
        if not soup:
            Log.W("[W] on visit() soup is None " + str(url));
            return;
        Log.I("[I] on visit() did get soup");
        #将本页所有url放入数据库中
        urls = self.addUrlsFromSoup(soup, url);
        if not Utils.isValidArr(urls):
            Log.W("[W] on visit() urls not found");
            return;
        #获取匹配的书页
        bookUrls = self.addBookPageUrls(urls);
        #遍历书页
        if len(bookUrls) > 0:
            for bookUrl in bookUrls:
                self.downloadBook(bookUrl);

        self.removeVisitUrl(url);

        Log.I("[I] on visit() finished " + str(url));


    #下载book信息
    def downloadBook(self, url):
        Log.I("[I] on downloadBook() " + str(url));

        #检查是否下载过了
        if self.checkDownloadedBookUrl(url):
            return;

        #设置visiting
        self.setVisitingBookUrl(url)

        #尝试获取bookInfo
        bookInfo = self.getBookinfo(url);
        sectionInfo = None;
        existsBookId = None;
        if bookInfo != None:
            existsBookId = bookInfo.bookId;
            sectionInfo = self.getChapter(bookInfo.bookId);
            if sectionInfo == None or sectionInfo.chapters == None or len(sectionInfo.chapters) == 0:
                sectionInfo = None;
                bookInfo = None;
            else:
                sectionInfo.bookInfo = bookInfo;

        if bookInfo == None :
            Log.I("[I] on downloadBook() will get soup " + url);
            bookSoup = Utils.soupUrl(url);
            Log.I("[I] on downloadBook() did get soup (%s) %s " % (str(bookSoup != None), str(url)));
            if bookSoup != None:
                Log.I("[I] on downloadBook() will get muluSoup");
                muluUrl = self.bookMuluUrl(bookSoup);
                muluSoup = Utils.soupUrl(muluUrl);
                Log.I("[I] on downloadBook() did get muluSoup %s" % (str(muluSoup != None)));
                if muluSoup != None:
                    bookInfo = self.bookInfo(bookSoup, muluSoup);
                    Log.I("[I] on downloadBook get bookInfo " + str(bookInfo));
                    if bookInfo != None:
                        bookInfo.setUniqueKey();
                        bookInfo.downBookUrl = url;
                        bookInfo.downMuluUrl = muluUrl;

                        #bookId
                        if existsBookId == None:
                            bookInfo.bookId = BookId.nextBookId();
                        else:
                            bookInfo.bookId = existsBookId;

                        #获取章节信息
                        sectionInfo = self.sectionInfo(bookInfo, muluUrl, muluSoup);
                        if sectionInfo != None:
                            #最新章节
                            bookInfo.chapterCount = len(sectionInfo.chapters);
                        else:
                            bookInfo.status = BookInfoStatus.Error;
                            bookInfo.downloadStatus = BookDownloadStatus.Completed;
                        #保存bookInfo
                        self.saveBookinfo(bookInfo);
                        self.saveChapter(bookInfo.bookId, sectionInfo);

        #下载bookImg
        self.downloadBookImg(bookInfo.bookImg, bookInfo.uniqueKey);
        if sectionInfo != None:
            self.downloadSection(sectionInfo);
            self.setDownloadedForBookUrl(url)
        self.chapterDb = None;

        #移除visiting book url
        self.removeBookUrl(url);

    #下载封面
    def pushContent(self, content, fileuniquekey, toDir, complete):
        c = content;
        if Utils.isValidStr(self.aescode):
            c = Aes.encode(c, self.aescode, fileuniquekey);
        self.storge.pushContent(c, fileuniquekey, toDir, complete);

    def _downloadBookImg(self, url, uniqueKey, toDir):
        content = Utils.readUrl(url);
        if content == None:
            return;
        self.pushContent(content, uniqueKey, toDir, None);

    def downloadBookImg(self, url, toDir):
        Log.I("[I] dowlonad bookImg " + url);
        uniqueKey = Utils.md5str(url);
        self.storge.checkFileExists(uniqueKey, toDir, lambda exists: not exists and self._downloadBookImg(url, uniqueKey, toDir))

    #下载章节
    def onDownloadSectionCompleted(self, idx, uniqueKey, succ):
        Log.I("[I] download section(%s) completed succ(%s)" % (str(idx), str(succ)));
        if succ:
            self.sectionDownloadSuccCount += 1;
            self.chapterDb.setDownloaded(uniqueKey, 1);
        else:
            self.sectionDownloadFailedCount += 1;
            self.chapterDb.setDownloaded(uniqueKey, 2);

    def _downloadOneSection(self, idx, url, uniqueKey, toDir):
        contentSoup = Utils.soupUrl(url);
        if contentSoup == None:
            self.onDownloadSectionCompleted(idx, uniqueKey, False);
            return;

        content = self.chapterContent(contentSoup);
        if content == None:
            self.onDownloadSectionCompleted(idx, uniqueKey, False);
            return;

        self.pushContent(content, uniqueKey, toDir, lambda succ: self.onDownloadSectionCompleted(idx, uniqueKey, succ));

    def downloadOneSection(self, idx, oneSectionModel, toDir):
        Log.I("[I] downloading section(%s) (%s) (%s)" % (str(idx), str(oneSectionModel.title), str(oneSectionModel.downUrl)));
        uniqueKey = oneSectionModel.uniqueKey;
        url = oneSectionModel.downUrl;
        self.storge.checkFileExists(oneSectionModel.uniqueKey, toDir, lambda exists: not exists and (self._downloadOneSection(idx, url, uniqueKey, toDir) or True) or self.onDownloadSectionCompleted(idx, uniqueKey, True));

    def downloadSection(self, sectionInfo):
        sectionCount = len(sectionInfo.chapters);
        Log.I("[I] on downloadSection() enter will download section count %s" % (str(sectionCount)));
        self.sectionDownloadSuccCount = 0;
        self.sectionDownloadFailedCount = 0;
        toDir = sectionInfo.bookInfo.uniqueKey;
        for i in range(0, sectionCount):
            self.downloadOneSection(i, sectionInfo.chapters[i], toDir);

        Log.I("[I] on downloadSection() exit download all section(%s) succ section(%s) failed section(%s)" % (str(sectionCount), str(self.sectionDownloadSuccCount), str(self.sectionDownloadFailedCount)));

    '''
    ===========================================
    下面方法需要数据库操作
    '''
    #从数据库中找到一条searchUrl
    def nextVisitUrl(self):
        url = self.visitUrlDb.getOneUrl();
        if url == None:
            self.visitUrlDb.insertUrl(self.rootUrl);
            return self.rootUrl;
        return url;

    def visitingUrl(self):
        return self.kvDb.get("lastVisitingUrl");

    def setVisitingUrl(self, url):
        return self.kvDb.get("lastVisitingUrl");

    #获取正在下载的书
    def visitingBookUrl(self):
        return self.kvDb.get("lastBookUrl");

    #设置正在访问的url
    def setVisitingBookUrl(self, bookUrl):
        return self.kvDb.set("lastBookUrl", bookUrl);

    #是否已经下载完成
    def checkDownloadedBookUrl(self, downBookUrl):
        return self.bookDb.isAlreadyDownloadWithBookUrl(downBookUrl);

    #保存bookinfo
    def saveBookinfo(self, bookInfo):
        if self.bookDb.isExistsWithKey(bookInfo.uniqueKey):
            self.bookDb.update(bookInfo);
        else:
            self.bookDb.insert(bookInfo);

    #根据downBookUrl获取bookinfo
    def getBookinfo(self, downBookUrl):
        return self.bookDb.getBookinfo(downBookUrl);

    #保存章节
    def saveChapter(self, bookId, sectionInfo):
        self.chapterDb = ChapterDb(bookId);
        return self.chapterDb.setSectionInfoModel(sectionInfo);

    def getChapter(self, bookId):
        self.chapterDb = ChapterDb(bookId);
        return self.chapterDb.getSectionInfoModel();



    #设置某本书的下载状态
    def setDownloadedForBookUrl(self, bookUrl):
        self.bookDb.setDownloadStautsForBookUrl(BookDownloadStatus.Completed, bookUrl)

    #从数据库中找到一条书页
    def nextPageUrl(self):
        return self.visitBookUrlDb.getOneUrl();

    def addUrlsFromSoup(self, soup, curUrl):
        if not soup:
            return None;
        urls = [];
        for tag in soup.find_all("a"):
            url = Utils.absoluteUrl(tag["href"], curUrl, self.rootUrl);
            if url != None and url not in urls:
                urls.append(url);

        urls = filter(lambda url: self.isValidVisitUrl(url), urls);

        for url in urls:
            self.visitUrlDb.insertUrl(url);

        return urls;

    def removeVisitUrl(self, url):
        self.visitUrlDb.setVisited(url);

    def addBookPageUrls(self, urls):
        if not urls or len(urls) == 0:
            return None;
        urls = self.bookPageUrls(urls);

        for url in urls:
            self.visitBookUrlDb.insertUrl(url);

        return urls;

    def removeBookUrl(self, url):
        self.visitBookUrlDb.setVisited(url);

    def isValidVisitUrl(self, url):
        valid = self.host in url and not self.ignoreVisitUrl(url);
        valid = valid and not self.visitUrlDb.isExistsUrl(url);
        return valid;

    '''
    ===============================================
    下面是子类需要实现的方法
    '''
    #从一堆url中获取符合书页格式的url
    def bookPageUrls(self, urls):
        raise Exception("子类实现");

    #获取目录soup
    def bookMuluUrl(self, bookPageSoup):
        raise Exception("子类实现");

    #获取book信息
    def bookInfo(self, bookPageSoup, bookMuluSoup):
        raise Exception("子类实现");
    
    #忽略访问的url
    def ignoreVisitUrl(self, url):
        raise Exception("子类实现");

    def sectionInfo(self, bookInfo, muluUrl, bookMuluSoup):
        raise Exception("子类实现");

    def bookCategory(self, categoryStr):
        raise Exception("子类实现");

    def chapterContent(self, chapterSoup):
        raise Exception("子类实现");

