from .building import Building
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

class ConveyorBelt(Building):
    def __init__(self, name, pos: Vector, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.output_object_index = output_object_index
        self.output_to_slot = output_to_slot
        
        self.output_from_slot = 0
        self.input_to_slot = 1
        self.input_from_slot = 0
        
    def connect_to_belt(belt1, belt2):
        dir = Yaw.direction_to_unit_vector(belt1.yaw)
        if ((int(belt1.pos.x + dir.x) == belt2.pos.x) and (int(belt1.pos.y + dir.y) == belt2.pos.y) and belt1.yaw == belt2.yaw):
            belt1.output_object_index = belt2.index
            belt1.output_to_slot = 1
        else:
            assert False, f"Wrong use of belt-to_belt connection. Belt1: pos = {belt1.pos}, dir = {belt1.yaw}; Belt2: pos = {belt2.pos}, dir = {belt2.yaw}"
            
    def connect_to_splitter(self, splitter):
        assert (int(splitter.yaw - self.yaw) % 180 == 0), f"Wrong orientation (splitter: {splitter.yaw}, belt: {self.yaw})"
        
        self.output_object_index = splitter.index
        self.output_to_slot = 1
        
        if self.yaw == splitter.yaw:
            self.output_to_slot = 2
        else:
            self.output_to_slot = 0
        if self.pos.z == 1:
            self.output_to_slot += 1
        
        # Move the belt back 0.2 spaces
        dir = Yaw.direction_to_unit_vector(self.yaw)
        self.move_relative(Vector(-dir.x * 0.2, -dir.y * 0.2))

    def connect_to_sorter(self, sorter):
        pass

    def generate_belt(name, pos, yaw, length: int, belt_type):
        if type(yaw) != list:
            yaw = [yaw]
        if type(length) != list:
            length = [length]
        assert len(yaw) == len(length), "\"yaw\" and \"length\" must have the same length"
        
        for l in length:
            assert l > 0, "Belt length is less than one!"
        
        belts = []
        for i in range(len(yaw)):
            dir = Yaw.direction_to_unit_vector(yaw[i])
            for j in range(length[i]):
                belt = belt_type(
                    name = f"{name}:{len(belts)}",
                    pos = pos,
                    yaw = yaw[i],
                    output_object_index = Building.count() + 1,
                    output_to_slot = 1
                )
                belts.append(belt)
                pos += Vector(dir.x, dir.y)
            
            if (i != len(yaw) - 1):
                belt.yaw = Yaw.direction_average(yaw[i], yaw[i + 1])
            else:
                belt.output_object_index = -1
                belt.output_to_slot = 0
        return belts
        
class ConveyorBeltMKI(ConveyorBelt):
    MAX_THROUGHPUT = 6.0
    def __init__(self, name, pos: Vector, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            yaw = yaw,
            output_object_index = output_object_index,
            input_object_index = input_object_index,
            output_to_slot = output_to_slot
        )
        self.item_id = BuildingItem.ConveyorBeltMKI
        self.model_index = BuildingModel.ConveyorBeltMKI
    
    def generate_belt(name, pos, yaw, length: int):
        return ConveyorBelt.generate_belt(name, pos, yaw, length, ConveyorBeltMKI)
        
class ConveyorBeltMKII(ConveyorBelt):
    MAX_THROUGHPUT = 12.0
    def __init__(self, name, pos: Vector, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            yaw = yaw,
            output_object_index = output_object_index,
            input_object_index = input_object_index,
            output_to_slot = output_to_slot
        )
        self.item_id = BuildingItem.ConveyorBeltMKII
        self.model_index = BuildingModel.ConveyorBeltMKII

    def generate_belt(name, pos, yaw, length: int):
        return ConveyorBelt.generate_belt(name, pos, yaw, length, ConveyorBeltMKII)
        
class ConveyorBeltMKIII(ConveyorBelt):
    MAX_THROUGHPUT = 30.0
    def __init__(self, name, pos: Vector, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            yaw = yaw,
            output_object_index = output_object_index,
            input_object_index = input_object_index,
            output_to_slot = output_to_slot
        )
        self.item_id = BuildingItem.ConveyorBeltMKIII
        self.model_index = BuildingModel.ConveyorBeltMKIII

    def generate_belt(name, pos, yaw, length: int):
        return ConveyorBelt.generate_belt(name, pos, yaw, length, ConveyorBeltMKIII)
        