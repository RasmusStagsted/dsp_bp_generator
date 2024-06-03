from .packet import Packet
from ..utils import Pos
import sys

class BlueprintArea:

    def __init__(self, size: Pos = Pos(), offset: Pos = Pos()):
        self.index = 0
        self.parent_index = -1
        self.tropic_anchor = 0
        self.area_segments = 200
        self.anchor_local_offset_x = int(offset.x)
        self.anchor_local_offset_y = int(offset.y)
        self.width = int(size.x)
        self.height = int(size.y)

    def parse(self, packet):
        self.index = packet.parse_byte()
        self.parent_index = packet.parse_byte()
        self.tropic_anchor = packet.parse_half_word()
        self.area_segments = packet.parse_half_word()
        self.anchor_local_offset_x = packet.parse_half_word()
        self.anchor_local_offset_y = packet.parse_half_word()
        self.width = packet.parse_half_word()
        self.height = packet.parse_half_word()

    def serialize(self):
        packet = Packet()
        packet.serialize_byte(self.index)
        packet.serialize_byte(self.parent_index)
        packet.serialize_half_word(self.tropic_anchor)
        packet.serialize_half_word(self.area_segments)
        packet.serialize_half_word(self.anchor_local_offset_x)
        packet.serialize_half_word(self.anchor_local_offset_y)
        packet.serialize_half_word(self.width)
        packet.serialize_half_word(self.height)
        return packet
    
    def get_area_from_building_list(buildings):
        min_x = 0x7fff
        max_x = -0x7fff
        min_y = 0x7fff
        max_y = -0x7fff
        for building in buildings:
            min_x = min(min_x, min(building.pos1.x, building.pos2.x))
            max_x = max(max_x, max(building.pos1.x, building.pos2.x))
            min_y = min(min_y, min(building.pos1.y, building.pos2.y))
            max_y = max(max_y, max(building.pos1.y, building.pos2.y))
        size = Pos(max_x - min_x + 1, max_y - min_y + 1)
        offset = Pos((max_x - min_x) // 2, (max_y - min_y) // 2)
        return size, offset

    def __str__(self):
        return f"""
Blueprint Area:
===============
Binary data: {self.serialize().data}
===============
Index: {self.index}
Parent index: {self.parent_index}
Tropic anchor: {self.tropic_anchor}
Area segments: {self.area_segments}
Anchor local offset x: {self.anchor_local_offset_x}
Anchor local offset Y: {self.anchor_local_offset_y}
Width: {self.width}
Height: {self.height}
"""