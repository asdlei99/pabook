#coding=utf-8

from src.utils import Utils

class ChapterModel:
    def __init__(self, url = None, title = None, uniqueKey = None):
        self.downUrl = url;
        self.title = title;
        self.uniqueKey = uniqueKey;
        self.downloaded = -1;

    def applyDict(self, d):
        attrnames = dir(self);
        for key, value in d.items():
            if key in attrnames:
                setattr(self, key, value);