import struct
from binascii import unhexlify

class File:
    def __init__(self, filePath):
        self.__fileName  = filePath.split("\\")[-1]
        self.__filePath = filePath
        self.__rawBinary    = None
        
        try:
            fd = open(self.__filePath, "rb")
            self.__rawBinary = fd.read()
            fd.close()
        except:
            print("[Error] Can't open the binary or binary not found")
            return None

    def getFileName(self):
        return self.__fileName

    def getFilePath(self):
        return self.__filePath

class AroidManifest:
    def __init__(self, fileInfo):
        self.__fileInfo = fileInfo

    def analyze(self):
        outFile = self.__fileInfo.__filePath + "out.xml"
        head = self.readHead()
        print("Magic num: " + head[0])
        print("File Size: " + struct.unpack('L', bytes(head[1]))[0])


    def readHead(self):
        return [self.__fileInfo.__rawBinary[:4], self.__fileInfo.__rawBinary[4:8]]

    def readStringChunk(self):
        pass