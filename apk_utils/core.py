import cmd
import os
import sys
import re
import codecs
import sqlite3
import zipfile
import platform
from sys import exit
from apk_utils.file import *
from apk_utils.options import *
from apk_utils.dexFile import DalvikVMFormat

WINDOWS = 1
LINUX   = 2

class Core(cmd.Cmd):
    def __init__(self, res, path):
        cmd.Cmd.__init__(self)
        self.__isConsole = res["console"]
        self.__androidmanifest = res["androidmanifest"]
        self.__dex       = res["dex"]
        self.__filePath  = res["filePath"]
        self.__fileInfo  = None
        self.__outDirPath= res["outDir"]
        self.os = None
        self.path = path
        self.prompt = 'Apk_utils—> '
        self.__parse()

    def __parse(self):
        if self.__filePath:
            self.__fileInfo = File(self.__filePath)
            self.__outDirPath = self.__fileInfo.getFilePath().replace(self.__fileInfo.getFileName(), self.__outDirPath)

        if os.path.exists(self.__outDirPath):
            pass
        else:
            os.mkdir(self.__outDirPath)

        if self.__androidmanifest:
            if self.__fileInfo == None or self.__fileInfo.getFileName() != "AndroidManifest.xml":
                print("File is not AndroidManifest.xml")
                exit(0)

        sysstr = platform.system()
        if sysstr == 'Windows':
            self.os = WINDOWS
        elif sysstr == 'Linux':
            self.os = LINUX
        else:
            print("Unknow os")
            sys.exit(0)

    def analyze(self):
        if self.__androidmanifest:
            AndroidManifest(self.__fileInfo).analyze()


        if self.__isConsole:
            self.cmdloop()

    def do_filename(self, s, silent=False):
        self.__filePath = s
        self.__fileInfo = File(self.__filePath)
        self.__outDirPath = self.__fileInfo.getFilePath().replace(self.__fileInfo.getFileName(), self.__outDirPath)

        if self.__fileInfo.getFileName() == "AndroidManifest.xml":
            self.__androidmanifest = True
        elif self.__fileInfo.getFileName().split('.')[-1] == "dex":
            self.__dex = True

    def do_parse(self, s, silent=False):
        if not self.__fileInfo:
            print("No file to parse!")

        if self.__androidmanifest:
            AndroidManifest(self.__fileInfo).analyze()
        elif self.__dex:
            self.do_dex()


    def do_unzip(self, s, silent=False):
        uPath = os.path.join(self.__outDirPath, 'unzip')
        os.mkdir(uPath)
        f = zipfile.ZipFile(self.__fileInfo.getFilePath(), 'r')
        for file in f.namelist():
            f.extract(file, uPath)


    def do_apktool(self, s=None, silent=False):
        if self.os == WINDOWS:
            apktool_win(self.__fileInfo.getFilePath(), self.get_curr_path(),
                        os.path.join(self.__outDirPath, 'apktool_out'))


    def do_dex(self, s, silent=False):
        DalvikVMFormat(self.__fileInfo)

    def get_curr_path(self):
        return self.path.replace('/', '\\')