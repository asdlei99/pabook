
#coding=utf-8

'''
1. 安装最新版本pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py
2. pip install PyMySQL
3. 安装mysql并启动，mysql中建立一个名字为book的数据库
'''

'''
#安装美丽汤
sudo pip install beautifulsoup4
sudo pip install html5lib
sudo pip install lxml
'''

'''
#若用aws需安装boto3
1. 安装开发依赖：boto3 pip install boto3
2. 创建文件 ~/.aws/credentials 内容为： 
[default]
aws_access_key_id = 你的aws key id
aws_secret_access_key = 你的aws access key
'''

'''
#若用七牛云，需安装七牛 
pip install qiniu
'''

'''
#运行
python run.py -r "http://www.ybdu.com" -o ./out -p YbduParser -s FileStorge -a "helloworld"
'''

from src.utils import Utils

from src.db.BookinfoDb import BookinfoDb
from src.db.ChapterDb import ChapterDb
from src.db.VisitUrlDb import *
from src.db.KeyValueDb import *
from src.db import Db

from src.utils.Aes import Aes

from src.Prepare import Prepare

from src.parser import BookId

from src.utils import Log

import sys

#from qiniu import Auth, put_file, etag, BucketManager
# import boto3
# from botocore.exceptions import ClientError

def dropAllTables():
    Db.instance.executeSql('''show tables;''');
    ret = Db.instance.fetchAll();
    for item in ret:
        for k, v in item.items():
            Db.instance.executeSql('''drop table if exists {};'''.format(v));
            Log.I("droping table " + str(v));
    Log.I("droped all tables finished");

def test():
    Log.I("--test--");
    # dbins = BookinfoDb();
    # dbins.test();

    # chapterDb = ChapterDb(101);
    # chapterDb.test();

    # visitUrlDb = VisitBookUrlDb();
    # visitUrlDb.test();

    # kvDb = KeyValueDb();
    # kvDb.test();

    # Aes.test();

    # BookId.test();

    dropAllTables();
    # Log.test();
    # ak = "qiniu access key";
    # sk = "qiniu secret key";
    # bk = "qiniu bucket name";
    # qn = Auth(ak, sk);
    # key = "logs/test-log1.txt";
    # token = qn.upload_token(bk, key, 3600);
    # ret, info = put_file(token, key, "./out/logs/error/log-error-20180706000000.txt")
    # Log.D(str(ret));
    # Log.D(str(info));

    # bkManager = BucketManager(qn);
    # ret, resp = bkManager.stat(bk, key);
    # Log.D(str(ret) + " ~~~~ " + str(resp));
    # ret1, resp1 = bkManager.stat(bk, "asdasdas");
    # Log.D(str(ret1) + " ~~~~ " + str(resp1));

    # s3 = boto3.resource("s3");
    # bucket = s3.Bucket("aw-kaso");
    # obj = None;
    # try:
    #     obj = s3.ObjectSummary("aw-kaso", "testxxx.txt").get();
    # except Exception, e:
    #     Log.Exc(e);
    #     Log.D("错误了");


    # Log.D(" -- objSummary = " + str(obj))
    # Log.D(" -- bucketname= " + str(bucket.name) + ", allobject = " + str(bucket.objects));
    # for obj in bucket.objects.all():
    #     Log.D(" -- obj.key = " + obj.key);
    # # data = open("./out/logs/error/log-error-20180706000000.txt", "rb");
    # ret = bucket.put_object(Key="test3.txt", Body="hello world");
    # Log.D(" -- upload file ret="+str(ret));

reload(sys);
sys.setdefaultencoding("utf-8");

# Config.py
def createConfigFile():
    fd = open("Config.sample.py", "r");
    content = fd.read();
    fd.close();
    wfd = open("Config.py", "w");
    wfd.write(content);
    wfd.flush();
    wfd.close();

if __name__ == '__main__':
    # test();
    createConfigFile();
    Prepare();
else:
    print("error");
