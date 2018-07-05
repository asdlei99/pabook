
#coding=utf-8

'''
1. 安装最新版本pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
2. pip install PyMySQL
3. brew install mysql
'''

'''
#安装美丽汤
sudo pip install beautifulsoup4
sudo pip install html5lib
sudo pip install lxml
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

    # dropAllTables();
    # Log.test();

if __name__ == '__main__':
    # test();
    Prepare();
else:
    print("error");