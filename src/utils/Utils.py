#coding=utf-8

import sys, os, json
import traceback

import chardet

import urllib2

import bs4

from bs4 import BeautifulSoup

import re

import time

import md5

reload(sys);
sys.setdefaultencoding("utf-8");

charset = "utf-8";
#打印log

def log(msg):
    print(msg);

#打印Except

def logE(e):
    log("[E] %s \n %s" %(str(e), str(traceback.format_exc())));

#读取文件内容

def readFile(path):
    if not os.path.isfile(path):
        return None;
    try:
        f = open(path);
        if f != None:
            data = f.read();
            f.close();
            if len(data) > 0:
                return data;
    except Exception, e:
        logE(e);
    return None;

#将内容写入本地文件

def writeFile(path, content, mode):
    f = None;
    try:
        f = open(path, mode);
        f.write(content);
        f.flush();
        f.close();
        return True;
    except Exception, e:
        logE(e);
        if f != None:
            f.close();
    return False;


def createDir(dirPath):
    if not dirPath:
        return False;
    if not os.path.exists(dirPath):
        os.makedirs(dirPath);

    return os.path.exists(dirPath);

#GET请求

def readUrl(url, retryLimit = 10):
    res = None;
    times = 0;
    while res == None and times < retryLimit:
        resp = None;
        try:
            req = urllib2.Request(url);
            resp = urllib2.urlopen(req);
            res = resp.read();
        except Exception, e:
            logE(e);
            if isinstance(e, urllib2.HTTPError) and e.code == 404:
                break;
        finally:
            if resp != None:
                resp.close();
        times += 1;
        if times > 1:
            log("[E] readUrl retry times(%s) to download url(%s)" % (str(times), str(url)));
    return res;


def soupUrl(url):
    content = readUrl(url);
    if content == None:
        return None;
    return BeautifulSoup(content, "lxml");


def isSoupStr(str):
    return type(str) == bs4.element.NavigableString;


def normalizeUrl(url):
    u = url;
    while u.endswith(os.sep):
        u = u[:-1];
    return u;


def absoluteUrl(url, fromUrl, rootUrl):
    if url == None:
        return None;
    if url.startswith("http://") or url.startswith("https://"):
        return url;
    elif url.startswith("/") and rootUrl != None:
        return normalizeUrl(rootUrl) + url;
    elif fromUrl != None:
        return normalizeUrl(fromUrl) + os.sep + url;
    return None;


def deduplicateList(list):
    return list(set(list));


def isMatch(pat, text):
    return re.compile(pat).match(text) != None;


def findAll(pat, text):
    return re.compile(pat).findall(text);


def replaceAll(content, pat, replace):
    if content == None:
        return;
    return re.sub(pat, replace, content);


def isValidUrl(url):
    return isValidStr(url) and isMatch(r"http[s]?://.+", url);


def isValidStr(s):
    return isinstance(s, str) and len(s) > 0;


def isValidArr(arr):
    return arr != None and len(arr) > 0;


def findAllClassTag(soup, tagname, clazz):
    return soup.find_all(lambda tag: tag.name == tagname and tag.has_attr("class") and tag["class"][0] == clazz);


def getTimestamp(str, format):
    return time.mktime(time.strptime(str, format));


def md5str(str):
    return md5.md5(str).hexdigest();

