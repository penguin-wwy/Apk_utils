
import apk_utils.options

from struct import unpack, pack

TYPE_ITEM = {
    0x0: "TYPE_HEADER_ITEM",
    0x1: "TYPE_STRING_ID_ITEM",
    0x2: "TYPE_TYPE_ID_ITEM",
    0x3: "TYPE_PROTO_ID_ITEM",
    0x4: "TYPE_FIELD_ID_ITEM",
    0x5: "TYPE_METHOD_ID_ITEM",
    0x6: "TYPE_CLASS_DEF_ITEM",
    0x1000: "TYPE_MAP_LIST",
    0x1001: "TYPE_TYPE_LIST",
    0x1002: "TYPE_ANNOTATION_SET_REF_LIST",
    0x1003: "TYPE_ANNOTATION_SET_ITEM",
    0x2000: "TYPE_CLASS_DATA_ITEM",
    0x2001: "TYPE_CODE_ITEM",
    0x2002: "TYPE_STRING_DATA_ITEM",
    0x2003: "TYPE_DEBUG_INFO_ITEM",
    0x2004: "TYPE_ANNOTATION_ITEM",
    0x2005: "TYPE_ENCODED_ARRAY_ITEM",
    0x2006: "TYPE_ANNOTATIONS_DIRECTORY_ITEM",
}

class HeaderItem(object):
    def __init__(self, buff, cm):
        self.__CM = cm

        self.offset = buff.get_idx()

        self.magic = unpack("=Q", buff.read(8))[0]
        self.checksum = unpack("=i", buff.read(4))[0]
        self.signature = unpack("=20s", buff.read(20))[0]
        self.file_size = unpack("=I", buff.read(4))[0]
        self.header_size = unpack("=I", buff.read(4))[0]
        self.endian_tag = unpack("=I", buff.read(4))[0]
        self.link_size = unpack("=I", buff.read(4))[0]
        self.link_off = unpack("=I", buff.read(4))[0]
        self.map_off = unpack("=I", buff.read(4))[0]
        self.string_ids_size = unpack("=I", buff.read(4))[0]
        self.string_ids_off = unpack("=I", buff.read(4))[0]
        self.type_ids_size = unpack("=I", buff.read(4))[0]
        self.type_ids_off = unpack("=I", buff.read(4))[0]
        self.proto_ids_size = unpack("=I", buff.read(4))[0]
        self.proto_ids_off = unpack("=I", buff.read(4))[0]
        self.field_ids_size = unpack("=I", buff.read(4))[0]
        self.field_ids_off = unpack("=I", buff.read(4))[0]
        self.method_ids_size = unpack("=I", buff.read(4))[0]
        self.method_ids_off = unpack("=I", buff.read(4))[0]
        self.class_defs_size = unpack("=I", buff.read(4))[0]
        self.class_defs_off = unpack("=I", buff.read(4))[0]
        self.data_size = unpack("=I", buff.read(4))[0]
        self.data_off = unpack("=I", buff.read(4))[0]

        self.map_off_obj = None
        self.string_off_obj = None
        self.type_off_obj = None
        self.proto_off_obj = None
        self.field_off_obj = None
        self.method_off_obj = None
        self.class_off_obj = None
        self.data_off_obj = None

    def reload(self):
      pass

    def get_obj(self):
      if self.map_off_obj == None:
        self.map_off_obj = self.__CM.get_item_by_offset( self.map_off )

      if self.string_off_obj == None:
        self.string_off_obj = self.__CM.get_item_by_offset( self.string_ids_off )

      if self.type_off_obj == None:
        self.type_off_obj = self.__CM.get_item_by_offset( self.type_ids_off )

      if self.proto_off_obj == None:
        self.proto_off_obj = self.__CM.get_item_by_offset( self.proto_ids_off )

      if self.field_off_obj == None:
        self.field_off_obj = self.__CM.get_item_by_offset( self.field_ids_off )

      if self.method_off_obj == None:
        self.method_off_obj = self.__CM.get_item_by_offset( self.method_ids_off )

      if self.class_off_obj == None:
        self.class_off_obj = self.__CM.get_item_by_offset( self.class_defs_off )

      if self.data_off_obj == None:
        self.data_off_obj = self.__CM.get_item_by_offset( self.data_off )

      self.map_off = self.map_off_obj.get_off()

      self.string_ids_size = len(self.string_off_obj)
      self.string_ids_off = self.string_off_obj[0].get_off()

      self.type_ids_size = len(self.type_off_obj.type)
      self.type_ids_off = self.type_off_obj.get_off()

      self.proto_ids_size = len(self.proto_off_obj.proto)
      self.proto_ids_off = self.proto_off_obj.get_off()

      self.field_ids_size = len(self.field_off_obj.elem)
      self.field_ids_off = self.field_off_obj.get_off()

      self.method_ids_size = len(self.method_off_obj.methods)
      self.method_ids_off = self.method_off_obj.get_off()

      self.class_defs_size = len(self.class_off_obj.class_def)
      self.class_defs_off = self.class_off_obj.get_off()

      self.data_size = len(self.data_off_obj.map_item)
      self.data_off = self.data_off_obj.get_off()

      return pack("=Q", self.magic) +                                 \
             pack("=i", self.checksum) +                              \
             pack("=20s", self.signature) +                           \
             pack("=I", self.file_size) +                             \
             pack("=I", self.header_size) +                           \
             pack("=I", self.endian_tag) +                            \
             pack("=I", self.link_size) +                             \
             pack("=I", self.link_off) +                              \
             pack("=I", self.map_off) +              \
             pack("=I", self.string_ids_size) +      \
             pack("=I", self.string_ids_off) +       \
             pack("=I", self.type_ids_size) +        \
             pack("=I", self.type_ids_off) +         \
             pack("=I", self.proto_ids_size) +       \
             pack("=I", self.proto_ids_off) +        \
             pack("=I", self.field_ids_size) +       \
             pack("=I", self.field_ids_off) +        \
             pack("=I", self.method_ids_size) +      \
             pack("=I", self.method_ids_off) +       \
             pack("=I", self.class_defs_size) +      \
             pack("=I", self.class_defs_off) +       \
             pack("=I", self.data_size) +            \
             pack("=I", self.data_off)

    def get_raw(self):
        return self.get_obj()

    def get_length(self):
      return len(self.get_raw())

    def show(self):
        print("Header Item")
        print("magic=%s, checksum=%s, signature=%s\n" % (self.magic, self.checksum, self.signature))
        print("file_size=%x, header_size=%x, endian_tag=%x\n" % (self.file_size, self.header_size, self.endian_tag))
        print("link_size=%x, link_off=%x\n" % (self.link_size, self.link_off))
        print("map_off=%x\n" % (self.map_off))
        print("string_ids_size=%x, string_ids_off=%x\n" % (self.string_ids_size, self.string_ids_off))
        print("type_ids_size=%x, type_ids_off=%x\n" % (self.type_ids_size, self.type_ids_off))
        print("proto_ids_size=%x, proto_ids_off=%x\n" % (self.proto_ids_size, self.proto_ids_off))
        print("field_ids_size=%x, field_ids_off=%x\n" % (self.field_ids_size, self.field_ids_off))
        print("method_ids_size=%x, method_ids_off=%x\n" % (self.method_ids_size, self.method_ids_off))
        print("class_defs_size=%x, class_defs_off=%x\n" % (self.class_defs_size, self.class_defs_off))
        print("data_size=%x, data_off=%x\n" % (self.data_size, self.data_off))

    def set_off(self, off):
      self.offset = off

    def get_off(self):
      return self.offset


class MapItem(object):
    switcher = {
        0x0: ["TYPE_HEADER_ITEM", HeaderItem],
        0x1: ["TYPE_STRING_ID_ITEM",],
        0x2: ["TYPE_TYPE_ID_ITEM",],
        0x3: ["TYPE_PROTO_ID_ITEM",],
        0x4: ["TYPE_FIELD_ID_ITEM",],
        0x5: ["TYPE_METHOD_ID_ITEM",],
        0x6: ["TYPE_CLASS_DEF_ITEM",],
        0x1000: ["TYPE_MAP_LIST",],
        0x1001: ["TYPE_TYPE_LIST",],
        0x1002: ["TYPE_ANNOTATION_SET_REF_LIST",],
        0x1003: ["TYPE_ANNOTATION_SET_ITEM",],
        0x2000: ["TYPE_CLASS_DATA_ITEM",],
        0x2001: ["TYPE_CODE_ITEM",],
        0x2002: ["TYPE_STRING_DATA_ITEM",],
        0x2003: ["TYPE_DEBUG_INFO_ITEM",],
        0x2004: ["TYPE_ANNOTATION_ITEM",],
        0x2005: ["TYPE_ENCODED_ARRAY_ITEM",],
        0x2006: ["TYPE_ANNOTATIONS_DIRECTORY_ITEM",]
    }

    def __init__(self, buff, cm):
        self.__CM = cm

        self.off = buff.get_idx()

        self.type = unpack("=H", buff.read(2))[0]
        self.unused = unpack("=H", buff.read(2))[0]
        self.size = unpack("=I", buff.read(4))[0]
        self.offset = unpack("=I", buff.read(4))[0]

        self.item = None

        buff.set_index(self.offset)

        self.next(buff, cm)

    def reload(self):
        pass

    def next(self, buff, cm):
        self.item = MapItem.switcher[self.type][1](buff, cm)

class MapList(object):
    def __init__(self, cm, off, buff):
        self.CM = cm
        buff.set_idx(off)
        self.offset = off
        self.size = unpack("=I", buff.read( 4 ) )[0]
        self.map_item = []

        for i in range(0, self.size):
            idx = buff.get_index()

            mi = MapItem(buff, self.CM)
            self.map_item.append(mi)

            self.CM.add_type_item(mi)

        for i in self.map_item:
            i.reload()

    def reload(self):
        pass



class ClassManager():
    def __init__(self):
        pass

class DalvikVMFormat():
    def __init__(self):
        pass