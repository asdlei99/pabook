#coding=utf-8

from src.utils import Utils
import os, sys

import re

import BookCategories

import urlparse

from src.model import *

from src.db.BookinfoDb import BookinfoDb

from src.utils.Aes import Aes

class Parser:

	#参数检查
	def checkInput(self):
		if not Utils.isValidUrl(self.rootUrl):
			raise Exception("rootUrl is not valid");
		elif not Utils.isValidStr(self.outPath):
			raise Exception("outPath is not valid");
		elif not Utils.isValidStr(self.charset):
			raise Exception("charset is not valid");

	#构造函数
	def __init__(self, rootUrl, outPath, charset, aescode):
		self.rootUrl = rootUrl;

		urlParseResult = urlparse.urlsplit(rootUrl);
		self.scheme = urlParseResult.scheme;
		self.host = urlParseResult.netloc;

		self.outPath = outPath;
		self.tmpPath = outPath + os.sep + ".tmp";
		if not Utils.createDir(self.tmpPath):
			raise Exception("--创建tmpdir失败");
		self.charset = charset;
		Utils.charset = charset;
		self.aescode = aescode;
		self.checkInput();

		self.sectionDownloadSuccCount = 0;
		self.sectionDownloadFailedCount = 0;

		self.bookDb = BookinfoDb();

		Utils.log("[I] Parser.inited");

	#析构函数
	def __del__(self):
		Utils.log("[I] Parser dealloc");

	#测试
	def test(self):
		pat = r".+?/xiazai/\d+/\d+/?$";
		Utils.log(re.compile(pat).match("https://www.ybdu.com/xiazai/15/15360/"));
		sys.exit(1);

	#入口函数
	def execute(self):
		# self.test();
		#如果在数据库中能找到visitUrl，说明程序已经运行过了，可以从数据库中恢复现场
		Utils.log("[I] onExecute()");

		#检查是否有visiting的book
		visitingBookUrl = self.visitingBookUrl();
		if visitingBookUrl != None:
			self.downloadBook(visitingBookUrl);

		#否则从root开始搜索
		visitUrl = self.nextVisitUrl();
		if visitUrl == None:
			self.visit(self.rootUrl);
		else:
			self.visit(visitUrl);

		Utils.log("[I] willVisitNext");
		#处理下一个
		while True:
			visitUrl = self.nextVisitUrl();
			if visitUrl != None:
				self.visit(visitUrl);
			else:
				break;

		Utils.log("[I] willVisitNextPageUrl");
		#网页遍历完成
		while True:
			bookUrl = self.nextPageUrl();
			if bookUrl != None:
				self.downloadBook(bookUrl);
			else:
				break;
		Utils.log("------parse finished------");

	#开始搜索某个url
	#将url页内包含的所有url都记录下来
	#将url页内包含所有的书页都记录并下载下来
	def visit(self, url):
		Utils.log("[I] on visit() " + str(url));
		soup = Utils.soupUrl(url);
		if not soup:
			Utils.log("[W] on visit() soup is None " + str(url));
			return;
		Utils.log("[I] on visit() did get soup");
		#将本页所有url放入数据库中
		urls = self.addUrlsFromSoup(soup, url);
		if not Utils.isValidArr(urls):
			Utils.log("[W] on visit() urls not found");
			return;
		#获取匹配的书页
		bookUrls = self.addBookPageUrls(urls);
		#遍历书页
		if len(bookUrls) > 0:
			for bookUrl in bookUrls:
				self.downloadBook(bookUrl);

		Utils.log("[I] on visit() finished " + str(url));

	#下载book信息
	def downloadBook(self, url):
		Utils.log("[I] on downloadBook() " + str(url));
		if not self.isValidBookUrl(url):
			Utils.log("[W] downloadBook() is not valid " + str(url));
			return;

		#检查是否下载过了
		if self.checkDownloadedBookUrl():
			return;

		Utils.log("[I] on downloadBook() will get soup " + url);
		bookSoup = Utils.soupUrl(url);
		Utils.log("[I] on downloadBook() did get soup (%s) %s " % (str(bookSoup != None), str(url)));
		if bookSoup != None:
			Utils.log("[I] on downloadBook() will get muluSoup");
			muluUrl = self.bookMuluUrl(bookSoup);
			muluSoup = Utils.soupUrl(muluUrl);
			Utils.log("[I] on downloadBook() did get muluSoup %s" % (str(muluSoup != None)));
			if muluSoup != None:
				bookInfo = self.bookInfo(bookSoup, muluSoup);
				Utils.log("[I] on downloadBook get bookInfo " + str(bookInfo));
				if bookInfo != None:
					bookInfo.setUniqueKey();
					bookInfo.downBookUrl = url;
					bookInfo.downMuluUrl = muluUrl;

					#下载bookImg
					self.downloadBookImg(bookInfo.bookImg, bookInfo.uniqueKey);

					#获取章节信息
					sectionInfo = self.sectionInfo(bookInfo, muluUrl, muluSoup);
					if sectionInfo != None:

						#最新章节
						bookInfo.chapterCount = len(sectionInfo.chapters);

						self.downloadSection(sectionInfo);
					else:
						bookInfo.status = BookInfoStatus.Error;

		Utils.log("------暂时退出------");
		sys.exit(0);

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
		Utils.log("[I] dowlonad bookImg " + url);
		uniqueKey = Utils.md5str(url);
		self.storge.checkFileExists(uniqueKey, toDir, lambda exists, fileurl: not exists and self._downloadBookImg(url, uniqueKey, toDir))

	#下载章节
	def onDownloadSectionCompleted(self, idx, succ, fileurl):
		Utils.log("[I] download section(%s) completed succ(%s) file(%s)" % (str(idx), str(succ), str(fileurl)));
		if idx == 1715 and succ:
			raise Exception("xxx");
		if succ:
			self.sectionDownloadSuccCount += 1;
		else:
			self.sectionDownloadFailedCount += 1;

	def _downloadOneSection(self, idx, url, uniqueKey, toDir):
		contentSoup = Utils.soupUrl(url);
		if contentSoup == None:
			self.onDownloadSectionCompleted(idx, False, None);
			return;

		content = self.chapterContent(contentSoup);
		if content == None:
			self.onDownloadSectionCompleted(idx, False, None);
			return;

		self.pushContent(content, uniqueKey, toDir, lambda succ, fileurl: self.onDownloadSectionCompleted(idx, succ, fileurl));

	def downloadOneSection(self, idx, oneSectionModel, toDir):
		Utils.log("[I] downloading section(%s) (%s) (%s)" % (str(idx), str(oneSectionModel.title), str(oneSectionModel.downUrl)));
		uniqueKey = oneSectionModel.uniqueKey;
		url = oneSectionModel.downUrl;
		self.storge.checkFileExists(oneSectionModel.uniqueKey, toDir, lambda exists, fileurl: not exists and (self._downloadOneSection(idx, url, uniqueKey, toDir) or True) or self.onDownloadSectionCompleted(idx, True, fileurl));

	def downloadSection(self, sectionInfo):
		sectionCount = len(sectionInfo.chapters);
		Utils.log("[I] on downloadSection() enter will download section count %s" % (str(sectionCount)));
		self.sectionDownloadSuccCount = 0;
		self.sectionDownloadFailedCount = 0;
		toDir = sectionInfo.bookInfo.uniqueKey;
		for i in range(0, sectionCount):
			self.downloadOneSection(i, sectionInfo.chapters[i], toDir);

		Utils.log("[I] on downloadSection() exit download all section(%s) succ section(%s) failed section(%s)" % (str(sectionCount), str(self.sectionDownloadSuccCount), str(self.sectionDownloadFailedCount)));

	'''
	===========================================
	下面方法需要数据库操作
	'''
	#从数据库中找到一条searchUrl
	def nextVisitUrl(self):
		return None;

	def visitingBookUrl(self):
		return None;

	def checkDownloadedBookUrl(self):
		return False;

	#从数据库中找到一条书页
	def nextPageUrl(self):
		#TODO 从数据库中获取一条url
		return None;

	def addUrlsFromSoup(self, soup, curUrl):
		if not soup:
			return None;
		urls = [];
		for tag in soup.find_all("a"):
			url = Utils.absoluteUrl(tag["href"], curUrl, self.rootUrl);
			if url != None and url not in urls:
				urls.append(url);

		urls = filter(lambda url: self.isValidVisitUrl(url), urls);
		#TODO 从soup中获取合法url，放入数据库中，检查数据库中是否存在

		return urls;

	def addBookPageUrls(self, urls):
		if not urls or len(urls) == 0:
			return None;
		urls = self.bookPageUrls(urls);
		#TODO 将urls添加到数据库
		return urls;

	def isValidVisitUrl(self, url):
		valid = self.host in url and not self.ignoreVisitUrl(url);
		valid = valid;
		#TODO 检查是否数据库中已经存在
		return valid;

	def isValidBookUrl(self, url):
		#TODO 检查是否数据库中已经处理过
		return True;

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

