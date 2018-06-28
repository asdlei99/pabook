#coding=utf-8

from src.model import *

class BookInfoModel:
	def __init__(self):
		self.clickCount = -1;#点击数
		self.monthClickCount = -1;#月点击数
		self.weekClickCount = -1;#周点击数
		self.collectionCount = -1;#收藏数
		self.recommendCount = -1;#推荐数
		self.monthRecommendCount = -1;#月推荐数
		self.weekRecommendCount = -1;#周推荐数
		self.status = BookInfoStatus.Completed;#状态

		self.wordsCount = -1;#字数
		self.category = "";#分类名称
		self.title = "";#书名
		self.author = "";#作者
		self.des = "";#简介
		self.updateTime = -1;#更新时间
		self.chapterCount = -1;#最新章节
		self.bookImg = "";#图片

		self.downBookUrl = "";
		self.downMuluUrl = "";
		self.uniqueKey = "";

	def setUniqueKey(self):
		self.uniqueKey = Utils.md5str(self.category + self.title + self.author);

	def toDict(self, ignoreEmptyStr):
		attrnames = dir(self);
		d = {};
		for n in attrnames:
			if not n.startswith("_") and n != "toDict" and n != "setUniqueKey":
				v = getattr(self, n);
				if isinstance(v, str):
					if not ignoreEmptyStr or len(v) > 0:
						d[n] = v;
				else:
					d[n] = v;
		return d;

	def __str__(self):
		return str(self.toDict(False));

class ChapterModel:
	def __init__(self, url, title, uniqueKey):
		self.downUrl = url;
		self.title = title;
		self.uniqueKey = uniqueKey;

class SectionInfoModel:
	def __init__(self):
		self.chapters = [];
		self.bookInfo = None;

	def addChapter(self, url, title):
		key = Utils.md5str(self.bookInfo.uniqueKey + str(len(self.chapters)) + title + url);
		self.chapters.append(ChapterModel(url, title, key));

	def getChapter(self, index):
		return self.chapters[index];