#coding=utf-8

from src.db import *
from src.utils import Factory

class StorgeFactory(Factory):
    shared = None;
    def createInstance(self, name, *args):
        exec("from src.storge.{} import {}".format(name, name));
        if args != None:
            return eval('''{}("{}")'''.format(name, *args));
        else:
            return eval('''{}()'''.format(name));

StorgeFactory.shared = StorgeFactory();