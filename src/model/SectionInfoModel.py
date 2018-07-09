#coding=utf-8

from src.utils import Utils

from ChapterModel import ChapterModel

class SectionInfoModel:
    def __init__(self):
        self.chapters = [];
        self.bookInfo = None;

    def addChapter(self, url, title):
        key = Utils.md5str(self.bookInfo.uniqueKey + str(len(self.chapters)) + title + url);
        self.chapters.append(ChapterModel(url, title, key));

    def getChapter(self, index):
        return self.chapters[index];