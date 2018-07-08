#coding=utf-8

import time

from src.utils import Utils

import traceback

import sys, os

#当前时间戳
def currTimestamp():
    return int(time.time());

#格式化
def _timeFormat(timestamp, format):
    return time.strftime(format, time.localtime(timestamp));

#适合阅读的
def prettyTimeFormat(timestamp):
    return _timeFormat(timestamp, "[%Y-%m-%d %H:%M:%S]");

#时间格式化
def timeFormat(timestamp):
    return _timeFormat(timestamp, "%Y%m%d%H%M%S");

#时间戳格式化201807030923
def currPrettyTimeFormat():
    return prettyTimeFormat(currTimestamp());

class _redirection:
    def __init__(self):
        self.buff = "";
        self.stdout = sys.stdout;
        sys.stdout = self;

    def write(self, output):
        self.buff += output;

    def toConsole(self):
        self.stdout.write(self.buff);

    def toFile(self, filepath):
        file = open(filepath, "a");
        file.write(self.buff);
        file.flush();
        file.close();

    def clean(self):
        self.buff = "";

logRedirect = _redirection();

def logFileSuffix(logInterval):
    s = currTimestamp();
    return timeFormat(s - s % logInterval) + ".txt";

class Log:
    def __init__(self, outpath = None, logInterval = 3600):
        self.logInterval = logInterval;
        self.setOutPath(outpath);

    def setOutPath(self, path):
        if path != None:
            self.outPath = path;
            self.infoDir = self.outPath + os.sep + "logs" + os.sep + "info";
            Utils.createDir(self.infoDir);
            self.errorDir = self.outPath + os.sep + "logs" + os.sep + "error";
            Utils.createDir(self.errorDir);
            self.debugDir = self.outPath + os.sep + "logs" + os.sep + "debug";
            Utils.createDir(self.debugDir);
            self.warnDir = self.outPath + os.sep + "logs" + os.sep + "warn";
            Utils.createDir(self.warnDir);
        else:
            self.infoDir = None;
            self.errorDir = None;
            self.debugDir = None;
            self.warnDir = None;

    def errorLogFileName(self):
        return currErrorFileName(self.logInterval);

    def infoLogFileName(self):
        return currInfoFileName(self.logInterval);

    def _log(self, msg, prefixStr, toConsole, toFile, filePath):
        print(prefixStr + currPrettyTimeFormat() + " - " + msg);
        if toConsole:
            logRedirect.toConsole()
        if toFile and filePath != None:
            logRedirect.toFile(filePath);
        logRedirect.clean();

    def I(self, msg, toConsole = False, toFile = True):
        filePath = None;
        if toFile and self.infoDir != None:
            filePath = self.infoDir + os.sep + "log-info-" + logFileSuffix(self.logInterval)
        self._log(msg, "[I]", toConsole, toFile, filePath);

    def Exc(self, e, toConsole = False, toFile = True):
        msg = str(traceback.format_exc());
        self.E(msg, toConsole, toFile);

    def E(self, msg, toConsole = False, toFile = True):
        filePath = None;
        if toFile and self.errorDir != None:
            filePath = self.errorDir + os.sep + "log-error-" + logFileSuffix(self.logInterval)
        self._log(msg, "[E]", toConsole, toFile, filePath);

    def D(self, msg, toConsole = False, toFile = True):
        filePath = None;
        if toFile and self.debugDir != None:
            filePath = self.debugDir + os.sep + "log-debug-" + logFileSuffix(self.logInterval)
        self._log(msg, "[D]", toConsole, toFile, filePath);

    def W(self, msg, toConsole = False, toFile = True):
        filePath = None;
        if toFile and self.warnDir != None:
            filePath = self.warnDir + os.sep + "log-warn-" + logFileSuffix(self.logInterval)
        self._log(msg, "[D]", toConsole, toFile, filePath);

shared = Log();

def setOutPath(outPath):
    shared.setOutPath(outPath);

def I(msg, toConsole = False, toFile = True):
    shared.I(msg, toConsole, toFile);

def E(msg, toConsole = True, toFile = True):
    shared.E(msg, toConsole, toFile);

def Exc(e, toConsole = True, toFile = True):
    shared.Exc(e, toConsole, toFile);

def D(msg, toConsole = True, toFile = True):
    shared.D(msg, toConsole, toFile);

def W(msg, toConsole = False, toFile = True):
    shared.W(msg, toConsole, toFile);

#检查删除log文件
def checkLogEntired(dir, saveDuration = 3600 * 24 * 3):
    totalCount = 0;
    count = 0;
    for root, dirs, files in os.walk(dir):
        for name in files:
            file = os.path.join(root, name);
            totalCount += 1;
            timestamp = os.path.getmtime(file);
            if currTimestamp() - timestamp > saveDuration:
                os.path.remove(file);
                I("删除文件 " + file + " 修改时间：" + timeFormat(timestamp), toConsole = True, toFile = False);
                count += 1;
            else:
                I("保留文件 " + file + " 修改时间：" + timeFormat(timestamp), toConsole = True, toFile = False);
    I("完成：发现log文件 " + str(totalCount) + "个，过期删除文件 "+ str(count) + "个");

def test():
    I("hello world", True, True);
    E("hello world", True, True);
    D("hello world", True, True);
    W("hello world", True, True);
    try:
        raise Exception("this is test Exception")
    except Exception, e:
        Exc(e, True, True);
    I("finally code", True, True);
