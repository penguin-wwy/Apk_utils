from struct import unpack, pack, calcsize

KIND_METH           = 0
KIND_STRING         = 1
KIND_FIELD          = 2
KIND_TYPE           = 3
VARIES              = 4
INLINE_METHOD       = 5
VTABLE_OFFSET       = 6
FIELD_OFFSET        = 7
KIND_RAW_STRING     = 8

OPERAND_REGISTER = 0
OPERAND_LITERAL = 1
OPERAND_RAW = 2
OPERAND_OFFSET = 3
OPERAND_KIND = 0x100

class FillArrayData(object):
    """
        This class can parse a FillArrayData instruction

        :param buff: a Buff object which represents a buffer where the instruction is stored
    """
    def __init__(self, buff):
        self.notes = []

        self.format_general_size = calcsize("=HHI")
        self.ident = unpack("=H", buff[0:2])[0]
        self.element_width = unpack("=H", buff[2:4])[0]
        self.size = unpack("=I", buff[4:8])[0]

        buf_len = self.size * self.element_width
        if buf_len % 2:
            buf_len += 1

        self.data = buff[self.format_general_size:self.format_general_size + buf_len]

    def add_note(self, msg):
      """
        Add a note to this instruction

        :param msg: the message
        :type msg: objects (string)
      """
      self.notes.append(msg)

    def get_notes(self):
      """
        Get all notes from this instruction

        :rtype: a list of objects
      """
      return self.notes

    def get_op_value(self):
      """
        Get the value of the opcode

        :rtype: int
      """
      return self.ident

    def get_data(self):
        """
            Return the data of this instruction (the payload)

            :rtype: string
        """
        return self.data

    def get_output(self, idx=-1):
        """
            Return an additional output of the instruction

            :rtype: string
        """
        buff = ""

        data = self.get_data()

        buff += repr(data) + " | "
        for i in range(0, len(data)):
          buff += "\\x%02x" % ord(data[i])

        return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_RAW, repr(self.get_data()))]

    def get_formatted_operands(self):
      return None

    def get_name(self):
        """
            Return the name of the instruction

            :rtype: string
        """
        return "fill-array-data-payload"

    def show_buff(self, pos):
        """
            Return the display of the instruction

            :rtype: string
        """
        buff = self.get_name() + " "

        for i in range(0, len(self.data)):
            buff += "\\x%02x" % ord(self.data[i])
        return buff

    def show(self, pos):
        """
            Print the instruction
        """
        print (self.show_buff(pos), end='')

    def get_length(self):
        """
            Return the length of the instruction

            :rtype: int
        """
        return ((self.size * self.element_width + 1) / 2 + 4) * 2

    def get_raw(self):
        return pack("=H", self.ident) + pack("=H", self.element_width) + pack("=I", self.size) + self.data

class SparseSwitch(object):
    """
        This class can parse a SparseSwitch instruction

        :param buff: a Buff object which represents a buffer where the instruction is stored
    """
    def __init__(self, buff):
        self.notes = []

        self.format_general_size = calcsize("=HH")
        self.ident = unpack("=H", buff[0:2])[0]
        self.size = unpack("=H", buff[2:4])[0]

        self.keys = []
        self.targets = []

        idx = self.format_general_size
        for i in range(0, self.size):
            self.keys.append(unpack('=l', buff[idx:idx + 4])[0])
            idx += 4

        for i in range(0, self.size):
            self.targets.append(unpack('=l', buff[idx:idx + 4])[0])
            idx += 4

    def add_note(self, msg):
      """
        Add a note to this instruction

        :param msg: the message
        :type msg: objects (string)
      """
      self.notes.append(msg)

    def get_notes(self):
      """
        Get all notes from this instruction

        :rtype: a list of objects
      """
      return self.notes

    def get_op_value(self):
        """
          Get the value of the opcode

          :rtype: int
        """
        return self.ident

    def get_keys(self):
        """
            Return the keys of the instruction

            :rtype: a list of long
        """
        return self.keys

    def get_values(self):
      return self.get_keys()

    def get_targets(self):
        """
            Return the targets (address) of the instruction

            :rtype: a list of long
        """
        return self.targets

    def get_output(self, idx=-1):
      """
          Return an additional output of the instruction

          :rtype: string
      """
      return " ".join("%x" % i for i in self.keys)

    def get_operands(self, idx=-1):
      """
          Return an additional output of the instruction

          :rtype: string
      """
      return []

    def get_formatted_operands(self):
      return None

    def get_name(self):
        """
            Return the name of the instruction

            :rtype: string
        """
        return "sparse-switch-payload"

    def show_buff(self, pos):
        """
            Return the display of the instruction

            :rtype: string
        """
        buff = self.get_name() + " "
        for i in range(0, len(self.keys)):
            buff += "%x:%x " % (self.keys[i], self.targets[i])

        return buff

    def show(self, pos):
        """
            Print the instruction
        """
        print (self.show_buff(pos), end='')

    def get_length(self):
        return self.format_general_size + (self.size * calcsize('<L')) * 2

    def get_raw(self):
        return pack("=H", self.ident) + pack("=H", self.size) + ''.join(pack("=l", i) for i in self.keys) + ''.join(pack("=l", i) for i in self.targets)


class PackedSwitch(object):
    """
        This class can parse a PackedSwitch instruction

        :param buff: a Buff object which represents a buffer where the instruction is stored
    """
    def __init__(self, buff):
        self.notes = []

        self.format_general_size = calcsize("=HHI")

        self.ident = unpack("=H", buff[0:2])[0]
        self.size = unpack("=H", buff[2:4])[0]
        self.first_key = unpack("=i", buff[4:8])[0]

        self.targets = []

        idx = self.format_general_size

        max_size = self.size
        if (max_size * 4) > len(buff):
            max_size = len(buff) - idx - 8

        for i in range(0, max_size):
            self.targets.append(unpack('=l', buff[idx:idx + 4])[0])
            idx += 4

    def add_note(self, msg):
      """
        Add a note to this instruction

        :param msg: the message
        :type msg: objects (string)
      """
      self.notes.append(msg)

    def get_notes(self):
      """
        Get all notes from this instruction

        :rtype: a list of objects
      """
      return self.notes

    def get_op_value(self):
        """
          Get the value of the opcode

          :rtype: int
        """
        return self.ident

    def get_keys(self):
        """
            Return the keys of the instruction

            :rtype: a list of long
        """
        return [(self.first_key + i) for i in range(0, len(self.targets))]

    def get_values(self):
        return self.get_keys()

    def get_targets(self):
        """
            Return the targets (address) of the instruction

            :rtype: a list of long
        """
        return self.targets

    def get_output(self, idx=-1):
      """
          Return an additional output of the instruction

          :rtype: string
      """
      return " ".join("%x" % (self.first_key + i) for i in range(0, len(self.targets)))

    def get_operands(self, idx=-1):
      """
          Return an additional output of the instruction

          :rtype: string
      """
      return []

    def get_formatted_operands(self):
      return None

    def get_name(self):
        """
            Return the name of the instruction

            :rtype: string
        """
        return "packed-switch-payload"

    def show_buff(self, pos):
        """
            Return the display of the instruction

            :rtype: string
        """
        buff = self.get_name() + " "
        buff += "%x:" % self.first_key

        for i in self.targets:
            buff += " %x" % i

        return buff

    def show(self, pos):
        """
            Print the instruction
        """
        print (self.show_buff(pos), end='')

    def get_length(self):
        return self.format_general_size + (self.size * calcsize('=L'))

    def get_raw(self):
        return pack("=H", self.ident) + pack("=H", self.size) + pack("=i", self.first_key) + ''.join(pack("=l", i) for i in self.targets)

def get_kind(cm, kind, value):
  """
    Return the value of the 'kind' argument

    :param cm: a ClassManager object
    :type cm: :class:`ClassManager`
    :param kind: the type of the 'kind' argument
    :type kind: int
    :param value: the value of the 'kind' argument
    :type value: int

    :rtype: string
  """
  if kind == KIND_METH:
    method = cm.get_method_ref(value)
    class_name = method.get_class_name()
    name = method.get_name()
    descriptor = method.get_descriptor()

    return "%s->%s%s" % (class_name, name, descriptor)

  elif kind == KIND_STRING:
    return repr(cm.get_string(value))

  elif kind == KIND_RAW_STRING:
    return cm.get_string(value)

  elif kind == KIND_FIELD:
    class_name, proto, field_name = cm.get_field(value)
    return "%s->%s %s" % (class_name, field_name, proto)

  elif kind == KIND_TYPE:
    return cm.get_type(value)

  elif kind == VTABLE_OFFSET:
    return "vtable[0x%x]" % value

  elif kind == FIELD_OFFSET:
    return "field[0x%x]" % value

  elif kind == INLINE_METHOD:
    buff = "inline[0x%x]" % value

    # FIXME: depends of the android version ...
    if len(INLINE_METHODS) > value:
        elem = INLINE_METHODS[value]
        buff += " %s->%s%s" % (elem[0], elem[1], elem[2])

    return buff

  return None

class Instruction(object):
    """
        This class represents a dalvik instruction
    """
    def get_kind(self):
        """
            Return the 'kind' argument of the instruction

            :rtype: int
        """
        if self.OP > 0xff:
          if self.OP >= 0xf2ff:
            return DALVIK_OPCODES_OPTIMIZED[self.OP][1][1]
          return DALVIK_OPCODES_EXTENDED_WIDTH[self.OP][1][1]
        return DALVIK_OPCODES_FORMAT[self.OP][1][1]

    def get_name(self):
        """
            Return the name of the instruction

            :rtype: string
        """
        if self.OP > 0xff:
          if self.OP >= 0xf2ff:
            return DALVIK_OPCODES_OPTIMIZED[self.OP][1][0]
          return DALVIK_OPCODES_EXTENDED_WIDTH[self.OP][1][0]
        return DALVIK_OPCODES_FORMAT[self.OP][1][0]

    def get_op_value(self):
        """
            Return the value of the opcode

            :rtype: int
        """
        return self.OP

    def get_literals(self):
        """
            Return the associated literals

            :rtype: list of int
        """
        return []

    def show(self, idx):
        """
            Print the instruction
        """
        print (self.get_name() + " " + self.get_output(idx), end='')

    def show_buff(self, idx):
        """
            Return the display of the instruction

            :rtype: string
        """
        return self.get_output(idx)

    def get_translated_kind(self):
        """
            Return the translated value of the 'kind' argument

            :rtype: string
        """
        return get_kind(self.cm, self.get_kind(), self.get_ref_kind())

    def get_output(self, idx=-1):
      """
          Return an additional output of the instruction

          :rtype: string
      """
      raise("not implemented")

    def get_operands(self, idx=-1):
      """
          Return all operands

          :rtype: list
      """
      raise("not implemented")

    def get_length(self):
      """
          Return the length of the instruction

          :rtype: int
      """
      raise("not implemented")

    def get_raw(self):
      """
          Return the object in a raw format

          :rtype: string
      """
      raise("not implemented")

    def get_ref_kind(self):
      """
          Return the value of the 'kind' argument

          :rtype: value
      """
      raise("not implemented")

    def get_formatted_operands(self):
      return None


class InstructionInvalid(Instruction):
    """
        This class represents an invalid instruction
    """
    def __init__(self, cm, buff):
      super(InstructionInvalid, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff

      #debug("OP:%x" % (self.OP))

    def get_name(self):
        """
            Return the name of the instruction

            :rtype: string
        """
        return "AG:invalid_instruction"

    def get_output(self, idx=-1):
      return "(OP:%x)" % self.OP

    def get_operands(self, idx=-1):
      return []

    def get_length(self):
      return 2

    def get_raw(self):
      return pack("=H", self.OP)

class Instruction35c(Instruction):
    """
        This class represents all instructions which have the 35c format
    """
    def __init__(self, cm, buff):
      super(Instruction35c, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.G = (i16 >> 8) & 0xf
      self.A = (i16 >> 12) & 0xf
      self.BBBB = unpack("=H", buff[2:4])[0]

      i16 = unpack("=H", buff[4:6])[0]
      self.C = i16 & 0xf
      self.D = (i16 >> 4) & 0xf
      self.E = (i16 >> 8) & 0xf
      self.F = (i16 >> 12) & 0xf

    def get_output(self, idx=-1):
      buff = ""
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.A == 0:
        buff += "%s" % (kind)
      elif self.A == 1:
        buff += "v%d, %s" % (self.C, kind)
      elif self.A == 2:
        buff += "v%d, v%d, %s" % (self.C, self.D, kind)
      elif self.A == 3:
        buff += "v%d, v%d, v%d, %s" % (self.C, self.D, self.E, kind)
      elif self.A == 4:
        buff += "v%d, v%d, v%d, v%d, %s" % (self.C, self.D, self.E, self.F, kind)
      elif self.A == 5:
        buff += "v%d, v%d, v%d, v%d, v%d, %s" % (self.C, self.D, self.E, self.F, self.G, kind)

      return buff

    def get_operands(self, idx=-1):
      l = []
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.A == 0:
        l.append((self.get_kind() + OPERAND_KIND, self.BBBB, kind))
      elif self.A == 1:
        l.extend([(OPERAND_REGISTER, self.C), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 2:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 3:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 4:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (OPERAND_REGISTER, self.F), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 5:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (OPERAND_REGISTER, self.F), (OPERAND_REGISTER, self.G), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])

      return l

    def get_length(self):
      return 6

    def get_ref_kind(self):
      return self.BBBB

    def get_raw(self):
      return pack("=HHH", (self.A << 12) | (self.G << 8) | self.OP, self.BBBB, (self.F << 12) | (self.E << 8) | (self.D << 4) | self.C)

class Instruction10x(Instruction):
    """
        This class represents all instructions which have the 10x format
    """
    def __init__(self, cm, buff):
      super(Instruction10x, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff

      #log_andro.debug("OP:%x %s" % (self.OP, args[0]))

    def get_output(self, idx=-1):
      return ""

    def get_operands(self, idx=-1):
      return []

    def get_length(self):
      return 2

    def get_raw(self):
      return pack("=H", self.OP)


class Instruction21h(Instruction):
    """
        This class represents all instructions which have the 21h format
    """
    def __init__(self, cm, buff):
      super(Instruction21h, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=h", buff[2:4])[0]

      #log_andro.debug("OP:%x %s AA:%x BBBBB:%x" % (self.OP, args[0], self.AA, self.BBBB))

      self.formatted_operands = []

      if self.OP == 0x15:
        self.formatted_operands.append(unpack('=f', '\x00\x00' + pack('=h', self.BBBB))[0])
      elif self.OP == 0x19:
        self.formatted_operands.append(unpack('=d', '\x00\x00\x00\x00\x00\x00' + pack('=h', self.BBBB))[0])

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, %d" % (self.AA, self.BBBB)

      if self.formatted_operands != []:
        buff += " # %s" % (str(self.formatted_operands))

      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_LITERAL, self.BBBB)]

    def get_formatted_operands(self):
      return self.formatted_operands

    def get_literals(self):
      return [self.BBBB]

    def get_raw(self):
      return pack("=Hh", (self.AA << 8) | self.OP, self.BBBB)


class Instruction11n(Instruction):
    """
        This class represents all instructions which have the 11n format
    """
    def __init__(self, cm, buff):
      super(Instruction11n, self).__init__()

      i16 = unpack("=h", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.A = (i16 >> 8) & 0xf
      self.B = (i16 >> 12)

      #log_andro.debug("OP:%x %s A:%x B:%x" % (self.OP, args[0], self.A, self.B))

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, %d" % (self.A, self.B)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.A), (OPERAND_LITERAL, self.B)]

    def get_literals(self):
      return [self.B]

    def get_length(self):
      return 2

    def get_raw(self):
      return pack("=h", (self.B << 12) | (self.A << 8) | self.OP)


class Instruction21c(Instruction):
    """
        This class represents all instructions which have the 21c format
    """
    def __init__(self, cm, buff):
      super(Instruction21c, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=H", buff[2:4])[0]
      #log_andro.debug("OP:%x %s AA:%x BBBBB:%x" % (self.OP, args[0], self.AA, self.BBBB))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      buff += "v%d, %s" % (self.AA, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)
      return [(OPERAND_REGISTER, self.AA), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)]

    def get_ref_kind(self):
      return self.BBBB

    def get_string(self):
      return get_kind(self.cm, self.get_kind(), self.BBBB)

    def get_raw_string(self):
      return get_kind(self.cm, KIND_RAW_STRING, self.BBBB)

    def get_raw(self):
      return pack("=HH", (self.AA << 8) | self.OP, self.BBBB)


class Instruction21s(Instruction):
    """
        This class represents all instructions which have the 21s format
    """
    def __init__(self, cm, buff):
      super(Instruction21s, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=h", buff[2:4])[0]

      self.formatted_operands = []

      if self.OP == 0x16:
        self.formatted_operands.append(unpack('=d', pack('=d', self.BBBB))[0])

      #log_andro.debug("OP:%x %s AA:%x BBBBB:%x" % (self.OP, args[0], self.AA, self.BBBB))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, %d" % (self.AA, self.BBBB)

      if self.formatted_operands != []:
        buff += " # %s" % str(self.formatted_operands)

      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_LITERAL, self.BBBB)]

    def get_literals(self):
      return [self.BBBB]

    def get_formatted_operands(self):
      return self.formatted_operands

    def get_raw(self):
      return pack("=Hh", (self.AA << 8) | self.OP, self.BBBB)


class Instruction22c(Instruction):
    """
        This class represents all instructions which have the 22c format
    """
    def __init__(self, cm, buff):
      super(Instruction22c, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.A = (i16 >> 8) & 0xf
      self.B = (i16 >> 12) & 0xf
      self.CCCC = unpack("=H", buff[2:4])[0]

      #log_andro.debug("OP:%x %s A:%x B:%x CCCC:%x" % (self.OP, args[0], self.A, self.B, self.CCCC))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      kind = get_kind(self.cm, self.get_kind(), self.CCCC)
      buff += "v%d, v%d, %s" % (self.A, self.B, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.CCCC)
      return [(OPERAND_REGISTER, self.A), (OPERAND_REGISTER, self.B), (self.get_kind() + OPERAND_KIND, self.CCCC, kind)]

    def get_ref_kind(self):
      return self.CCCC

    def get_raw(self):
      return pack("=HH", (self.B << 12) | (self.A << 8) | (self.OP), self.CCCC)


class Instruction22cs(Instruction):
    """
        This class represents all instructions which have the 22cs format
    """
    def __init__(self, cm, buff):
      super(Instruction22cs, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.A = (i16 >> 8) & 0xf
      self.B = (i16 >> 12) & 0xf
      self.CCCC = unpack("=H", buff[2:4])[0]

      #log_andro.debug("OP:%x %s A:%x B:%x CCCC:%x" % (self.OP, args[0], self.A, self.B, self.CCCC))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      kind = get_kind(self.cm, self.get_kind(), self.CCCC)
      buff += "v%d, v%d, %s" % (self.A, self.B, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.CCCC)
      return [(OPERAND_REGISTER, self.A), (OPERAND_REGISTER, self.B), (self.get_kind() + OPERAND_KIND, self.CCCC, kind)]

    def get_ref_kind(self):
      return self.CCCC

    def get_raw(self):
      return pack("=HH", (self.B << 12) | (self.A << 8) | (self.OP), self.CCCC)


class Instruction31t(Instruction):
    """
        This class represents all instructions which have the 31t format
    """
    def __init__(self, cm, buff):
      super(Instruction31t, self).__init__()
      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBBBBBB = unpack("=i", buff[2:6])[0]
      #log_andro.debug("OP:%x %s AA:%x BBBBBBBBB:%x" % (self.OP, args[0], self.AA, self.BBBBBBBB))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, +%x (0x%x)" % (self.AA, self.BBBBBBBB, self.BBBBBBBB * 2 + idx)

      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_LITERAL, self.BBBBBBBB)]

    def get_ref_off(self):
      return self.BBBBBBBB

    def get_raw(self):
      return pack("=Hi", (self.AA << 8) | self.OP, self.BBBBBBBB)


class Instruction31c(Instruction):
    """
        This class represents all instructions which have the 31c format
    """
    def __init__(self, cm, buff):
      super(Instruction31c, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBBBBBB = unpack("=I", buff[2:6])[0]
      #log_andro.debug("OP:%x %s AA:%x BBBBBBBBB:%x" % (self.OP, args[0], self.AA, self.BBBBBBBB))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""

      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)
      buff += "v%d, %s" % (self.AA, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)
      return [(OPERAND_REGISTER, self.AA), (self.get_kind() + OPERAND_KIND, self.BBBBBBBB, kind)]

    def get_ref_kind(self):
      return self.BBBBBBBB

    def get_string(self):
      """
          Return the string associated to the 'kind' argument

          :rtype: string
      """
      return get_kind(self.cm, self.get_kind(), self.BBBBBBBB)

    def get_raw_string(self):
      return get_kind(self.cm, KIND_RAW_STRING, self.BBBBBBBB)

    def get_raw(self):
      return pack("=HI", (self.AA << 8) | self.OP, self.BBBBBBBB)


class Instruction12x(Instruction):
    """
        This class represents all instructions which have the 12x format
    """
    def __init__(self, cm, buff):
      super(Instruction12x, self).__init__()

      i16 = unpack("=h", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.A = (i16 >> 8) & 0xf
      self.B = (i16 >> 12) & 0xf

      #log_andro.debug("OP:%x %s A:%x B:%x" % (self.OP, args[0], self.A, self.B))

    def get_length(self):
      return 2

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, v%d" % (self.A, self.B)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.A), (OPERAND_REGISTER, self.B)]

    def get_raw(self):
      return pack("=H", (self.B << 12) | (self.A << 8) | (self.OP))


class Instruction11x(Instruction):
    """
        This class represents all instructions which have the 11x format
    """
    def __init__(self, cm, buff):
      super(Instruction11x, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      #log_andro.debug("OP:%x %s AA:%x" % (self.OP, args[0], self.AA))

    def get_length(self):
      return 2

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d" % (self.AA)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA)]

    def get_raw(self):
      return pack("=H", (self.AA << 8) | self.OP)


class Instruction51l(Instruction):
    """
        This class represents all instructions which have the 51l format
    """
    def __init__(self, cm, buff):
      super(Instruction51l, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBBBBBBBBBBBBBB = unpack("=q", buff[2:10])[0]

      self.formatted_operands = []

      if self.OP == 0x18:
        self.formatted_operands.append(unpack('=d', pack('=q', self.BBBBBBBBBBBBBBBB))[0])

      #log_andro.debug("OP:%x %s AA:%x BBBBBBBBBBBBBBBB:%x" % (self.OP, args[0], self.AA, self.BBBBBBBBBBBBBBBB))

    def get_length(self):
      return 10

    def get_output(self, idx=-1):
      buff = ""

      buff += "v%d, %d" % (self.AA, self.BBBBBBBBBBBBBBBB)

      if self.formatted_operands:
        buff += " # %s" % str(self.formatted_operands)

      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_LITERAL, self.BBBBBBBBBBBBBBBB)]

    def get_formatted_operands(self):
      return self.formatted_operands

    def get_literals(self):
      return [self.BBBBBBBBBBBBBBBB]

    def get_raw(self):
      return pack("=Hq", (self.AA << 8) | self.OP, self.BBBBBBBBBBBBBBBB)


class Instruction31i(Instruction):
    """
        This class represents all instructions which have the 3li format
    """
    def __init__(self, cm, buff):
      super(Instruction31i, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBBBBBB = unpack("=i", buff[2:6])[0]

      self.formatted_operands = []

      if self.OP == 0x14:
        self.formatted_operands.append(unpack("=f", pack("=i", self.BBBBBBBB))[0])

      elif self.OP == 0x17:
        self.formatted_operands.append(unpack('=d', pack('=d', self.BBBBBBBB))[0])

      #log_andro.debug("OP:%x %s AA:%x BBBBBBBBB:%x" % (self.OP, args[0], self.AA, self.BBBBBBBB))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, %d" % (self.AA, self.BBBBBBBB)

      if self.formatted_operands:
        buff += " # %s" % str(self.formatted_operands)

      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_LITERAL, self.BBBBBBBB)]

    def get_formatted_operands(self):
      return self.formatted_operands

    def get_literals(self):
      return [self.BBBBBBBB]

    def get_raw(self):
      return pack("=Hi", (self.AA << 8) | self.OP, self.BBBBBBBB)


class Instruction22x(Instruction):
    """
        This class represents all instructions which have the 22x format
    """
    def __init__(self, cm, buff):
      super(Instruction22x, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=H", buff[2:4])[0]

      #log_andro.debug("OP:%x %s AA:%x BBBBB:%x" % (self.OP, args[0], self.AA, self.BBBB))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, v%d" % (self.AA, self.BBBB)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_REGISTER, self.BBBB)]

    def get_raw(self):
      return pack("=HH", (self.AA << 8) | self.OP, self.BBBB)


class Instruction23x(Instruction):
    """
        This class represents all instructions which have the 23x format
    """
    def __init__(self, cm, buff):
      super(Instruction23x, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      i16 = unpack("=H", buff[2:4])[0]
      self.BB = i16 & 0xff
      self.CC = (i16 >> 8) & 0xff

      #log_andro.debug("OP:%x %s AA:%x BB:%x CC:%x" % (self.OP, args[0], self.AA, self.BB, self.CC))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, v%d, v%d" % (self.AA, self.BB, self.CC)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_REGISTER, self.BB), (OPERAND_REGISTER, self.CC)]

    def get_raw(self):
      return pack("=HH", (self.AA << 8) | self.OP, (self.CC << 8) | self.BB)


class Instruction20t(Instruction):
    """
        This class represents all instructions which have the 20t format
    """
    def __init__(self, cm, buff):
      super(Instruction20t, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AAAA = unpack("=h", buff[2:4])[0]

      #log_andro.debug("OP:%x %s AAAA:%x" % (self.OP, args[0], self.AAAA))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "%+x" % (self.AAAA)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_OFFSET, self.AAAA)]

    def get_ref_off(self):
      return self.AAAA

    def get_raw(self):
      return pack("=Hh", self.OP, self.AAAA)


class Instruction21t(Instruction):
    """
        This class represents all instructions which have the 21t format
    """
    def __init__(self, cm, buff):
      super(Instruction21t, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=h", buff[2:4])[0]

      #log_andro.debug("OP:%x %s AA:%x BBBBB:%x" % (self.OP, args[0], self.AA, self.BBBB))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, %+x" % (self.AA, self.BBBB)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_OFFSET, self.BBBB)]

    def get_ref_off(self):
      return self.BBBB

    def get_raw(self):
      return pack("=Hh", (self.AA << 8) | self.OP, self.BBBB)


class Instruction10t(Instruction):
    """
        This class represents all instructions which have the 10t format
    """
    def __init__(self, cm, buff):
      super(Instruction10t, self).__init__()

      self.OP = unpack("=B", buff[0:1])[0]
      self.AA = unpack("=b", buff[1:2])[0]

      #log_andro.debug("OP:%x %s AA:%x" % (self.OP, args[0], self.AA))

    def get_length(self):
      return 2

    def get_output(self, idx=-1):
      buff = ""
      buff += "%+x" % (self.AA)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_OFFSET, self.AA)]

    def get_ref_off(self):
      return self.AA

    def get_raw(self):
      return pack("=Bb", self.OP, self.AA)


class Instruction22t(Instruction):
    """
        This class represents all instructions which have the 22t format
    """
    def __init__(self, cm, buff):
      super(Instruction22t, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.A = (i16 >> 8) & 0xf
      self.B = (i16 >> 12) & 0xf
      self.CCCC = unpack("=h", buff[2:4])[0]

      #log_andro.debug("OP:%x %s A:%x B:%x CCCC:%x" % (self.OP, args[0], self.A, self.B, self.CCCC))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, v%d, %+x" % (self.A, self.B, self.CCCC)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.A), (OPERAND_REGISTER, self.B), (OPERAND_OFFSET, self.CCCC)]

    def get_ref_off(self):
      return self.CCCC

    def get_raw(self):
      return pack("=Hh", (self.B << 12) | (self.A << 8) | self.OP, self.CCCC)


class Instruction22s(Instruction):
    """
        This class represents all instructions which have the 22s format
    """
    def __init__(self, cm, buff):
      super(Instruction22s, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.A = (i16 >> 8) & 0xf
      self.B = (i16 >> 12) & 0xf
      self.CCCC = unpack("=h", buff[2:4])[0]

      #log_andro.debug("OP:%x %s A:%x B:%x CCCC:%x" % (self.OP, args[0], self.A, self.B, self.CCCC))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, v%d, %d" % (self.A, self.B, self.CCCC)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.A), (OPERAND_REGISTER, self.B), (OPERAND_LITERAL, self.CCCC)]

    def get_literals(self):
      return [self.CCCC]

    def get_raw(self):
      return pack("=Hh", (self.B << 12) | (self.A << 8) | self.OP, self.CCCC)


class Instruction22b(Instruction):
    """
        This class represents all instructions which have the 22b format
    """
    def __init__(self, cm, buff):
      super(Instruction22b, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BB = unpack("=B", buff[2:3])[0]
      self.CC = unpack("=b", buff[3:4])[0]

      #log_andro.debug("OP:%x %s AA:%x BB:%x CC:%x" % (self.OP, args[0], self.AA, self.BB, self.CC))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, v%d, %d" % (self.AA, self.BB, self.CC)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AA), (OPERAND_REGISTER, self.BB), (OPERAND_LITERAL, self.CC)]

    def get_literals(self):
      return [self.CC]

    def get_raw(self):
      return pack("=Hh", (self.AA << 8) | self.OP, (self.CC << 8) | self.BB)


class Instruction30t(Instruction):
    """
        This class represents all instructions which have the 30t format
    """
    def __init__(self, cm, buff):
      super(Instruction30t, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff

      self.AAAAAAAA = unpack("=i", buff[2:6])[0]

      #log_andro.debug("OP:%x %s AAAAAAAA:%x" % (self.OP, args[0], self.AAAAAAAA))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""
      buff += "%+x" % (self.AAAAAAAA)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_OFFSET, self.AAAAAAAA)]

    def get_ref_off(self):
      return self.AAAAAAAA

    def get_raw(self):
      return pack("=Hi", self.OP, self.AAAAAAAA)


class Instruction3rc(Instruction):
    """
        This class represents all instructions which have the 3rc format
    """
    def __init__(self, cm, buff):
      super(Instruction3rc, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=H", buff[2:4])[0]
      self.CCCC = unpack("=H", buff[4:6])[0]

      self.NNNN = self.CCCC + self.AA - 1

      #log_andro.debug("OP:%x %s AA:%x BBBB:%x CCCC:%x NNNN:%d" % (self.OP, args[0], self.AA, self.BBBB, self.CCCC, self.NNNN))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""

      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.CCCC == self.NNNN:
        buff += "v%d, %s" % (self.CCCC, kind)
      else:
        buff += "v%d ... v%d, %s" % (self.CCCC, self.NNNN, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.CCCC == self.NNNN:
        return [(OPERAND_REGISTER, self.CCCC), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)]
      else:
        l = []
        for i in range(self.CCCC, self.NNNN):
          l.append((OPERAND_REGISTER, i))

        l.append((self.get_kind() + OPERAND_KIND, self.BBBB, kind))
        return l

    def get_ref_kind(self):
      return self.BBBB

    def get_raw(self):
      return pack("=HHH", (self.AA << 8) | self.OP, self.BBBB, self.CCCC)


class Instruction32x(Instruction):
    """
        This class represents all instructions which have the 32x format
    """
    def __init__(self, cm, buff):
      super(Instruction32x, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AAAA = unpack("=H", buff[2:4])[0]
      self.BBBB = unpack("=H", buff[4:6])[0]

      #log_andro.debug("OP:%x %s AAAAA:%x BBBBB:%x" % (self.OP, args[0], self.AAAA, self.BBBB))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""
      buff += "v%d, v%d" % (self.AAAA, self.BBBB)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_REGISTER, self.AAAA), (OPERAND_REGISTER, self.BBBB)]

    def get_raw(self):
      return pack("=HHH", self.OP, self.AAAA, self.BBBB)


class Instruction20bc(Instruction):
    """
        This class represents all instructions which have the 20bc format
    """
    def __init__(self, cm, buff):
      super(Instruction20bc, self).__init__()

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=H", buff[2:4])[0]

      #log_andro.debug("OP:%x %s AA:%x BBBBB:%x" % (self.OP, args[0], self.AA, self.BBBB))

    def get_length(self):
      return 4

    def get_output(self, idx=-1):
      buff = ""
      buff += "%d, %d" % (self.AA, self.BBBB)
      return buff

    def get_operands(self, idx=-1):
      return [(OPERAND_LITERAL, self.AA), (OPERAND_LITERAL, self.BBBB)]

    def get_raw(self):
      return pack("=HH", (self.AA << 8) | self.OP, self.BBBB)


class Instruction35mi(Instruction):
    """
        This class represents all instructions which have the 35mi format
    """
    def __init__(self, cm, buff):
      super(Instruction35mi, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.G = (i16 >> 8) & 0xf
      self.A = (i16 >> 12) & 0xf
      self.BBBB = unpack("=H", buff[2:4])[0]

      i16 = unpack("=H", buff[4:6])[0]
      self.C = i16 & 0xf
      self.D = (i16 >> 4) & 0xf
      self.E = (i16 >> 8) & 0xf
      self.F = (i16 >> 12) & 0xf

      #log_andro.debug("OP:%x %s G:%x A:%x BBBB:%x C:%x D:%x E:%x F:%x" % (self.OP, args[0], self.G, self.A, self.BBBB, self.C, self.D, self.E, self.F))

    def get_output(self, idx=-1):
      buff = ""

      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.A == 1:
        buff += "v%d, %s" % (self.C, kind)
      elif self.A == 2:
        buff += "v%d, v%d, %s" % (self.C, self.D, kind)
      elif self.A == 3:
        buff += "v%d, v%d, v%d, %s" % (self.C, self.D, self.E, kind)
      elif self.A == 4:
        buff += "v%d, v%d, v%d, v%d, %s" % (self.C, self.D, self.E, self.F, kind)
      elif self.A == 5:
        buff += "v%d, v%d, v%d, v%d, v%d, %s" % (self.C, self.D, self.E, self.F, self.G, kind)

      return buff

    def get_operands(self, idx=-1):
      l = []
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.A == 1:
        l.extend([(OPERAND_REGISTER, self.C), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 2:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 3:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 4:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (OPERAND_REGISTER, self.F), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 5:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (OPERAND_REGISTER, self.F), (OPERAND_REGISTER, self.G), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])

      return l

    def get_length(self):
      return 6

    def get_ref_kind(self):
      return self.BBBB

    def get_raw(self):
      return pack("=HHH", (self.A << 12) | (self.G << 8) | self.OP, self.BBBB, (self.F << 12) | (self.E << 8) | (self.D << 4) | self.C)


class Instruction35ms(Instruction):
    """
        This class represents all instructions which have the 35ms format
    """
    def __init__(self, cm, buff):
      super(Instruction35ms, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.G = (i16 >> 8) & 0xf
      self.A = (i16 >> 12) & 0xf
      self.BBBB = unpack("=H", buff[2:4])[0]

      i16 = unpack("=H", buff[4:6])[0]
      self.C = i16 & 0xf
      self.D = (i16 >> 4) & 0xf
      self.E = (i16 >> 8) & 0xf
      self.F = (i16 >> 12) & 0xf

      #log_andro.debug("OP:%x %s G:%x A:%x BBBB:%x C:%x D:%x E:%x F:%x" % (self.OP, args[0], self.G, self.A, self.BBBB, self.C, self.D, self.E, self.F))

    def get_output(self, idx=-1):
      buff = ""

      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.A == 1:
        buff += "v%d, %s" % (self.C, kind)
      elif self.A == 2:
        buff += "v%d, v%d, %s" % (self.C, self.D, kind)
      elif self.A == 3:
        buff += "v%d, v%d, v%d, %s" % (self.C, self.D, self.E, kind)
      elif self.A == 4:
        buff += "v%d, v%d, v%d, v%d, %s" % (self.C, self.D, self.E, self.F, kind)
      elif self.A == 5:
        buff += "v%d, v%d, v%d, v%d, v%d, %s" % (self.C, self.D, self.E, self.F, self.G, kind)

      return buff

    def get_operands(self, idx=-1):
      l = []
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.A == 1:
        l.extend([(OPERAND_REGISTER, self.C), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 2:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 3:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 4:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (OPERAND_REGISTER, self.F), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])
      elif self.A == 5:
        l.extend([(OPERAND_REGISTER, self.C), (OPERAND_REGISTER, self.D), (OPERAND_REGISTER, self.E), (OPERAND_REGISTER, self.F), (OPERAND_REGISTER, self.G), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)])

      return l

    def get_length(self):
      return 6

    def get_ref_kind(self):
      return self.BBBB

    def get_raw(self):
      return pack("=HHH", (self.A << 12) | (self.G << 8) | self.OP, self.BBBB, (self.F << 12) | (self.E << 8) | (self.D << 4) | self.C)


class Instruction3rmi(Instruction):
    """
        This class represents all instructions which have the 3rmi format
    """
    def __init__(self, cm, buff):
      super(Instruction3rmi, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=H", buff[2:4])[0]
      self.CCCC = unpack("=H", buff[4:6])[0]

      self.NNNN = self.CCCC + self.AA - 1

      #log_andro.debug("OP:%x %s AA:%x BBBB:%x CCCC:%x NNNN:%d" % (self.OP, args[0], self.AA, self.BBBB, self.CCCC, self.NNNN))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""

      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.CCCC == self.NNNN:
        buff += "v%d, %s" % (self.CCCC, kind)
      else:
        buff += "v%d ... v%d, %s" % (self.CCCC, self.NNNN, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.CCCC == self.NNNN:
        return [(OPERAND_REGISTER, self.CCCC), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)]
      else:
        l = []
        for i in range(self.CCCC, self.NNNN):
          l.append((OPERAND_REGISTER, i))

        l.append((self.get_kind() + OPERAND_KIND, self.BBBB, kind))
        return l

    def get_ref_kind(self):
      return self.BBBB

    def get_raw(self):
      return pack("=HHH", (self.AA << 8) | self.OP, self.BBBB, self.CCCC)


class Instruction3rms(Instruction):
    """
        This class represents all instructions which have the 3rms format
    """
    def __init__(self, cm, buff):
      super(Instruction3rms, self).__init__()
      self.cm = cm

      i16 = unpack("=H", buff[0:2])[0]
      self.OP = i16 & 0xff
      self.AA = (i16 >> 8) & 0xff

      self.BBBB = unpack("=H", buff[2:4])[0]
      self.CCCC = unpack("=H", buff[4:6])[0]

      self.NNNN = self.CCCC + self.AA - 1

      #log_andro.debug("OP:%x %s AA:%x BBBB:%x CCCC:%x NNNN:%d" % (self.OP, args[0], self.AA, self.BBBB, self.CCCC, self.NNNN))

    def get_length(self):
      return 6

    def get_output(self, idx=-1):
      buff = ""

      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.CCCC == self.NNNN:
        buff += "v%d, %s" % (self.CCCC, kind)
      else:
        buff += "v%d ... v%d, %s" % (self.CCCC, self.NNNN, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBB)

      if self.CCCC == self.NNNN:
        return [(OPERAND_REGISTER, self.CCCC), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)]
      else:
        l = []
        for i in range(self.CCCC, self.NNNN):
          l.append((OPERAND_REGISTER, i))

        l.append((self.get_kind() + OPERAND_KIND, self.BBBB, kind))
        return l

    def get_ref_kind(self):
      return self.BBBB

    def get_raw(self):
      return pack("=HHH", (self.AA << 8) | self.OP, self.BBBB, self.CCCC)


class Instruction41c(Instruction):
    """
        This class represents all instructions which have the 41c format
    """
    def __init__(self, cm, buff):
      super(Instruction41c, self).__init__()
      self.cm = cm

      self.OP = unpack("=H", buff[0:2])[0]
      self.BBBBBBBB = unpack("=I", buff[2:6])[0]

      self.AAAA = unpack("=H", buff[6:8])[0]

      #log_andro.debug("OP:%x %s AAAAA:%x BBBBB:%x" % (self.OP, args[0], self.AAAA, self.BBBBBBBB))

    def get_length(self):
      return 8

    def get_output(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)

      buff = ""
      buff += "v%d, %s" % (self.AAAA, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)
      return [(OPERAND_REGISTER, self.AAAA), (self.get_kind() + OPERAND_KIND, self.BBBBBBBB, kind)]

    def get_ref_kind(self):
      return self.BBBBBBBB

    def get_raw(self):
      return pack("=HIH", self.OP, self.BBBBBBBB, self.AAAA)


class Instruction40sc(Instruction):
    """
        This class represents all instructions which have the 40sc format
    """
    def __init__(self, cm, buff):
      super(Instruction40sc, self).__init__()
      self.cm = cm

      self.OP = unpack("=H", buff[0:2])[0]
      self.BBBBBBBB = unpack("=I", buff[2:6])[0]
      self.AAAA = unpack("=H", buff[6:8])[0]

      #log_andro.debug("OP:%x %s AAAAA:%x BBBBB:%x" % (self.OP, args[0], self.AAAA, self.BBBBBBBB))

    def get_length(self):
      return 8

    def get_output(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)

      buff = ""
      buff += "%d, %s" % (self.AAAA, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)
      return [(OPERAND_LITERAL, self.AAAA), (self.get_kind() + OPERAND_KIND, self.BBBBBBBB, kind)]

    def get_ref_kind(self):
      return self.BBBBBBBB

    def get_raw(self):
      return pack("=HIH", self.OP, self.BBBBBBBB, self.AAAA)


class Instruction52c(Instruction):
    """
        This class represents all instructions which have the 52c format
    """
    def __init__(self, cm, buff):
      super(Instruction52c, self).__init__()
      self.cm = cm

      self.OP = unpack("=H", buff[0:2])[0]
      self.CCCCCCCC = unpack("=I", buff[2:6])[0]
      self.AAAA = unpack("=H", buff[6:8])[0]
      self.BBBB = unpack("=H", buff[8:10])[0]

      #log_andro.debug("OP:%x %s AAAAA:%x BBBBB:%x" % (self.OP, args[0], self.AAAA, self.BBBB))

    def get_length(self):
      return 10

    def get_output(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.CCCCCCCC)

      buff = ""
      buff += "v%d, v%d, %s" % (self.AAAA, self.BBBB, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.CCCCCCCC)
      return [(OPERAND_LITERAL, self.AAAA), (OPERAND_LITERAL, self.BBBB), (self.get_kind() + OPERAND_KIND, self.CCCCCCCC, kind)]

    def get_ref_kind(self):
      return self.CCCCCCCC

    def get_raw(self):
      return pack("=HIHH", self.OP, self.CCCCCCCC, self.AAAA, self.BBBB)


class Instruction5rc(Instruction):
    """
        This class represents all instructions which have the 5rc format
    """
    def __init__(self, cm, buff):
      super(Instruction5rc, self).__init__()
      self.cm = cm

      self.OP = unpack("=H", buff[0:2])[0]
      self.BBBBBBBB = unpack("=I", buff[2:6])[0]
      self.AAAA = unpack("=H", buff[6:8])[0]
      self.CCCC = unpack("=H", buff[8:10])[0]

      self.NNNN = self.CCCC + self.AAAA - 1

      #log_andro.debug("OP:%x %s AA:%x BBBB:%x CCCC:%x NNNN:%d" % (self.OP, args[0], self.AAAA, self.BBBBBBBB, self.CCCC, self.NNNN))

    def get_length(self):
      return 10

    def get_output(self, idx=-1):
      buff = ""

      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)

      if self.CCCC == self.NNNN:
        buff += "v%d, %s" % (self.CCCC, kind)
      else:
        buff += "v%d ... v%d, %s" % (self.CCCC, self.NNNN, kind)
      return buff

    def get_operands(self, idx=-1):
      kind = get_kind(self.cm, self.get_kind(), self.BBBBBBBB)

      if self.CCCC == self.NNNN:
        return [(OPERAND_REGISTER, self.CCCC), (self.get_kind() + OPERAND_KIND, self.BBBB, kind)]
      else:
        l = []
        for i in range(self.CCCC, self.NNNN):
          l.append((OPERAND_REGISTER, i))

        l.append((self.get_kind() + OPERAND_KIND, self.BBBB, kind))
        return l

    def get_ref_kind(self):
      return self.BBBBBBBB

    def get_raw(self):
      return pack("=HIHH", self.OP, self.BBBBBBBB, self.AAAA, self.CCCC)

DALVIK_OPCODES_FORMAT = {
  0x00 : [Instruction10x, [ "nop" ] ],
  0x01 : [Instruction12x, [ "move" ] ],
  0x02 : [Instruction22x, [ "move/from16" ] ],
  0x03 : [Instruction32x, [ "move/16" ] ],
  0x04 : [Instruction12x, [ "move-wide" ] ],
  0x05 : [Instruction22x, [ "move-wide/from16" ] ],
  0x06 : [Instruction32x, [ "move-wide/16" ] ],
  0x07 : [Instruction12x, [ "move-object" ] ],
  0x08 : [Instruction22x, [ "move-object/from16" ] ],
  0x09 : [Instruction32x, [ "move-object/16" ] ],
  0x0a : [Instruction11x, [ "move-result" ] ],
  0x0b : [Instruction11x, [ "move-result-wide" ] ],
  0x0c : [Instruction11x, [ "move-result-object" ] ],
  0x0d : [Instruction11x, [ "move-exception" ] ],
  0x0e : [Instruction10x, [ "return-void" ] ],
  0x0f : [Instruction11x, [ "return" ] ],
  0x10 : [Instruction11x, [ "return-wide" ] ],
  0x11 : [Instruction11x, [ "return-object" ] ],
  0x12 : [Instruction11n, [ "const/4" ] ],
  0x13 : [Instruction21s, [ "const/16" ] ],
  0x14 : [Instruction31i, [ "const" ] ],
  0x15 : [Instruction21h, [ "const/high16" ] ],
  0x16 : [Instruction21s, [ "const-wide/16" ] ],
  0x17 : [Instruction31i, [ "const-wide/32" ] ],
  0x18 : [Instruction51l, [ "const-wide" ] ],
  0x19 : [Instruction21h, [ "const-wide/high16" ] ],
  0x1a : [Instruction21c, [ "const-string", KIND_STRING ] ],
  0x1b : [Instruction31c, [ "const-string/jumbo", KIND_STRING ] ],
  0x1c : [Instruction21c, [ "const-class", KIND_TYPE ] ],
  0x1d : [Instruction11x, [ "monitor-enter" ] ],
  0x1e : [Instruction11x, [ "monitor-exit" ] ],
  0x1f : [Instruction21c, [ "check-cast", KIND_TYPE ] ],
  0x20 : [Instruction22c, [ "instance-of", KIND_TYPE ] ],
  0x21 : [Instruction12x, [ "array-length" ] ],
  0x22 : [Instruction21c, [ "new-instance", KIND_TYPE ] ],
  0x23 : [Instruction22c, [ "new-array", KIND_TYPE ] ],

  0x24 : [Instruction35c, [ "filled-new-array", KIND_TYPE ] ],
  0x25 : [Instruction3rc, [ "filled-new-array/range", KIND_TYPE ] ],
  0x26 : [Instruction31t, [ "fill-array-data" ] ],

  0x27 : [Instruction11x, [ "throw" ] ],

  0x28 : [Instruction10t, [ "goto" ] ],
  0x29 : [Instruction20t, [ "goto/16" ] ],
  0x2a : [Instruction30t, [ "goto/32" ] ],

  0x2b : [Instruction31t, [ "packed-switch" ] ],
  0x2c : [Instruction31t, [ "sparse-switch" ] ],

  0x2d : [Instruction23x, [ "cmpl-float"  ] ],
  0x2e : [Instruction23x, [ "cmpg-float" ] ],
  0x2f : [Instruction23x, [ "cmpl-double" ] ],
  0x30 : [Instruction23x, [ "cmpg-double" ] ],
  0x31 : [Instruction23x, [ "cmp-long" ] ],

  0x32 : [Instruction22t, [ "if-eq" ] ],
  0x33 : [Instruction22t, [ "if-ne" ] ],
  0x34 : [Instruction22t, [ "if-lt" ] ],
  0x35 : [Instruction22t, [ "if-ge" ] ],
  0x36 : [Instruction22t, [ "if-gt" ] ],
  0x37 : [Instruction22t, [ "if-le" ] ],

  0x38 : [Instruction21t, [ "if-eqz" ] ],
  0x39 : [Instruction21t, [ "if-nez" ] ],
  0x3a : [Instruction21t, [ "if-ltz" ] ],
  0x3b : [Instruction21t, [ "if-gez" ] ],
  0x3c : [Instruction21t, [ "if-gtz" ] ],
  0x3d : [Instruction21t, [ "if-lez" ] ],

  #unused
  0x3e : [Instruction10x, [ "nop" ] ],
  0x3f : [Instruction10x, [ "nop" ] ],
  0x40 : [Instruction10x, [ "nop" ] ],
  0x41 : [Instruction10x, [ "nop" ] ],
  0x42 : [Instruction10x, [ "nop" ] ],
  0x43 : [Instruction10x, [ "nop" ] ],

  0x44 : [Instruction23x, [ "aget" ] ],
  0x45 : [Instruction23x, [ "aget-wide" ] ],
  0x46 : [Instruction23x, [ "aget-object" ] ],
  0x47 : [Instruction23x, [ "aget-boolean" ] ],
  0x48 : [Instruction23x, [ "aget-byte" ] ],
  0x49 : [Instruction23x, [ "aget-char" ] ],
  0x4a : [Instruction23x, [ "aget-short" ] ],
  0x4b : [Instruction23x, [ "aput" ] ],
  0x4c : [Instruction23x, [ "aput-wide" ] ],
  0x4d : [Instruction23x, [ "aput-object" ] ],
  0x4e : [Instruction23x, [ "aput-boolean" ] ],
  0x4f : [Instruction23x, [ "aput-byte" ] ],
  0x50 : [Instruction23x, [ "aput-char" ] ],
  0x51 : [Instruction23x, [ "aput-short" ] ],

  0x52 : [Instruction22c, [ "iget", KIND_FIELD ] ],
  0x53 : [Instruction22c, [ "iget-wide", KIND_FIELD ] ],
  0x54 : [Instruction22c, [ "iget-object", KIND_FIELD ] ],
  0x55 : [Instruction22c, [ "iget-boolean", KIND_FIELD ] ],
  0x56 : [Instruction22c, [ "iget-byte", KIND_FIELD ] ],
  0x57 : [Instruction22c, [ "iget-char", KIND_FIELD ] ],
  0x58 : [Instruction22c, [ "iget-short", KIND_FIELD ] ],
  0x59 : [Instruction22c, [ "iput", KIND_FIELD ] ],
  0x5a : [Instruction22c, [ "iput-wide", KIND_FIELD ] ],
  0x5b : [Instruction22c, [ "iput-object", KIND_FIELD ] ],
  0x5c : [Instruction22c, [ "iput-boolean", KIND_FIELD ] ],
  0x5d : [Instruction22c, [ "iput-byte", KIND_FIELD ] ],
  0x5e : [Instruction22c, [ "iput-char", KIND_FIELD ] ],
  0x5f : [Instruction22c, [ "iput-short", KIND_FIELD ] ],


  0x60 : [Instruction21c, [ "sget", KIND_FIELD ] ],
  0x61 : [Instruction21c, [ "sget-wide", KIND_FIELD ] ],
  0x62 : [Instruction21c, [ "sget-object", KIND_FIELD ] ],
  0x63 : [Instruction21c, [ "sget-boolean", KIND_FIELD ] ],
  0x64 : [Instruction21c, [ "sget-byte", KIND_FIELD ] ],
  0x65 : [Instruction21c, [ "sget-char", KIND_FIELD ] ],
  0x66 : [Instruction21c, [ "sget-short", KIND_FIELD ] ],
  0x67 : [Instruction21c, [ "sput", KIND_FIELD ] ],
  0x68 : [Instruction21c, [ "sput-wide", KIND_FIELD ] ],
  0x69 : [Instruction21c, [ "sput-object", KIND_FIELD ] ],
  0x6a : [Instruction21c, [ "sput-boolean", KIND_FIELD ] ],
  0x6b : [Instruction21c, [ "sput-byte", KIND_FIELD ] ],
  0x6c : [Instruction21c, [ "sput-char", KIND_FIELD ] ],
  0x6d : [Instruction21c, [ "sput-short", KIND_FIELD ] ],


  0x6e : [Instruction35c, [ "invoke-virtual", KIND_METH ] ],
  0x6f : [Instruction35c, [ "invoke-super", KIND_METH ] ],
  0x70 : [Instruction35c, [ "invoke-direct", KIND_METH ] ],
  0x71 : [Instruction35c, [ "invoke-static", KIND_METH ] ],
  0x72 : [Instruction35c, [ "invoke-interface", KIND_METH ] ],

  # unused
  0x73 : [Instruction10x, [ "nop" ] ],

  0x74 : [Instruction3rc, [ "invoke-virtual/range", KIND_METH ] ],
  0x75 : [Instruction3rc, [ "invoke-super/range", KIND_METH ] ],
  0x76 : [Instruction3rc, [ "invoke-direct/range", KIND_METH ] ],
  0x77 : [Instruction3rc, [ "invoke-static/range", KIND_METH ] ],
  0x78 : [Instruction3rc, [ "invoke-interface/range", KIND_METH ] ],

  # unused
  0x79 : [Instruction10x, [ "nop" ] ],
  0x7a : [Instruction10x, [ "nop" ] ],


  0x7b : [Instruction12x, [ "neg-int" ] ],
  0x7c : [Instruction12x, [ "not-int" ] ],
  0x7d : [Instruction12x, [ "neg-long" ] ],
  0x7e : [Instruction12x, [ "not-long" ] ],
  0x7f : [Instruction12x, [ "neg-float" ] ],
  0x80 : [Instruction12x, [ "neg-double" ] ],
  0x81 : [Instruction12x, [ "int-to-long" ] ],
  0x82 : [Instruction12x, [ "int-to-float" ] ],
  0x83 : [Instruction12x, [ "int-to-double" ] ],
  0x84 : [Instruction12x, [ "long-to-int" ] ],
  0x85 : [Instruction12x, [ "long-to-float" ] ],
  0x86 : [Instruction12x, [ "long-to-double" ] ],
  0x87 : [Instruction12x, [ "float-to-int" ] ],
  0x88 : [Instruction12x, [ "float-to-long" ] ],
  0x89 : [Instruction12x, [ "float-to-double" ] ],
  0x8a : [Instruction12x, [ "double-to-int" ] ],
  0x8b : [Instruction12x, [ "double-to-long" ] ],
  0x8c : [Instruction12x, [ "double-to-float" ] ],
  0x8d : [Instruction12x, [ "int-to-byte" ] ],
  0x8e : [Instruction12x, [ "int-to-char" ] ],
  0x8f : [Instruction12x, [ "int-to-short" ] ],


  0x90 : [Instruction23x, [ "add-int" ] ],
  0x91 : [Instruction23x, [ "sub-int" ] ],
  0x92 : [Instruction23x, [ "mul-int" ] ],
  0x93 : [Instruction23x, [ "div-int" ] ],
  0x94 : [Instruction23x, [ "rem-int" ] ],
  0x95 : [Instruction23x, [ "and-int" ] ],
  0x96 : [Instruction23x, [ "or-int" ] ],
  0x97 : [Instruction23x, [ "xor-int" ] ],
  0x98 : [Instruction23x, [ "shl-int" ] ],
  0x99 : [Instruction23x, [ "shr-int" ] ],
  0x9a : [Instruction23x, [ "ushr-int" ] ],
  0x9b : [Instruction23x, [ "add-long" ] ],
  0x9c : [Instruction23x, [ "sub-long" ] ],
  0x9d : [Instruction23x, [ "mul-long" ] ],
  0x9e : [Instruction23x, [ "div-long" ] ],
  0x9f : [Instruction23x, [ "rem-long" ] ],
  0xa0 : [Instruction23x, [ "and-long" ] ],
  0xa1 : [Instruction23x, [ "or-long" ] ],
  0xa2 : [Instruction23x, [ "xor-long" ] ],
  0xa3 : [Instruction23x, [ "shl-long" ] ],
  0xa4 : [Instruction23x, [ "shr-long" ] ],
  0xa5 : [Instruction23x, [ "ushr-long" ] ],
  0xa6 : [Instruction23x, [ "add-float" ] ],
  0xa7 : [Instruction23x, [ "sub-float" ] ],
  0xa8 : [Instruction23x, [ "mul-float" ] ],
  0xa9 : [Instruction23x, [ "div-float" ] ],
  0xaa : [Instruction23x, [ "rem-float" ] ],
  0xab : [Instruction23x, [ "add-double" ] ],
  0xac : [Instruction23x, [ "sub-double" ] ],
  0xad : [Instruction23x, [ "mul-double" ] ],
  0xae : [Instruction23x, [ "div-double" ] ],
  0xaf : [Instruction23x, [ "rem-double" ] ],


  0xb0 : [Instruction12x, [ "add-int/2addr" ] ],
  0xb1 : [Instruction12x, [ "sub-int/2addr" ] ],
  0xb2 : [Instruction12x, [ "mul-int/2addr" ] ],
  0xb3 : [Instruction12x, [ "div-int/2addr" ] ],
  0xb4 : [Instruction12x, [ "rem-int/2addr" ] ],
  0xb5 : [Instruction12x, [ "and-int/2addr" ] ],
  0xb6 : [Instruction12x, [ "or-int/2addr" ] ],
  0xb7 : [Instruction12x, [ "xor-int/2addr" ] ],
  0xb8 : [Instruction12x, [ "shl-int/2addr" ] ],
  0xb9 : [Instruction12x, [ "shr-int/2addr" ] ],
  0xba : [Instruction12x, [ "ushr-int/2addr" ] ],
  0xbb : [Instruction12x, [ "add-long/2addr" ] ],
  0xbc : [Instruction12x, [ "sub-long/2addr" ] ],
  0xbd : [Instruction12x, [ "mul-long/2addr" ] ],
  0xbe : [Instruction12x, [ "div-long/2addr" ] ],
  0xbf : [Instruction12x, [ "rem-long/2addr" ] ],
  0xc0 : [Instruction12x, [ "and-long/2addr" ] ],
  0xc1 : [Instruction12x, [ "or-long/2addr" ] ],
  0xc2 : [Instruction12x, [ "xor-long/2addr" ] ],
  0xc3 : [Instruction12x, [ "shl-long/2addr" ] ],
  0xc4 : [Instruction12x, [ "shr-long/2addr" ] ],
  0xc5 : [Instruction12x, [ "ushr-long/2addr" ] ],
  0xc6 : [Instruction12x, [ "add-float/2addr" ] ],
  0xc7 : [Instruction12x, [ "sub-float/2addr" ] ],
  0xc8 : [Instruction12x, [ "mul-float/2addr" ] ],
  0xc9 : [Instruction12x, [ "div-float/2addr" ] ],
  0xca : [Instruction12x, [ "rem-float/2addr" ] ],
  0xcb : [Instruction12x, [ "add-double/2addr" ] ],
  0xcc : [Instruction12x, [ "sub-double/2addr" ] ],
  0xcd : [Instruction12x, [ "mul-double/2addr" ] ],
  0xce : [Instruction12x, [ "div-double/2addr" ] ],
  0xcf : [Instruction12x, [ "rem-double/2addr" ] ],

  0xd0 : [Instruction22s, [ "add-int/lit16" ] ],
  0xd1 : [Instruction22s, [ "rsub-int" ] ],
  0xd2 : [Instruction22s, [ "mul-int/lit16" ] ],
  0xd3 : [Instruction22s, [ "div-int/lit16" ] ],
  0xd4 : [Instruction22s, [ "rem-int/lit16" ] ],
  0xd5 : [Instruction22s, [ "and-int/lit16" ] ],
  0xd6 : [Instruction22s, [ "or-int/lit16" ] ],
  0xd7 : [Instruction22s, [ "xor-int/lit16" ] ],


  0xd8 : [Instruction22b, [ "add-int/lit8" ] ],
  0xd9 : [Instruction22b, [ "rsub-int/lit8" ] ],
  0xda : [Instruction22b, [ "mul-int/lit8" ] ],
  0xdb : [Instruction22b, [ "div-int/lit8" ] ],
  0xdc : [Instruction22b, [ "rem-int/lit8" ] ],
  0xdd : [Instruction22b, [ "and-int/lit8" ] ],
  0xde : [Instruction22b, [ "or-int/lit8" ] ],
  0xdf : [Instruction22b, [ "xor-int/lit8" ] ],
  0xe0 : [Instruction22b, [ "shl-int/lit8" ] ],
  0xe1 : [Instruction22b, [ "shr-int/lit8" ] ],
  0xe2 : [Instruction22b, [ "ushr-int/lit8" ] ],


  # expanded opcodes
  0xe3 : [Instruction22c, [ "iget-volatile", KIND_FIELD ] ],
  0xe4 : [Instruction22c, [ "iput-volatile", KIND_FIELD ] ],
  0xe5 : [Instruction21c, [ "sget-volatile", KIND_FIELD ] ],
  0xe6 : [Instruction21c, [ "sput-volatile", KIND_FIELD ] ],
  0xe7 : [Instruction22c, [ "iget-object-volatile", KIND_FIELD ] ],
  0xe8 : [Instruction22c, [ "iget-wide-volatile", KIND_FIELD ] ],
  0xe9 : [Instruction22c, [ "iput-wide-volatile", KIND_FIELD ] ],
  0xea : [Instruction21c, [ "sget-wide-volatile", KIND_FIELD ] ],
  0xeb : [Instruction21c, [ "sput-wide-volatile", KIND_FIELD ] ],

  0xec : [Instruction10x,   [ "breakpoint" ] ],
  0xed : [Instruction20bc,  [ "throw-verification-error", VARIES ] ],
  0xee : [Instruction35mi,  [ "execute-inline", INLINE_METHOD ] ],
  0xef : [Instruction3rmi,  [ "execute-inline/range", INLINE_METHOD ] ],
  0xf0 : [Instruction35c,   [ "invoke-object-init/range", KIND_METH ] ],
  0xf1 : [Instruction10x,   [ "return-void-barrier" ] ],

  0xf2 : [Instruction22cs,  [ "iget-quick", FIELD_OFFSET ] ],
  0xf3 : [Instruction22cs,  [ "iget-wide-quick", FIELD_OFFSET ] ],
  0xf4 : [Instruction22cs,  [ "iget-object-quick", FIELD_OFFSET ] ],
  0xf5 : [Instruction22cs,  [ "iput-quick", FIELD_OFFSET ] ],
  0xf6 : [Instruction22cs,  [ "iput-wide-quick", FIELD_OFFSET ] ],
  0xf7 : [Instruction22cs,  [ "iput-object-quick", FIELD_OFFSET ] ],
  0xf8 : [Instruction35ms,  [ "invoke-virtual-quick", VTABLE_OFFSET ] ],
  0xf9 : [Instruction3rms,  [ "invoke-virtual-quick/range", VTABLE_OFFSET ] ],
  0xfa : [Instruction35ms,  [ "invoke-super-quick", VTABLE_OFFSET ] ],
  0xfb : [Instruction3rms,  [ "invoke-super-quick/range", VTABLE_OFFSET ] ],
  0xfc : [Instruction22c,   [ "iput-object-volatile", KIND_FIELD ] ],
  0xfd : [Instruction21c,   [ "sget-object-volatile", KIND_FIELD ] ],
  0xfe : [Instruction21c,   [ "sput-object-volatile", KIND_FIELD ] ],
}

DALVIK_OPCODES_PAYLOAD = {
    0x0100 : [PackedSwitch],
    0x0200 : [SparseSwitch],
    0x0300 : [FillArrayData],
}

INLINE_METHODS = [
    [ "Lorg/apache/harmony/dalvik/NativeTestTarget;", "emptyInlineMethod", "()V" ],

    [ "Ljava/lang/String;", "charAt", "(I)C" ],
    [ "Ljava/lang/String;", "compareTo", "(Ljava/lang/String;)I" ],
    [ "Ljava/lang/String;", "equals", "(Ljava/lang/Object;)Z" ],
    [ "Ljava/lang/String;", "fastIndexOf", "(II)I" ],
    [ "Ljava/lang/String;", "isEmpty", "()Z" ],
    [ "Ljava/lang/String;", "length", "()I" ],

    [ "Ljava/lang/Math;", "abs", "(I)I" ],
    [ "Ljava/lang/Math;", "abs", "(J)J" ],
    [ "Ljava/lang/Math;", "abs", "(F)F" ],
    [ "Ljava/lang/Math;", "abs", "(D)D" ],
    [ "Ljava/lang/Math;", "min", "(II)I" ],
    [ "Ljava/lang/Math;", "max", "(II)I" ],
    [ "Ljava/lang/Math;", "sqrt", "(D)D" ],
    [ "Ljava/lang/Math;", "cos", "(D)D" ],
    [ "Ljava/lang/Math;", "sin", "(D)D" ],

    [ "Ljava/lang/Float;", "floatToIntBits", "(F)I" ],
    [ "Ljava/lang/Float;", "floatToRawIntBits", "(F)I" ],
    [ "Ljava/lang/Float;", "intBitsToFloat", "(I)F" ],
    [ "Ljava/lang/Double;", "doubleToLongBits", "(D)J" ],
    [ "Ljava/lang/Double;", "doubleToRawLongBits", "(D)J" ],
    [ "Ljava/lang/Double;", "longBitsToDouble", "(J)D" ],
]

DALVIK_OPCODES_EXTENDED_WIDTH = {
    0x00ff: [ Instruction41c, ["const-class/jumbo", KIND_TYPE ] ],
    0x01ff: [ Instruction41c, ["check-cast/jumbo", KIND_TYPE ] ],

    0x02ff: [ Instruction52c, ["instance-of/jumbo", KIND_TYPE ] ],

    0x03ff: [ Instruction41c, ["new-instance/jumbo", KIND_TYPE ] ],

    0x04ff: [ Instruction52c, ["new-array/jumbo", KIND_TYPE ] ],

    0x05ff: [ Instruction5rc, ["filled-new-array/jumbo", KIND_TYPE ] ],

    0x06ff: [ Instruction52c, ["iget/jumbo", KIND_FIELD ] ],
    0x07ff: [ Instruction52c, ["iget-wide/jumbo", KIND_FIELD ] ],
    0x08ff: [ Instruction52c, ["iget-object/jumbo", KIND_FIELD ] ],
    0x09ff: [ Instruction52c, ["iget-boolean/jumbo", KIND_FIELD ] ],
    0x0aff: [ Instruction52c, ["iget-byte/jumbo", KIND_FIELD ] ],
    0x0bff: [ Instruction52c, ["iget-char/jumbo", KIND_FIELD ] ],
    0x0cff: [ Instruction52c, ["iget-short/jumbo", KIND_FIELD ] ],
    0x0dff: [ Instruction52c, ["iput/jumbo", KIND_FIELD ] ],
    0x0eff: [ Instruction52c, ["iput-wide/jumbo", KIND_FIELD ] ],
    0x0fff: [ Instruction52c, ["iput-object/jumbo", KIND_FIELD ] ],
    0x10ff: [ Instruction52c, ["iput-boolean/jumbo", KIND_FIELD ] ],
    0x11ff: [ Instruction52c, ["iput-byte/jumbo", KIND_FIELD ] ],
    0x12ff: [ Instruction52c, ["iput-char/jumbo", KIND_FIELD ] ],
    0x13ff: [ Instruction52c, ["iput-short/jumbo", KIND_FIELD ] ],

    0x14ff: [ Instruction41c, ["sget/jumbo", KIND_FIELD ] ],
    0x15ff: [ Instruction41c, ["sget-wide/jumbo", KIND_FIELD ] ],
    0x16ff: [ Instruction41c, ["sget-object/jumbo", KIND_FIELD ] ],
    0x17ff: [ Instruction41c, ["sget-boolean/jumbo", KIND_FIELD ] ],
    0x18ff: [ Instruction41c, ["sget-byte/jumbo", KIND_FIELD ] ],
    0x19ff: [ Instruction41c, ["sget-char/jumbo", KIND_FIELD ] ],
    0x1aff: [ Instruction41c, ["sget-short/jumbo", KIND_FIELD ] ],
    0x1bff: [ Instruction41c, ["sput/jumbo", KIND_FIELD ] ],
    0x1cff: [ Instruction41c, ["sput-wide/jumbo", KIND_FIELD ] ],
    0x1dff: [ Instruction41c, ["sput-object/jumbo", KIND_FIELD ] ],
    0x1eff: [ Instruction41c, ["sput-boolean/jumbo", KIND_FIELD ] ],
    0x1fff: [ Instruction41c, ["sput-byte/jumbo", KIND_FIELD ] ],
    0x20ff: [ Instruction41c, ["sput-char/jumbo", KIND_FIELD ] ],
    0x21ff: [ Instruction41c, ["sput-short/jumbo", KIND_FIELD ] ],

    0x22ff: [ Instruction5rc, ["invoke-virtual/jumbo", KIND_METH ] ],
    0x23ff: [ Instruction5rc, ["invoke-super/jumbo", KIND_METH ] ],
    0x24ff: [ Instruction5rc, ["invoke-direct/jumbo", KIND_METH ] ],
    0x25ff: [ Instruction5rc, ["invoke-static/jumbo", KIND_METH ] ],
    0x26ff: [ Instruction5rc, ["invoke-interface/jumbo", KIND_METH ] ],
}

DALVIK_OPCODES_OPTIMIZED = {
    0xf2ff : [ Instruction5rc, ["invoke-object-init/jumbo", KIND_METH ] ],

    0xf3ff : [ Instruction52c, ["iget-volatile/jumbo", KIND_FIELD ] ],
    0xf4ff : [ Instruction52c, ["iget-wide-volatile/jumbo", KIND_FIELD ] ],
    0xf5ff : [ Instruction52c, ["iget-object-volatile/jumbo ", KIND_FIELD ] ],
    0xf6ff : [ Instruction52c, ["iput-volatile/jumbo", KIND_FIELD ] ],
    0xf7ff : [ Instruction52c, ["iput-wide-volatile/jumbo", KIND_FIELD ] ],
    0xf8ff : [ Instruction52c, ["iput-object-volatile/jumbo", KIND_FIELD ] ],
    0xf9ff : [ Instruction41c, ["sget-volatile/jumbo", KIND_FIELD ] ],
    0xfaff : [ Instruction41c, ["sget-wide-volatile/jumbo", KIND_FIELD ] ],
    0xfbff : [ Instruction41c, ["sget-object-volatile/jumbo", KIND_FIELD ] ],
    0xfcff : [ Instruction41c, ["sput-volatile/jumbo", KIND_FIELD ] ],
    0xfdff : [ Instruction41c, ["sput-wide-volatile/jumbo", KIND_FIELD ] ],
    0xfeff : [ Instruction41c, ["sput-object-volatile/jumbo", KIND_FIELD ] ],

    0xffff : [ Instruction40sc, ["throw-verification-error/jumbo", VARIES ] ],
}