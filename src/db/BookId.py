#coding=utf-8

from src.utils import Utils, Log
from src.db.KeyValueDb import KeyValueDb

_lastBookId = None;

_kvDb = None;

def init(kvDb):
    global _kvDb;
    global _lastBookId;
    if _lastBookId != None:
        return;
    _kvDb = kvDb;
    id = kvDb.get("lastBookId");
    if id != None:
        _lastBookId = int(id);

def checkBookId(bookId):
    #不能有相邻的相同的数字
    #不能有2位顺子
    #不能是等比等差
    #不能有重复 030303 这种
    idstr = str(bookId);
    idlen = len(idstr);
    lc = None;
    llc = None;
    for c in idstr:
        if lc != None and llc != None:
            illc = int(llc);
            ilc = int(lc);
            ic = int(c);
            #相邻相等
            if ilc == ic and ilc == illc:
                return False;
            #顺子
            if (ilc - ic == 1 and illc - ilc == 1) or (ilc - ic == -1 and illc - ilc == 1):
                return False;
            #检查等比等差
            if illc - ilc == ilc - ic:
                return False;
            if ilc != 0 and ic != 0 and illc / ilc != 0 and illc / ilc == ilc / ic:
                return False;
        llc = lc;
        lc = c;
    #检查是否重复
    for i in range(0, idlen / 2):
        if idstr[0:i+1] * 2 in idstr:
            return False;
    return True;

def nextBookId():
    global _lastBookId;
    global _kvDb;
    bookId = None;
    if _lastBookId == None:
        bookId = 101
    else:
        bookId = _lastBookId + 1;

    while True:
        valid = checkBookId(bookId)
        if valid:
            break;
        else:
            bookId += 1;

    _lastBookId = bookId;

    _kvDb.set("lastBookId", str(_lastBookId));

    Log.D(" generate new bookId " + str(bookId));

    return bookId;

def test():
    # valid = checkBookId(3870370);
    # print("valid = %d" % (valid));
    count = 0;
    for i in xrange(0,10000):
        count += 1;
        print(" --- bookId = " + str(nextBookId()) + " valid count ============ " + str(count));
    print("-- 100 - 1000 total valid booid = " + str(count));