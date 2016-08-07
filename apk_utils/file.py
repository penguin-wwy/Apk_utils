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
