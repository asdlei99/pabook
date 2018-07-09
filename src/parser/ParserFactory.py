#coding=utf-8

from src.parser import *
from src.utils import Factory, Log

class ParserFactory(Factory):
    shared = None;
    def createInstance(self, name, *args):
        if args != None and len(args) > 0:
            return eval("{}({})".format(name, *args));
        else:
            return eval("{}()".format(name));

ParserFactory.shared = ParserFactory();