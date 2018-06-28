#coding=utf-8

import pymysql
import pymysql.cursors

from src.utils import Utils

class Db:
	#pymysql接口
	def __init__(self):
		connConfig = {
			'host': '127.0.0.1',
			'user': 'wanghy',
			'password': 'wang@1234',
			'db': 'book',
			'charset': 'utf8',
			'cursorclass': pymysql.cursors.DictCursor,
			'autocommit': True
		};
		self.conn = pymysql.connect(**connConfig);
		self.cursor = self.conn.cursor();

	def executeSql(self, sql):
		try:
			self.cursor.execute(sql);
			Utils.log("[I] 执行 " + sql.strip() + " 成功");
			return True;
		except Exception as e:
			Utils.log("[I] 执行 " + sql.strip() + " 失败");
			Utils.logE(e);
		return False;

	def fetchOne(self):
		return self.cursor.fetchone();

	def __del__(self):
		self.conn.close();

instance = Db();

