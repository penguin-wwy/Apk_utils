import cmd
import os
import re
import codecs
import sqlite3
import zipfile
from sys import exit
from apk_utils.file import *

class Core(cmd.Cmd):
    def __init__(self, res):
        cmd.Cmd.__init__(self)
        self.__isConsole = res["console"]
        self.__androidmanifest = res["androidmanifest"]
        self.__filePath  = res["filePath"]
        self.__fileInfo  = None
        self.__outDirPath= res["outDir"]
        self.prompt = 'Apk_utils—> '
        self.__parse()

    def __parse(self):
        if self.__filePath:
            self.__fileInfo = File(self.__filePath)
            self.__outDirPath = self.__fileInfo.getFilePath().replace(self.__fileInfo.getFileName(), self.__outDirPath)

        if self.__androidmanifest:
            if self.__fileInfo or self.__fileInfo.getFileName() != "AndroidManifest.xml":
                print("File is not AndroidManifest.xml")
                exit(0)

    def analyze(self):
        if self.__androidmanifest:
            AroidManifest(self.__fileInfo).analyze()

        if self.__isConsole:
            self.cmdloop()

    def do_unzip(self, s, silent=False):
        pass

    def do_apktool(self, s, silent=False):
        pass

    def do_dex(self, s, silent=False):
        pass