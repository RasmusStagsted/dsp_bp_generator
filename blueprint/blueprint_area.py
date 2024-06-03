if __name__ != "__main__" and __name__ != "blueprint_area":
    from .packet import Packet

class BlueprintArea:

    def __init__(self, width = 0, height = 0):
        self.index = 0
        self.parent_index = -1
        self.tropic_anchor = 0
        self.area_segments = 200
        self.anchor_local_offset_x = 0
        self.anchor_local_offset_y = 0
        self.width = width
        self.height = height

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

if __name__ == "__main__":
    from packet import Packet
    from colorama import Fore, Style
    
    area = BlueprintArea()
    input_data = b'\x00\xff\x00\x00\xc8\x00\x00\x00\x00\x00\x01\x00\x01\x00'
    input_packet = Packet(input_data)
    area.parse(input_packet)
    
    output_data = area.serialize().data
    
    print("Input data: ", input_data)
    print("Output data:", output_data)
    print(area)
    print("Remaining data:", input_packet.data)
    assert(len(input_packet.data) == 0)
    assert(input_data == output_data)
    print(Fore.GREEN + "Passed!")
    Style.RESET_ALL