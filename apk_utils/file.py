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

class AndroidManifest:
    def __init__(self, fileInfo):
        self.__fileInfo = fileInfo
        self.strTable = []
        self.namespaceMap = {}

    def analyze(self):
        outFile = self.__fileInfo.getFilePath().replace("AroidManifest", "out.xml")

        rawChunk = self.__fileInfo.getRawBinary()

        switcher = {
            0x001c0001: self.readStringChunk,
            0x00080180: self.readResourceIdChunk,
            0x00100100: self.readStartNamespaceChunk,
            0x00100101: self.readEndNamespaceChunk,
            0x00100102: self.readStratTagChunk,
            0x00100103: self.readEndTagChunk,
            0x00100104: self.readTextChunk
        }

        self.readHead(rawChunk)
        rawChunk = rawChunk[8:]

        while 1:
            if not rawChunk:
                break
            start2End = toLong(rawChunk[4:8])
            headTag = rawChunk[0:4]
            switcher.get(toLong(headTag), self.readBreak)(rawChunk)
            rawChunk = rawChunk[start2End:]

    def readHead(self, rawBinary):
        head = [rawBinary[:4], rawBinary[4:8]]
        print("Magic num: " + printHex(head[0]))
        print("File Size: " + str(toLong(head[1])))

    def readStringChunk(self, rawBinary):
        chunkSize = rawBinary[4:8]
        chunkSize = toLong(chunkSize)
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


    def readResourceIdChunk(self, rawBinary):
        chunkSize = rawBinary[4:8]
        chunkSize = toLong(chunkSize)

        print("ResourceId Chunk Type: " + printHex(rawBinary[0:4]))
        print("ResourceId Chunk Size: " + str(chunkSize))

        count = (chunkSize - 8) // 4
        for i in range(0, count):
            id = toLong(rawBinary[8+i*4:12+i*4])
            strHex = hex(id)
            if len(strHex) != 10:
                strHex = '0x' + (10-len(strHex)) * '0' + strHex[2:]
                print("id: " + str(id) + " hex: " + strHex)


    def readStartNamespaceChunk(self, rawBinary):
        chunkSize = rawBinary[4:8]
        chunkSize = toLong(chunkSize)

        print("Start Namespace Chunk Type: " + printHex(rawBinary[0:4]))
        print("Start Namespace Chunk Size: " + str(chunkSize))

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
            if not self.strTable[prefix] in self.namespaceMap:
                self.namespaceMap[self.strTable[prefix]] = self.strTable[Uri]
            if not self.strTable[Uri] in self.namespaceMap:
                self.namespaceMap[self.strTable[Uri]] = self.strTable[prefix]

    def readEndNamespaceChunk(self, rawBinary):
        chunkSize = rawBinary[4:8]
        chunkSize = toLong(chunkSize)

        print("End Namespace Chunk Type: " + printHex(rawBinary[0:4]))
        print("End Namespace Chunk Size: " + str(chunkSize))

        lineNum = rawBinary[8:12]
        print("line number: " + str(toLong(lineNum)))

        prefix = rawBinary[12:16]
        prefixIndex = toLong(prefix)
        if prefixIndex == -1:
            print("prefix null")
        else:
            print("prefix: " + str(prefixIndex))
            print("prefix str: " + self.strTable[prefixIndex])

        namespaceUri = rawBinary[16:20]
        uriIndex = toLong(namespaceUri)
        if uriIndex == -1:
            print("Uri null")
        else:
            print("uri: " + str(uriIndex))
            print("uri str: " + self.strTable[uriIndex])

        name = rawBinary[20:24]
        nameIndex = toLong(name)
        if nameIndex == -1:
            print("tag name null")
        else:
            print("tag name index: " + str(nameIndex))
            print("tag name str: " + self.strTable[nameIndex])



    def readStratTagChunk(self, rawChunk):
        chunkSize = rawChunk[4:8]
        chunkSize = toLong(chunkSize)

        rawBinary = rawChunk[:chunkSize]

        print("Start Tag Chunk Type: " + printHex(rawBinary[0:4]))
        print("Start Tag Chunk Size: " + str(chunkSize))

        res_s = ''

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
                res_s = res_s + "<" + self.strTable[nameIndex] + ' '

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
                            res_s = res_s + self.namespaceMap[self.strTable[value]] + ':'
                    elif j == 1:
                        entry["name"] = value
                        if value == -1:
                            print("name null")
                        else:
                            print("name: " + str(value))
                            print("name: " + self.strTable[value])
                            res_s = res_s + self.strTable[value] + '='
                    elif j == 2:
                        entry["valueString"] = value
                        if value == -1:
                            print("valueString null")
                        else:
                            print("valueString: " + str(value))
                            print("valueString str: " + self.strTable[value])
                            res_s = res_s + self.strTable[value] + ' '
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


    def readEndTagChunk(self, rawBinary):
        chunkSize = rawBinary[4:8]
        chunkSize = toLong(chunkSize)

        print("End Tag Chunk Type: " + printHex(rawBinary[0:4]))
        print("End Tag Chunk Size: " + str(chunkSize))

        lineNum = rawBinary[8:12]
        print("line number: " + str(toLong(lineNum)))

        prefix = rawBinary[12:16]
        prefixIndex = toLong(prefix)
        if prefixIndex == -1:
            print("prefix null")
        else:
            print("prefix: " + str(prefixIndex))
            print("prefix str: " + self.strTable[prefixIndex])

        namespaceUri = rawBinary[16:20]
        uriIndex = toLong(namespaceUri)
        if uriIndex == -1:
            print("Uri null")
        else:
            print("uri: " + str(uriIndex))
            print("uri str: " + self.strTable[uriIndex])

        name = rawBinary[20:24]
        nameIndex = toLong(name)
        if nameIndex == -1:
            print("tag name null")
        else:
            print("tag name index: " + str(nameIndex))
            print("tag name str: " + self.strTable[nameIndex])

    def readTextChunk(self, rawBinary):
        pass

    def readBreak(self, rawBinary):
        print("Unkonw Chunk!")
        print(printHex(rawBinary[:4]))
        print("Left %d bytes." % len(rawBinary))

    class resultText:
        def __init__(self):
            pass

        res_text = []

        @staticmethod
        def append(d):
            pass

