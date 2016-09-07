import os
import sys
import logging
import logging.handlers

def apktool_win(path, indir, outdir):
    bat = indir + '\\tool\\apktool.bat'
    info = os.popen(bat + " d " + path + " -o " + outdir)
    print(info.read())

def apktool_lin(path, indir, outdir):
    sh = indir + '\\tool\\apktool'
    info = os.popen(sh + ' d ' + path + "-o" + outdir)
    print(info.read())

class Logger(object):
    FileMaxSize = 10485760
    FileMaxCount = 5

    logFolder = '.'

    def __init__(self):
        pass

    @staticmethod
    def setLogFolder(logFolder):
        Logger.logFolder = logFolder

    @staticmethod
    def getLogger(logFile, logName):
        logger = logging.getLogger(logName)
        handler = logging.handlers.RotatingFileHandler(os.path.join(Logger.logFolder, logFile),
                                                       maxBytes=Logger.FileMaxSize, backupCount=Logger.FileMaxCount)
        """
        %(name)s Logger的名字
        %(levelno)s 数字形式的日志级别
        %(levelname)s 文本形式的日志级别
        %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
        %(filename)s 调用日志输出函数的模块的文件名
        %(module)s 调用日志输出函数的模块名
        %(funcName)s 调用日志输出函数的函数名
        %(lineno)d 调用日志输出函数的语句所在的代码行
        %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
        %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
        %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
        %(thread)d 线程ID。可能没有
        %(threadName)s 线程名。可能没有
        %(process)d 进程ID。可能没有
        %(message)s用户输出的消息
        """
        formatter = logging.Formatter("\n[%(asctime)s] [%(leavelname)s] %(module)s %(funcName)s :\n\
                                       %(message)s\n")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        logger.setLevel(logging.INFO)
        return logger

class ByteCode(object):
    def __init__(self, rawBinary):
        self.__buff = rawBinary
        self.__index = 0

    def read(self, size):
        buff = self.__buff[self.__index:self.__index+size]
        self.__index += size

        return buff

    def readat(self, off):
        return self.__buff[off:]

    def set_idx(self, index):
        self.__index = index

    def get_idx(self):
        return self.__index

    def get_buff(self):
        return self.__buff

    def len_buff(self):
        return len(self.__buff)