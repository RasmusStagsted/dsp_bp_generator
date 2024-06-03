from .building import Building
from ..utils import Pos, Yaw
from ..ItemEnum import ItemEnum

class ConveyorBelt(Building):
    def __init__(self, name, pos: Pos, yaw: Yaw, item_id: ItemEnum, model_index: int, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = item_id
        self.model_index = model_index
        self.output_object_index = output_object_index
        self.output_to_slot = output_to_slot
        
        self.output_from_slot = 0
        self.input_to_slot = 1
        
    def connect_to_belt(belt1, belt2):
        dx, dy = direction_to_unit_vector(belt1.yaw)
        if ((int(belt1.pos1.x + dx) == belt2.pos1.x) and (int(belt1.pos1.y + dy) == belt2.pos1.y) and belt1.yaw == belt2.yaw):
            belt1.output_object_index = belt2.index
            belt1.output_to_slot = 1
        else:
            dx, dy = direction_to_unit_vector(belt2.yaw)
            assert False, "Wrong use of belt-to_belt connection"
            
    def connect_to_splitter(self, splitter):
        assert (int(splitter.yaw - self.yaw) % 180 == 0), f"Wrong orientation (splitter: {splitter.yaw}, belt: {self.yaw})"
        
        self.output_object_index = splitter.index
        self.output_to_slot = 1
        
        if self.yaw == splitter.yaw:
            self.output_to_slot = 2
        else:
            self.output_to_slot = 0
        if self.pos1.z == 1:
            self.output_to_slot += 1
        
        # Move the belt back 0.2 spaces
        dx, dy = direction_to_unit_vector(self.yaw)
        self.move(-dx * 0.2, -dy * 0.2)

    def connect_to_sorter(self, sorter):
        pass

    def generate_belt(name, pos, yaw, length: int):
        
        if type(yaw) != list:
            yaw = [yaw]
        if type(length) != list:
            length = [length]
        assert len(yaw) == len(length), "\"yaw\" and \"length\" must have the same length"
        
        belts = []
        for i in range(len(yaw)):
            dx, dy = Yaw.direction_to_unit_vector(yaw[i])
            for j in range(length[i]):
                belt = ConveyorBeltMKIII(
                    name = f"{name}:{len(belts)}",
                    pos = pos,
                    yaw = yaw[i],
                    output_object_index = Building.count() + 1,
                    output_to_slot = 1
                )
                belts.append(belt)
                pos += Pos(dx, dy)
            
            if (i != len(yaw) - 1):
                belt.yaw = Yaw.direction_average(yaw[i], yaw[i + 1])
            else:
                belt.output_object_index = -1
                belt.output_to_slot = -1
        return belts
    
class ConveyorBeltMKI(ConveyorBelt):
    def __init__(self, name, pos: Pos, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            yaw = yaw,
            item_id = ItemEnum.ConveyorBeltMKI,
            model_index = 37, # TODO Find the right index
            output_object_index = output_object_index,
            input_object_index = input_object_index,
            output_to_slot = output_to_slot
        )
        
class ConveyorBeltMKII(ConveyorBelt):
    def __init__(self, name, pos: Pos, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            yaw = yaw,
            item_id = ItemEnum.ConveyorBeltMKII,
            model_index = 37, # TODO Find the right index
            output_object_index = output_object_index,
            input_object_index = input_object_index,
            output_to_slot = output_to_slot
        )

class ConveyorBeltMKIII(ConveyorBelt):
    def __init__(self, name, pos: Pos, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            yaw = yaw,
            item_id = ItemEnum.ConveyorBeltMKIII,
            model_index = 37,
            output_object_index = output_object_index,
            input_object_index = input_object_index,
            output_to_slot = output_to_slot
        )