import struct
from binascii import unhexlify

def printHex(arr):
    res = ''
    for i in range(0, len(arr)):
        res = res + hex(arr[i]) + ' '
    return res

def toLong(arr):
    if arr == b'\xff\xff\xff\xff':
        return -1
    return struct.unpack('L', bytes(arr))[0]

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

    def getRawBinary(self):
        return self.__rawBinary

class AroidManifest:
    def __init__(self, fileInfo):
        self.__fileInfo = fileInfo
        self.strTable = []
        self.namespaceMap = {}

    def analyze(self):
        outFile = self.__fileInfo.getFilePath().replace("AroidManifest", "out.xml")
        head = self.readHead()
        print("Magic num: " + printHex(head[0]))
        print("File Size: " + str(toLong(head[1])))

        endOfStr = self.readStringChunk()
        endOfR   = self.readResourceIdChunk(endOfStr)
        endOfStartN = self.readStartNamespaceChunk(endOfR)
        endOfStartTag = self.readStratTagChunk(endOfStartN)
        self.readEndTagChunk(endOfStartTag)



    def readHead(self):
        return [self.__fileInfo.getRawBinary()[:4], self.__fileInfo.getRawBinary()[4:8]]

    def readStringChunk(self):
        chunkSize = self.__fileInfo.getRawBinary()[12:16]
        chunkSize = toLong(chunkSize)
        rawBinary = self.__fileInfo.getRawBinary()[8:chunkSize+8]
        strCount = toLong(rawBinary[8:12])
        offset = toLong(rawBinary[20:24]) + 8
        offOfEachStr = []

        print("String Chunk Type: " + printHex(rawBinary[0:4]))
        print("String Chunk Size: " + str(chunkSize))
        print("String Count: " + str(strCount))
        print("Style Count: " + printHex(rawBinary[12:16]))
        print("Unknow: " + printHex(rawBinary[16:20]))
        print("String Start: " + str(hex(offset)))

        for i in range(0, strCount):
            offOfEachStr.append(rawBinary[28+4*i:32+4*i])

        for i in range(0, strCount):
            string = ''
            startOffset = offset + toLong(offOfEachStr[i]) - 8
            chrOffset = startOffset + 2
            while rawBinary[chrOffset] != 0:
                string += chr(rawBinary[chrOffset])
                chrOffset += 2
            print("Str: " + string)
            self.strTable.append(string)

        return chunkSize+8

    def readResourceIdChunk(self, endOfStr):
        chunkSize = self.__fileInfo.getRawBinary()[endOfStr+4:endOfStr+8]
        chunkSize = toLong(chunkSize)
        rawBinary = self.__fileInfo.getRawBinary()[endOfStr:endOfStr+chunkSize]

        print("ResourceId Chunk Type: " + printHex(rawBinary[0:4]))
        print("ResourceId Chunk Size: " + str(chunkSize))

        count = (chunkSize - 8) // 4
        for i in range(0, count):
            id = toLong(rawBinary[8+i*4:12+i*4])
            strHex = hex(id)
            if len(strHex) != 10:
                strHex = '0x' + (10-len(strHex)) * '0' + strHex[2:]
                print("id: " + str(id) + " hex: " + strHex)

        return endOfStr + chunkSize

    def readStartNamespaceChunk(self, endOfR):
        chunkSize = self.__fileInfo.getRawBinary()[endOfR+4:endOfR+8]
        chunkSize = toLong(chunkSize)
        rawBinary = self.__fileInfo.getRawBinary()[endOfR:endOfR+chunkSize]

        print("Namespace Chunk Type: " + printHex(rawBinary[0:4]))
        print("Namespace Chunk Size: " + str(chunkSize))

        count = (chunkSize - 8) // 16
        for i in range(0, count):
            table = rawBinary[8+i*16:24+i*16]
            lineNum = toLong(table[0:4])
            prefix = toLong(table[8:12])
            Uri = toLong(table[12:16])
            print("Line Number: " + str(lineNum))
            print("Prefix: " + str(prefix))
            print("Prefix Str: " + self.strTable[prefix])
            print("Uri: " + str(Uri))
            print("Uri Str: " + self.strTable[Uri])
            #self.namespaceMap.updata({self.strTable[prefix], self.strTable[Uri]})

        return endOfR + chunkSize

    def readStratTagChunk(self, endOfStartN):
        chunkSize = self.__fileInfo.getRawBinary()[endOfStartN+4:endOfStartN+8]
        chunkSize = toLong(chunkSize)
        rawBinary = self.__fileInfo.getRawBinary()[endOfStartN:endOfStartN+chunkSize]

        print("Start Tag Chunk Type: " + printHex(rawBinary[0:4]))
        print("Start Tag Chunk Size: " + str(chunkSize))

        table = rawBinary[8:]
        while table != b'':
            lineNum = table[0:4]
            print("line number: " + str(toLong(lineNum)))

            prefix = table[4:8]
            prefixIndex = toLong(prefix)
            if prefixIndex == -1:
                print("prefix null")
            else:
                print("prefix: " + str(prefixIndex))
                print("prefix str: " + self.strTable[prefixIndex])

            namespaceUri = table[8:12]
            uriIndex = toLong(namespaceUri)
            if uriIndex == -1:
                print("Uri null")
            else:
                print("uri: " + str(uriIndex))
                print("uri str: " + self.strTable[uriIndex])

            name = table[12:16]
            nameIndex = toLong(name)
            if nameIndex == -1:
                print("tag name null")
            else:
                print("tag name index: " + str(nameIndex))
                print("tag name str: " + self.strTable[nameIndex])

            flags= table[16:20]

            AttributeCount = table[20:24]
            attrCount = toLong(AttributeCount)
            print("attr count" + str(attrCount))

            ClassAtrribute = table[24:28]

            Atrributes = []
            for i in range(0, attrCount):
                entry = {}
                for j in range(5):
                    value = toLong(table[28+i*20+j*4:32+i*20+j*4])
                    if j == 0:
                        entry["nameSpaceUri"] = value
                        if value == -1:
                            print("nameSpaceUri null")
                        else:
                            print("nameSpaceUri: " + str(value))
                            print("nameSpaceUri str: " + self.strTable[value])
                    elif j == 1:
                        entry["name"] = value
                        if value == -1:
                            print("name null")
                        else:
                            print("name: " + str(value))
                            print("name: " + self.strTable[value])
                    elif j == 2:
                        entry["valueString"] = value
                        if value == -1:
                            print("valueString null")
                        else:
                            print("valueString: " + str(value))
                            print("valueString str: " + self.strTable[value])
                    elif j == 3:
                        entry["type"] = (value >> 24)
                        if value == -1:
                            print("type null")
                        else:
                            print("type: " + str(value>>24))
                    elif j == 4:
                        entry["data"] = value
                        if value == -1:
                            print("data null")
                        else:
                            print("data: " + str(value))
                Atrributes.append(entry)

            splitSize = 28
            splitSize += attrCount * 5 * 4
            table = table[splitSize:]

        return endOfStartN + chunkSize

    def readEndTagChunk(self, endOfStartTag):
        chunkSize = self.__fileInfo.getRawBinary()[endOfStartTag+4:endOfStartTag+8]
        chunkSize = toLong(chunkSize)
        rawBinary = self.__fileInfo.getRawBinary()[endOfStartTag:endOfStartTag+chunkSize]

        print("End Tag Chunk Type: " + printHex(rawBinary[0:4]))
        print("End Tag Chunk Size: " + str(chunkSize))

