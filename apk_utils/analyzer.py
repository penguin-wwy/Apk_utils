import cmd
from apk_utils.file import *

class Analyzer(cmd.Cmd):
    def __int__(self, res):
        #cmd.Cmd.__init__(self)
        self.__isConsole = res["console"]
        self.__filePath  = res["filePath"]
        self.prompt = 'Apk_utils—> '

    def run(self):
        if self.__isConsole:
            if self.__filePath:
                fileInfo = File(self.__filePath)
            self.cmdloop()

    def do_unzip(self, s, silent=False):
        pass