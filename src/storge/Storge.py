#coding=utf-8

from src.utils import Utils

import os

from src.utils import Log

class Storge(object):
    def __init__(self, outPath = None):
        Log.D("[I] Storge inited");
        self.outPath = outPath;

    def pushFile(self, filepath, fileuniquekey, toDir, complete):
        content = Utils.readFile(filepath);
        self.pushContent(self, content, fileuniquekey, toDir, complete);

    def pushContent(self, content, fileuniquekey, toDir, complete):
        raise Exception("子类实现");

    def checkFileExists(self, fileuniquekey, toDir, complete):
        raise Exception("子类实现");
