#coding=utf-8

import time

from src.utils import *

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

class _Log:
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
            self.verboseDir = self.outPath + os.sep + "logs" + os.sep + "verbose"
            Utils.createDir(self.verboseDir);
        else:
            self.infoDir = None;
            self.errorDir = None;
            self.debugDir = None;
            self.warnDir = None;
            self.verboseDir = None;

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

    def _logEnabled(self, tag):
        from Config import Config
        if Config.shared.logLevel == None:
            return False;
        return tag in Config.shared.logLevel;

    def I(self, msg):
        filePath = None;
        if self.infoDir != None:
            filePath = self.infoDir + os.sep + "log-info-" + logFileSuffix(self.logInterval)
        self._log(msg, "[I]", self._logEnabled("I"), True, filePath);

    def Exc(self, e):
        self.E(str(traceback.format_exc()));

    def E(self, msg):
        filePath = None;
        if self.errorDir != None:
            filePath = self.errorDir + os.sep + "log-error-" + logFileSuffix(self.logInterval)
        self._log(msg, "[E]", self._logEnabled("E"), True, filePath);

    def D(self, msg):
        filePath = None;
        if self.debugDir != None:
            filePath = self.debugDir + os.sep + "log-debug-" + logFileSuffix(self.logInterval)
        self._log(msg, "[D]", self._logEnabled("D"), True, filePath);

    def W(self, msg):
        filePath = None;
        if self.warnDir != None:
            filePath = self.warnDir + os.sep + "log-warn-" + logFileSuffix(self.logInterval)
        self._log(msg, "[D]", self._logEnabled("W"), True, filePath);

    def V(self, msg):
        filePath = None;
        if self.verboseDir != None:
            filePath = self.verboseDir + os.sep + "log-verbose-" + logFileSuffix(self.logInterval)
        self._log(msg, "[V]", True, True, filePath);

Log = _Log();

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
                Log.I("删除文件 " + file + " 修改时间：" + timeFormat(timestamp), toConsole = True, toFile = False);
                count += 1;
            else:
                Log.I("保留文件 " + file + " 修改时间：" + timeFormat(timestamp), toConsole = True, toFile = False);
    Log.I("完成：发现log文件 " + str(totalCount) + "个，过期删除文件 "+ str(count) + "个");

def test():
    Log.I("hello world", True, True);
    Log.E("hello world", True, True);
    Log.D("hello world", True, True);
    Log.W("hello world", True, True);
    try:
        raise Exception("this is test Exception")
    except Exception, e:
        Log.Exc(e, True, True);
    Log.I("finally code", True, True);
