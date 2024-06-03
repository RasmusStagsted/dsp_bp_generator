if __name__ != "__main__":
    from .packet import Packet
from utils import Pos
from ItemEnum import ItemEnum
from copy import copy

class BlueprintBuilding:

    def __init__(self, index: int = 0, area_index: int = 0, pos1 = Pos(0, 0, 0), pos2 = Pos(0, 0, 0), yaw: int = 0, yaw2: int = 0, item_id: int = 0, model_index: int = 0, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0, input_from_slot: int = 0, output_from_slot: int = 0, input_to_slot: int = 0, output_offset: int = 0, input_offset: int = 0, recipe_id: int = 0, filter_id: int = 0, parameters = []):
        self.index = index
        self.area_index = area_index
        self.pos1 = copy(pos1)
        self.pos2 = copy(pos2)
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = item_id
        self.model_index = model_index
        self.output_object_index = output_object_index
        self.input_object_index = input_object_index
        self.output_to_slot = output_to_slot
        self.input_from_slot = input_from_slot
        self.output_from_slot = output_from_slot
        self.input_to_slot = input_to_slot
        self.output_offset = output_offset
        self.input_offset = input_offset
        self.recipe_id = recipe_id
        self.filter_id = filter_id
        self.parameter_count = len(parameters)
        self.parameters = parameters

    def get_size(self):
        return 61 + 4 * self.parameter_count

    def parse(self, packet: Packet):
        start_size = len(packet.data)
        self.index = packet.parse_int()
        self.area_index = packet.parse_byte()
        self.pos1.x = packet.parse_float()
        self.pos1.y = packet.parse_float()
        self.pos1.z = packet.parse_float()
        self.pos2.x = packet.parse_float()
        self.pos2.y = packet.parse_float()
        self.pos2.z = packet.parse_float()
        self.yaw = packet.parse_float()
        self.yaw2 = packet.parse_float()
        self.item_id = packet.parse_half_word()
        self.model_index = packet.parse_half_word()
        self.output_object_index = packet.parse_int()
        self.input_object_index = packet.parse_int()
        self.output_to_slot = packet.parse_byte()
        self.input_from_slot = packet.parse_byte()
        self.output_from_slot = packet.parse_byte()
        self.input_to_slot = packet.parse_byte()
        self.output_offset = packet.parse_byte()
        self.input_offset = packet.parse_byte()
        self.recipe_id = packet.parse_half_word()
        self.filter_id = packet.parse_half_word()
        self.parameter_count = packet.parse_half_word()
        self.parameters = []
        for i in range(self.parameter_count):
            self.parameters.append(packet.parse_int())
        end_size = len(packet.data)
        assert start_size - end_size == self.get_size(), "Wrong amount of data parsed!"
        
    def serialize(self):
        packet = Packet()
        packet.serialize_int(self.index)
        packet.serialize_byte(self.area_index)
        packet.serialize_float(self.pos1.x)
        packet.serialize_float(self.pos1.y)
        packet.serialize_float(self.pos1.z)
        packet.serialize_float(self.pos2.x)
        packet.serialize_float(self.pos2.y)
        packet.serialize_float(self.pos2.z)
        packet.serialize_float(self.yaw)
        packet.serialize_float(self.yaw2)
        packet.serialize_half_word(self.item_id)
        packet.serialize_half_word(self.model_index)
        packet.serialize_int(self.output_object_index)
        packet.serialize_int(self.input_object_index)
        packet.serialize_byte(self.output_to_slot)
        packet.serialize_byte(self.input_from_slot)
        packet.serialize_byte(self.output_from_slot)
        packet.serialize_byte(self.input_to_slot)
        packet.serialize_byte(self.output_offset)
        packet.serialize_byte(self.input_offset)
        packet.serialize_half_word(self.recipe_id)
        packet.serialize_half_word(self.filter_id)
        packet.serialize_half_word(self.parameter_count)
        for param in self.parameters:
            packet.serialize_int(param)
        assert len(packet.data) == self.get_size(), "Wrong amount of data serialized!"
        return packet

    def __str__(self):
        packet = self.serialize()
        string = f"""
Blue Print Building:
====================
Length: {len(packet.data)}
Binary data: {packet.data}
====================
Index: {self.index}
Area index: {self.area_index}
position 1 x: {self.pos1.x}
position 1 y: {self.pos1.y}
position 1 z: {self.pos1.z}
position 2 x: {self.pos2.x}
position 2 y: {self.pos2.y}
position 2 z: {self.pos2.z}
Yaw: {self.yaw}
Yaw2: {self.yaw2}
Item ID: {str(ItemEnum(self.item_id))[9:]} ({self.item_id})
Model index: {self.model_index}
Output object index: {self.output_object_index}
Input object index: {self.input_object_index}
Output to slot: {self.output_to_slot}
Input from slot: {self.input_from_slot}
Output from slot: {self.output_from_slot}
Input to slot: {self.input_to_slot}
Output offset: {self.output_offset}
Input offset: {self.input_offset}
Recipe id: {self.recipe_id}
Filter id: {self.filter_id}
Parameter count: {self.parameter_count}
"""
        for i in range(self.parameter_count):
            string += f"\tParam_{i}: {self.parameters[i]}\n"
        return string

if __name__ == "__main__":
    from packet import Packet
    from copy import copy
    from colorama import Fore, Style
    
    building = BlueprintBuilding()
    # iterable as source
    input_data = bytearray([i for i in range(59)] + [0, 0])
    #input_data = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x90\x197\x00\x00\x00\x00\x00\x00\x00\x00\x01\x90\x197\x00\x00\x00\x00\x00\x00\x00\x00\xe4\x07&\x00\xff\xff\xff\xff\xff\xff\xff\xff\x0e\x0f\x0f\x0e\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    input_packet = Packet(input_data)
    building.parse(input_packet)
    
    output_data = building.serialize().data
    
    print("Input data: ", input_data)
    print("Output data:", output_data)
    print(building)
    print("Remaining data:", input_packet.data)
    assert(len(input_packet.data) == 0)
    assert(input_data == output_data)
    print(Fore.GREEN + "Passed!")
    Style.RESET_ALL
