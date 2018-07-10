
#coding=utf-8

'''
需要安装的软件：
1. mysql
2. pip
需要安装的python插件
1. PyMySQL
2. beautifulsoup4
3. html5lib
4. lxml
5. pycrypto
'''

'''
#运行
1. 修改Config.sample.py
2. 执行python run.py
'''

from src.utils import Log

import sys, os

#清空数据库中的表
def dropAllTables():
    from src.db import Db
    Db.instance.executeSql('''show tables;''');
    ret = Db.instance.fetchAll();
    for item in ret:
        for k, v in item.items():
            Db.instance.executeSql('''drop table if exists {};'''.format(v));
            Log.I("droping table " + str(v));
    Log.I("droped all tables finished");

def test():
    Log.I("--test--");
    dropAllTables();

# 将Config.sample.py复制出一个Config.py文件
def createConfigFile():
    if not os.path.exists("Config.py"):
        fd = open("Config.sample.py", "r");
        content = fd.read();
        fd.close();
        wfd = open("Config.py", "w");
        wfd.write(content);
        wfd.flush();
        wfd.close();

if __name__ == '__main__':
    createConfigFile();
    # test();
    try:
        from src.Prepare import Prepare
        Prepare();
    except Exception, e:
        Log.E("--------异常退出--------");
        Log.Exc(e);
        sys.exit(0);
else:
    Log.E("-错误")
