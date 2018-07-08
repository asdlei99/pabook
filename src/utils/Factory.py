#coding=utf-8

class Factory:
    def __init__(self):
        self.map = {}

    def createInstance(self, name, *args):
        raise Exception("子类实现");

    def get(self, name, *args):
        instance = None;
        if self.map.has_key(name):
            instance = self.map[name];
        else:
            instance = self.createInstance(name, *args);
            self.map[name] = instance;
        return instance;