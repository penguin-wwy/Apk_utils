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
from apk_utils.file import *

class Core(cmd.Cmd):
    def __init__(self, res):
        cmd.Cmd.__init__(self)
        self.__isConsole = res["console"]
        self.__filePath  = res["filePath"]
        self.prompt = 'Apk_utils—> '

    def analyze(self):
        if self.__isConsole:
            if self.__filePath:
                fileInfo = File(self.__filePath)
            self.cmdloop()

    def do_unzip(self, s, silent=False):
        pass

    def do_apktool(self, s, silent=False):
        pass

