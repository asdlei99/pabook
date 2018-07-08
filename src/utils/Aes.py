#coding=utf-8

from Crypto.Cipher import AES
from src.utils import Utils
from src.utils import Log

class Aes:
    @classmethod
    def aeskey(cls, aescode, uniqueKey):
        key = Utils.md5str(aescode + uniqueKey);
        Log.D(" md5 key = " + str(key));
        return key;

    @classmethod
    def alignContent(cls, content):
        l = len(content);
        padding = 16 - l % 16;
        content += hex(padding)[-1:] * padding;
        return content;

    @classmethod
    def dealignContent(cls, content):
        last = content[-1:];
        padding = int(last, 16);
        return content[:-padding];

    @classmethod
    def encode(cls, content, aescode, uniqueKey, needEncode = True):
        obj = AES.new(cls.aeskey(aescode, uniqueKey), AES.MODE_ECB);
        c = content;
        if needEncode:
            c = c.encode("utf-8");
        c = cls.alignContent(c);
        e = obj.encrypt(c);
        return e;

    @classmethod
    def decode(cls, content, aescode, uniqueKey, needDecode = True):
        obj = AES.new(cls.aeskey(aescode, uniqueKey), AES.MODE_ECB);
        c = obj.decrypt(content);
        if needDecode:
            c = c.decode()
        return cls.dealignContent(c);

    @classmethod
    def test(cls):
        aescode = "123";
        uniqueKey = "@$sswq112$FF";
        s = "helloworld~~~";

        encoded = cls.encode(s, aescode, uniqueKey);
        Log.D("encode result = " + str(encoded));

        decoded = cls.decode(encoded, aescode, uniqueKey);
        Log.D("decode result = " + str(decoded));

        #图片测试
        from Config import Config
        import os
        jpgFile = Config.shared.outPath + os.sep + "nocover.jpg";
        jpgFd = open(jpgFile, "r");
        jpgData = jpgFd.read();
        jpgFd.close();
        
        encodeJpgData = cls.encode(jpgData, aescode, uniqueKey, False);
        jpgFd = open(Config.shared.outPath + os.sep + "nocover-encode.jpg", "w");
        jpgFd.write(encodeJpgData);
        jpgFd.flush();
        jpgFd.close();

        decodeJpgData = cls.decode(encodeJpgData, aescode, uniqueKey, False);
        jpgFd = open(Config.shared.outPath + os.sep + "nocover-decode.jpg", "w");
        jpgFd.write(decodeJpgData);
        jpgFd.flush();
        jpgFd.close();



