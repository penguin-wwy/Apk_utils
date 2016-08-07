## -*- coding: utf-8 -*-
##
##  Jonathan Salwan - 2014-05-17 - ROPgadget tool
## 
##  http://twitter.com/JonathanSalwan
##  http://shell-storm.org/project/ROPgadget/
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software  Foundation, either  version 3 of  the License, or
##  (at your option) any later version.

import cmd
import os
import re
import codecs
import sqlite3
import zipfile
from apk_utils.file import *

class Core(cmd.Cmd):
    def __init__(self, res):
        cmd.Cmd.__init__(self)
        self.__isConsole = res["console"]
        self.__filePath  = res["filePath"]
        self.__fileInfo  = None
        self.__outDirPath= res["outDir"]
        self.prompt = 'Apk_utils—> '
        self.__parse()

    def __parse(self):
        if self.__filePath:
            self.__fileInfo = File(self.__filePath)
            self.__outDirPath = self.__fileInfo.getFilePath().replace(self.__fileInfo.getFileName(), self.__outDirPath)

    def analyze(self):
        if self.__isConsole:
            self.cmdloop()

    def do_unzip(self, s, silent=False):
        pass

    def do_apktool(self, s, silent=False):
        pass

    def do_dex(self, s, silent=False):
        pass