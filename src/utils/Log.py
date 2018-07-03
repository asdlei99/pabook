#coding=utf-8

import time

#当前时间戳
def currTimestamp():
	return int(time.time());

#时间戳格式化201807030923
def currTimeFormat():
	return time.strftime("%Y%m%d%H%M%S", time.localtime(currTimestamp()));

class _redirection:
	

def I(msg):
	_log()