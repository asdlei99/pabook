#coding=utf-8

from src.storge.Storge import Storge

from src.utils import Utils

import os

class FileStorge(Storge):
	def __init__(self, outPath):
		Utils.log("[I] FileStorge inited");
		super(FileStorge, self).__init__(outPath);
		self.filespath = self.outPath + os.sep + "files";
		Utils.createDir(self.filespath);

	def checkFileExists(self, fileuniquekey, toDir, complete):
		outDir = self.filespath;
		if toDir != None:
			outDir = self.filespath + os.sep + toDir;
			Utils.createDir(outDir);
		outfile = outDir + os.sep + fileuniquekey;
		if os.path.isfile(outfile) and os.path.getsize(outfile) > 0:
			complete(True, outfile);
		else:
			complete(False, None);

	def pushContent(self, content, fileuniquekey, toDir, complete):
		if content == None:
			if complete != None:
				complete(False, None);
				return;
		outDir = self.filespath;
		if toDir != None:
			outDir = self.filespath + os.sep + toDir;
			Utils.createDir(outDir);
		outfile = outDir + os.sep + fileuniquekey;
		succ = Utils.writeFile(outfile, content, "w");
		if not succ:
			if complete != None:
				complete(False, None);
			return;
		if complete != None:
			complete(True, outfile);
