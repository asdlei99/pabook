#coding=utf-8

from Storge import Storge
from src.Config import Config
from src.Options import Options
from src.utils import Utils, Log

from qiniu import Auth, put_file, BucketManager

import os

class QiniuStorge(Storge):
    def __init__(self, outPath):
        super(QiniuStorge, self).__init__(outPath);
        self.ak = Config.shared.qnAK;
        if not Utils.isValidStr(self.ak):
            raise Exception("七牛云AK未添加，请在Config.py中设置");
        self.sk = Config.shared.qnSK;
        if not Utils.isValidStr(self.sk):
            raise Exception("七牛云SK未添加，请在Config.py中设置");
        self.bk = Config.shared.qnBK;
        if not Utils.isValidStr(self.bk):
            raise Exception("七牛云buckname未添加，请在Config.py中设置");
        self.qn = Auth(self.ak, self.sk);
        self.bkManager = BucketManager(self.qn);

        self.filepath = "files"

    def checkFileExists(self, fileuniquekey, toDir, complete):
        outDir = self.filepath;
        if toDir != None:
            outDir = outDir + os.sep + toDir;
        file = outDir + os.sep + fileuniquekey;

        ret = None;
        try:
            ret, resp = self.bkManager.stat(self.bk, file);
        except Exception, e:
            Log.Exc(e);

        if complete != None:
            if ret != None:
                complete(True);
            else:
                complete(False);

    def pushContent(self, content, fileuniquekey, toDir, complete):
        outDir = self.filepath;
        if toDir != None:
            outDir = outDir + os.sep + toDir;
        file = outDir + os.sep + fileuniquekey;

        ret = None;
        tmpFile = None;
        try:
            tmpFile = Options.shared.tmpPath + os.sep + (toDir != None and str(toDir) + "-" or "") + fileuniquekey;
            tmpFileFd = open(tmpFile, "w");
            tmpFileFd.write(content);
            tmpFileFd.flush();
            tmpFileFd.close();
            token = self.qn.upload_token(self.bk, file, 3600);
            ret, info = put_file(token, file, tmpFile)
        except Exception, e:
            Log.Exc(e);
        try:
            if tmpFile != None:
                os.remove(tmpFile);
        except Exception, e:
            Log.Exc(e);

        if complete != None:
            if ret != None:
                complete(True);
            else:
                complete(False);