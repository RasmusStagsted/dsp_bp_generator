from .packet import Packet

class BlueprintHeader:

    def __init__(self, size_x = 0, size_y = 0):
        self.version = 1
        self.cursor_offset_x = size_x // 2
        self.cursor_offset_y = size_y // 2
        self.cursor_target_area = 0
        self.dragbox_size_x = size_x
        self.dragbox_size_y = size_y
        self.primary_area_index = 0
        self.area_count = 1

    def parse(self, packet):
        self.version = packet.parse_int()
        self.cursor_offset_x = packet.parse_int()
        self.cursor_offset_y = packet.parse_int()
        self.cursor_target_area = packet.parse_int()
        self.dragbox_size_x = packet.parse_int()
        self.dragbox_size_y = packet.parse_int()
        self.primary_area_index = packet.parse_int()
        self.area_count = packet.parse_byte()

    def serialize(self):
        packet = Packet()
        packet.serialize_int(self.version)
        packet.serialize_int(self.cursor_offset_x)
        packet.serialize_int(self.cursor_offset_y)
        packet.serialize_int(self.cursor_target_area)
        packet.serialize_int(self.dragbox_size_x)
        packet.serialize_int(self.dragbox_size_y)
        packet.serialize_int(self.primary_area_index)
        packet.serialize_byte(self.area_count)
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