from struct import pack, unpack
from copy import copy

class Packet:

    def __init__(self, data = b""):
        self.data = copy(data)

    def parse_int8(self):
        value = unpack("b", self.data[0:1])[0]
        self.data = self.data[1:]
        return value

    def parse_int16(self):
        value = unpack("h", self.data[0:2])[0]
        self.data = self.data[2:]
        return value

    def parse_int32(self):
        value = unpack("i", self.data[0:4])[0]
        self.data = self.data[4:]
        return value

    def parse_float32(self):
        value = unpack("f", self.data[0:4])[0]
        self.data = self.data[4:]
        return value

    def peak_parse_int8(self):
        value = unpack("b", self.data[0:1])[0]
        return value

    def peak_parse_int16(self):
        value = unpack("h", self.data[0:2])[0]
        return value

    def peak_parse_int32(self):
        value = unpack("i", self.data[0:4])[0]
        return value

    def peak_parse_float32(self):
        value = unpack("f", self.data[0:4])[0]
        return value

    def serialize_int8(self, value):
        self.data += pack("b", value)

    def serialize_int16(self, value: int):
        self.data += pack("h", value)

    def serialize_int32(self, value: int):
        self.data += pack("i", value)

    def serialize_float32(self, value: float):
        self.data += pack("f", value)
