from .packet import Packet
from ..utils import Vector
from ..enums import BuildingItem, BuildingModel
from copy import copy
import enum

class BlueprintBuilding:
    
    def __init__(self):
        self.index = 0
        self.area_index = 0
        self.pos = Vector()
        self.pos2 = Vector()
        self.yaw = 0
        self.yaw2 = 0
        self.item_id = 0
        self.model_index = 0
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = -1
        self.input_from_slot = -1
        self.output_from_slot = -1
        self.input_to_slot = -1
        self.output_offset = 0
        self.input_offset = 0
        self.recipe_id = 0
        self.filter_id = 0
        self.parameter_count = 0
        self.parameters = []
    
    def move_relative(self, pos: Vector):
        self.pos.x += pos.x
        self.pos.y += pos.y
        self.pos.z += pos.z
        self.pos2.x += pos.x
        self.pos2.y += pos.y
        self.pos2.z += pos.z

    def move_absolute(self, pos: Vector):
        self.pos.x = pos.x
        self.pos.y = pos.y
        self.pos.z = pos.z
        self.pos2.x = pos.x
        self.pos2.y = pos.y
        self.pos2.z = pos.z

    def get_version(packet):
        data = packet.peak_parse_int32()
        if data == -100:
            return BlueprintBuildingV2
        else:
            return BlueprintBuildingV1

class BlueprintBuildingV1(BlueprintBuilding):

    def __init__(self, building):
        super().__init__()
        self.index = building.index
        self.area_index = building.area_index
        self.pos.x = building.pos.x
        self.pos.y = building.pos.y
        self.pos.z = building.pos.z
        self.pos2.x = building.pos2.x
        self.pos2.y = building.pos2.y
        self.pos2.z = building.pos2.z
        self.yaw = building.yaw
        self.yaw2 = building.yaw2
        self.item_id = building.item_id
        self.model_index = building.model_index
        self.output_object_index = building.output_object_index
        self.input_object_index = building.input_object_index
        self.output_to_slot = building.output_to_slot
        self.input_from_slot = building.input_from_slot
        self.output_from_slot = building.output_from_slot
        self.input_to_slot = building.input_to_slot
        self.output_offset = building.output_offset
        self.input_offset = building.input_offset
        self.recipe_id = building.recipe_id
        self.filter_id = building.filter_id
        self.parameter_count = building.parameter_count
        self.parameters = building.parameters
        
    
    def get_size(self):
        return 61 + 4 * self.parameter_count
    
    def parse(self, packet: Packet):
        start_size = len(packet.data)
        self.index = packet.parse_int32()
        self.area_index = packet.parse_int8()
        self.pos.x = packet.parse_float32()
        self.pos.y = packet.parse_float32()
        self.pos.z = packet.parse_float32()
        self.pos2.x = packet.parse_float32()
        self.pos2.y = packet.parse_float32()
        self.pos2.z = packet.parse_float32()
        self.yaw = packet.parse_float32()
        self.yaw2 = packet.parse_float32()
        self.item_id = packet.parse_int16()
        self.model_index = packet.parse_int16()
        self.output_object_index = packet.parse_int32()
        self.input_object_index = packet.parse_int32()
        self.output_to_slot = packet.parse_int8()
        self.input_from_slot = packet.parse_int8()
        self.output_from_slot = packet.parse_int8()
        self.input_to_slot = packet.parse_int8()
        self.output_offset = packet.parse_int8()
        self.input_offset = packet.parse_int8()
        self.recipe_id = packet.parse_int16()
        self.filter_id = packet.parse_int16()
        self.parameter_count = packet.parse_int16()
        self.parameters = []
        for i in range(self.parameter_count):
            self.parameters.append(packet.parse_int32())
        end_size = len(packet.data)
        assert start_size - end_size == self.get_size(), "Wrong amount of data parsed!"
        
    def serialize(self):
        packet = Packet()
        packet.serialize_int32(self.index)
        packet.serialize_int8(self.area_index)
        packet.serialize_float32(self.pos.x)
        packet.serialize_float32(self.pos.y)
        packet.serialize_float32(self.pos.z)
        packet.serialize_float32(self.pos2.x)
        packet.serialize_float32(self.pos2.y)
        packet.serialize_float32(self.pos2.z)
        packet.serialize_float32(self.yaw)
        packet.serialize_float32(self.yaw2)
        packet.serialize_int16(self.item_id)
        packet.serialize_int16(self.model_index)
        packet.serialize_int32(self.output_object_index)
        packet.serialize_int32(self.input_object_index)
        packet.serialize_int8(self.output_to_slot)
        packet.serialize_int8(self.input_from_slot)
        packet.serialize_int8(self.output_from_slot)
        packet.serialize_int8(self.input_to_slot)
        packet.serialize_int8(self.output_offset)
        packet.serialize_int8(self.input_offset)
        packet.serialize_int16(self.recipe_id)
        packet.serialize_int16(self.filter_id)
        packet.serialize_int16(self.parameter_count)
        for param in self.parameters:
            packet.serialize_int32(param)
        assert len(packet.data) == self.get_size(), "Wrong amount of data serialized!"
        return packet

    def __str__(self):
        packet = self.serialize()
        string = f"""
Blue Print Building:
====================
Version: 1
====================
Length: {len(packet.data)}
Binary data: {packet.data}
====================
Index: {self.index}
Area index: {self.area_index}
position 1 x: {self.pos.x}
position 1 y: {self.pos.y}
position 1 z: {self.pos.z}
position 2 x: {self.pos2.x}
position 2 y: {self.pos2.y}
position 2 z: {self.pos2.z}
Yaw: {self.yaw}
Yaw2: {self.yaw2}
Item ID: {self.item_id} ({BuildingItem(self.item_id).name})
Model index: {self.model_index} ({BuildingModel(self.model_index).name})
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
    
class BlueprintBuildingV2(BlueprintBuilding):

    def __init__(self, building):
        super().__init__()
        self.dummy1 = -100
        self.dummy2 = 0
        self.index = building.index
        self.area_index = building.area_index
        self.pos.x = building.pos.x
        self.pos.y = building.pos.y
        self.pos.z = building.pos.z
        self.pos2.x = building.pos2.x
        self.pos2.y = building.pos2.y
        self.pos2.z = building.pos2.z
        self.yaw = building.yaw
        self.yaw2 = building.yaw2
        self.item_id = building.item_id
        self.model_index = building.model_index
        self.output_object_index = building.output_object_index
        self.input_object_index = building.input_object_index
        self.output_to_slot = building.output_to_slot
        self.input_from_slot = building.input_from_slot
        self.output_from_slot = building.output_from_slot
        self.input_to_slot = building.input_to_slot
        self.output_offset = building.output_offset
        self.input_offset = building.input_offset
        self.recipe_id = building.recipe_id
        self.filter_id = building.filter_id
        self.parameter_count = building.parameter_count
        self.parameters = building.parameters
    
    def get_size(self):
        return 69 + 4 * self.parameter_count
    
    def parse(self, packet: Packet):
        start_size = len(packet.data)
        self.dummy1 = packet.parse_int32()
        self.index = packet.parse_int32()
        self.area_index = packet.parse_int8()
        self.pos.x = packet.parse_float32()
        self.pos.y = packet.parse_float32()
        self.pos.z = packet.parse_float32()
        self.pos2.x = packet.parse_float32()
        self.pos2.y = packet.parse_float32()
        self.pos2.z = packet.parse_float32()
        self.yaw = packet.parse_float32()
        self.yaw2 = packet.parse_float32()
        self.output_object_index = packet.parse_int32()
        self.item_id = packet.parse_int16()
        self.model_index = packet.parse_int16()
        self.input_object_index = packet.parse_int32()
        self.output_to_slot = packet.parse_int8()
        self.input_from_slot = packet.parse_int8()
        self.output_from_slot = packet.parse_int8()
        self.input_to_slot = packet.parse_int8()
        self.output_offset = packet.parse_int8()
        self.input_offset = packet.parse_int8()
        self.dummy2 = packet.parse_int32()
        self.recipe_id = packet.parse_int16()
        self.filter_id = packet.parse_int16()
        self.parameter_count = packet.parse_int16()
        self.parameters = []
        for i in range(self.parameter_count):
            self.parameters.append(packet.parse_int32())
        end_size = len(packet.data)
        assert start_size - end_size == self.get_size(), "Wrong amount of data parsed!"
        
    def serialize(self):
        packet = Packet()
        packet.serialize_int32(self.dummy1)
        packet.serialize_int32(self.index)
        packet.serialize_int8(self.area_index)
        packet.serialize_float32(self.pos.x)
        packet.serialize_float32(self.pos.y)
        packet.serialize_float32(self.pos.z)
        packet.serialize_float32(self.pos2.x)
        packet.serialize_float32(self.pos2.y)
        packet.serialize_float32(self.pos2.z)
        packet.serialize_float32(self.yaw)
        packet.serialize_float32(self.yaw2)
        packet.serialize_int32(self.output_object_index)
        packet.serialize_int16(self.item_id)
        packet.serialize_int16(self.model_index)
        packet.serialize_int32(self.input_object_index)
        packet.serialize_int8(self.output_to_slot)
        packet.serialize_int8(self.input_from_slot)
        packet.serialize_int8(self.output_from_slot)
        packet.serialize_int8(self.input_to_slot)
        packet.serialize_int8(self.output_offset)
        packet.serialize_int8(self.input_offset)
        packet.serialize_int32(self.dummy2)
        packet.serialize_int16(self.recipe_id)
        packet.serialize_int16(self.filter_id)
        packet.serialize_int16(self.parameter_count)
        for param in self.parameters:
            packet.serialize_int32(param)
        assert len(packet.data) == self.get_size(), "Wrong amount of data serialized!"
        return packet

    def __str__(self):
        packet = self.serialize()
        string = f"""
Blue Print Building:
====================
Version: 2
====================
Length: {len(packet.data)}
Binary data: {packet.data}
====================
Dummy 1: {self.dummy1}
Index: {self.index}
Area index: {self.area_index}
position 1 x: {self.pos.x}
position 1 y: {self.pos.y}
position 1 z: {self.pos.z}
position 2 x: {self.pos2.x}
position 2 y: {self.pos2.y}
position 2 z: {self.pos2.z}
Yaw: {self.yaw}
Yaw2: {self.yaw2}
Output object index: {self.output_object_index}
Item ID: {self.item_id} ({BuildingItem(self.item_id).name})
Model index: {self.model_index} ({BuildingModel(self.model_index).name})
Input object index: {self.input_object_index}
Output to slot: {self.output_to_slot}
Input from slot: {self.input_from_slot}
Output from slot: {self.output_from_slot}
Input to slot: {self.input_to_slot}
Output offset: {self.output_offset}
Input offset: {self.input_offset}
Dummy 2: {self.dummy2}
Recipe id: {self.recipe_id}
Filter id: {self.filter_id}
Parameter count: {self.parameter_count}
"""
        for i in range(self.parameter_count):
            string += f"\tParam_{i}: {self.parameters[i]}\n"
        return string