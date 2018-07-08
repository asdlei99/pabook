#coding=utf-8

from Storge import Storge
from src.Config import Config
from src.utils import Utils, Log

import boto3

import os

class AWSStorge(Storge):
    def __init__(self, outPath):
        super(AWSStorge, self).__init__(outPath);
        self.bk = Config.shared.awsBK;
        self.filepath = "files";
        self.s3 = boto3.resource("s3");
        self.bucket = s3.Bucket(self.bk);

    def checkFileExists(self, fileuniquekey, toDir, complete):
        outDir = self.filepath;
        if toDir != None:
            outDir = outDir + os.sep + toDir;
        file = outDir + os.sep + fileuniquekey;

        objSummary = None;
        try:
            objSummary = self.s3.ObjectSummary(self.bk, file).get();
        except Exception, e:
            Log.Exc(e);

        if objSummary != None:
            complete(True);
        else:
            complete(False);

    def pushContent(self, content, fileuniquekey, toDir, complete):
        outDir = self.filepath;
        if toDir != None:
            outDir = outDir + os.sep + toDir;
        file = outDir + os.sep + fileuniquekey;
        pushRet = None;
        try:
            pushRet = self.bucket.put_object(Key = file, Body = content);
        except Exception, e:
            Log.Exc(e);

        if pushRet != None:
            complete(True);
        else:
            complete(False);
