#coding=utf-8

from src.utils import Utils

class Enum(tuple):
	__getattr__ = tuple.index;

#Ongoing表示正在连载
#Completed表示已完本
#Error表示书籍错误
BookInfoStatus = Enum(["Ongoing", "Completed", "Error"])

BookDownloadStatus = Enum(["Ongoing", "Completed"]);

BookVistUrlStatus = Enum(["Ready", "Visited"])