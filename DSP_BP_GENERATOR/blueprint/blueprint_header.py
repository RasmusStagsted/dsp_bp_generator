from .packet import Packet
from ..utils import Vector

class BlueprintHeader:

    def __init__(self, size: Vector = Vector()):
        self.version = 1
        self.cursor_offset_x = int(size.x // 2)
        self.cursor_offset_y = int(size.y // 2)
        self.cursor_target_area = 0
        self.dragbox_size_x = int(size.x)
        self.dragbox_size_y = int(size.y)
        self.primary_area_index = 0
        self.area_count = 1

    def parse(self, packet):
        self.version = packet.parse_int32()
        self.cursor_offset_x = packet.parse_int32()
        self.cursor_offset_y = packet.parse_int32()
        self.cursor_target_area = packet.parse_int32()
        self.dragbox_size_x = packet.parse_int32()
        self.dragbox_size_y = packet.parse_int32()
        self.primary_area_index = packet.parse_int32()
        self.area_count = packet.parse_int8()

    def serialize(self):
        packet = Packet()
        packet.serialize_int32(self.version)
        packet.serialize_int32(self.cursor_offset_x)
        packet.serialize_int32(self.cursor_offset_y)
        packet.serialize_int32(self.cursor_target_area)
        packet.serialize_int32(self.dragbox_size_x)
        packet.serialize_int32(self.dragbox_size_y)
        packet.serialize_int32(self.primary_area_index)
        packet.serialize_int8(self.area_count)
        return packet

    def __str__(self):
        return f"""
Blueprint header:
=================
Binary data: {self.serialize().data}
=================
Version: {self.version}
Cursor offset x: {self.cursor_offset_x}
Cursor offset y: {self.cursor_offset_y}
Cursor target area: {self.cursor_target_area}
Dragbox size x: {self.dragbox_size_x}
Dragbox size y: {self.dragbox_size_y}
Primary area index: {self.primary_area_index}
Area count: {self.area_count}
"""