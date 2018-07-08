#coding=utf-8

from src.db import *
from src.utils import Factory
from src.utils import Log

class DbFactory(Factory):
    shared = None;
    def createInstance(self, name, *args):
        Log.D(" ----- test name = " + str(name) + ", args = " + str(args));
        if args != None and len(args) > 0:
            return eval("{}({})".format(name, *args));
        else:
            return eval("{}()".format(name));

DbFactory.shared = DbFactory();