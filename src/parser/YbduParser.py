#coding=utf-8

from Parser import Parser

from src.utils import Utils

from src.model import *

# http://www.ybdu.com
class YbduParser(Parser):
	def bookPageUrls(self, urls):
		pat = r".+?/xiazai/\d+/\d+/?$";
		return filter(lambda url: Utils.isMatch(pat, url) , urls);

	def bookMuluUrl(self, bookPageSoup):
		Utils.log("[D] bookMuluSoup input = None " + str(bookPageSoup == None));
		spans = Utils.findAllClassTag(bookPageSoup, "span", "btopt");
		if len(spans) <= 0 or len(spans[0].contents) <= 0:
			return None;
		span = spans[0];
		a = span.contents[0];
		url = a["href"];
		Utils.log("[D] muluurl = " + str(url));
		return url;

	def ignoreVisitUrl(self, url):
		return url.endswith(".html");

	def _getIntFromTLJTag(self, tag, rep):
		if rep in tag.string:
			s = tag.string.replace(rep, "");
			try:
				i = int(s);
				if i != None:
					return i;
			except Exception as e:
				if s == "连载中":
					return 0;
				elif s == "已完成":
					return 1;
		return None;

	def _checkTLJTag(self, tag, model):
		tljMap = {
			"总点击数：": "clickCount",
			"本月点击：": "monthClickCount",
			"本周点击：": "weekClickCount",
			"收 藏 数：": "collectionCount",
			"总推荐数：": "recommendCount",
			"本月推荐：": "monthRecommendCount",
			"本周推荐：": "weekRecommendCount",
			"文章状态：": "status"
		}

		setted = False;
		for key, value in tljMap.items():
			count = self._getIntFromTLJTag(tag, key);
			if count != None:
				setattr(model, value, count);
				setted = True;
				break;

		if not setted:
			Utils.log("[W] 未完全设置tljtag "+ str(tag));

	def _checkMetaTag(self, tag, model):
		metaMap = {
			"og:novel:category": "category",
			"og:novel:book_name": "title",
			"og:novel:author": "author",
			"og:description": "des",
			"og:novel:update_time": "updateTime",
			"og:image": "bookImg"
		}
		setted = False;
		for key, value in metaMap.items():
			if tag["property"] == key:
				c = tag["content"];
				if value == "updateTime":
					c = Utils.getTimestamp(c, "%Y-%m-%d %H:%M");
				setattr(model, value, c);
				setted = True;
				break;

		if not setted:
			Utils.log("[W] 未完全设置metatag "+ str(tag));

	def bookInfo(self, bookPageSoup, bookMuluSoup):
		Utils.log("[I] on get bookInfo ");
		model = BookInfoModel();
		#检查书页中的tlj标签
		tLJTags = Utils.findAllClassTag(bookPageSoup, "div", "tLJ");
		for tag in tLJTags:
			self._checkTLJTag(tag, model);

		#字数
		find = Utils.findAll(r"已写了(\d+)字", str(bookPageSoup));
		if find and len(find) > 0:
			self.wordsCount = find[0];

		#检查目录页中的数据
		metaTags = bookMuluSoup.find_all(lambda t: t.name == "meta" and t.has_attr("property") and Utils.isMatch("og:.+?\"", t["property"]) != None);
		for tag in metaTags:
			self._checkMetaTag(tag, model);

		return model;

	def sectionInfo(self, bookInfo, muluUrl, bookMuluSoup):
		Utils.log("[I] on get sectionInfo");
		model = SectionInfoModel();
		model.bookInfo = bookInfo;

		muluList = bookMuluSoup.find(lambda tag: tag.name == "ul" and tag.has_attr("class") and tag["class"][0] == "mulu_list");
		if muluList == None or muluList.contents == None or len(muluList.contents) <= 0:
			return None;

		setted = False;
		for c in muluList.contents:
			atag = c.find("a");
			if atag != -1:
				href = Utils.absoluteUrl(atag["href"], muluUrl, None) ;
				title = atag.string;
				model.addChapter(href, title);
				setted = True;

		if not setted:
			return None;

		return model;

	def bookCategory(self, categoryStr):
		return super.bookCategory(categoryStr);

	def chapterContent(self, chapterSoup):
		tag = chapterSoup.find(id = "htmlContent");
		if tag == None:
			return None;

		content = "";	
		for c in tag.contents:
			if Utils.isSoupStr(c):
				part = c;
				part = part.strip();
				if "全本小说" in part:
					Utils.log("[W] ignore line " + str(part));
					continue;
				if len(part) > 0:
					content += part + "\n";
		return content;
