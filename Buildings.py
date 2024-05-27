from BlueprintBuilding import BlueprintBuilding
from ItemEnum import ItemEnum, Yaw
from utils import direction_to_unit_vector

class Building(BlueprintBuilding):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class AssemblingMachineMkIII(Building):
    def __init__(self, index, x, y, z, yaw = Yaw.North, recipe_id = 0):
        super().__init__()
        self.index = index
        self.x = x
        self.y = y
        self.z = z
        self.x2 = x
        self.y2 = y
        self.z2 = z
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.AssemblingMachineMkIII
        self.model_index = 67
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]
    
class Smelter(Building):
    def __init__(self, index, x, y, z, yaw = Yaw.North, recipe_id = 0):
        super().__init__()
        self.index = index
        self.x = x
        self.y = y
        self.z = z
        self.x2 = x
        self.y2 = y
        self.z2 = z
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.Smelter
        self.model_index = 62
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]

class Belt(Building):
    def __init__(self, index, x, y, z, yaw, output_object_index = -1, input_object_index = -1, output_to_slot = 0):
        super().__init__()
        self.index = index
        self.x = x
        self.y = y
        self.z = z
        self.x2 = x
        self.y2 = y
        self.z2 = z
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.ConveyorBeltMKIII
        self.model_index = 37
        self.output_object_index = output_object_index
        self.output_to_slot = output_to_slot
        
        self.output_from_slot = 0
        self.input_to_slot = 1
        
    def connect_to_belt(self, belt2):
        dx, dy = direction_to_unit_vector(self.yaw)
        if ((int(self.x + dx) == belt2.x) and (int(self.y + dy) == belt2.y) and self.yaw == belt2.yaw):
            self.output_object_index = belt2.index
            self.output_to_slot = 1
        else:
            print(self)
            print(belt2)
            assert False, "Not supported use"
            
    def connect_to_splitter(self, splitter):
        assert (int(splitter.yaw - self.yaw) % 180 == 0), f"Wrong orientation (splitter: {splitter.yaw}, belt: {self.yaw})"
        
        self.output_object_index = splitter.index
        self.output_to_slot = 1
        
        if self.yaw == splitter.yaw:
            self.output_to_slot = 2
        else:
            self.output_to_slot = 0
        if self.z == 1:
            self.output_to_slot += 1
        
        # Move the belt back 0.2 spaces
        dx, dy = direction_to_unit_vector(self.yaw)
        self.x -= dx * 0.2
        self.x2 -= dx * 0.2
        self.y -= dy * 0.2
        self.y2 -= dy * 0.2

    def connect_to_sorter(self, sorter):
        pass

class Sorter(Building):
    def __init__(self, index, x1, y1, z1, x2, y2, z2, yaw, output_object_index = -1, input_object_index = -1, output_to_slot = -1, input_from_slot = -1, output_from_slot = -1, input_to_slot = -1, output_offset = -1, input_offset = -1, parameters = []):
        super().__init__()
        self.index = index
        self.x = x1
        self.y = y1
        self.z = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.SorterMKIII
        self.model_index = 43
        self.output_object_index = output_object_index
        self.input_object_index = input_object_index
        self.output_to_slot = output_to_slot
        self.input_from_slot = input_from_slot
        self.output_from_slot = output_from_slot
        self.input_to_slot = input_to_slot
        self.output_offset = output_offset
        self.input_offset = input_offset
        self.parameter_count = len(parameters)
        self.parameters = parameters

    def connect_to_belt(self, belt):
        pass

class Splitter(Building):
    def __init__(self, index, x, y, z, yaw):
        super().__init__()
        self.index = index
        self.x = x
        self.y = y
        self.z = z
        self.x2 = x
        self.y2 = y
        self.z2 = z
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.Splitter
        self.model_index = 39
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = 14
        self.input_from_slot = 15
        self.output_from_slot = 15
        self.input_to_slot = 14
        self.output_offset = 0
        self.input_offset = 0
        self.parameter_count = 6
        self.parameters = [0, 0, 0, 0, 0, 0]
        
    def connect_to_belt(self, belt):
        assert (int(self.yaw - belt.yaw) % 180 == 0), f"Wrong orientation (splitter: {splitter.yaw}, belt: {belt.yaw})"
        
        belt.input_object_index = self.index
        
        
        if self.yaw == belt.yaw:
            belt.input_from_slot = 0
        else:
            belt.input_from_slot = 2
        if belt.z == 1:
            belt.input_from_slot += 1
        
        dx, dy = direction_to_unit_vector(belt.yaw)
        belt.x += dx * 0.2
        belt.x2 += dx * 0.2
        belt.y += dy * 0.2
        belt.y2 += dy * 0.2
        
class TeslaTower(Building):
    def __init__(self, index, x, y):
        super().__init__()
        self.index = index
        self.x = x
        self.y = y
        self.z = 0.0
        self.x2 = x
        self.y2 = y
        self.z2 = 0.0
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = ItemEnum.TeslaTower
        self.model_index = 44
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = 0
        self.input_from_slot = 0
        self.output_from_slot = 0
        self.input_to_slot = 0
        self.output_offset = 0
        self.input_offset = 0
        self.parameter_count = 0
        self.parameters = []