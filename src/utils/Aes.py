#coding=utf-8

from Crypto.Cipher import AES
from src.utils import Utils

class Aes:
	@classmethod
	def aeskey(cls, aescode, uniqueKey):
		key = Utils.md5str(aescode + uniqueKey);
		Utils.log(" md5 key = " + str(key));
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
	def encode(cls, content, aescode, uniqueKey):
		obj = AES.new(cls.aeskey(aescode, uniqueKey), AES.MODE_ECB);
		c = content.encode("utf-8");
		c = cls.alignContent(c);
		e = obj.encrypt(c);
		return e;

	@classmethod
	def decode(cls, content, aescode, uniqueKey):
		obj = AES.new(cls.aeskey(aescode, uniqueKey), AES.MODE_ECB);
		c = obj.decrypt(content).decode();
		return cls.dealignContent(c);

	@classmethod
	def test(cls):
		aescode = "123";
		uniqueKey = "@$sswq112$FF";
		s = "helloworld~~~";

		encoded = cls.encode(s, aescode, uniqueKey);
		Utils.log("encode result = " + str(encoded));

		decoded = cls.decode(encoded, aescode, uniqueKey);
		Utils.log("decode result = " + str(decoded));
