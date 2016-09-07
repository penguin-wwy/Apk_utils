
import apk_utils.options
import struct
from struct import unpack, pack, calcsize
from apk_utils.instruction import *



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
    def __init__(self, size, buff, cm):
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

class LinearSweepAlgorithm(object):
    @staticmethod
    def get_instructions(self, cm, size, insn, idx):
        max_idx = size * calcsize('=H')
        if max_idx > len(insn):
          max_idx = len(insn)

        # Get instructions
        while idx < max_idx:
          obj = None
          classic_instruction = True

          op_value = unpack('=B', insn[idx])[0]

          #print "%x %x" % (op_value, idx)

          #payload instructions or extented/optimized instructions
          if (op_value == 0x00 or op_value == 0xff) and ((idx + 2) < max_idx):
            op_value = unpack('=H', insn[idx:idx + 2])[0]

            # payload instructions ?
            if op_value in DALVIK_OPCODES_PAYLOAD:
              try:
                obj = get_instruction_payload(op_value, insn[idx:])
                classic_instruction = False
              except struct.error:
                warning("error while decoding instruction ...")

            elif op_value in DALVIK_OPCODES_EXTENDED_WIDTH:
              try:
                obj = get_extented_instruction(cm, op_value, insn[idx:])
                classic_instruction = False
              except struct.error, why:
                warning("error while decoding instruction ..." + why.__str__())

            # optimized instructions ?
            elif self.odex and (op_value in DALVIK_OPCODES_OPTIMIZED):
              obj = get_optimized_instruction(cm, op_value, insn[idx:])
              classic_instruction = False

          # classical instructions
          if classic_instruction:
            op_value = unpack('=B', insn[idx])[0]
            obj = get_instruction(cm, op_value, insn[idx:], self.odex)

          # emit instruction
          yield obj
          idx = idx + obj.get_length()

class DCode(object):
    def __int__(self, class_manager, offset, size, buff):
        self.CM = class_manager
        self.insn = buff
        self.offset = offset
        self.size = size

        self.notes = {}
        self.cached_instructions = []
        self.rcache = 0

        self.idx = 0

    def get_insn(self):
      """
          Get the insn buffer

          :rtype: string
      """
      return self.insn

    def set_insn(self, insn):
      """
          Set a new raw buffer to disassemble

          :param insn: the buffer
          :type insn: string
      """
      self.insn = insn
      self.size = len(self.insn)

    def set_idx(self, idx):
        """
            Set the start address of the buffer

            :param idx: the index
            :type idx: int
        """
        self.idx = idx

    def set_instructions(self, instructions):
      """
          Set the instructions

          :param instructions: the list of instructions
          :type instructions: a list of :class:`Instruction`
      """
      self.cached_instructions = instructions

    def get_instructions(self):
        """
            Get the instructions

            :rtype: a generator of each :class:`Instruction` (or a cached list of instructions if you have setup instructions)
        """
        # it is possible to a cache for instructions (avoid a new disasm)
        if self.cached_instructions:
          for i in self.cached_instructions:
            yield i

        else:
          if self.rcache >= 5:
            lsa = LinearSweepAlgorithm()
            for i in lsa.get_instructions(self.CM, self.size, self.insn, self.idx):
              self.cached_instructions.append(i)

            for i in self.cached_instructions:
              yield i
          else:
            self.rcache += 1
            if self.size >= 1000:
              self.rcache = 5

            lsa = LinearSweepAlgorithm()
            for i in lsa.get_instructions(self.CM, self.size, self.insn, self.idx):
                yield i

    def reload(self):
        pass

    def add_inote(self, msg, idx, off=None):
      """
          Add a message to a specific instruction by using (default) the index of the address if specified

          :param msg: the message
          :type msg: string
          :param idx: index of the instruction (the position in the list of the instruction)
          :type idx: int
          :param off: address of the instruction
          :type off: int
      """
      if off != None:
        idx = self.off_to_pos(off)

      if idx not in self.notes:
        self.notes[idx] = []

      self.notes[idx].append(msg)

    def get_instruction(self, idx, off=None):
        """
            Get a particular instruction by using (default) the index of the address if specified

            :param idx: index of the instruction (the position in the list of the instruction)
            :type idx: int
            :param off: address of the instruction
            :type off: int

            :rtype: an :class:`Instruction` object
        """
        if off != None:
          idx = self.off_to_pos(off)
        return [i for i in self.get_instructions()][idx]

    def off_to_pos(self, off):
        """
            Get the position of an instruction by using the address

            :param off: address of the instruction
            :type off: int

            :rtype: int
        """
        idx = 0
        nb = 0
        for i in self.get_instructions():
            if idx == off:
                return nb
            nb += 1
            idx += i.get_length()
        return -1

    def get_ins_off(self, off):
        """
            Get a particular instruction by using the address

            :param off: address of the instruction
            :type off: int

            :rtype: an :class:`Instruction` object
        """
        idx = 0
        for i in self.get_instructions():
            if idx == off:
                return i
            idx += i.get_length()
        return None

    def show(self):
        """
            Display this object
        """
        nb = 0
        idx = 0
        for i in self.get_instructions():
            print ("%-8d(%08x)" % (nb, idx), end='')
            i.show(nb)
            print

            idx += i.get_length()
            nb += 1

    def get_raw(self):
        """
            Return the raw buffer of this object

            :rtype: string
        """
        return ''.join(i.get_raw() for i in self.get_instructions())

    def get_length(self):
      """
          Return the length of this object

          :rtype: int
      """
      return len(self.get_raw())

class DalvikCode(object):
    def __init__(self, buff, cm):
        self.__CM = cm
        self.offset = buff.get_idx()

        self.int_padding = ""
        off = buff.get_idx()
        while off % 4 != 0:
            self.int_padding += '\00'
            off += 1
        buff.set_idx(off)

        self.__off = buff.get_idx()

        self.registers_size = unpack("=H", buff.read(2))[0]
        self.ins_size = unpack("=H", buff.read(2))[0]
        self.outs_size = unpack("=H", buff.read(2))[0]
        self.tries_size = unpack("=H", buff.read(2))[0]
        self.debug_info_off = unpack("=I", buff.read(4))[0]
        self.insns_size = unpack("=I", buff.read(4))[0]

        ushort = calcsize('=H')

        self.code = DCode(self.__CM, buff.get_idx(), self.insns_size, buff.read(self.insns_size * ushort))


class CodeItem(object):
    def __init__(self, size, buff, cm):



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
        self.item = MapItem.switcher[self.type][1](self.size, buff, cm)

class MapList(object):
    def __init__(self, cm, off, buff):
        self.CM = cm
        buff.set_idx(off)
        self.offset = off
        self.size = unpack("=I", buff.read( 4 ) )[0]
        self.map_item = []

        for i in range(0, self.size):
            idx = buff.get_idx()

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