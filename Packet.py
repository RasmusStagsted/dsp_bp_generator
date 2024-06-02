from struct import pack, unpack
from copy import copy

class Packet:

    def __init__(self, data = b""):
        self.data = copy(data)

    def parse_int(self):
        value = unpack("i", self.data[0:4])[0]
        self.data = self.data[4:]
        return value

    def parse_float(self):
        value = unpack("f", self.data[0:4])[0]
        self.data = self.data[4:]
        return value

    def parse_byte(self):
        value = unpack("b", self.data[0:1])[0]
        self.data = self.data[1:]
        return value

    def parse_half_word(self):
        value = unpack("H", self.data[0:2])[0]
        self.data = self.data[2:]
        return value

    def serialize_int(self, value: int):
        self.data += pack("i", value)

    def serialize_float(self, value: float):
        self.data += pack("f", value)

    def serialize_byte(self, value):
        self.data += pack("b", value)

    def serialize_half_word(self, value: int):
        self.data += pack("H", value)
